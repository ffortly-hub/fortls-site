(()=>{const ID="zbdjwrsl12",K="fortls-consent";
const load=()=>{(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)})(window,document,"clarity","script",ID)};
let v=null;try{v=localStorage.getItem(K)}catch(e){}
const cs=document.getElementById("cs");if(cs)cs.onclick=e=>{e.preventDefault();try{localStorage.removeItem(K)}catch(x){}location.reload()};
if(v==="yes")return load();if(v==="no")return;
const b=document.createElement("div");b.className="consent";b.setAttribute("role","dialog");b.setAttribute("aria-label","Analytics consent");
b.innerHTML='<p>May we use Microsoft Clarity analytics to improve the site? Nothing loads unless you accept. <a href="/privacy">Privacy</a></p><button>Accept</button><button class="alt">Decline</button>';
document.body.appendChild(b);const [y,n]=b.querySelectorAll("button");
const set=x=>{try{localStorage.setItem(K,x)}catch(e){}b.remove();if(x==="yes")load()};y.onclick=()=>set("yes");n.onclick=()=>set("no")})();
