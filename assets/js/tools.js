(()=>{const $=i=>document.getElementById(i),list=v=>v.split(/\n|,/).map(s=>s.trim()).filter(Boolean);
const B=["autocomplete_no_prefix", "autocomplete_no_snippets", "autocomplete_name_only", "lowercase_intrinsics", "use_signature_help", "variable_hover", "hover_signature", "enable_code_actions", "symbol_skip_mem", "incremental_sync", "preserve_keyword_order", "debug_log"],ARR=["source_dirs","ext_source_dirs","excl_paths","excl_suffixes","incl_suffixes","pp_suffixes","include_dirs"];
const T={pp_defs:"object",nthreads:"number",max_line_length:"number",max_comment_line_length:"number",hover_language:"string",config:"string",notify_init:"boolean",disable_diagnostics:"boolean"};
ARR.forEach(k=>T[k]="array");B.forEach(k=>T[k]="boolean");
const strip=s=>{let o="",q=0,i=0;while(i<s.length){const c=s[i],n=s[i+1];if(q){o+=c;if(c==="\\"){o+=n||"";i++}else if(c==='"')q=0}else if(c==='"'){q=1;o+=c}else if(c==="/"&&n==="/"){while(i<s.length&&s[i]!=="\n")i++;continue}else if(c==="/"&&n==="*"){i+=2;while(i<s.length&&!(s[i]==="*"&&s[i+1]==="/"))i++;i++}else o+=c;i++}return o};
const gen=()=>{if(!$("g-out"))return;const o={};[["source_dirs","g-src"],["ext_source_dirs","g-ext"],["excl_paths","g-exp"],["excl_suffixes","g-exs"],["include_dirs","g-inc"]].forEach(([k,id])=>{const l=list($(id).value);if(l.length)o[k]=l});B.forEach(k=>{if($("b-"+k).checked)o[k]=true});$("g-out").value=JSON.stringify(o,null,2)+"\n"};
const q=s=>'"'+s.replace(/\\/g,"\\\\").replace(/"/g,'\\"')+'"',g=i=>$(i).value.trim();
const fpm=()=>{if(!$("f-out"))return;let o="name = "+q(g("f-name")||"my_project")+"\nversion = "+q(g("f-ver")||"0.1.0")+"\n";[["license","f-lic"],["author","f-au"],["maintainer","f-mt"]].forEach(([k,i])=>{if(g(i))o+=k+" = "+q(g(i))+"\n"});
o+="\n[build]\nauto-executables = "+$("f-ae").checked+"\nauto-tests = "+$("f-at").checked+"\nauto-examples = "+$("f-ax").checked+"\n";if($("f-lib").checked)o+="\n[install]\nlibrary = true\n";
o+='\n[fortran]\nimplicit-typing = false\nimplicit-external = false\nsource-form = "free"\n';const d=list($("f-dep").value.replace(/\n/g,",").replace(/,\s*(?=\S)/g,"\n")).map(l=>l.split(/\s+/)).filter(a=>a[0]);
if(d.length){o+="\n[dependencies]\n";d.forEach(a=>{o+=a[0]+" = "+(a[1]?"{ git = "+q(a[1])+" }":'"*"')+"\n"})}$("f-out").value=o};
const lint=()=>{const s=$("l-out");let j;try{j=JSON.parse(strip($("l-in").value))}catch(e){s.className="bad";s.textContent="Invalid JSON: "+e.message;return null}
if(!j||typeof j!=="object"||Array.isArray(j)){s.className="bad";s.textContent="Top level must be a JSON object.";return null}const m=[];
for(const[k,v]of Object.entries(j)){const t=T[k];if(!t){m.push('? "'+k+'" is not in this tool\'s list (a typo, or an option from a newer fortls).');continue}const a=Array.isArray(v)?"array":v===null?"null":typeof v;if(a!==t)m.push('! "'+k+'" should be '+t+", found "+a+".")}
s.className=m.length?"warn":"ok";s.textContent=m.length?m.join("\n"):"Valid syntax; all keys recognised with the expected types.";return j};
const flash=(id,t)=>{const s=$("g-st")||$("l-out");const o=s.textContent;s.textContent=t;setTimeout(()=>{s.textContent=o},1200)};
document.addEventListener("input",()=>{gen();fpm()});document.addEventListener("change",()=>{gen();fpm()});
document.addEventListener("click",e=>{const t=e.target;if(t.dataset.copy){const v=$(t.dataset.copy).value;(navigator.clipboard?navigator.clipboard.writeText(v):Promise.reject()).then(()=>flash(0,"Copied."),()=>{$(t.dataset.copy).select();document.execCommand("copy")})}
if(t.dataset.dl){const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([$(t.dataset.dl).value],{type:"text/plain"}));a.download=t.dataset.name;a.click();URL.revokeObjectURL(a.href)}
if(t.id==="l-go")lint();if(t.id==="l-fmt"){const j=lint();if(j)$("l-in").value=JSON.stringify(j,null,2)+"\n"}});
gen();fpm()})();
