"use strict";
const $ = id => document.getElementById(id);
let catalog, result, applied, locale = "fr", view = "roles", requestId = 0, timer;
let extraFilter = {};
const strings = {
  fr: {
    rolesView:"Structures",lexiconView:"Lexique culturel",api:"Contrat d’API",language:"Langue",
    headline:"Un système. Une culture. Tous les rôles.",
    intro:"Du trône impérial à la cellule d’un culte secret : choisissez l’organisation, puis donnez-lui les titres de votre monde.",
    chooseSystem:"Choisir un système",family:"Famille d’organisation",findSystem:"Rechercher un système",system:"Système",
    chooseTheme:"Choisir les titres",theme:"Thème / culture",size:"Taille de l’organisation",options:"Structure et pouvoir",
    structure:"Structure",authority:"Exercice du pouvoir",members:"Effectif exact (facultatif)",resolve:"Afficher les titres et rôles",
    try:"Aller directement à",east:"Nation aristocratique, Europe de l’Est",west:"La même, Europe de l’Ouest",
    tswana:"Village tswana",cult:"Cellule secrète de quatre personnes",jointFamily:"Famille hindoue indivise",
    filterRoles:"Filtrer les rôles et titres",minImportance:"Importance minimale",maxLevel:"Jusqu’au niveau",
    request:"La requête",requestDescription:"Le moteur Rust renvoie les titres FR/EN, fonctions, niveaux, importance, responsabilités et relations. Aucun compte ni service externe.",
    copy:"Copier",exportQuery:"Exporter la requête",exportResult:"Exporter le résultat",import:"Importer une requête",
    footer:"Des thèmes de worldbuilding, librement combinables avec les systèmes. Les fonctions restent stables ; leurs titres changent avec la culture.",
    default:"Défaut du système",all:"Tous",full:"Tous les échelons",tiny:"Minuscule / cellule",small:"Petit groupe",medium:"Organisation moyenne",large:"Grande organisation",vast:"Organisation immense",
    hierarchical:"Verticale / hiérarchique",horizontal:"Horizontale",network:"En réseau",cellular:"Cellulaire",
    hereditary:"Héréditaire",aristocratic:"Aristocratique",authoritarian:"Autoritaire",democratic:"Démocratique",theocratic:"Théocratique",
    military:"Militaire",bureaucratic:"Bureaucratique",meritocratic:"Méritocratique",consensual:"Par consensus",personal:"Fidélité personnelle",
    political:"Gouvernance et territoires",administrative:"Administration",religious:"Religions et cultes",economic:"Métiers et économie",kinship:"Maisons, clans et lignages",judicial:"Justice",educational:"Savoir et enseignement",civic:"Associations et vie collective",clandestine:"Sociétés secrètes et clandestinité",fantastic:"Organisations fantastiques",
    importance:"Importance",level:"Niveau",collective:"Organe collectif",individual:"Fonction individuelle",optional:"Charge facultative",reportsTo:"Rend compte à",powers:"Pouvoirs et compétences",selection:"Accès à la charge",variants:"Autres formes et titres",related:"Organisations associées",empty:"Aucun rôle ne correspond aux filtres.",
    copied:"Requête copiée.",exported:"Fichier exporté.",imported:"Requête importée.",invalidImport:"Le fichier doit contenir une requête JSON valide.",error:"Impossible de charger le résultat.",lexicalKey:"Fonction lexicale",native:"Titre d’origine",titleFr:"Titre français",titleEn:"Titre anglais",lexSearch:"Rechercher dans le lexique",feminine:"Féminin",plural:"Pluriel",alternative:"Variante",neutral:"Forme neutre"
  },
  en: {
    rolesView:"Structures",lexiconView:"Cultural lexicon",api:"API contract",language:"Language",
    headline:"One system. One culture. Every role.",
    intro:"From an imperial throne to a secret cult cell: choose the organization, then give it the titles of your world.",
    chooseSystem:"Choose a system",family:"Organization family",findSystem:"Find a system",system:"System",chooseTheme:"Choose the titles",theme:"Theme / culture",size:"Organization size",options:"Structure and power",structure:"Structure",authority:"Exercise of power",members:"Exact membership (optional)",resolve:"Show titles and roles",
    try:"Jump directly to",east:"Aristocratic nation, Eastern Europe",west:"The same, Western Europe",tswana:"Tswana village",cult:"Secret cell of four people",jointFamily:"Hindu joint family",
    filterRoles:"Filter roles and titles",minImportance:"Minimum importance",maxLevel:"Through level",
    request:"The request",requestDescription:"The Rust engine returns FR/EN titles, functions, levels, importance, responsibilities and relationships. No account or external service.",
    copy:"Copy",exportQuery:"Export request",exportResult:"Export result",import:"Import request",footer:"Worldbuilding themes freely combined with systems. Functions stay stable; titles change with culture.",
    default:"System default",all:"All",full:"Every tier",tiny:"Tiny / cell",small:"Small group",medium:"Medium organization",large:"Large organization",vast:"Vast organization",
    hierarchical:"Vertical / hierarchical",horizontal:"Horizontal",network:"Network",cellular:"Cellular",hereditary:"Hereditary",aristocratic:"Aristocratic",authoritarian:"Authoritarian",democratic:"Democratic",theocratic:"Theocratic",military:"Military",bureaucratic:"Bureaucratic",meritocratic:"Meritocratic",consensual:"Consensus",personal:"Personal loyalty",
    political:"Government and territories",administrative:"Administration",religious:"Religions and cults",economic:"Crafts and economy",kinship:"Houses, clans and lineages",judicial:"Justice",educational:"Learning and teaching",civic:"Associations and civic life",clandestine:"Secret and clandestine groups",fantastic:"Fantastic organizations",
    importance:"Importance",level:"Level",collective:"Collective body",individual:"Individual office",optional:"Optional office",reportsTo:"Reports to",powers:"Powers and competences",selection:"Access to office",variants:"Other forms and titles",related:"Related organizations",empty:"No roles match these filters.",copied:"Request copied.",exported:"File exported.",imported:"Request imported.",invalidImport:"The file must contain a valid JSON request.",error:"Could not load the result.",lexicalKey:"Lexical function",native:"Original title",titleFr:"French title",titleEn:"English title",lexSearch:"Search the lexicon",feminine:"Feminine",plural:"Plural",alternative:"Alternative",neutral:"Neutral form"
  }
};
const t = key => strings[locale][key] || key;
const localized = value => value?.[locale] || value?.en || "";
const normalized = value => value.normalize('NFKD').replace(/\p{M}/gu,'').toLowerCase().split(/[^\p{L}\p{N}]+/u).filter(Boolean).join('-');
strings.fr.masculine="Masculin";strings.en.masculine="Masculine";
strings.fr.glossary="Glossaire complet";strings.en.glossary="Complete glossary";
function element(tag,text,cls) {
  const node=document.createElement(tag);
  if(text!==undefined)node.textContent=text;
  if(cls)node.className=cls;
  return node;
}
function options(node,rows,chosen) {
  node.replaceChildren(...rows.map(([value,label])=>{const option=element("option",label);option.value=value;return option;}));
  if(rows.some(row=>row[0]===chosen))node.value=chosen;
}
function rebuildSystems(chosen) {
  const family=$("family").value, search=$("system-search").value.toLocaleLowerCase();
  const systems=catalog.systems.filter(s=>(!family||s.family===family)&&(!search||`${s.id} ${s.label.fr} ${s.label.en}`.toLocaleLowerCase().includes(search)));
  options($("system"),systems.map(s=>[s.id,localized(s.label)]),chosen);
  updateSystem();
}
function updateSystem() {
  const system=catalog.systems.find(s=>s.id===$("system").value);
  $("system-description").textContent=system?localized(system.description):"";
  const previous=$("max-level").value;
  options($("max-level"),[["",t("all")],...Array.from({length:(system?.max_level??10)+1},(_,i)=>[String(i),`${t("level")} ${i}`])],previous);
}
function translate() {
  document.documentElement.lang=locale;
  for(const node of document.querySelectorAll("[data-t]"))node.textContent=t(node.dataset.t);
  const family=$("family").value,system=$("system").value,theme=$("theme").value;
  options($("family"),[["",t("all")],...[...new Set(catalog.systems.map(s=>s.family))].map(f=>[f,t(f)])],family);
  rebuildSystems(system);
  options($("theme"),catalog.themes.map(c=>[c.id,localized(c.label)]),theme);
  for(const [id,values] of [["size",catalog.sizes],["structure",catalog.structures],["authority",catalog.authorities]]) {
    const current=$(id).value;
    options($(id),[...(id==="size"?[]:[["",t("default")]]),...values.map(v=>[v,t(v)])],current);
  }
  const c=catalog.counts;
  $("counts").textContent=locale==="fr"?`${c.systems} systèmes · ${c.themes} thèmes\n${c.roles} rôles · ${c.titles} titres FR/EN`:`${c.systems} systems · ${c.themes} themes\n${c.roles} roles · ${c.titles} FR/EN titles`;
  $("counts").style.whiteSpace="pre-line";
}
function getQuery() {
  const q={system:$("system").value,theme:$("theme").value,locale};
  if($("size").value!=="full")q.size=$("size").value;
  if($("members").value)q.members=Number($("members").value);
  if($("structure").value)q.structure=$("structure").value;
  if($("authority").value)q.authority=$("authority").value;
  const filter={...extraFilter};
  if($("role-search").value.trim())filter.text=$("role-search").value.trim();
  if(Number($("importance").value)>0)filter.min_importance=Number($("importance").value);
  if($("max-level").value!=="")filter.max_level=Number($("max-level").value);
  if(Object.keys(filter).length)q.filter=filter;
  return q;
}
function setQuery(q) {
  const systemId=q&&catalog.system_aliases[normalized(q.system||"")];
  if(!systemId)throw new Error("system");
  if(q.locale&&["fr","en"].includes(q.locale)&&q.locale!==locale){locale=q.locale;$("locale").value=locale;translate();}
  $("system-search").value="";$("family").value="";rebuildSystems(systemId);
  const themeId=catalog.theme_aliases[normalized(q.theme||"generic")];
  const theme=catalog.themes.find(x=>x.id===themeId);
  if(!theme)throw new Error("theme");
  $("theme").value=theme.id;$("size").value=q.size||"full";$("members").value=q.members??"";
  $("structure").value=q.structure||"";$("authority").value=q.authority||"";
  $("role-search").value=q.filter?.text||"";$("importance").value=q.filter?.min_importance||0;$("importance-value").textContent=$("importance").value;
  $("max-level").value=q.filter?.max_level===undefined?"":String(q.filter.max_level);
  extraFilter={};for(const key of ["functions","scopes"])if(q.filter?.[key])extraFilter[key]=q.filter[key];
  $("advanced").open=Boolean(q.structure||q.authority||q.members);
}
function renderRoles() {
  $("roles").replaceChildren();$("related").replaceChildren();$("notes").replaceChildren();$("result-heading").replaceChildren();
  if(!result)return;
  $("result-heading").append(element("h2",`${localized(result.system.label)} · ${localized(result.theme.label)}`),element("p",localized(result.description)));
  const tags=element("div",undefined,"summary-line");
  for(const tag of [result.size,result.structure,result.authority])tags.append(element("span",t(tag),"tag"));
  $("result-heading").append(tags);
  $("role-count").textContent=locale==="fr"?`${result.roles.length} rôles affichés sur ${result.available_role_count} · niveau 0 = autorité supérieure`:`${result.roles.length} roles shown of ${result.available_role_count} · level 0 = highest authority`;
  if(!result.roles.length)$("roles").append(element("p",t("empty"),"note"));
  const titleById=id=>{const role=result.roles.find(r=>r.id===id);return role?localized(role.title):id;};
  for(const role of result.roles) {
    const details=element("details",undefined,`role level-${role.level}`);details.dataset.role=role.id;
    const summary=element("summary");summary.append(element("span",String(role.level),"level"));
    const names=element("div");names.append(element("h3",localized(role.title),"title"));
    names.append(element("p",`FR : ${role.title.fr} / EN : ${role.title.en}`,"translation"));
    if(role.title.native&&role.title.native!==role.title.fr&&role.title.native!==role.title.en)names.append(element("p",role.title.native,"native"));
    const weight=element("div",undefined,"importance");weight.append(element("span",t("importance")),element("br"),element("strong",String(role.importance)));
    const bar=element("div",undefined,"bar"),fill=element("span");fill.style.setProperty("--value",`${role.importance}%`);bar.append(fill);weight.append(bar);
    summary.append(names,weight);details.append(summary);
    const body=element("div",undefined,"role-body");
    const facts=element("div",undefined,"role-facts");facts.append(element("span",role.collective?t("collective"):t("individual")),element("span",`${role.function} / ${role.scope}`));
    if(role.optional)facts.append(element("span",t("optional")));body.append(facts,element("p",localized(role.duties)));
    if(role.reports_to.length)body.append(element("p",`${t("reportsTo")} : ${role.reports_to.map(titleById).join(", ")}`));
    body.append(element("strong",t("powers")));const powers=element("div",undefined,"power-list");
    for(const power of role.powers)powers.append(element("span",localized(power.label),"power"));body.append(powers);
    body.append(element("p",`${t("selection")} : ${localized(role.selection)}`));
    if(role.title.variants.length){const variants=element("div",undefined,"variants");variants.append(element("strong",t("variants")));for(const v of role.title.variants)variants.append(element("p",`${t(v.qualifier)} : ${v.fr} / ${v.en}`));body.append(variants);}
    details.append(body);$("roles").append(details);
  }
  if(result.related.length){$("related").append(element("h3",t("related")));for(const other of result.related){const b=element("button",localized(other.label));b.onclick=()=>{$("family").value="";$("system-search").value="";rebuildSystems(other.id);run();};$("related").append(b);}}
  for(const note of result.notes)$("notes").append(element("p",localized(note),"note"));
}
async function renderLexicon() {
  if(view!=="lexicon"||!result)return;
  const theme=result.theme.id;
  const response=await fetch(`/api/themes/${encodeURIComponent(theme)}`);const data=await response.json();
  if(view!=="lexicon"||result?.theme.id!==theme)return;
  $("lexicon").replaceChildren();
  const tools=element("div",undefined,"lexicon-tools"),search=element("input");search.type="search";search.placeholder=t("lexSearch");search.setAttribute("aria-label",t("lexSearch"));
  tools.append(element("h3",localized(data.label)),search);$("lexicon").append(tools);
  const table=element("table",undefined,"lexicon-table"),thead=element("thead"),tr=element("tr");
  for(const key of ["lexicalKey","titleFr","titleEn","native"])tr.append(element("th",t(key)));thead.append(tr);table.append(thead);const tbody=element("tbody");table.append(tbody);$("lexicon").append(table);
  function rows(){tbody.replaceChildren();const needle=search.value.toLocaleLowerCase();for(const [key,entry] of Object.entries(data.titles)){const v=entry.title;if(needle&&!`${key} ${v.fr} ${v.en} ${v.native||""}`.toLocaleLowerCase().includes(needle))continue;const row=element("tr");for(const value of [key,v.fr,v.en,v.native||""])row.append(element("td",value));tbody.append(row);}}
  search.oninput=rows;rows();
}
function switchView(next) {
  view=next;$("view-roles").classList.toggle("active",view==="roles");$("view-lexicon").classList.toggle("active",view==="lexicon");
  for(const id of ["filter-panel","role-count","roles","related","notes"])$(id).hidden=view!=="roles";
  $("lexicon").hidden=view!=="lexicon";if(view==="lexicon")renderLexicon().catch(showError);
}
function showError(error) {$("error").replaceChildren(element("p",error?.message?.[locale]||error?.message?.en||t("error"),"error"));}
async function run(imported) {
  if(!$("system").value)return;
  const id=++requestId,q=imported||getQuery();applied=q;$("request-json").textContent=JSON.stringify(q,null,2);$("error").replaceChildren();
  const button=$("query-form").querySelector("button");button.disabled=true;
  try {const response=await fetch("/api/resolve",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(q)});const data=await response.json();if(id!==requestId)return;if(!response.ok){result=null;renderRoles();showError(data);return;}result=data;renderRoles();if(view==="lexicon")await renderLexicon();}
  catch(error){if(id===requestId)showError(error);}finally{if(id===requestId)button.disabled=false;}
}
function debounceRun(){clearTimeout(timer);timer=setTimeout(()=>run(),180);}
function download(data,name){if(!data)return;const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)+"\n"],{type:"application/json"}));const a=element("a");a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);$("action-message").textContent=t("exported");}
const examples={
  east:{system:"aristocratic_nation",theme:"russian-kremlin",authority:"aristocratic"},
  west:{system:"aristocratic_nation",theme:"european-organic",authority:"aristocratic"},
  tswana:{system:"village",theme:"tswana"},
  cult:{system:"cult_cell",theme:"drow-enclave",members:4,structure:"cellular"},
  family:{system:"joint_family",theme:"indian-temple"}
};
$("query-form").onsubmit=e=>{e.preventDefault();run();};
$("family").onchange=()=>{rebuildSystems();run();};$("system-search").oninput=()=>rebuildSystems($("system").value);
$("system").onchange=()=>{updateSystem();extraFilter={};run();};
for(const id of ["theme","size","structure","authority","members"])$(id).onchange=()=>run();
$("role-search").oninput=debounceRun;$("importance").oninput=()=>{$("importance-value").textContent=$("importance").value;debounceRun();};$("max-level").onchange=()=>run();
$("locale").onchange=()=>{locale=$("locale").value;translate();run();};
for(const button of document.querySelectorAll("[data-example]"))button.onclick=()=>{try{setQuery(examples[button.dataset.example]);run();}catch(error){showError(error);}};
$("view-roles").onclick=()=>switchView("roles");$("view-lexicon").onclick=()=>switchView("lexicon");
$("copy").onclick=async()=>{try{await navigator.clipboard.writeText(JSON.stringify(applied,null,2));$("action-message").textContent=t("copied");}catch{$("action-message").textContent=t("error");}};
$("export-query").onclick=()=>download(applied,"pecking-order-request.json");$("export-result").onclick=()=>download(result,"pecking-order-result.json");
$("import-query").onchange=async event=>{const file=event.target.files[0];if(!file)return;try{if(file.size>65536)throw new Error("size");const q=JSON.parse(await file.text());setQuery(q);await run(q);$("action-message").textContent=result?t("imported"):t("invalidImport");}catch{$("action-message").textContent=t("invalidImport");}finally{event.target.value="";}};
(async()=>{try{const response=await fetch("/api/catalog");catalog=await response.json();translate();const params=new URLSearchParams(location.search);setQuery(params.has("system")?{system:params.get("system"),theme:params.get("theme")||"generic",locale:params.get("locale")||"fr"}:examples.east);await run();}catch(error){showError(error);}})();
