"use strict";
const $ = id => document.getElementById(id);
let locale = "fr", catalog, result, currentQuery, sequence = 0, importedExtras = {};
const words = {
  fr: {language:"Langue", headline:"Qui porte le titre ?\nQui détient le pouvoir ?",intro:"Explorez les institutions d’un monde : leurs charges, leurs règles et leurs titres, dans leur contexte culturel.",scope:"Des modèles réutilisables et des références culturelles délimitées. Le corpus historique est en cours de constitution.",queryHeading:"Composer une institution",example:"Point de départ",culture:"Contexte culturel",domain:"Domaine",kind:"Institution",scale:"Échelle de portée",role:"Fonction recherchée (facultatif)",options:"Contexte et mode",mode:"Mode",historical:"Référence culturelle",inspired:"Adaptation pour un univers",generic:"Modèle générique",date:"Année (facultatif)",traits:"Caractéristiques exigées (séparées par des virgules)",resolve:"Explorer la structure",notice:"Une religion ou un continent ne définit pas à lui seul un titre. Une référence manquante reste visible.",contract:"La même requête, partout",contractText:"Python, ligne de commande et HTTP partagent le contrat JSON. Les identifiants restent stables d’une langue à l’autre.",copy:"Copier la requête",exportQuery:"Exporter la requête",exportResult:"Exporter le résultat",importQuery:"Importer une requête",querySchema:"Schéma de requête",responseSchema:"Schéma de réponse",catalog:"Catalogue",footer:"Des institutions et des fonctions. Les personnes et leur histoire appartiennent à votre monde.",all:"Tous les domaines",noCulture:"Sans déclinaison culturelle",generic_model:"Modèle générique",source_supported:"Référence sourcée",adapted:"Adaptation",powers:"Pouvoirs et limites",duties:"Mission",rules:"Règles institutionnelles",structure:"Relations entre fonctions",sources:"Sources et portée",capacity:"Titulaires possibles",collective:"Organe collectif",person:"Charge individuelle",rank:"Grade habituel",native:"Titre d’origine",unsupported:"Contexte non couvert",needs_context:"Contexte à préciser",conflict:"Contraintes incompatibles",role_not_found:"Fonction absente",resolved:"Structure résolue",units:"Unités constituantes",fr:"Français",en:"English",copied:"Requête copiée.",downloaded:"Fichier exporté.",imported:"Requête importée.",invalidFile:"Requête invalide. Vérifiez le fichier JSON et le contrat.",networkError:"Impossible de charger le résultat. Vérifiez le serveur local.",selection:"Fonctions affichées",min:"minimum",max:"maximum",unbounded:"non fixé",period:"Période du profil",genericOffices:"Les charges génériques sont signalées individuellement.",sampleTswana:"Village tswana : Kgosi",sampleFamily:"Famille indivise : Karta",sampleSultan:"Cour du Deccan : Sultan",sampleRaya:"Vijayanagara : Raya",sampleCouncil:"Confédération sans chef unique",sampleCorps:"Corps d’armée britannique",sampleEdo:"Japon d’Edo : pouvoirs distincts",sampleGuild:"Compagnie de livrée londonienne",sampleBroad:"« Africain » : préciser le contexte",sampleGeneric:"Modèle générique : roi / king"},
  en: {language:"Language",headline:"Who holds the title?\nWho holds the power?",intro:"Explore a world's institutions: their offices, rules and titles, in their cultural context.",scope:"Reusable blueprints and bounded cultural references. The historical corpus is still being built.",queryHeading:"Compose an institution",example:"Starting point",culture:"Cultural context",domain:"Domain",kind:"Institution",scale:"Scale of reach",role:"Requested function (optional)",options:"Context and mode",mode:"Mode",historical:"Cultural reference",inspired:"Worldbuilding adaptation",generic:"Generic blueprint",date:"Year (optional)",traits:"Required traits (comma-separated)",resolve:"Explore the structure",notice:"A religion or continent alone does not determine a title. Missing references stay visible.",contract:"The same request, everywhere",contractText:"Python, command line and HTTP share the JSON contract. Identifiers stay stable across languages.",copy:"Copy request",exportQuery:"Export request",exportResult:"Export result",importQuery:"Import request",querySchema:"Request schema",responseSchema:"Response schema",catalog:"Catalogue",footer:"Institutions and functions. The people and their history belong to your world.",all:"All domains",noCulture:"Without a cultural binding",generic_model:"Generic model",source_supported:"Sourced reference",adapted:"Adaptation",powers:"Powers and limits",duties:"Purpose",rules:"Institutional rules",structure:"Relations between functions",sources:"Sources and scope",capacity:"Possible office holders",collective:"Collective body",person:"Individual office",rank:"Typical rank",native:"Original title",unsupported:"Context not covered",needs_context:"More context needed",conflict:"Incompatible constraints",role_not_found:"Function absent",resolved:"Structure resolved",units:"Constituent units",fr:"Français",en:"English",copied:"Request copied.",downloaded:"File exported.",imported:"Request imported.",invalidFile:"Invalid request. Check the JSON file and contract.",networkError:"Could not load the result. Check the local server.",selection:"Displayed functions",min:"minimum",max:"maximum",unbounded:"unspecified",period:"Profile period",genericOffices:"Generic offices are labelled individually.",sampleTswana:"Tswana village: Kgosi",sampleFamily:"Joint household: Karta",sampleSultan:"Deccan court: Sultan",sampleRaya:"Vijayanagara: Raya",sampleCouncil:"Confederation without a single chief",sampleCorps:"British Army corps",sampleEdo:"Edo Japan: distinct powers",sampleGuild:"London livery company",sampleBroad:"“African”: refine the context",sampleGeneric:"Generic blueprint: king / roi"}
};
const domainWords = {political:["Politique","Political"],administrative:["Administration","Administration"],military:["Armée","Military"],religious:["Religion","Religion"],economic:["Économie et métiers","Economy and crafts"],kinship:["Maisons et parenté organisée","Houses and corporate kinship"],judicial:["Justice","Justice"],educational:["Savoirs et enseignement","Learning and education"],civic:["Vie collective","Civic life"],clandestine:["Réseaux et clandestinité","Networks and clandestine groups"],diplomatic:["Diplomatie","Diplomacy"],fantastic:["Institutions imaginaires","Fantastic institutions"]};
const scaleWords = {household:["Maison / famille organisée","Corporate household"],local:["Locale","Local"],district:["District","District"],regional:["Régionale","Regional"],polity:["Entité politique","Polity"],imperial:["Impériale","Imperial"],transregional:["Transrégionale","Transregional"]};
const relationWords = {reports_to:["rend compte à","reports to"],advises:["conseille","advises"],appoints:["désigne","appoints"],removes:["peut révoquer","may remove"],elects:["élit","elects"],checks:["contrôle","checks"],represents:["représente","represents"],member_of:["siège dans","sits in"],coordinates:["coordonne","coordinates"],ritually_legitimizes:["légitime rituellement","ritually legitimizes"]};
const basisWords = {de_jure:["Autorité institutionnelle","Institutional authority"],de_facto:["Pouvoir de fait","Effective power"],ritual:["Autorité rituelle","Ritual authority"],advisory:["Avis consultatif","Advisory voice"]};
const samples = [
  ["sampleTswana","tswana_bogosi_contemporary","village_council","local"],
  ["sampleFamily","hindu_joint_family_india","corporate_household","household"],
  ["sampleSultan","deccan_sultanates","hereditary_monarchy","polity"],
  ["sampleRaya","vijayanagara_krishnadevaraya","empire","imperial"],
  ["sampleCouncil","haudenosaunee_confederacy_reference","confederation","polity"],
  ["sampleCorps","british_army_contemporary","army_corps","regional"],
  ["sampleEdo","japan_edo_reference","empire","imperial"],
  ["sampleGuild","london_livery_reference","craft_guild","local"],
  ["sampleBroad","africain","village_council","local"],
  ["sampleGeneric","*","hereditary_monarchy","polity"],
  ["sampleAuthoritarian","vijayanagara_krishnadevaraya","hereditary_monarchy","polity", {mode:"inspired", adaptations:[{kind:"authoritarian",target_role:"sovereign"}]}]
];
words.fr.sampleAuthoritarian="Raya : adaptation autoritaire fictive";
words.en.sampleAuthoritarian="Raya: fictional authoritarian adaptation";
const t = key => words[locale][key] || key;
const l = node => node?.labels?.[locale] || node?.labels?.en || "";
const pair = node => node?.[locale === "fr" ? 0 : 1] || "";
function el(tag, text, className) { const node=document.createElement(tag); if(text!==undefined)node.textContent=text; if(className)node.className=className; return node; }
function options(node, items, selected) { node.replaceChildren(...items.map(([value,label])=>{const o=el("option",label);o.value=value;return o;})); if(items.some(x=>x[0]===selected))node.value=selected; }
function rebuildKinds(selected) { const domain=$("domain").value; const items=catalog.templates.filter(x=>!domain||x.domain===domain); options($("kind"),items.map(x=>[x.id,l(x.label)]),selected); rebuildScales(); }
function rebuildScales(selected) {const kind=catalog.templates.find(x=>x.id===$("kind").value);options($("scale"),kind.scales.map(s=>[s,pair(scaleWords[s])]),selected);}
function translateControls() {
  document.documentElement.lang=locale;
  for(const node of document.querySelectorAll("[data-i18n]")) {node.textContent=t(node.dataset.i18n);if(node.tagName==="H1")node.style.whiteSpace="pre-line";}
  const c=$("culture").value,k=$("kind").value,s=$("scale").value,d=$("domain").value,e=$("example").value;
  options($("example"),samples.map((row,i)=>[String(i),t(row[0])]),e);
  options($("culture"),[["*",t("noCulture")],...catalog.cultures.map(x=>[x.id,l(x.label)]),...["hindou","africain"].map(x=>[x,x])],c);
  options($("domain"),[["",t("all")],...Object.keys(domainWords).map(x=>[x,pair(domainWords[x])])],d);
  rebuildKinds(k);rebuildScales(s);
  const coverage=catalog.coverage;
  $("coverage").textContent=locale==="fr"?`${coverage.generic_templates} modèles génériques · ${coverage.cultural_profiles} profils · ${coverage.cultural_bindings} déclinaisons`:`${coverage.generic_templates} generic blueprints · ${coverage.cultural_profiles} profiles · ${coverage.cultural_bindings} bindings`;
}
function setQuery(q) {
  if(!q || typeof q!=="object" || !q.organization || !catalog.templates.some(x=>x.id===q.organization.kind))throw new Error("invalid query");
  importedExtras={};for(const key of ["adaptations","fallback_locale"])if(q[key]!==undefined)importedExtras[key]=q[key];
  if(["fr","en"].includes(q.locale)&&q.locale!==locale){locale=q.locale;$("locale").value=locale;translateControls();}
  $("culture").value=q.culture;
  if($("culture").value!==q.culture){const o=el("option",q.culture);o.value=q.culture;$("culture").append(o);$("culture").value=q.culture;}
  $("domain").value="";rebuildKinds(q.organization.kind);rebuildScales(q.organization.scale);
  $("mode").value=q.mode||"historical";$("role").value=q.role||"";$("year").value=q.as_of??"";$("traits").value=(q.organization.traits||[]).join(", ");
}
function makeQuery() { const q={schema_version:"1.0",culture:$("culture").value,organization:{kind:$("kind").value,scale:$("scale").value},locale,mode:$("mode").value,...importedExtras};if($("role").value.trim())q.role=$("role").value.trim();if($("year").value)q.as_of=Number($("year").value);const traits=$("traits").value.split(",").map(x=>x.trim()).filter(Boolean);if(traits.length)q.organization.traits=traits;return q; }
function badge(ev) {return el("span",t(ev.status),"badge"+(ev.status==="source_supported"?" sourced":""));}
function heading(target,key) {target.append(el("h3",t(key),"subsection"));}
function render() {
  for(const id of ["diagnostics","candidates","institution","roles","structure","sources"])$(id).replaceChildren();
  if(!result)return;
  for(const d of result.diagnostics)$("diagnostics").append(el("p",l(d.message),"diagnostic"+(result.status==="resolved"?"":" error")));
  if(result.status!=="resolved")$("diagnostics").prepend(el("h2",t(result.status),"subsection"));
  for(const c of result.candidates){const b=el("button",l(c.label),"candidate");b.type="button";b.onclick=()=>{$("culture").value=c.culture;run();};$("candidates").append(b);}
  const bp=result.blueprint;if(!bp)return;
  const head=el("div",undefined,"institution-head"),labels=el("div");labels.append(el("h2",l(bp.label)));
  if(result.culture)labels.append(el("p",`${l(result.culture.label)} · ${result.culture.period.join("–")}`,"meta"));
  labels.append(el("p",`${pair(domainWords[bp.domain])} · ${pair(scaleWords[result.request.organization.scale])}`,"meta"));head.append(labels,badge(bp.evidence));$("institution").append(head,el("p",t("genericOffices"),"description"));
  for(const r of bp.roles.filter(x=>result.selected_roles.includes(x.id))) {
    const article=el("article",undefined,"office");article.dataset.role=r.id;
    const h=el("div",undefined,"office-heading"),names=el("div");names.append(el("h3",r.title.labels[locale]||r.title.labels.en,"office-title"));
    if(r.title.native)names.append(el("p",r.title.native,"native"));
    const translations=el("div",undefined,"translations");for(const lang of ["fr","en"]){const p=el("span");p.append(el("b",t(lang)+" : "),document.createTextNode(r.title.labels[lang]));translations.append(p);}names.append(translations);h.append(names,badge(r.title_evidence));article.append(h);
    const b=el("div",undefined,"office-body");b.append(el("p",`${r.function} / ${r.id}`,"role-function"));
    b.append(el("p",`${t(r.holder)} · ${t("capacity")} : ${r.min_holders}–${r.max_holders??t("unbounded")}`,"meta"));
    if(r.rank)b.append(el("p",`${t("rank")} : ${r.rank.labels[locale]}`));
    b.append(el("p",l(r.duties)));
    b.append(el("strong",t("powers")));
    const powers=el("ul");for(const p of r.powers){const li=el("li");li.append(el("span",pair(basisWords[p.basis])),badge(p.evidence),el("p",l(p.scope)),el("p",l(p.limits),"meta"));powers.append(li);}b.append(powers);
    if(r.rules.length){b.append(el("strong",t("rules")));const list=el("ul");for(const entry of r.rules){const li=el("li",l(entry.description));li.append(badge(entry.evidence));list.append(li);}b.append(list);}
    article.append(b);$("roles").append(article);
  }
  const name=id=>{const role=bp.roles.find(r=>r.id===id);return role?.title.labels[locale]||id;};
  if(bp.relations.length){heading($("structure"),"structure");const links=el("div",undefined,"relations");for(const r of bp.relations){const p=el("p",`${name(r.source)} — ${pair(relationWords[r.kind])} — ${name(r.target)}`);p.append(badge(r.evidence));links.append(p);}$("structure").append(links);}
  if(bp.rules.length){heading($("structure"),"rules");const rules=el("ul",undefined,"rules");for(const r of bp.rules){const li=el("li",l(r.description));li.append(badge(r.evidence));rules.append(li);}$("structure").append(rules);}
  if(bp.units.length){heading($("structure"),"units");for(const u of bp.units){const target=catalog.templates.find(t=>t.id===u.kind);$("structure").append(el("p",`${target?l(target.label):u.kind} : ${l(u.note)}`,"meta"));}}
  if(result.sources.length){heading($("sources"),"sources");for(const s of result.sources){const div=el("div",undefined,"source");const link=el("a",`${s.publisher} — ${s.title}`);link.href=s.url;link.target="_blank";link.rel="noopener noreferrer";div.append(link,el("p",s.locator),el("p",l(s.supports)),el("p",l(s.limitations)));$("sources").append(div);}}
}
async function run(importedQuery) {
  const id=++sequence;const q=importedQuery||makeQuery();currentQuery=q;$("request-preview").textContent=JSON.stringify(q,null,2);$("query-form").querySelector("button").disabled=true;document.querySelector(".results").setAttribute("aria-busy","true");
  try{const response=await fetch("/api/resolve",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(q)});const data=await response.json();if(id!==sequence)return;if(!response.ok)throw new Error("invalid query");result=data;render();}
  catch(error){if(id===sequence){console.error(error);result=null;render();$("diagnostics").append(el("p",importedQuery?t("invalidFile"):t("networkError"),"diagnostic error"));}}
  finally{if(id===sequence){$("query-form").querySelector("button").disabled=false;document.querySelector(".results").setAttribute("aria-busy","false");}}
}
function download(value,name){if(!value)return;const blob=new Blob([JSON.stringify(value,null,2)+"\n"],{type:"application/json"});const url=URL.createObjectURL(blob);const a=el("a");a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);$("action-message").textContent=t("downloaded");}
$("query-form").onsubmit=e=>{e.preventDefault();run();};
$("domain").onchange=()=>rebuildKinds();$("kind").onchange=()=>rebuildScales();
$("culture").onchange=()=>{if($("culture").value==="*")$("mode").value="generic";else if($("mode").value==="generic")$("mode").value="historical";};
$("example").onchange=()=>{const s=samples[Number($("example").value)];setQuery({culture:s[1],organization:{kind:s[2],scale:s[3]},mode:s[1]==="*"?"generic":"historical",...(s[4]||{})});run();};
$("locale").onchange=()=>{locale=$("locale").value;translateControls();run();};
$("copy").onclick=async()=>{try{await navigator.clipboard.writeText(JSON.stringify(currentQuery,null,2));$("action-message").textContent=t("copied");}catch{$("request-preview").focus();}};
$("download-query").onclick=()=>download(currentQuery,"pecking-order-request.json");$("download-result").onclick=()=>download(result,"pecking-order-result.json");
$("import-query").onchange=async e=>{const file=e.target.files[0];if(!file)return;try{if(file.size>32768)throw new Error("size");const q=JSON.parse(await file.text());setQuery(q);await run(q);$("action-message").textContent=result?t("imported"):t("invalidFile");}catch{$("action-message").textContent=t("invalidFile");}finally{e.target.value="";}};
(async()=>{try{const response=await fetch("/api/catalog");if(!response.ok)throw new Error("catalog");catalog=await response.json();translateControls();const s=samples[0];setQuery({culture:s[1],organization:{kind:s[2],scale:s[3]}});await run();}catch{$("diagnostics").append(el("p",t("networkError"),"diagnostic error"));}})();
