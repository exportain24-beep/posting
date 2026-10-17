// ===================== Logistics — helpers + scenes 00–09 (brand palette) =====================
const R5L=['পোশাক','সবজি, আইটি','মাছ, পাট','সেবা','কোনটা আগে'],R5C=[C.b,C.t,C.o,C.g,C.gd];
function road5(P){return `<g data-k="${P}road"><rect x="140" y="268" width="800" height="12" rx="6" fill="#ffffff" opacity=".75"/>
 ${R5L.map((l,i)=>`<g data-k="${P}m${i}"><circle data-k="${P}mc${i}" cx="${140+i*200}" cy="274" r="34" fill="#cbd5e1" stroke="#fff" stroke-width="6"/>${lat(140+i*200,288,String(i+1),34,'#fff',800)}${tx(140+i*200,350,l,26,C.ink,800)}</g>`).join('')}</g>`}
function road5Upd(q,P,lt,t,cur,b=0){T(q(P+'road'),{o:cl((lt-b+.4)*3)});for(let i=0;i<5;i++){const c=q(P+'mc'+i);if(c)c.setAttribute('fill',i<cur-1?C.g:i==cur-1?R5C[i]:'#cbd5e1');
  const p=i==cur-1?pe(lt,b,.5):1;T(q(P+'m'+i),{s:i==cur-1?L(.6,1.15,p)+Math.sin(t*3)*.03:1})}}
function carton(x,y,s=1,c1='#d9a55c',c2='#b9853d',c3='#e9c287',lab=''){return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-70 -35 L0 -70 L70 -35 L0 0Z" fill="${c3}"/><path d="M-70 -35 L0 0 L0 80 L-70 45Z" fill="${c1}"/><path d="M70 -35 L0 0 L0 80 L70 45Z" fill="${c2}"/><path d="M-35 -52 L35 -18" stroke="#fff7e6" stroke-width="9" opacity=".8"/>${lab?`<text x="-36" y="34" font-family="Pop" font-size="18" font-weight="800" fill="#5b3b12" text-anchor="middle" transform="skewY(27)">${lab}</text>`:''}</g>`}
function box2(x,y,w,h,col,lab,sub,labCol='#fff'){return `<g>${cont(x,y,w,h,col)}${lab?tx(x+w/2,y+h/2+(sub?-4:16),lab,Math.min(52,h*.32),labCol,800,'middle','Pop'):''}${sub?tx(x+w/2,y+h/2+44,sub,Math.min(34,h*.2),labCol,800):''}</g>`}
function plane(x,y,s=1,col='#fff'){return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-110 0 Q-110 -16 -90 -16 L90 -16 Q130 -16 140 0 Q130 16 90 16 L-90 16 Q-110 16 -110 0Z" fill="${col}"/><path d="M-10 -14 L-60 -90 L-28 -90 L40 -14Z M-10 14 L-60 90 L-28 90 L40 14Z" fill="${C.gd}"/><path d="M-96 -14 L-120 -56 L-100 -56 L-74 -14Z" fill="${C.gd}"/>${[0,1,2,3,4].map(i=>`<circle cx="${-50+i*28}" cy="-3" r="5" fill="#93c5fd"/>`).join('')}</g>`}
function pallet(x,y,w=300,stamp=true){return `<g transform="translate(${x} ${y})"><rect x="${-w/2}" y="0" width="${w}" height="24" rx="4" fill="#c8945a"/>${[0,1,2].map(i=>`<rect x="${-w/2+i*(w/2-24)}" y="24" width="48" height="40" fill="#a8743a"/>`).join('')}<rect x="${-w/2}" y="64" width="${w}" height="22" rx="4" fill="#c8945a"/>
 ${stamp?`<g transform="translate(${w/2-80} 30)"><rect x="-40" y="-2" width="110" height="52" rx="4" fill="none" stroke="#1f2937" stroke-width="3"/><path d="M-30 40 Q-14 4 2 40Z" fill="#1f2937"/>${lat(38,18,'BD-000',13,'#1f2937',800)}${lat(38,40,'HT',18,'#1f2937',800)}</g>`:''}</g>`}
function meter(x,y,w,h,col,id){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h/2}" fill="#e2e8f0"/><rect data-k="${id}" x="${x}" y="${y}" width="0" height="${h}" rx="${h/2}" fill="${col}"/>`}


// ---- pacing helpers: nothing flashes by — min gap between reveals, slower easing, ghost placeholders
const pS=(lt,b,d=.85)=>eb(cl((lt-b)/d));
function seqB(times,gap=.7){const o=[];let p=-1e9;for(const v of times){const r=Math.max(v,p+gap);o.push(r);p=r}return o}
function popG(el,lt,b,t,i=0,dy=60,bob=4,d=.85){if(!el)return;if(lt<b){T(el,{o:.16,s:.97});return}popIn(el,pS(lt,b,d),t,i,dy,bob)}
function slideG(el,lt,b,dx,t,i=0){if(!el)return;if(lt<b){T(el,{o:.16});return}slideIn(el,pS(lt,b),dx,t,i)}
