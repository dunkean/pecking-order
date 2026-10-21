"use strict";
const $ = id => document.getElementById(id);
const words = {
  fr: {
    glossary:"Glossaire complet",structures:"Structures",language:"Langue",intro:"Tous les titres, leurs variantes et leurs fonctions, dans un seul index. Parcourez les termes sans choisir d’abord une organisation.",
    downloadAll:"Télécharger tout le glossaire (JSON)",search:"Rechercher un terme ou une fonction",culture:"Culture / thème",reset:"Tout réafficher",employment:"Filtrer par emploi dans les organisations",system:"Organisation",family:"Domaine",function:"Famille de rôle",sort:"Tri",perPage:"Par page",exportCsv:"Exporter la sélection (CSV)",previous:"Précédent",next:"Suivant",back:"Ouvrir l’explorateur de structures",
    explanation:"Les mêmes intitulés sont regroupés ; chaque culture, variante et emploi reste consultable. Les niveaux et l’importance sont propres à l’organisation où le rôle est utilisé.",
    all:"Tous",allThemes:"Toutes les cultures",allSystems:"Toutes les organisations",allFunctions:"Tous les rôles",allFamilies:"Tous les domaines",showAll:"Tout afficher",titles:"Titres et variantes",functions:"Fonctions",systems:"Organisations",powers:"Pouvoirs",primary:"Titre principal",feminine:"Féminin",masculine:"Masculin",plural:"Pluriel",alternative:"Variante",neutral:"Forme neutre",functional:"Intitulé fonctionnel",
    cultures:"Cultures et thèmes",meanings:"Fonctions et emplois",variantsOf:"Variante de",noUse:"Titre disponible dans le lexique ; aucune organisation actuelle ne l’emploie.",noMatch:"Aucun terme ne correspond à ces filtres. Vous pouvez tout réafficher pour reprendre la consultation.",level:"Niveau",importance:"Importance",collective:"Organe collectif",individual:"Fonction individuelle",optional:"Charge facultative",open:"Ouvrir l’organisation",key:"Référence du rôle",powerKey:"Référence du pouvoir",roles:"rôles",termCount:"termes",functionCount:"fonctions",systemCount:"organisations",powerCount:"pouvoirs",more:"autres",error:"Impossible de charger le glossaire. Vérifiez que le serveur Rust est lancé.",exported:"La sélection complète a été exportée, sur toutes les pages.",definition:"Mission / définition",fr:"Français",en:"English",native:"Forme d’origine",
    political:"Gouvernance et territoires",administrative:"Administration",military:"Armée",religious:"Religions et cultes",economic:"Métiers et économie",kinship:"Maisons, clans et lignages",judicial:"Justice",educational:"Savoir et enseignement",civic:"Associations et vie collective",clandestine:"Sociétés secrètes",fantastic:"Organisations fantastiques"
  },
  en: {
    glossary:"Complete glossary",structures:"Structures",language:"Language",intro:"Every title, its variants and its functions in one index. Browse the terms without choosing an organization first.",
    downloadAll:"Download the entire glossary (JSON)",search:"Find a term or function",culture:"Culture / theme",reset:"Show everything",employment:"Filter by use in organizations",system:"Organization",family:"Domain",function:"Role family",sort:"Sort",perPage:"Per page",exportCsv:"Export selection (CSV)",previous:"Previous",next:"Next",back:"Open the structure explorer",explanation:"Identical titles are grouped together; every culture, variant and use remains available. Level and importance belong to the organization in which a role is used.",
    all:"All",allThemes:"All cultures",allSystems:"All organizations",allFunctions:"All roles",allFamilies:"All domains",showAll:"Show all",titles:"Titles and variants",functions:"Functions",systems:"Organizations",powers:"Powers",primary:"Main title",feminine:"Feminine",masculine:"Masculine",plural:"Plural",alternative:"Variant",neutral:"Neutral form",functional:"Functional title",
    cultures:"Cultures and themes",meanings:"Functions and uses",variantsOf:"Variant of",noUse:"This title is available in the lexicon; no current organization assigns it.",noMatch:"No terms match these filters. Show everything to start browsing again.",level:"Level",importance:"Importance",collective:"Collective body",individual:"Individual office",optional:"Optional office",open:"Open organization",key:"Role reference",powerKey:"Power reference",roles:"roles",termCount:"terms",functionCount:"functions",systemCount:"organizations",powerCount:"powers",more:"more",error:"Could not load the glossary. Check that the Rust server is running.",exported:"The complete selection has been exported across all pages.",definition:"Duty / definition",fr:"Français",en:"English",native:"Original form",
    political:"Government and territories",administrative:"Administration",military:"Military",religious:"Religions and cults",economic:"Crafts and economy",kinship:"Houses, clans and lineages",judicial:"Justice",educational:"Learning and teaching",civic:"Associations and civic life",clandestine:"Secret societies",fantastic:"Fantastic organizations"
  }
};
const params = new URLSearchParams(location.search);
let locale = params.get("locale") === "en" ? "en" : "fr";
const state = {
  tab:["titles","functions","systems","powers"].includes(params.get("tab")) ? params.get("tab") : "titles",
  q:params.get("q") || "",theme:params.get("theme") || "",system:params.get("system") || "",
  family:params.get("family") || "",function:params.get("function") || "",
  letter:params.get("letter") || "",sort:params.get("sort") === "en" ? "en" : "fr",
  size:["100","250","500","all"].includes(params.get("size")) ? params.get("size") : "100",
  page:Math.max(1,Number(params.get("page")) || 1)
};
let data, rawGlossary, matches = [], timer;
let themes, systems, functions, termsByKey, powers;
const t = key => words[locale][key] || key;
const l = value => value?.[locale] || value?.en || "";
const normalize = value => String(value || "").normalize("NFKD").replace(/\p{M}/gu, "").toLowerCase().replace(/[^\p{L}\p{N}]+/gu," ").trim();
const number = value => new Intl.NumberFormat(locale).format(value);
const collator = () => new Intl.Collator(state.sort,{sensitivity:"base",numeric:true});
function node(tag,text,cls) {
  const result = document.createElement(tag);
  if(text !== undefined)result.textContent = text;
  if(cls)result.className = cls;
  return result;
}
function selectOptions(id,rows,selected) {
  const target=$(id);
  target.replaceChildren(...rows.map(([value,label]) => {const option=node("option",label);option.value=value;return option;}));
  target.value=rows.some(row=>row[0]===selected)?selected:"";
}
function prepare() {
  themes=new Map(data.themes.map(theme=>[theme.id,theme]));
  systems=new Map(data.systems.map(system=>[system.id,system]));
  functions=new Map(data.functions.map(fn=>[fn.key,fn]));
  termsByKey=new Map();
  powers=new Map(data.powers.map(power=>[power.id,power]));
  for(const fn of data.functions) {
    fn.search=normalize(`${fn.key} ${fn.label.fr} ${fn.label.en} ${fn.uses.map(use=>`${use.function} ${use.duties.fr} ${use.duties.en}`).join(" ")}`);
  }
  for(const term of data.terms) {
    term.keys=[...new Set(term.bindings.map(binding=>binding.key))];
    term.search=normalize(`${term.fr} ${term.en} ${term.native||""} ${term.keys.map(key=>`${key} ${functions.get(key)?.label.fr||""} ${functions.get(key)?.label.en||""}`).join(" ")} ${term.bindings.map(b=>b.parent?`${b.parent.fr} ${b.parent.en}`:"").join(" ")}`);
    for(const key of term.keys){if(!termsByKey.has(key))termsByKey.set(key,[]);termsByKey.get(key).push(term);}
  }
  for(const system of data.systems) {
    system.keys=data.functions.filter(fn=>fn.uses.some(use=>use.system===system.id)).map(fn=>fn.key);
    system.search=normalize(`${system.id} ${system.label.fr} ${system.label.en} ${system.description.fr} ${system.description.en}`);
  }
  for(const power of data.powers) {
    power.uses=data.functions.flatMap(fn=>fn.uses.filter(use=>use.powers.includes(power.id)).map(use=>({...use,key:fn.key})));
    power.search=normalize(`${power.id} ${power.label.fr} ${power.label.en}`);
  }
}
function useMatches(use,binding) {
  return (!state.system||use.system===state.system)&&(!state.family||use.family===state.family)&&(!binding?.system||use.system===binding.system);
}
function bindingMatches(binding) {
  if(state.theme && binding.theme!==state.theme) {
    // Functional titles are shared across cultures when no cultural lexical
    // entry replaces them. Keep these context-specific roles visible too.
    if(binding.theme || (termsByKey.get(binding.key)||[]).some(term=>term.bindings.some(b=>b.theme===state.theme)))return false;
  }
  if(state.function && binding.key!==state.function)return false;
  if(!state.system&&!state.family)return true;
  return (functions.get(binding.key)?.uses||[]).some(use=>useMatches(use,binding));
}
function matchingBindings(term) {return term.bindings.filter(bindingMatches);}
function termMatches(term,needle) {
  const bindings=matchingBindings(term);
  if(!bindings.length)return false;
  return !needle||term.search.includes(needle)||bindings.some(binding=>(functions.get(binding.key)?.search||"").includes(needle));
}
function usesFor(term) {
  const found=new Map();
  for(const binding of matchingBindings(term)) {
    for(const use of functions.get(binding.key)?.uses||[])if(useMatches(use,binding))found.set(`${binding.key}:${use.system}:${use.role}`,{...use,key:binding.key});
  }
  return [...found.values()];
}
function label(item) {return state.tab==="titles"?item[state.sort]:item.label[state.sort];}
function letter(item) {const start=normalize(label(item)).charAt(0).toUpperCase();return /^[A-Z]$/.test(start)?start:"#";}
function filtered() {
  const needle=normalize(state.q);
  let result;
  if(state.tab==="titles")result=data.terms.filter(term=>termMatches(term,needle));
  else if(state.tab==="functions")result=data.functions.filter(fn=>
    (!state.function||fn.key===state.function)&&
    (!state.system&&!state.family||fn.uses.some(use=>useMatches(use)))&&
    (!state.theme||(termsByKey.get(fn.key)||[]).some(term=>term.bindings.some(b=>b.key===fn.key&&b.theme===state.theme)))&&
    (!needle||fn.search.includes(needle)||(termsByKey.get(fn.key)||[]).some(term=>term.search.includes(needle)&&matchingBindings(term).some(b=>b.key===fn.key)))
  );
  else if(state.tab==="systems")result=data.systems.filter(system=>
    (!state.system||system.id===state.system)&&(!state.family||system.family===state.family)&&(!state.function||system.keys.includes(state.function))&&
    (!needle||system.search.includes(needle)||system.keys.some(key=>(functions.get(key)?.search||"").includes(needle)))
  );
  else result=data.powers.filter(power=>
    (!state.function&&!state.system&&!state.family||power.uses.some(use=>useMatches(use)&&(!state.function||use.key===state.function)))&&
    (!needle||power.search.includes(needle))
  );
  const available=new Set(result.map(letter));
  if(state.letter)result=result.filter(item=>letter(item)===state.letter);
  result.sort((a,b)=>collator().compare(label(a),label(b))||collator().compare(state.tab==="titles"?a.en:a.id||a.key,state.tab==="titles"?b.en:b.id||b.key));
  return {result,available};
}
function translate() {
  document.documentElement.lang=locale;document.title=`${t("glossary")} — Pecking Order`;
  for(const item of document.querySelectorAll("[data-i]"))item.textContent=t(item.dataset.i);
  $("locale").value=locale;
  const cmp=(a,b)=>new Intl.Collator(locale,{sensitivity:"base"}).compare(l(a.label),l(b.label));
  selectOptions("theme",[["",t("allThemes")],...[...data.themes].sort(cmp).map(theme=>[theme.id,l(theme.label)])],state.theme);
  selectOptions("system",[["",t("allSystems")],...[...data.systems].sort(cmp).map(system=>[system.id,l(system.label)])],state.system);
  selectOptions("family",[["",t("allFamilies")],...[...new Set(data.systems.map(s=>s.family))].sort((a,b)=>t(a).localeCompare(t(b))).map(f=>[f,t(f)])],state.family);
  selectOptions("function",[["",t("allFunctions")],...[...data.functions].sort(cmp).map(fn=>[fn.key,`${l(fn.label)} (${fn.key})`])],state.function);
  $("per-page").querySelector('[value="all"]').textContent=t("showAll");
  $("search").placeholder=locale==="fr"?"Tsar, reine, Karta, chef…":"Tsar, queen, Karta, chief…";
  $("search").value=state.q;$("sort").value=state.sort;$("per-page").value=state.size;
  $("employment-filters").open=Boolean(state.system||state.family||state.function);
  const count=data.counts;
  $("totals").textContent=locale==="fr"?
    `${number(count.terms)} termes distincts, variantes comprises · ${number(count.themes)} cultures · ${number(count.functions)} familles de rôles · ${number(count.systems)} organisations. Les ${number(count.authored_title_entries)} entrées de titres sont regroupées par libellé.`:
    `${number(count.terms)} distinct terms including variants · ${number(count.themes)} cultures · ${number(count.functions)} role families · ${number(count.systems)} organizations. The ${number(count.authored_title_entries)} title entries are grouped by wording.`;
  const counts={titles:count.terms,functions:count.functions,systems:count.systems,powers:count.powers};
  for(const button of document.querySelectorAll("[data-tab]")) {
    const tab=button.dataset.tab;button.textContent=`${t(tab)} (${number(counts[tab])})`;
    button.classList.toggle("selected",tab===state.tab);button.setAttribute("aria-pressed",String(tab===state.tab));
  }
  $("theme").disabled=state.tab==="systems"||state.tab==="powers";
}
function synchronizeUrl() {
  const params=new URLSearchParams();
  for(const key of ["q","theme","system","family","function","letter"])if(state[key])params.set(key,state[key]);
  if(state.tab!=="titles")params.set("tab",state.tab);
  if(state.size!=="100")params.set("size",state.size);
  if(state.sort!=="fr")params.set("sort",state.sort);
  if(state.page>1)params.set("page",String(state.page));
  if(locale!=="fr")params.set("locale",locale);
  history.replaceState(null,"",`/glossary${params.size?"?"+params:""}`);
}
function drawAlphabet(available) {
  $("alphabet").replaceChildren();
  for(const value of ["",..."ABCDEFGHIJKLMNOPQRSTUVWXYZ","#"]) {
    const button=node("button",value||t("all"),state.letter===value?"selected":undefined);
    button.type="button";button.disabled=Boolean(value&&!available.has(value)&&state.letter!==value);
    button.setAttribute("aria-pressed",String(state.letter===value));
    button.onclick=()=>{state.letter=value;state.page=1;render();};$("alphabet").append(button);
  }
}
function short(text,size=210) {return text.length>size?text.slice(0,size-1).trimEnd()+"…":text;}
function cultureIds(term) {return [...new Set(matchingBindings(term).map(binding=>binding.theme).filter(Boolean))];}
function systemHref(id,theme) {
  const params=new URLSearchParams({system:id,theme:theme||state.theme||"generic",locale});
  return `/?${params}`;
}
function usageGroups(uses) {
  const result=new Map();
  for(const use of uses) {
    const key=`${use.key}:${use.function}:${use.scope}:${use.duties.fr}:${use.duties.en}`;
    if(!result.has(key))result.set(key,{...use,systems:new Map(),levels:[],weights:[]});
    const group=result.get(key);group.systems.set(use.system,use);group.levels.push(use.level);group.weights.push(use.importance);
  }
  return [...result.values()];
}
function range(values) {const low=Math.min(...values),high=Math.max(...values);return low===high?String(low):`${low}–${high}`;}
function renderUsages(target,uses,term) {
  if(!uses.length){target.append(node("p",t("noUse"),"note"));return;}
  for(const group of usageGroups(uses)) {
    const block=node("section",undefined,"usage-group");
    const roleLabel=functions.get(group.key)?.label;
    block.append(node("h3",roleLabel?l(roleLabel):group.key),node("p",l(group.duties)));
    const meta=node("div",undefined,"usage-meta");
    for(const text of [`${t("level")} ${range(group.levels)}`,`${t("importance")} ${range(group.weights)}/100`,group.collective?t("collective"):t("individual"),`${group.function} / ${group.scope}`])meta.append(node("span",text));
    block.append(meta);
    const systemLinks=node("div",undefined,"system-links");
    const theme=state.theme||term?.bindings.find(b=>b.key===group.key&&b.theme)?.theme||"generic";
    for(const [id] of group.systems){const link=node("a",l(systems.get(id)?.label)||id);link.href=systemHref(id,theme);systemLinks.append(link);}
    block.append(systemLinks);target.append(block);
  }
}
function addTag(target,text,form=false) {target.append(node("span",text,`tag${form?" form-tag":""}`));}
function entryHead(fr,en,native) {
  const head=node("div",undefined,"term-heading");head.append(node("h2",fr),node("p",en,"english"));
  if(native)head.append(node("p",native,"term-native"));return head;
}
function titleEntry(term) {
  const entry=node("details",undefined,"glossary-entry");entry.dataset.term=term.fr;
  const summary=node("summary");summary.append(entryHead(term.fr,term.en,term.native));
  const uses=usesFor(term),bindings=matchingBindings(term),tags=node("div",undefined,"term-tags"),cultures=cultureIds(term);
  const forms=[...new Set(bindings.map(b=>b.form).filter(form=>form!=="primary"))];
  for(const form of forms)addTag(tags,t(form),true);
  for(const id of cultures.slice(0,3))addTag(tags,l(themes.get(id)?.label)||id);
  if(cultures.length>3)addTag(tags,`+ ${cultures.length-3} ${t("more")}`);
  summary.append(tags);
  const definition=uses[0]?.duties;
  summary.append(node("p",definition?short(l(definition)):bindings.map(b=>l(functions.get(b.key)?.label)).filter(Boolean).filter((v,i,a)=>a.indexOf(v)===i).join(" / "),"term-summary"));
  const detail=node("div",undefined,"term-detail");entry.append(summary,detail);
  entry.addEventListener("toggle",()=>{
    if(!entry.open||detail.childElementCount)return;
    const parents=[...new Set(bindings.filter(b=>b.parent).map(b=>`${b.parent.fr} / ${b.parent.en}`))];
    for(const parent of parents)detail.append(node("p",`${t("variantsOf")} : ${parent}`));
    if(cultures.length){detail.append(node("h3",t("cultures")));const list=node("div",undefined,"culture-list");for(const id of cultures){const button=node("button",l(themes.get(id).label));button.type="button";button.onclick=()=>{state.theme=id;state.page=1;translate();render();};list.append(button);}detail.append(list);}
    detail.append(node("h3",t("meanings")));renderUsages(detail,uses,term);
  });
  return entry;
}
function functionEntry(fn) {
  const entry=node("details",undefined,"glossary-entry"),summary=node("summary");summary.append(entryHead(fn.label.fr,fn.label.en));
  const uses=fn.uses.filter(use=>useMatches(use)).map(use=>({...use,key:fn.key}));
  summary.append(node("p",uses[0]?short(l(uses[0].duties)):t("noUse"),"term-summary"));
  const tags=node("div",undefined,"term-tags");addTag(tags,`${new Set(uses.map(use=>use.system)).size} ${t("systemCount")}`);summary.append(tags);
  const detail=node("div",undefined,"term-detail");entry.append(summary,detail);
  entry.addEventListener("toggle",()=>{if(!entry.open||detail.childElementCount)return;detail.append(node("p",`${t("key")} : ${fn.key}`,"muted"));
    const link=node("a",t("titles"));const params=new URLSearchParams({function:fn.key,locale});if(state.theme)params.set("theme",state.theme);link.href=`/glossary?${params}`;detail.append(link);renderUsages(detail,uses);
  });return entry;
}
function systemEntry(system) {
  const entry=node("details",undefined,"glossary-entry"),summary=node("summary");summary.append(entryHead(system.label.fr,system.label.en),node("p",short(l(system.description)),"term-summary"));
  const tags=node("div",undefined,"term-tags");addTag(tags,t(system.family));addTag(tags,`${system.role_count} ${t("roles")}`);summary.append(tags);
  const detail=node("div",undefined,"term-detail");entry.append(summary,detail);
  entry.addEventListener("toggle",()=>{if(!entry.open||detail.childElementCount)return;detail.append(node("p",l(system.description)));const link=node("a",t("open"),"system-open");link.href=systemHref(system.id);detail.append(link);
    const uses=system.keys.flatMap(key=>functions.get(key).uses.filter(use=>use.system===system.id&&(!state.function||key===state.function)).map(use=>({...use,key})));
    renderUsages(detail,uses);
  });return entry;
}
function powerEntry(power) {
  const entry=node("details",undefined,"glossary-entry"),summary=node("summary");summary.append(entryHead(power.label.fr,power.label.en));
  const uses=power.uses.filter(use=>useMatches(use)&&(!state.function||use.key===state.function));
  summary.append(node("p",`${new Set(uses.map(use=>use.system)).size} ${t("systemCount")}`,"term-summary"));const detail=node("div",undefined,"term-detail");entry.append(summary,detail);
  entry.addEventListener("toggle",()=>{if(!entry.open||detail.childElementCount)return;detail.append(node("p",`${t("powerKey")} : ${power.id}`,"muted"));renderUsages(detail,uses);});return entry;
}
function render() {
  const filteredResult=filtered();matches=filteredResult.result;drawAlphabet(filteredResult.available);
  const size=state.size==="all"?Math.max(1,matches.length):Number(state.size),pages=Math.max(1,Math.ceil(matches.length/size));
  state.page=Math.min(state.page,pages);const start=(state.page-1)*size,end=Math.min(matches.length,start+size);
  const kind=t({titles:"termCount",functions:"functionCount",systems:"systemCount",powers:"powerCount"}[state.tab]);
  $("results-count").textContent=locale==="fr"?`${number(matches.length)} ${kind} · ${matches.length?number(start+1):0}–${number(end)} affichés`:`${number(matches.length)} ${kind} · showing ${matches.length?number(start+1):0}–${number(end)}`;
  $("results-count").dataset.count=String(matches.length);
  const fragment=document.createDocumentFragment();
  const make={titles:titleEntry,functions:functionEntry,systems:systemEntry,powers:powerEntry}[state.tab];
  for(const item of matches.slice(start,end))fragment.append(make(item));
  if(!matches.length)fragment.append(node("p",t("noMatch"),"empty-state"));
  $("entries").replaceChildren(fragment);$("entries").setAttribute("aria-busy","false");
  $("previous").disabled=state.page<=1;$("next").disabled=state.page>=pages;$("page-label").textContent=`Page ${number(state.page)} / ${number(pages)}`;
  $("pagination").hidden=state.size==="all"||pages===1;synchronizeUrl();
}
function change(key,value) {state[key]=value;state.page=1;if(key==="q")state.letter="";render();}
function csvRows() {
  if(state.tab==="titles")return [[t("fr"),t("en"),t("native"),t("cultures"),t("function"),t("definition")],...matches.map(term=>[
    term.fr,term.en,term.native||"",cultureIds(term).map(id=>l(themes.get(id).label)).join(" | "),
    [...new Set(matchingBindings(term).map(binding=>l(functions.get(binding.key)?.label)||binding.key))].join(" | "),
    [...new Set(usesFor(term).map(use=>l(use.duties)))].join("\n")
  ])];
  return [["ID",t("fr"),t("en"),t("definition")],...matches.map(item=>[item.id||item.key,item.label.fr,item.label.en,item.description?l(item.description):[...new Set((item.uses||[]).filter(use=>useMatches(use)).map(use=>l(use.duties)))].join("\n")])];
}
function download(blob,name) {const url=URL.createObjectURL(blob),link=node("a");link.href=url;link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$("search").addEventListener("input",()=>{clearTimeout(timer);timer=setTimeout(()=>change("q",$("search").value),100);});
for(const key of ["theme","system","family","function"])$(key).addEventListener("change",()=>change(key,$(key).value));
$("sort").onchange=()=>change("sort",$("sort").value);$("per-page").onchange=()=>change("size",$("per-page").value);
$("locale").onchange=()=>{const before=locale;locale=$("locale").value;if(state.sort===before)state.sort=locale;translate();render();};
for(const button of document.querySelectorAll("[data-tab]"))button.onclick=()=>{state.tab=button.dataset.tab;state.page=1;state.letter="";translate();render();};
$("previous").onclick=()=>{state.page--;render();$("results-count").scrollIntoView({block:"start"});};$("next").onclick=()=>{state.page++;render();$("results-count").scrollIntoView({block:"start"});};
$("reset").onclick=()=>{for(const key of ["q","theme","system","family","function","letter"])state[key]="";state.page=1;translate();render();};
$("export-csv").onclick=()=>{const raw=csvRows().map(row=>row.map(cell=>'"'+String(cell).replaceAll('"','""')+'"').join(";")).join("\r\n");download(new Blob(["\ufeff",raw],{type:"text/csv;charset=utf-8"}),`pecking-order-${state.tab}.csv`);$("export-message").textContent=t("exported");};
$("download-all").onclick=event=>{if(!data)return;event.preventDefault();download(new Blob([rawGlossary],{type:"application/json"}),"pecking-order-glossary.json");};
(async()=>{try{
  const response=await fetch("/api/glossary");if(!response.ok)throw new Error("glossary");rawGlossary=await response.text();data=JSON.parse(rawGlossary);prepare();translate();render();
}catch(error){console.error(error);$("error").append(node("p",t("error"),"error"));$("entries").setAttribute("aria-busy","false");}})();
