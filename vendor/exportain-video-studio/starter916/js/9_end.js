K.PFX_cta=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="ct_who">${card(90,200,900,220,'#fff',40)}${bdflag(140,255,150)}${tx(620,295,'প্রস্তুতকারক বা',44,C.ink,800)}${tx(620,370,'রপ্তানিকারক?',56,C.g,800)}</g>
 <g data-k="ct_ph">${phone(290,480,500,940)}<rect x="310" y="550" width="460" height="230" rx="16" fill="#fff"/><image href="__LOGO__" x="330" y="600" width="420" height="130" preserveAspectRatio="xMidYMid meet"/>
  ${[0,1,2,3].map(i=>`<g data-k="ct_p${i}">${card(330+(i%2)*215,800+Math.floor(i/2)*230,200,210,'#f8fafc',18)}${[jutebag(430+(i%2)*215,920+Math.floor(i/2)*230,.32),icon('shirt',430+(i%2)*215,905+Math.floor(i/2)*230,110,C.b,7),icon('shoe',430+(i%2)*215,905+Math.floor(i/2)*230,110,C.o,7),icon('box',430+(i%2)*215,905+Math.floor(i/2)*230,110,C.p,7)][i]}</g>`).join('')}
  <g data-k="ct_btn">${card(340,1290,400,80,C.g,40)}${lat(540,1343,'Exportain.com',36,'#fff',800)}</g></g>
 <g data-k="ct_hand"><g transform="translate(0 0)">${icon('hand',0,0,150,'#fff',9)}</g></g>
 <g data-k="ct_w">${[['us',-1],['de',1],['uk',-1],['ae',1]].map(([c],i)=>`<g data-k="ct_f${i}"><circle cx="0" cy="0" r="56" fill="#fff"/>${icon('globe',0,0,70,[C.b,C.p,C.o,C.t][i],7)}</g>`).join('')}</g>
 <g data-k="ct_u">${chipT(540,1640,'আজই ভিজিট করুন Exportain.com',C.o,44)}</g>`,
 upd(q,lt,t,bt){popIn(q('ct_who'),pe(lt,bt(0),.6),t,0,40,2);popIn(q('ct_ph'),pe(lt,bt(0)+.4,.7),t,1,160,3);for(let i=0;i<4;i++)popIn(q('ct_p'+i),pe(lt,bt(0)+.9+i*.15,.45),t,i,20,0);
  for(let i=0;i<4;i++){const p=pe(lt,bt(1)+i*.15,.5),a=i*1.57+t*.4;T(q('ct_f'+i),{x:540+Math.cos(a)*440,y:950+Math.sin(a)*520,s:L(.2,1,p),o:cl(p*2)})}
  const h=cl((lt-bt(2))/.6);T(q('ct_hand'),{x:L(800,600,eo(h)),y:L(1560,1400,eo(h))+(h>=1?Math.sin(t*6)*8:0),o:cl(h*3)});
  T(q('ct_btn'),{s:lt>bt(2)+.5?1+.06*Math.sin(t*6):1});popIn(q('ct_u'),pe(lt,bt(2),.5),t,2,40,3)}});

