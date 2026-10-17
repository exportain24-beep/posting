// ===================== Provider ad 16:9 (1920×1080) =====================
// 00 — HOOK
K.pv_hook=()=>({svg:`${BG}
 ${kw('h_w0',540,270,'রপ্তানিকারকরা',100,'#fff')}${kw('h_w1',540,410,'আপনার সেবা খুঁজছে',78,C.g2)}
 ${kw('h_w2',540,700,'কিন্তু আপনাকে',72,'#fff')}${kw('h_w3',540,880,'পাচ্ছে না!',124,'#fff',C.r)}
 <g data-k="h_ph">${phone(1120,120,600,860)}<rect x="1142" y="190" width="556" height="90" fill="${C.g}"/>${lat(1170,248,'Find providers',32,'#fff',800,'start')}
  <rect x="1170" y="320" width="500" height="80" rx="40" fill="#f1f5f9" stroke="${C.g}" stroke-width="4"/>${icon('globe',1215,360,40,C.mute,6)}
  <clipPath id="h_cp"><rect data-k="h_tw" x="1250" y="330" width="0" height="60"/></clipPath><g clip-path="url(#h_cp)">${lat(1250,372,'C&F agent Chattogram',32,C.ink,800,'start')}</g>
  ${[0,1,2].map(i=>`<rect x="1170" y="${440+i*120}" width="500" height="96" rx="16" fill="#f1f5f9" opacity=".7"/>`).join('')}
  <g data-k="h_nr">${card(1200,520,440,170,'#fff4f2',24)}${cross(1280,605,36,C.r)}${lat(1340,595,'No results',38,C.r,800,'start')}${lat(1340,640,'0 providers found',24,C.mute,700,'start')}</g></g>`,
 upd(q,lt,t,bt){kwU(q,'h_w0',lt,Math.min(bt(0),.1),t);kwU(q,'h_w1',lt,bt(1)-.15,t);popG(q('h_ph'),lt,.2,t,0,60,0,.45);const tw=q('h_tw');if(tw)tw.setAttribute('width',420*cl((lt-.5)/1.4));
  popIn(q('h_nr'),pe(lt,bt(2)-.3,.4),t,1,0,0);if(lt>bt(2))T(q('h_nr'),{x:Math.sin(t*25)*cl((bt(2)+.8-lt)*2)*8,o:1});kwU(q,'h_w2',lt,bt(2)-.05,t);kwU(q,'h_w3',lt,bt(3)-.1,t)}});

// 01 — WHO: 10 categories, 5×2 grid
K.pv_who=()=>({svg:`${BG}
 ${kw('w_h',960,180,'আপনি কি এদের একজন?',60,C.gd)}
 ${PCAT.map((c,i)=>{const x=95+(i%5)*350,y=240+Math.floor(i/5)*270;return `<g data-k="w_c${i}">${card(x,y,330,245,'#fff',30)}<circle cx="${x+165}" cy="${y+85}" r="62" fill="#f1f8f6"/>${ticon(c[0],x+165,y+85,.9)}${lat(x+165,y+185,c[1].split(' ')[0],30,C.ink,800)}${lat(x+165,y+222,c[1].split(' ').slice(1).join(' '),22,C.mute,700)}</g>`}).join('')}
 <g data-k="w_e">${card(560,810,800,220,C.gd,60)}${tx(960,890,'আপনার সেবা তুলুন',52,'#fff',800)}<image href="__LOGO__" x="760" y="910" width="400" height="100" preserveAspectRatio="xMidYMid meet" style="filter:brightness(0) invert(1)"/></g>`,
 upd(q,lt,t,bt){kwU(q,'w_h',lt,.1,t);const KK=[0,1,2,6,3,8],T0={};KK.forEach((c,j)=>T0[c]=bt(j)-.1);[4,5,7,9].forEach((c,j)=>T0[c]=bt(2)+.25+j*.35);
  for(let i=0;i<10;i++){const p=pe(lt,T0[i],.35);T(q('w_c'+i),{s:L(.6,1,eb(p)),o:cl(p*3)});if(KK.includes(i)&&lt>T0[i]&&lt<T0[i]+.7)T(q('w_c'+i),{s:1+.06*Math.sin((lt-T0[i])*9),o:1})}
  popG(q('w_e'),lt,bt(6)-.3,t,0,40,2,.45)}});

// 02 — WHERE
K.pv_where=()=>({svg:`${BG}
 <g data-k="r_s">${card(100,170,420,520,'#fff',40)}${person(310,210,.7,'s','r_sp')}${bdflag(150,190,80)}${tx(310,540,'রপ্তানিকারক',40,C.ink,800)}${pill(310,625,'Find providers',C.g,28,'Pop')}</g>
 <g data-k="r_b">${card(1400,170,420,520,'#fff',40)}${person(1610,210,.7,'g','r_bp')}${deflag(1700,190,80)}${tx(1610,540,'বিদেশি বায়ার',40,C.ink,800)}${pill(1610,625,'Find services',C.b,28,'Pop')}</g>
 <path data-k="r_a0" d="M520 430 Q560 430 600 430" stroke="${C.g}" stroke-width="12" fill="none" stroke-dasharray="400" stroke-dashoffset="400"/><path data-k="r_a1" d="M1400 430 Q1360 430 1320 430" stroke="${C.b}" stroke-width="12" fill="none" stroke-dasharray="400" stroke-dashoffset="400"/>
 <g data-k="r_d">${card(600,150,720,580,'#fff',44)}<image href="__LOGO__" x="760" y="180" width="400" height="110" preserveAspectRatio="xMidYMid meet"/>${lat(960,330,'Services directory',32,C.mute,800)}
  <rect x="640" y="370" width="640" height="140" rx="20" fill="#e9f8ec" stroke="${C.g}" stroke-width="5"/>${lat(680,430,'Your company · C&F Agent',32,C.gd,800,'start')}${lat(680,475,'Chattogram Port · Verified',26,C.mute,700,'start')}
  <rect x="640" y="540" width="640" height="140" rx="20" fill="#f4f7f9"/><rect x="680" y="595" width="360" height="18" rx="9" fill="#dfe6ea"/></g>
 ${kw('r_w',960,900,'দুজনেই খোঁজেন এখানে',72,'#fff',C.gd)}`,
 upd(q,lt,t,bt){slideG(q('r_s'),lt,Math.min(bt(0)-.2,.15),-200,t,0);slideG(q('r_b'),lt,bt(1)-.2,200,t,1);const d=(e,b)=>{if(e)e.setAttribute('stroke-dashoffset',400*(1-eio(cl((lt-b)/.6))))};d(q('r_a0'),bt(2)-.2);d(q('r_a1'),bt(2));
  popG(q('r_d'),lt,bt(2)-.1,t,2,40,0,.45);kwU(q,'r_w',lt,bt(3)-.1,t)}});
