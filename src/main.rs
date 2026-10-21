use pecking_order::{
    Engine, Query,
    model::{Error, Response},
};
use std::{
    env, fs,
    io::{self, Read},
    path::Path,
};

fn main() {
    if let Err(message) = run() {
        eprintln!("{message}");
        std::process::exit(2);
    }
}

fn emit<T: serde::Serialize>(value: &T) -> Result<(), Box<dyn std::error::Error>> {
    println!("{}", serde_json::to_string_pretty(value)?);
    Ok(())
}

fn run() -> Result<(), Box<dyn std::error::Error>> {
    let args = env::args().skip(1).collect::<Vec<_>>();
    let engine = Engine::embedded()?;
    match args.first().map(String::as_str).unwrap_or("studio") {
        "catalog"=>emit(&engine.catalog())?,
        "glossary"=>emit(&engine.glossary())?,
        "validate"=>{
            // Resolve every combination, not only catalogue shape.
            let mut combinations=0usize;
            let mut missing=Vec::new();
            for system in &engine.content.systems {
                for theme in &engine.content.themes {
                    let query:Query=serde_json::from_value(serde_json::json!({"system":system.id,"theme":theme.id}))?;
                    match engine.resolve(query) { Ok(_)=>combinations+=1,Err(e)=>missing.push(e.to_string()) }
                }
            }
            if !missing.is_empty(){ return Err(missing.join("\n").into()); }
            emit(&serde_json::json!({"valid":true,"combinations":combinations,"counts":engine.catalog()["counts"]}))?;
        },
        "resolve"=>{
            let mut raw=String::new();
            match args.get(1).map(String::as_str) {
                None|Some("-")=>{io::stdin().read_to_string(&mut raw)?;},
                Some(value) if value.trim_start().starts_with('{')=>raw=value.into(),
                Some(path)=>raw=fs::read_to_string(path)?,
            }
            let query:Query=serde_json::from_str(raw.trim_start_matches('\u{feff}'))?;
            match engine.resolve(query){Ok(response)=>emit(&response)?,Err(error)=>{emit(&error)?;std::process::exit(2);}}
        },
        "schema"=>{
            let name=args.get(1).map(String::as_str).unwrap_or("query");
            match name {"query"=>emit(&schemars::schema_for!(Query))?,"response"=>emit(&schemars::schema_for!(Response))?,
                "error"=>emit(&schemars::schema_for!(Error))?,_=>return Err("schema query|response|error".into())}
        },
        "export-schemas"=>{
            let directory=args.get(1).map(String::as_str).unwrap_or("schemas");
            fs::create_dir_all(directory)?;
            for (name,schema) in [("query",schemars::schema_for!(Query)),("response",schemars::schema_for!(Response)),("error",schemars::schema_for!(Error))] {
                fs::write(Path::new(directory).join(format!("{name}.schema.json")),serde_json::to_string_pretty(&schema)?+"\n")?;
            }
        },
        "lexicon"=>emit(&engine.theme_lexicon(args.get(1).map(String::as_str).unwrap_or("generic"))?)?,
        "studio"=>{
            let port=args.iter().position(|a|a=="--port").and_then(|i|args.get(i+1)).map(|p|p.parse()).transpose()?.unwrap_or(8773);
            server(engine,port)?;
        },
        _=>return Err("pecking-order [studio --port 8773 | catalog | resolve request.json | lexicon theme | validate | schema query|response]".into())
    }
    Ok(())
}

fn server(engine: Engine, port: u16) -> Result<(), Box<dyn std::error::Error>> {
    let server = tiny_http::Server::http(("127.0.0.1", port)).map_err(|e| e.to_string())?;
    println!("Pecking Order Rust: http://127.0.0.1:{port}");
    for mut request in server.incoming_requests() {
        let path = request.url().split('?').next().unwrap_or("/").to_string();
        let mut status = 200;
        let mut mime = "application/json; charset=utf-8";
        let body: Vec<u8> = match (request.method().as_str(), path.as_str()) {
            ("GET", "/") => {
                mime = "text/html; charset=utf-8";
                include_bytes!("../web/index.html").to_vec()
            }
            ("GET", "/app.js") => {
                mime = "text/javascript; charset=utf-8";
                include_bytes!("../web/app.js").to_vec()
            }
            ("GET", "/combobox.js") => {
                mime = "text/javascript; charset=utf-8";
                include_bytes!("../web/combobox.js").to_vec()
            }
            ("GET", "/combobox.css") => {
                mime = "text/css; charset=utf-8";
                include_bytes!("../web/combobox.css").to_vec()
            }
            ("GET", "/glossary" | "/glossary.html") => {
                mime = "text/html; charset=utf-8";
                include_bytes!("../web/glossary.html").to_vec()
            }
            ("GET", "/glossary.js") => {
                mime = "text/javascript; charset=utf-8";
                include_bytes!("../web/glossary.js").to_vec()
            }
            ("GET", "/glossary.css") => {
                mime = "text/css; charset=utf-8";
                include_bytes!("../web/glossary.css").to_vec()
            }
            ("GET", "/style.css") => {
                mime = "text/css; charset=utf-8";
                include_bytes!("../web/style.css").to_vec()
            }
            ("GET", "/favicon.svg") => {
                mime = "image/svg+xml";
                include_bytes!("../web/favicon.svg").to_vec()
            }
            ("GET", "/api/catalog") => serde_json::to_vec(&engine.catalog())?,
            ("GET", "/api/glossary") => serde_json::to_vec(&engine.glossary())?,
            ("GET", "/api/schema/query") => serde_json::to_vec(&schemars::schema_for!(Query))?,
            ("GET", "/api/schema/response") => {
                serde_json::to_vec(&schemars::schema_for!(Response))?
            }
            ("GET", p) if p.starts_with("/api/themes/") => {
                match engine.theme_lexicon(p.trim_start_matches("/api/themes/")) {
                    Ok(data) => serde_json::to_vec(&data)?,
                    Err(e) => {
                        status = 404;
                        serde_json::to_vec(&e)?
                    }
                }
            }
            ("POST", "/api/resolve") => {
                let origin = request
                    .headers()
                    .iter()
                    .find(|h| h.field.equiv("Origin"))
                    .map(|h| h.value.as_str());
                let host = request
                    .headers()
                    .iter()
                    .find(|h| h.field.equiv("Host"))
                    .map(|h| h.value.as_str())
                    .unwrap_or("");
                let media = request
                    .headers()
                    .iter()
                    .find(|h| h.field.equiv("Content-Type"))
                    .map(|h| h.value.as_str())
                    .unwrap_or("");
                if origin.is_some_and(|value| value != format!("http://{host}")) {
                    status = 403;
                    b"{\"code\":\"foreign_origin\"}".to_vec()
                } else if !media
                    .split(';')
                    .next()
                    .is_some_and(|v| v.trim() == "application/json")
                {
                    status = 415;
                    b"{\"code\":\"json_required\"}".to_vec()
                } else if request.body_length().is_some_and(|n| n > 65536) {
                    status = 413;
                    b"{\"code\":\"body_too_large\"}".to_vec()
                } else {
                    let mut raw = String::new();
                    let read = request.as_reader().take(65537).read_to_string(&mut raw);
                    if raw.len() > 65536 {
                        status = 413;
                        b"{\"code\":\"body_too_large\"}".to_vec()
                    } else if read.is_err() {
                        status = 400;
                        b"{\"code\":\"invalid_encoding\"}".to_vec()
                    } else {
                        match serde_json::from_str::<Query>(&raw) {
                            Ok(q) => match engine.resolve(q) {
                                Ok(result) => serde_json::to_vec(&result)?,
                                Err(error) => {
                                    status = 400;
                                    serde_json::to_vec(&error)?
                                }
                            },
                            Err(e) => {
                                status = 400;
                                serde_json::to_vec(
                                    &serde_json::json!({"code":"invalid_request","message":{"fr":e.to_string(),"en":e.to_string()}}),
                                )?
                            }
                        }
                    }
                }
            }
            _ => {
                status = 404;
                b"{\"code\":\"not_found\"}".to_vec()
            }
        };
        let mut response = tiny_http::Response::from_data(body).with_status_code(status);
        for (key, value) in [
            ("Content-Type", mime),
            ("X-Content-Type-Options", "nosniff"),
            ("Cache-Control", "no-store"),
            (
                "Content-Security-Policy",
                "default-src 'self'; object-src 'none'; frame-ancestors 'none'",
            ),
        ] {
            response.add_header(
                tiny_http::Header::from_bytes(key, value).expect("Static valid header"),
            );
        }
        if let Err(e) = request.respond(response) {
            eprintln!("HTTP response: {e}");
        }
    }
    Ok(())
}
