// ===================== Provider ad (9:16) — kinetic type + directory UI =====================
const kw=(id,x,y,txt,size,col,hl,f='B')=>`<g data-k="${id}">${hl?`<rect x="${x-txt.length*size*.29-24}" y="${y-size*.95}" width="${txt.length*size*.58+48}" height="${size*1.3}" rx="${size*.3}" fill="${hl}"/>`:''}${f=='L'?lat(x,y,txt,size,col,800):tx(x,y,txt,size,col,800)}</g>`;
const kwU=(q,id,lt,b,t)=>{const e=q(id);if(!e)return;if(lt<b){T(e,{o:0,s:.6});return}const p=cl((lt-b)/.42);T(e,{s:L(.55,1,eb(p)),o:cl(p*3),y:L(30,0,eo(p))})};
const confetti=(id,cx,cy)=>`<g data-k="${id}">${Array.from({length:18},(_,i)=>`<rect data-k="${id}${i}" x="${cx-7}" y="${cy-7}" width="14" height="${i%2?14:22}" rx="3" fill="${[C.y,C.g2,C.o,C.t,C.b,C.r][i%6]}"/>`).join('')}</g>`;
const confU=(q,id,lt,b)=>{const p=cl((lt-b)/1.4);for(let i=0;i<18;i++){const a=i/18*6.283+.3,r=L(0,260+(i%3)*60,eo(p));T(q(id+i),{x:Math.cos(a)*r,y:Math.sin(a)*r+p*p*160,r:p*360*(i%2?1:-1),o:p>0?1-p*p:0})}};
const tap=(id)=>`<circle cx="0" cy="0" r="34" fill="#ffffff" opacity=".85" stroke="${C.ink}" stroke-width="6"/><circle data-k="${id}" cx="0" cy="0" r="34" fill="none" stroke="#fff" stroke-width="6"/>`;
const ticon=(k,x,y,s=1)=>({freight:plane(x,y,.42*s,C.b),ship:shipA(x,y+10,.3*s),cnf:icon('doc',x,y,80*s,C.p,7),insp:mag(x,y,.55*s,C.t),cert:icon('star',x,y,80*s,C.y,7),bond:icon('bld',x,y,80*s,C.bd,7),pack:carton(x,y-6,.5*s),buy:icon('shirt',x,y,80*s,C.o,7),ins:shield(x,y,.5*s,C.g,'✓'),fin:coin(x,y,34*s)})[k];
const PCAT=[['freight','Freight Forwarders'],['ship','Shipping Agents'],['cnf','Customs Brokers (C&F)'],['insp','Inspection & Audits'],['cert','Certification Bodies'],['bond','Bonded Warehousing'],['pack','Export Packaging'],['buy','Sourcing & Buying Houses'],['ins','Cargo Insurance'],['fin','Trade Finance']];

// 00 — HOOK: exporters search, can't find you
K.pv_hook=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 ${kw('h_w0',540,330,'রপ্তানিকারকরা',96,'#fff')}${kw('h_w1',540,470,'আপনার সেবা খুঁজছে',80,C.g2)}
 <g data-k="h_ph">${phone(240,560,600,820)}<rect x="262" y="630" width="556" height="90" fill="${C.g}"/>${lat(290,688,'Find providers',32,'#fff',800,'start')}
  <rect x="290" y="760" width="500" height="80" rx="40" fill="#f1f5f9" stroke="${C.g}" stroke-width="4"/>${icon('globe',335,800,40,C.mute,6)}
  <clipPath id="h_cp"><rect data-k="h_tw" x="370" y="770" width="0" height="60"/></clipPath><g clip-path="url(#h_cp)">${lat(370,812,'C&F agent Chattogram',32,C.ink,800,'start')}</g>
  ${[0,1,2].map(i=>`<rect x="290" y="${880+i*120}" width="500" height="96" rx="16" fill="#f1f5f9" opacity=".7"/>`).join('')}
  <g data-k="h_nr">${card(320,960,440,170,'#fff4f2',24)}${cross(400,1045,36,C.r)}${lat(460,1035,'No results',38,C.r,800,'start')}${lat(460,1080,'0 providers found',24,C.mute,700,'start')}</g></g>
 ${kw('h_w2',540,1530,'কিন্তু আপনাকে',72,'#fff')}${kw('h_w3',540,1700,'পাচ্ছে না!',120,'#fff',C.r)}`,
 upd(q,lt,t,bt){kwU(q,'h_w0',lt,Math.min(bt(0),.1),t);kwU(q,'h_w1',lt,bt(1)-.15,t);popG(q('h_ph'),lt,.2,t,0,60,0,.45);const tw=q('h_tw');if(tw)tw.setAttribute('width',420*cl((lt-.5)/1.4));
  popIn(q('h_nr'),pe(lt,bt(2)-.3,.4),t,1,0,0);if(lt>bt(2))T(q('h_nr'),{x:Math.sin(t*25)*cl((bt(2)+.8-lt)*2)*8,o:1});kwU(q,'h_w2',lt,bt(2)-.05,t);kwU(q,'h_w3',lt,bt(3)-.1,t)}});

// 01 — WHO: 10 provider categories
K.pv_who=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 ${kw('w_h',540,300,'আপনি কি এদের একজন?',56,C.gd)}
 ${PCAT.map((c,i)=>{const x=80+(i%2)*470,y=360+Math.floor(i/2)*215;return `<g data-k="w_c${i}">${card(x,y,450,195,'#fff',30)}<circle cx="${x+95}" cy="${y+97}" r="70" fill="#f1f8f6"/>${ticon(c[0],x+95,y+97)}${lat(x+180,y+90,c[1].split(' ')[0],30,C.ink,800,'start')}${lat(x+180,y+130,c[1].split(' ').slice(1).join(' '),24,C.mute,700,'start')}</g>`}).join('')}
 <g data-k="w_e">${card(140,1460,800,260,C.gd,60)}${tx(540,1560,'আপনার সেবা তুলুন',52,'#fff',800)}<image href="__LOGO__" x="340" y="1590" width="400" height="110" preserveAspectRatio="xMidYMid meet" style="filter:brightness(0) invert(1)"/></g>`,
 upd(q,lt,t,bt){kwU(q,'w_h',lt,.1,t);const K=[0,1,2,6,3,8],T0={};K.forEach((c,j)=>T0[c]=bt(j)-.1);[4,5,7,9].forEach((c,j)=>T0[c]=bt(2)+.25+j*.35);
  for(let i=0;i<10;i++){const p=pe(lt,T0[i],.35);T(q('w_c'+i),{s:L(.6,1,eb(p)),o:cl(p*3)});if(K.includes(i)&&lt>T0[i]&&lt<T0[i]+.7)T(q('w_c'+i),{s:1+.06*Math.sin((lt-T0[i])*9),o:1})}
  popG(q('w_e'),lt,bt(6)-.3,t,0,40,2,.45)}});

// 02 — WHERE: exporters + foreign buyers both search here
K.pv_where=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="r_s">${card(70,300,450,560,'#fff',40)}${person(295,350,.75,'s','r_sp')}${bdflag(130,320,80)}${tx(295,700,'রপ্তানিকারক',40,C.ink,800)}${pill(295,790,'Find providers',C.g,28,'Pop')}</g>
 <g data-k="r_b">${card(560,300,450,560,'#fff',40)}${person(785,350,.75,'g','r_bp')}${deflag(890,320,80)}${tx(785,700,'বিদেশি বায়ার',40,C.ink,800)}${pill(785,790,'Find services',C.b,28,'Pop')}</g>
 <path data-k="r_a0" d="M295 880 Q300 980 470 1010" stroke="${C.g}" stroke-width="12" fill="none" stroke-dasharray="400" stroke-dashoffset="400"/><path data-k="r_a1" d="M785 880 Q780 980 610 1010" stroke="${C.b}" stroke-width="12" fill="none" stroke-dasharray="400" stroke-dashoffset="400"/>
 <g data-k="r_d">${card(120,1020,840,560,'#fff',44)}<image href="__LOGO__" x="300" y="1050" width="480" height="120" preserveAspectRatio="xMidYMid meet"/>${lat(540,1210,'Services directory',34,C.mute,800)}
  ${[0,1].map(i=>`<rect x="170" y="${1250+i*150}" width="740" height="130" rx="20" fill="${i==0?'#e9f8ec':'#f4f7f9'}" ${i==0?`stroke="${C.g}" stroke-width="5"`:''}/>${i==0?`${lat(210,1305,'Your company · C&F Agent',32,C.gd,800,'start')}${lat(210,1350,'Chattogram Port · Verified',26,C.mute,700,'start')}`:`<rect x="210" y="1440" width="380" height="18" rx="9" fill="#dfe6ea"/>`}`).join('')}</g>
 ${kw('r_w',540,1720,'দুজনেই খোঁজেন এখানে',64,'#fff',C.gd)}`,
 upd(q,lt,t,bt){slideG(q('r_s'),lt,Math.min(bt(0)-.2,.15),-200,t,0);slideG(q('r_b'),lt,bt(1)-.2,200,t,1);const d=(e,b)=>{if(e)e.setAttribute('stroke-dashoffset',400*(1-eio(cl((lt-b)/.6))))};d(q('r_a0'),bt(2)-.2);d(q('r_a1'),bt(2));
  popG(q('r_d'),lt,bt(2)-.1,t,2,40,0,.45);kwU(q,'r_w',lt,bt(3)-.1,t)}});
