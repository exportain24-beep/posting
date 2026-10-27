// board: give the CTA entry  \"badge\": \"white\"  (dark background)\n// ===== Shorts CTA scenes (fast, 3-5 s). Use the one matching the Short's language as the LAST board kind:
//  "PFX_cta_en" keys: 3 substrings of the CTA line (e.g. "list your","Exportain","find you")
//  "PFX_cta_bn" keys: 3 substrings (e.g. "এক্সপোর্টেইনে","বিশ্বের ক্রেতারা","খুঁজে নেবে")
function ctaShort(lang){const en=lang==='en';return ()=>({svg:`<rect width="1080" height="1920" fill="url(#e_forest)"/>
 <g data-k="cs_logo"><image href="file://__KIT__/logo_white_big.png" x="160" y="430" width="760" height="230" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="cs_ph">${phone(300,720,480,820)}<rect x="322" y="800" width="436" height="150" rx="18" fill="#f3fcf4"/>${lat(540,860,'Company page',30,C.gd,800)}${lat(540,912,'✔ Verified',28,C.g,800)}
  ${[0,1,2].map(i=>`<g data-k="cs_i${i}">${card(330+i*142,990,126,150,'#fff',18)}${icon(['shirt','box','bag'][i],393+i*142,1060,84,[C.b,C.o,C.g][i],7)}</g>`).join('')}
  <g data-k="cs_bub">${card(330,1180,420,120,'#e6f4ff',24)}${en?lat(540,1255,'RFQ: 20,000 pcs?',30,C.bd,800):tx(540,1255,'নতুন অর্ডার রিকোয়েস্ট',32,C.bd,800)}</g></g>
 <g data-k="cs_btn">${card(240,1600,600,120,C.y,60)}${lat(540,1680,'Exportain.com',56,C.f,800)}</g>
 <g data-k="cs_tap">${icon('hand',0,0,140,'#fff',8)}</g>`,
 upd(q,lt,t,bt){popIn(q('cs_logo'),pe(lt,.05,.5),t,0,30,3);popIn(q('cs_ph'),pe(lt,Math.min(bt(0),.5),.6),t,1,120,3);
  for(let i=0;i<3;i++)popIn(q('cs_i'+i),pe(lt,Math.min(bt(0),.5)+.3+i*.15,.4),t,i,20,0);
  popIn(q('cs_bub'),pe(lt,bt(1),.5),t,2,30,2);popIn(q('cs_btn'),pe(lt,bt(2)-.2,.5),t,3,40,0);
  if(lt>bt(2)+.3)T(q('cs_btn'),{s:1+.05*Math.sin(t*7),o:1});
  const h=cl((lt-bt(2))/.5);T(q('cs_tap'),{x:L(860,700,eo(h)),y:L(1900,1720,eo(h))+(h>=1?Math.sin(t*6)*8:0),o:cl(h*3)})}})}
K.PFX_cta_en=ctaShort('en'); K.PFX_cta_bn=ctaShort('bn');
