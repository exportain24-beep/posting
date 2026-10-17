// ===================== Chamber vs association — scenes 11–19 =====================
// 11 — point 5: which first? one is enough for ERC, many have both
K.as_which=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>${road5('e1_')}
 ${ttl('e1_','৫','কোনটা আগে?',C.gd)}
 <g data-k="e1_r">${card(80,600,920,470,'#fff',40)}${cert(120,640,300,240,'ERC',C.g)}${tx(470,720,'চাওয়া হয়',34,C.mute,800,'start')}${tx(470,790,'একটি স্বীকৃত',44,C.ink,800,'start')}${tx(470,860,'সংগঠনের সদস্যপদ',44,C.ink,800,'start')}
  <g data-k="e1_k0">${pill(300,990,'চেম্বার ✓',C.b,40)}</g>${tx(540,1000,'বা',36,C.mute,800)}<g data-k="e1_k1">${pill(780,990,'অ্যাসোসিয়েশন ✓',C.g,40)}</g></g>
 <g data-k="e1_e">${browser(80,1120,920,620,'bangladesh.eregulations.org',C.gd)}${lat(130,1250,'Typical export procedure',32,C.ink,800,'start')}
  ${stepRow(130,1290,820,'1. DCCI Membership (chamber)',C.b,'e1_s0',true)}${stepRow(130,1390,820,'2. Export Registration (ERC)',C.mute,'e1_s1',false)}${stepRow(130,1490,820,'3. Sector association membership',C.g,'e1_s2',true)}
  <g data-k="e1_b">${pill(540,1660,'বাস্তবে অনেকের দুটোই থাকে',C.o,38)}</g></g>`,
 upd(q,lt,t,bt){road5Upd(q,'e1_',lt,t,5,0);popIn(q('e1_tt'),pe(lt,.2,.6),t,0,40,2);if(lt>bt(1))T(q('e1_tt'),{s:1+.015*Math.sin(t*4),o:1});popG(q('e1_r'),lt,bt(2)-.3,t,1,40,0);
  popG(q('e1_k0'),lt,bt(3)-.1,t,2,20,3,.5);popG(q('e1_k1'),lt,bt(3)+.6,t,3,20,3,.5);popG(q('e1_e'),lt,bt(4)-.3,t,4,30,0);for(let i=0;i<3;i++){const p=pe(lt,bt(4)+.2+i*.35,.35);T(q('e1_s'+i),{x:L(-40,0,eo(p)),o:cl(p*2)})}popG(q('e1_b'),lt,bt(5)-.2,t,5,20,3,.6)}});

// 12 — association first when you need UD/incentive/sector services
K.as_assoc=()=>{const N=[['UD',C.b],['নগদ সহায়তার সনদ',C.o],['খাতভিত্তিক সেবা',C.t]];return{svg:`<rect width="1080" height="1920" fill="url(#studio)"/>${road5('e2_')}
 <g data-k="e2_q">${card(80,410,920,470,'#fff',40)}${tx(540,500,'আপনার পণ্যে কি লাগে?',46,C.ink,800)}
  ${N.map((n,i)=>`<g data-k="e2_n${i}">${pill(540,600+i*100,n[0],n[1],40)}</g>`).join('')}</g>
 <g data-k="e2_y"><path d="M540 900 V990" stroke="${C.g}" stroke-width="14"/><path d="M505 985 L540 1035 L575 985Z" fill="${C.g}"/>${tx(620,975,'হ্যাঁ',40,C.g,800,'start')}</g>
 <g data-k="e2_a">${card(120,1050,840,280,C.g,50)}${tx(540,1160,'আগে',44,'#e3f8d3',800)}${tx(540,1260,'অ্যাসোসিয়েশন',76,'#fff',800)}</g>
 <g data-k="e2_e">${card(80,1380,920,340,'#fff',40)}${cert(130,1420,260,250,'ERC',C.g)}${tx(430,1520,'সেই সদস্যপদ দিয়েই',38,C.ink,800,'start')}${tx(430,1590,'ইআরসির কাজ শুরু',42,C.g,800,'start')}${check(900,1640,34,C.g)}</g>`,
 upd(q,lt,t,bt){road5Upd(q,'e2_',lt,t,5,0);popG(q('e2_q'),lt,.2,t,0,40,0);for(let i=0;i<3;i++)popG(q('e2_n'+i),lt,(i<2?bt(0)+.6+i*.9:bt(1)-.1),t,i,20,3,.5);
  popG(q('e2_y'),lt,bt(2)-.6,t,3,20,0,.5);popG(q('e2_a'),lt,bt(2)-.2,t,4,40,0,.6);if(lt>bt(2)+.6)T(q('e2_a'),{s:1+.02*Math.sin(t*3),o:1});popG(q('e2_e'),lt,bt(3)-.3,t,5,30,0)}}};

// 13 — chamber first for mixed products / weak sector bodies
K.as_chamber=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>${road5('e3_')}
 <g data-k="e3_p">${card(80,410,450,440,'#fff',40)}${icon('box',190,560,110,C.p,7)}${icon('bag',420,560,110,C.g,7)}${icon('shirt',190,700,110,C.b,7)}${icon('shoe',420,700,110,C.o,7)}${tx(305,810,'একাধিক পণ্য',36,C.ink,800)}</g>
 <g data-k="e3_h">${card(550,410,450,440,'#fff',40)}${kantha(625,450,300,230,C.r,C.y)}${tx(775,750,'হস্তশিল্প',38,C.ink,800)}${tx(775,810,'খাতের সংগঠন দুর্বল',28,C.mute,800)}</g>
 <g data-k="e3_c">${card(120,900,840,300,C.b,50)}${tx(540,1010,'নিজের জেলার',44,'#dbeafe',800)}${tx(540,1120,'চেম্বার',90,'#fff',800)}</g>
 <g data-k="e3_o">${card(80,1250,920,460,'#fff',40)}${cert(130,1300,380,300,'Certificate of Origin',C.b)}${tx(560,1420,'বাড়তি সেবা',36,C.mute,800,'start')}${tx(560,1490,'পণ্যের উৎস সনদ',42,C.b,800,'start')}${icon('globe',740,1600,90,C.t,7)}</g>`,
 upd(q,lt,t,bt){road5Upd(q,'e3_',lt,t,5,0);popG(q('e3_p'),lt,.2,t,0,40,3);popG(q('e3_h'),lt,bt(1)-.2,t,1,40,3);popG(q('e3_c'),lt,bt(2)-.2,t,2,40,0,.6);if(lt>bt(2)+.6)T(q('e3_c'),{s:1+.02*Math.sin(t*3),o:1});popG(q('e3_o'),lt,bt(3)-.3,t,3,30,0)}});

// 14 — lesson 1: BGMEA dropped ~690 for missing renewal
K.as_les1=()=>{const R=['কারখানা ক','কারখানা খ','কারখানা গ','কারখানা ঘ'];return{svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="f1_h">${card(80,290,920,170,C.gd,44)}${icon('star',180,375,80,C.y,8)}${tx(260,395,'বাস্তবের শিক্ষা ১ · নবায়ন',46,'#fff',800,'start')}</g>
 <g data-k="f1_l">${card(80,500,920,720,'#fff',40)}${lat(130,570,'BGMEA · Active members',32,C.ink,800,'start')}${tx(910,575,'২০২৫',32,C.mute,800,'end')}
  ${R.map((r,i)=>`<g data-k="f1_r${i}"><rect x="130" y="${620+i*140}" width="820" height="110" rx="20" fill="#f1f6fb"/>${icon('bld',200,675+i*140,70,C.b,6)}${tx(270,690+i*140,r,38,C.ink,800,'start')}<g data-k="f1_x${i}">${tx(890,690+i*140,'বাদ',34,C.r,800,'end')}<rect x="150" y="${669+i*140}" width="780" height="8" rx="4" fill="${C.r}"/></g></g>`).join('')}</g>
 <g data-k="f1_n">${card(80,1260,920,230,'#fff4f2',40)}${tx(540,1370,'≈ ৬৯০',90,C.r,800)}${tx(540,1450,'কারখানা সক্রিয় তালিকার বাইরে',34,C.r,800)}</g>
 <g data-k="f1_b">${cal(120,1530,190,'৳','নবায়ন',C.g)}${tx(350,1640,'নবায়ন কখনো ভুলবেন না',46,C.g,800,'start')}</g>`,
 upd(q,lt,t,bt){popG(q('f1_h'),lt,.2,t,0,30,0);popG(q('f1_l'),lt,bt(1)-.4,t,1,40,0);for(let i=0;i<4;i++){popIn(q('f1_r'+i),pe(lt,bt(1)+i*.2,.4),t,i,20,0);const p=pe(lt,bt(3)+i*.25,.4);T(q('f1_x'+i),{o:cl(p*2)});if(p>0)T(q('f1_r'+i),{o:1-.45*p})}
  popG(q('f1_n'),lt,bt(2)-.2,t,2,30,0,.6);popG(q('f1_b'),lt,bt(4)-.2,t,3,30,3,.6)}}};

// 15 — lesson 2: jute incentive manipulation
K.as_les2=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="f2_h">${card(80,290,920,170,C.juteD,44)}${tx(540,395,'শিক্ষা ২ · পাট খাত, ২০২৩',46,'#fff',800)}</g>
 <g data-k="f2_w">${card(80,500,920,190,'#fff4f2',40)}${shield(190,595,.8,C.r,'!')}${tx(290,580,'নগদ সহায়তার সনদে',38,C.ink,800,'start')}${tx(290,650,'কারসাজির অভিযোগ',46,C.r,800,'start')}</g>
 <g data-k="f2_a">${card(80,730,440,560,'#fff',40)}${jutebag(300,960,.85)}${tx(300,1140,'আসল পণ্য',34,C.mute,800)}${pill(300,1230,'কম হার',C.g,40)}</g>
 <g data-k="f2_b">${card(560,730,440,560,'#fff',40)}${jutebag(780,960,.85)}${tx(780,1140,'ঘোষণায় দেখানো',34,C.mute,800)}${pill(780,1230,'বেশি হার',C.r,40)}</g>
 <path data-k="f2_ar" d="M470 1010 H600" stroke="${C.r}" stroke-width="12" stroke-dasharray="18 12"/>
 <g data-k="f2_m">${card(80,1330,920,400,'#fff',40)}${docPage(130,1380,240,300,'Audit',C.r,5)}<g data-k="f2_mg">${mag(250,1500,1.1,C.ink)}</g>${tx(440,1490,'ভুল ঘোষণার সনদ',42,C.ink,800,'start')}${tx(440,1570,'নিরীক্ষায় বিপদ',48,C.r,800,'start')}</g>`,
 upd(q,lt,t,bt){popG(q('f2_h'),lt,.2,t,0,30,0);popG(q('f2_w'),lt,bt(1)-.2,t,1,30,0,.6);popG(q('f2_a'),lt,bt(2)-.2,t,2,40,3);popG(q('f2_b'),lt,bt(3)-.2,t,3,40,3);T(q('f2_ar'),{o:lt>bt(3)?1:.12});
  popG(q('f2_m'),lt,bt(4)-.3,t,4,30,0);T(q('f2_mg'),{x:Math.sin(t*2)*40,y:Math.cos(t*2.4)*24})}});

// 16 — lesson 3: betel leaf association certificate
K.as_les3=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="f3_h">${card(80,290,920,170,'#3f9b2f',44)}${tx(540,395,'শিক্ষা ৩ · পান রপ্তানি',46,'#fff',800)}</g>
 <g data-k="f3_l">${card(80,500,440,380,'#fff',40)}${leafB(300,680,1.2)}</g>
 <g data-k="f3_c">${card(560,500,440,180,'#fff4f2',36)}${coin(650,590,46)}${tx(720,605,'বাড়তি টাকা',38,C.r,800,'start')}</g>
 <g data-k="f3_d">${card(560,700,440,180,'#fff4f2',36)}${cross(650,790,40,C.r)}${tx(720,805,'তালিকা থেকে বাদ',30,C.r,800,'start')}</g>
 <g data-k="f3_g">${card(80,920,920,400,'#fff',40)}${tx(130,1000,'রপ্তানিকারক প্রতিষ্ঠান',36,C.ink,800,'start')}
  ${tx(130,1110,'২০২৩-২৪',30,C.mute,800,'start')}${meter(300,1075,560,50,C.g,'f3_w0')}<g data-k="f3_v0">${tx(950,1115,'৭২',48,C.g,800,'end')}</g>
  ${tx(130,1230,'২০২৫-২৬',30,C.mute,800,'start')}${meter(300,1195,560,50,C.r,'f3_w1')}<g data-k="f3_v1">${tx(950,1235,'৪৪',48,C.r,800,'end')}</g></g>
 <g data-k="f3_j">${card(80,1360,920,370,'#fff',40)}${gavel(230,1520,1.05)}${tx(400,1460,'অক্টোবর ২০২৬',34,C.mute,800,'start')}${tx(400,1530,'আপিল বিভাগের',36,C.ink,800,'start')}${tx(400,1590,'চেম্বার আদালত',36,C.ink,800,'start')}<g data-k="f3_s">${stampT(760,1650,'স্থগিত',C.r,46)}</g></g>`,
 upd(q,lt,t,bt){popG(q('f3_h'),lt,.2,t,0,30,0);popG(q('f3_l'),lt,.6,t,1,40,3);popG(q('f3_c'),lt,bt(1)-.2,t,2,30,3);popG(q('f3_d'),lt,bt(2)-.2,t,3,30,3);
  popG(q('f3_g'),lt,bt(3)-.5,t,4,30,0);fillTo(q('f3_w0'),lt,bt(3),560);popIn(q('f3_v0'),pe(lt,bt(3)+.6,.4),t,5,0,0);fillTo(q('f3_w1'),lt,bt(4),342);popIn(q('f3_v1'),pe(lt,bt(4)+.6,.4),t,6,0,0);
  popG(q('f3_j'),lt,bt(5)-.2,t,7,30,0);popIn(q('f3_s'),pe(lt,bt(6)-.1,.5),t,8,0,0)}});

// 17 — check three things before joining
K.as_tip=()=>{const I=[['DTO লাইসেন্সপ্রাপ্ত?','lock',C.b],['ফি ও বার্ষিক চাঁদা কত?','cart',C.o],['বাস্তবে কোন সেবা দেয়?','star',C.g]];return{svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="g1_h">${card(80,290,920,190,'#fff',44)}${tx(540,375,'সদস্য হওয়ার আগে',38,C.mute,800)}${tx(540,445,'তিনটি জিনিস দেখুন',52,C.gd,800)}</g>
 ${I.map((it,i)=>`<g data-k="g1_i${i}">${card(80,530+i*250,920,210,'#fff',36)}<circle cx="190" cy="${635+i*250}" r="62" fill="${it[2]}"/>${icon(it[1],190,635+i*250,74,'#fff',8)}${tx(290,655+i*250,it[0],44,C.ink,800,'start')}<g data-k="g1_k${i}">${check(920,635+i*250,36,C.g)}</g></g>`).join('')}
 <g data-k="g1_s">${card(80,1300,920,420,C.gd,44)}${shield(250,1500,1.1,C.y,'✓')}${tx(420,1460,'নিয়ম জানতে',40,'#d9f5c4',800,'start')}${tx(420,1540,'সরকারি সূত্র দেখুন',48,'#fff',800,'start')}${lat(420,1620,'eRegulations · DTO · CCI&E',28,'#bde5a8',800,'start')}</g>`,
 upd(q,lt,t,bt){popG(q('g1_h'),lt,.2,t,0,30,0);for(let i=0;i<3;i++){slideG(q('g1_i'+i),lt,Math.min(bt(i+1)-.6,1.3+i*.8),-140,t,i);popIn(q('g1_k'+i),pe(lt,bt(i+1)+.3,.4),t,i,0,0)}popG(q('g1_s'),lt,bt(4)-.3,t,3,40,0)}}};

// 18 — Exportain: add certificates to company page
K.as_brand=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="xb_logo"><image href="__LOGO__" x="190" y="300" width="700" height="210" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="xb_pg">${card(80,540,920,620,'#fff',40)}<rect x="80" y="540" width="920" height="90" rx="40" fill="${C.g}"/><rect x="80" y="590" width="920" height="40" fill="${C.g}"/>${lat(130,600,'Company page · Rakib Fresh Veg',30,'#fff',800,'start')}${basket(230,740,.9)}${lat(360,710,'Certificates',34,C.ink,800,'start')}
  ${[['BFVAPEA membership','Verified until Jun 2027'],['Chamber membership','Verified until Jun 2027'],['ERC','Verified']].map((c,i)=>`<g data-k="xb_c${i}"><rect x="130" y="${850+i*95}" width="820" height="80" rx="16" fill="#f1f8f1"/>${lat(160,900+i*95,c[0],28,C.ink,800,'start')}${lat(920,900+i*95,c[1],22,C.g,800,'end')}</g>`).join('')}</g>
 <g data-k="xb_tag">${card(90,1200,900,170,C.gd,40)}${tx(540,1270,'বাংলাদেশি প্রস্তুতকারক ও রপ্তানিকারকদের',36,'#fff',800)}${lat(400,1335,'B2B',40,C.y,800)}${tx(460,1335,'মার্কেটপ্লেস',40,'#e3f8d3',800,'start')}</g>
 <g data-k="xb_by">${card(80,1410,920,330,'#fff',40)}${person(220,1460,.6,'g','xb_bp')}${bub(620,1560,520,'Certificates verified ✓',C.b,'#fff',30,-1)}${tx(620,1690,'বিদেশি ক্রেতার আস্থা বাড়ে',36,C.g,800)}</g>`,
 upd(q,lt,t,bt){const l=pe(lt,.2,.8);T(q('xb_logo'),{s:L(.5,1,eo(l))+(l>=1?Math.sin(t*1.5)*.012:0),o:cl(l*2)});popG(q('xb_pg'),lt,bt(1)-.4,t,1,40,0);for(let i=0;i<3;i++){const p=pe(lt,bt(1)+i*.35,.4),e=q('xb_c'+i);if(e)T(e,{x:L(-50,0,eo(p)),o:cl(p*2)})}
  popG(q('xb_tag'),lt,bt(2)-.2,t,2,30,0);popG(q('xb_by'),lt,bt(3)-.2,t,3,30,2,.6)}});

// 19 — closing formula
K.as_close=()=>{const S=[['সময়','cal',C.b],['টাকা','cart',C.o],['ঝামেলা','check',C.g]];return{svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="zc_a">${card(80,330,920,220,'#fff',44)}${tx(540,420,'আগে',36,C.mute,800)}${tx(540,500,'পণ্যের প্রয়োজন',58,C.ink,800)}</g>
 <g data-k="zc_r"><path d="M540 570 V650" stroke="${C.g}" stroke-width="14"/><path d="M505 645 L540 695 L575 645Z" fill="${C.g}"/></g>
 <g data-k="zc_b">${card(80,710,920,220,C.g,44)}${tx(540,800,'তারপর',36,'#e3f8d3',800)}${tx(540,880,'সদস্যপদ',62,'#fff',800)}</g>
 ${S.map((s,i)=>`<g data-k="zc_s${i}">${card(90+i*310,1010,280,380,'#fff',40)}<circle cx="${230+i*310}" cy="${1140}" r="80" fill="${s[2]}"/>${icon(s[1],230+i*310,1140,90,'#fff',8)}${tx(230+i*310,1300,s[0],46,C.ink,800)}${tx(230+i*310,1360,'বাঁচে',32,s[2],800)}</g>`).join('')}
 <g data-k="zc_t">${pill(540,1520,'ঠিক সংগঠন = সঠিক শুরু',C.gd,44)}</g>`,
 upd(q,lt,t,bt){popG(q('zc_a'),lt,.2,t,0,30,3);popG(q('zc_r'),lt,bt(1)-.4,t,1,20,0,.5);popG(q('zc_b'),lt,bt(1)-.2,t,2,30,3);for(let i=0;i<3;i++)popG(q('zc_s'+i),lt,bt(i+2)-.15,t,i,40,4,.6);popG(q('zc_t'),lt,bt(4)+.8,t,3,20,3,.6)}}};
