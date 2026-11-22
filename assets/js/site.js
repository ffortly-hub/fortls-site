(()=>{const GTM="GTM-P54LMMLJ",GA4="G-1X1ZLKFJ9S",CL="zbdjwrsl12",K="fortls-consent",DIRECT=false;
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}
gtag("consent","default",{ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied",analytics_storage:"denied",wait_for_update:500});
const rd=()=>{try{const j=JSON.parse(localStorage.getItem(K));if(j&&Date.now()-j.t<31536e6)return j.v}catch(e){}return null};
const wr=v=>{try{localStorage.setItem(K,JSON.stringify({v:v,t:Date.now()}))}catch(e){}};
let on=false;
const loadGA=()=>{on=true;gtag("consent","update",{analytics_storage:"granted"});
(function(w,d,s,l,i){w[l].push({"gtm.start":Date.now(),event:"gtm.js"});const f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=1;j.src="https://www.googletagmanager.com/gtm.js?id="+i;f.parentNode.insertBefore(j,f)})(window,document,"script","dataLayer",GTM);
if(DIRECT){gtag("js",new Date());gtag("config",GA4);const s=document.createElement("script");s.async=1;s.src="https://www.googletagmanager.com/gtag/js?id="+GA4;document.head.appendChild(s)}};
const loadCL=()=>{(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)})(window,document,"clarity","script",CL);window.clarity("consentv2",{ad_Storage:"denied",analytics_Storage:"granted"})};
const purge=()=>{const h=location.hostname,p=h.split(".").slice(-2).join(".");document.cookie.split(";").forEach(c=>{const n=c.split("=")[0].trim();if(!/^(_ga|_ga_.+|_gid|_gat.*|_clck|_clsk)$/.test(n))return;const x="=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";document.cookie=n+x;[h,"."+h,"."+p,p].forEach(d=>{document.cookie=n+x+";domain="+d})})};
const track=(ev,p)=>{if(!on)return;p.page_path=location.pathname;dataLayer.push(Object.assign({event:ev},p));if(window.clarity){window.clarity("event",ev);for(const k in p)window.clarity("set",k,String(p[k]))}};
const EV={cloudways:"affiliate_click",vultr:"affiliate_click",beehiiv:"newsletter_click","github-sponsors":"github_sponsor_click",kofi:"kofi_click",paypal:"paypal_click",afternic:"offer_click"};
document.addEventListener("click",e=>{const t=e.target.closest("a,button");if(!t)return;const pe=t.closest("[data-placement]"),pl=pe?pe.dataset.placement:t.closest("footer")?"footer":t.closest("header")?"header":"content";
if(t.dataset.copy||t.dataset.dl){const s=t.closest("section.tool");track(t.dataset.copy?"tool_copy":"tool_download",{tool_name:s?s.id:"unknown",placement:pl});return}
const h=t.getAttribute("href")||"",m=h.match(/^\/go\/([a-z-]+)/);
if(m){const ev=EV[m[1]];if(ev){const p={placement:pl};if(ev==="affiliate_click")p.partner_name=m[1];else p.destination=m[1];track(ev,p)}return}
if(/\.pdf$/i.test(h))track("file_download",{file_name:h.split("/").pop(),file_category:t.dataset.category||"cheat-sheet",placement:pl})});
const cs=document.getElementById("cs");
if(cs)cs.onclick=e=>{e.preventDefault();gtag("consent","update",{analytics_storage:"denied"});purge();try{localStorage.removeItem(K)}catch(x){}location.reload()};
const v=rd();
if(v==="yes"){loadGA();loadCL();return}
if(v==="no")return;
const b=document.createElement("div");b.className="consent";b.setAttribute("role","dialog");b.setAttribute("aria-label","Analytics consent");
b.innerHTML='<p>We use Google Analytics and Microsoft Clarity to improve FORTLS. Nothing loads unless you accept. <a href="/privacy">Privacy</a>.</p><button>Accept</button><button class="alt">Decline</button>';
document.body.appendChild(b);const [y,n]=b.querySelectorAll("button");
y.onclick=()=>{wr("yes");b.remove();loadGA();loadCL()};n.onclick=()=>{wr("no");b.remove()}})();
