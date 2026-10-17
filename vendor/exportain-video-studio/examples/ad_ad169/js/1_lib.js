// ===================== Export Roadmap — shared library (9:16, 1080x1920) =====================
const C={g:'#2e8b2e',g2:'#5cbf14',gd:'#005a1e',f:'#003c10',l:'#5cbf14',b:'#0b5f8a',bd:'#0b3b5c',r:'#d93636',o:'#e8890c',y:'#f2b705',p:'#0e6e8c',pk:'#c26a00',t:'#0e8c88',ink:'#0f1f14',mute:'#4a5e52',jute:'#c8a165',juteD:'#a07a44'};
const ESC=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
function tx(x,y,s,size,col=C.ink,w=700,anc='middle',f='B'){return `<text x="${x}" y="${y}" font-family="${f}" font-size="${size}" font-weight="${w}" fill="${col}" text-anchor="${anc}">${ESC(s)}</text>`}
const lat=(x,y,s,size,col=C.ink,w=800,anc='middle')=>tx(x,y,s,size,col,w,anc,'Pop');
const pe=(lt,b,d=.6)=>eb(cl((lt-b)/d)), po=(lt,b,d=.6)=>eo(cl((lt-b)/d));
function popIn(el,p,t,i=0,dy=80,bob=5){if(!el)return;T(el,{y:L(dy,0,eo(p))+(p>=1?Math.sin(t*1.6+i)*bob:0),s:L(.35,1,p),o:cl(p*2.2)})}
function slideIn(el,p,dx=-140,t=0,i=0){if(!el)return;T(el,{x:L(dx,0,eo(p)),y:p>=1?Math.sin(t*1.4+i)*4:0,o:cl(p*2)})}
function fadeMul(el,v){if(el)el.style.opacity=(parseFloat(el.style.opacity)||0)*v}
function setW(el,w){if(el)el.setAttribute('width',Math.max(0,w).toFixed(1))}
function card(x,y,w,h,fill='#fff',rx=34){return `<g filter="url(#sh)"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}"/></g>`}
function chipT(x,y,label,col,size=36,f='B',fg='#fff'){const w=label.length*size*.6+64;return `<g filter="url(#sh2)"><rect x="${x-w/2}" y="${y-size*.95}" width="${w}" height="${size*1.75}" rx="${size*.87}" fill="${col}"/></g>${tx(x,y+size*.28,label,size,fg,800,'middle',f)}`}
function coin(x,y,r=40,sym='৳'){return `<g><circle cx="${x}" cy="${y+5}" r="${r}" fill="#b45309"/><circle cx="${x}" cy="${y}" r="${r}" fill="#fbbf24"/><circle cx="${x}" cy="${y}" r="${r*.74}" fill="none" stroke="#fde68a" stroke-width="${r*.1}"/>${tx(x,y+r*.38,sym,r*1.05,'#92400e',800,'middle',sym=='$'?'Pop':'B')}</g>`}
function check(x,y,r=44,col=C.g){return `<g><circle cx="${x}" cy="${y}" r="${r}" fill="${col}"/><path d="M${x-r*.45} ${y} l${r*.32} ${r*.32} l${r*.6} -${r*.62}" stroke="#fff" stroke-width="${r*.22}" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`}
function cross(x,y,r=44,col=C.r){return `<g><circle cx="${x}" cy="${y}" r="${r}" fill="${col}"/><path d="M${x-r*.38} ${y-r*.38} l${r*.76} ${r*.76} M${x+r*.38} ${y-r*.38} l-${r*.76} ${r*.76}" stroke="#fff" stroke-width="${r*.22}" stroke-linecap="round"/></g>`}
function shield(x,y,s=1,col=C.o,mark='!'){return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M0 -52 L44 -36 L44 4 Q44 40 0 58 Q-44 40 -44 4 L-44 -36Z" fill="${col}" stroke="#fff" stroke-width="6"/>${lat(0,22,mark,58,'#fff',800)}</g>`}
function bdflag(x,y,w=120){const h=w*.6;return `<g><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="#006a4e"/><circle cx="${x+w*.45}" cy="${y+h/2}" r="${h*.3}" fill="#f42a41"/></g>`}
function deflag(x,y,w=120){const h=w*.6;return `<g><rect x="${x}" y="${y}" width="${w}" height="${h/3+1}" rx="0" fill="#111"/><rect x="${x}" y="${y+h/3}" width="${w}" height="${h/3+1}" fill="#dd0000"/><rect x="${x}" y="${y+2*h/3}" width="${w}" height="${h/3}" fill="#ffce00"/></g>`}
function euflag(x,y,w=120){const h=w*.66;return `<g><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="#003399"/>${Array.from({length:12},(_,i)=>{const a=i/12*6.283;return `<circle cx="${x+w/2+Math.cos(a)*h*.3}" cy="${y+h/2+Math.sin(a)*h*.3}" r="${h*.045}" fill="#ffcc00"/>`}).join('')}</g>`}
// people: 's' = Sumon (BD jute-bag maker), 'g' = German buyer
function person(x,y,s,kind,id){const skin=kind=='s'?'#a8714a':'#f2c9a6',hair=kind=='s'?'#1c1917':'#d6a24a',top=kind=='s'?'#0d9488':'#334155';
 return `<g data-k="${id}"><g transform="translate(${x} ${y}) scale(${s})">
 <ellipse cx="0" cy="196" rx="100" ry="14" fill="#000" opacity=".14"/>
 <path d="M-92 196 Q-96 74 0 70 Q96 74 92 196Z" fill="${top}"/>
 ${kind=='g'?`<path d="M-30 74 L0 160 L30 74Z" fill="#f8fafc"/><path d="M-7 84 L0 150 L7 84Z" fill="#2563eb"/><path d="M-30 74 L-8 120 L-46 92Z M30 74 L8 120 L46 92Z" fill="#1e293b"/>`:`<path d="M-24 72 L0 104 L24 72Z" fill="#ccfbf1"/>${[0,1,2].map(i=>`<circle cx="0" cy="${118+i*24}" r="4.5" fill="#ccfbf1"/>`).join('')}`}
 <rect x="-17" y="40" width="34" height="38" rx="6" fill="${skin}"/>
 <circle cx="0" cy="0" r="58" fill="${skin}"/><circle cx="-57" cy="6" r="11" fill="${skin}"/><circle cx="57" cy="6" r="11" fill="${skin}"/>
 <path d="M-58 -6 Q-62 -70 0 -70 Q62 -70 58 -6 Q44 -42 0 -44 Q-44 -42 -58 -6Z" fill="${hair}"/>
 ${kind=='g'?`<rect x="-36" y="-10" width="30" height="22" rx="8" fill="none" stroke="#334155" stroke-width="4"/><rect x="6" y="-10" width="30" height="22" rx="8" fill="none" stroke="#334155" stroke-width="4"/><path d="M-6 0 H6" stroke="#334155" stroke-width="4"/>`:''}
 <ellipse cx="-21" cy="2" rx="6.5" ry="7.5" fill="#1f2937"/><ellipse cx="21" cy="2" rx="6.5" ry="7.5" fill="#1f2937"/>
 <path d="M-15 32 Q0 44 15 32" stroke="#7f1d1d" stroke-width="5" fill="none" stroke-linecap="round"/>
 </g></g>`}
// jute tote bag with handles (the hero product) and jute sack
function jutebag(x,y,s=1,logo=true,hl=1){return `<g transform="translate(${x} ${y}) scale(${s})">
 <path d="M-70 -110 Q-70 ${-110-120*hl} 0 ${-110-120*hl} Q70 ${-110-120*hl} 70 -110" fill="none" stroke="#7c5a2e" stroke-width="16" stroke-linecap="round"/>
 <path d="M-150 -110 L150 -110 L130 150 L-130 150Z" fill="${C.jute}"/>
 ${Array.from({length:14},(_,i)=>`<line x1="${-145+i*21}" y1="-110" x2="${-127+i*19}" y2="150" stroke="${C.juteD}" stroke-width="3" opacity=".6"/>`).join('')}
 ${Array.from({length:12},(_,i)=>`<line x1="-148" y1="${-96+i*21}" x2="148" y2="${-96+i*21}" stroke="#dcbb83" stroke-width="3" opacity=".7"/>`).join('')}
 <rect x="-150" y="-118" width="300" height="20" rx="6" fill="${C.juteD}"/>
 ${logo?`<circle cx="0" cy="20" r="54" fill="#fff" opacity=".9"/><path d="M-26 34 Q0 -22 26 34Z" fill="${C.g}"/><rect x="-3" y="10" width="6" height="40" fill="${C.gd}"/>`:''}</g>`}
function sack(x,y,s=1){return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-110 -130 Q-120 40 -100 150 L100 150 Q120 40 110 -130 Q60 -110 0 -140 Q-60 -110 -110 -130Z" fill="#b8925c"/>
 <path d="M-60 -125 Q0 -160 60 -125" fill="none" stroke="#7c5a2e" stroke-width="12"/>${Array.from({length:8},(_,i)=>`<line x1="-100" y1="${-90+i*30}" x2="100" y2="${-90+i*30}" stroke="#a07a44" stroke-width="3" opacity=".6"/>`).join('')}</g>`}
function phone(x,y,w=360,h=660,inner=''){return `<g>${card(x,y,w,h,'#0f172a',48)}<rect x="${x+18}" y="${y+60}" width="${w-36}" height="${h-110}" rx="20" fill="#fff"/><rect x="${x+w/2-50}" y="${y+24}" width="100" height="14" rx="7" fill="#334155"/>${inner}</g>`}
function docPage(x,y,w,h,title,col=C.b,lines=4){return `${card(x,y,w,h,'#fff',22)}<rect x="${x}" y="${y}" width="${w}" height="64" rx="22" fill="${col}"/><rect x="${x}" y="${y+40}" width="${w}" height="24" fill="${col}"/>${lat(x+w/2,y+46,title,Math.min(34,w/title.length*1.5),'#fff',800)}${skel(x+28,y+100,Array.from({length:lines},(_,i)=>w*(.78-.14*(i%3))),40,16)}`}
// decision roadmap header: 4 milestones, cur = 1..4 (0 = none)
const ROADL=['দাম','HS Code','স্যাম্পল','পেমেন্ট'],ROADC=[C.y,C.p,C.pk,C.t];
function roadSVG(P){return `<g data-k="${P}road"><rect x="150" y="266" width="780" height="14" rx="7" fill="#ffffff" opacity=".7"/>
 ${ROADL.map((l,i)=>`<g data-k="${P}m${i}"><circle cx="${150+i*260}" cy="273" r="46" fill="#fff"/><circle data-k="${P}mc${i}" cx="${150+i*260}" cy="273" r="38" fill="#cbd5e1"/>${lat(150+i*260,289,String(i+1),42,'#fff',800)}${tx(150+i*260,368,l,30,C.ink,800,'middle',i==1?'Pop':'B')}</g>`).join('')}</g>`}
function roadUpd(q,P,lt,t,cur,b=0){T(q(P+'road'),{o:cl((lt-b+.3)*3)});for(let i=0;i<4;i++){const c=q(P+'mc'+i);if(c)c.setAttribute('fill',i<cur-1?C.g:i==cur-1?ROADC[i]:'#cbd5e1');
  if(i==cur-1){const p=pe(lt,b,.6);T(q(P+'m'+i),{s:L(.6,1.25,p)+Math.sin(t*3)*.03})}else T(q(P+'m'+i),{s:1})}}
function bigTitle(id,y,line,col){return `<g data-k="${id}">${card(80,y,920,150,col,40)}${tx(540,y+100,line,62,'#fff',800)}</g>`}
const ring=(id,x,y,r,col)=>`<g data-k="${id}"><circle cx="${x}" cy="${y}" r="${r}" fill="none" stroke="${col}" stroke-width="9" stroke-dasharray="20 13"/></g>`;
function pulse(el,p,t){if(!el)return;T(el,{s:L(.5,1,eo(p))+(p>=1?Math.sin(t*4)*.04:0),r:t*20,o:cl(p*2)})}
const QB=(a,c,b,u)=>[(1-u)*(1-u)*a[0]+2*(1-u)*u*c[0]+u*u*b[0],(1-u)*(1-u)*a[1]+2*(1-u)*u*c[1]+u*u*b[1]];
function crane(c='#f59e0b'){return `<g><rect x="-72" y="-250" width="16" height="250" fill="${c}"/><rect x="38" y="-250" width="16" height="250" fill="${c}"/>
 <path d="M-64 -240 L46 -150 M46 -240 L-64 -150" stroke="${c}" stroke-width="7"/><rect x="-100" y="-150" width="170" height="12" fill="${c}"/>
 <rect x="-120" y="-268" width="320" height="22" rx="3" fill="${c}"/><rect x="-150" y="-290" width="50" height="34" rx="4" fill="#334155"/><rect x="-4" y="-246" width="34" height="24" fill="#334155"/></g>`}
// ---- cash-incentive additions
const BN=n=>String(n).replace(/\d/g,d=>'০১২৩৪৫৬৭৮৯'[d]);
const _person=person;
person=function(x,y,s,kind,id){if(kind!='n'&&kind!='a')return _person(x,y,s,kind,id);
 const skin=kind=='n'?'#b07a52':'#c68b5e',top=kind=='n'?'#db2777':'#1e3a8a';
 return `<g data-k="${id}"><g transform="translate(${x} ${y}) scale(${s})"><ellipse cx="0" cy="196" rx="100" ry="14" fill="#000" opacity=".14"/>
 ${kind=='n'?`<path d="M-62 -10 Q-80 90 -60 150 L60 150 Q80 90 62 -10Z" fill="#1c1917"/>`:''}
 <path d="M-92 196 Q-96 74 0 70 Q96 74 92 196Z" fill="${top}"/>
 ${kind=='n'?`<path d="M-80 100 Q0 150 84 86 L92 120 Q0 190 -88 130Z" fill="#fbbf24"/>`:`<path d="M-26 74 L0 150 L26 74Z" fill="#f8fafc"/><path d="M-6 84 L0 140 L6 84Z" fill="${C.r}"/>`}
 <rect x="-17" y="40" width="34" height="38" rx="6" fill="${skin}"/><circle cx="0" cy="0" r="58" fill="${skin}"/>
 <path d="M-60 6 Q-66 -72 0 -72 Q66 -72 60 6 Q50 -40 0 -46 Q-50 -40 -60 6Z" fill="#1c1917"/>
 ${kind=='a'?`<rect x="-36" y="-10" width="30" height="22" rx="8" fill="none" stroke="#0f172a" stroke-width="4"/><rect x="6" y="-10" width="30" height="22" rx="8" fill="none" stroke="#0f172a" stroke-width="4"/><path d="M-6 0 H6" stroke="#0f172a" stroke-width="4"/>`:`<circle cx="0" cy="-8" r="4" fill="${C.r}"/>`}
 <ellipse cx="-21" cy="2" rx="6.5" ry="7.5" fill="#1f2937"/><ellipse cx="21" cy="2" rx="6.5" ry="7.5" fill="#1f2937"/>
 <path d="M-15 30 Q0 42 15 30" stroke="#7f1d1d" stroke-width="5" fill="none" stroke-linecap="round"/></g></g>`};
function cal(x,y,w,day,mon,col=C.r){return `${card(x,y,w,w*1.05,'#fff',26)}<rect x="${x}" y="${y}" width="${w}" height="${w*.3}" rx="26" fill="${col}"/><rect x="${x}" y="${y+w*.18}" width="${w}" height="${w*.12}" fill="${col}"/>
 ${tx(x+w/2,y+w*.22,mon,w*.15,'#fff',800)}${tx(x+w/2,y+w*.8,day,w*.42,C.ink,800)}`}
function bank(x,y,s=1,col=C.g){return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-130 -80 L0 -150 L130 -80Z" fill="${col}"/>${[-90,-30,30,90].map(c=>`<rect x="${c-14}" y="-70" width="28" height="120" fill="#f1f5f9"/>`).join('')}<rect x="-140" y="50" width="280" height="26" rx="6" fill="#cbd5e1"/><rect x="-130" y="-84" width="260" height="16" fill="#e2e8f0"/></g>`}
function jar(x,y,s=1){return `<g transform="translate(${x} ${y}) scale(${s})"><rect x="-50" y="-70" width="100" height="24" rx="6" fill="#16a34a"/><path d="M-60 -46 H60 V60 Q60 80 40 80 H-40 Q-60 80 -60 60Z" fill="#fbbf24"/><rect x="-60" y="-10" width="120" height="44" fill="#fff" opacity=".9"/><path d="M-20 12 q20 -26 40 0 q-20 18 -40 0Z" fill="#f59e0b"/></g>`}
function mango(x,y,s=1){return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M0 -50 Q50 -50 50 10 Q45 60 -5 55 Q-50 45 -45 0 Q-40 -50 0 -50Z" fill="#f59e0b"/><path d="M-10 -30 Q-30 -10 -25 20" stroke="#fde68a" stroke-width="8" fill="none" opacity=".7"/><path d="M0 -50 Q20 -80 50 -70 Q30 -50 0 -50Z" fill="#16a34a"/></g>`}
function laptop(x,y,s=1,col=C.b){return `<g transform="translate(${x} ${y}) scale(${s})"><rect x="-90" y="-70" width="180" height="120" rx="10" fill="#1e293b"/><rect x="-78" y="-58" width="156" height="96" rx="4" fill="${col}"/>${lat(0,6,'</>',40,'#fff',800)}<path d="M-120 50 H120 L104 70 H-104Z" fill="#94a3b8"/></g>`}
function gear(x,y,r,col){let d='';for(let i=0;i<8;i++){const a=i/8*6.283;d+=`<rect x="${x-r*.18}" y="${y-r*1.25}" width="${r*.36}" height="${r*.5}" rx="4" fill="${col}" transform="rotate(${i*45} ${x} ${y})"/>`}return `<g>${d}<circle cx="${x}" cy="${y}" r="${r}" fill="${col}"/><circle cx="${x}" cy="${y}" r="${r*.4}" fill="#fff"/></g>`}
function cert(x,y,w,h,title,col=C.g){return `${card(x,y,w,h,'#fffbeb',20)}<rect x="${x+12}" y="${y+12}" width="${w-24}" height="${h-24}" rx="12" fill="none" stroke="#c9a227" stroke-width="4"/>${tx(x+w/2,y+h*.32,title,Math.min(40,w*.1),C.ink,800)}<rect x="${x+w*.2}" y="${y+h*.48}" width="${w*.6}" height="12" rx="6" fill="#e2e8f0"/><rect x="${x+w*.28}" y="${y+h*.6}" width="${w*.44}" height="12" rx="6" fill="#e2e8f0"/><circle cx="${x+w*.78}" cy="${y+h*.78}" r="${h*.13}" fill="${col}"/>`}
function stampT(x,y,txt,col,size=48){const w=txt.length*size*.62+60;return `<g transform="translate(${x} ${y}) rotate(-12)"><rect x="${-w/2}" y="${-size*.95}" width="${w}" height="${size*1.9}" rx="16" fill="none" stroke="${col}" stroke-width="9"/>${tx(0,size*.35,txt,size,col,800)}</g>`}
const mag=(x,y,s,c)=>`<g transform="translate(${x} ${y}) scale(${s})"><circle cx="0" cy="0" r="46" fill="#fff" fill-opacity=".5" stroke="${c}" stroke-width="14"/><path d="M34 34 L80 80" stroke="${c}" stroke-width="18" stroke-linecap="round"/></g>`;
function counter(el,v){if(el)el.textContent=v}
