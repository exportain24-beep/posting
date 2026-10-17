// ===================== EPB enrolment 16:9 — scenes 10–18 =====================
// 10 — point 4: fee by term + VAT
K.ep_fee=()=>({svg:`${BG}${rd('f_')}${ttl2('f_','৪','ফি ও ভ্যাট',C.o)}
 <g data-k="f_r">${card(500,330,920,640,'#fff',44)}<rect x="500" y="330" width="920" height="100" rx="44" fill="${C.o}"/><rect x="500" y="380" width="920" height="50" fill="${C.o}"/>${lat(560,398,'Fee receipt',40,'#fff',800,'start')}
  <g data-k="f_l1"><rect x="560" y="480" width="800" height="110" rx="18" fill="#fff7ed"/>${tx(600,550,'নির্ধারিত ফি × বেছে নেওয়া মেয়াদ',40,C.ink,800,'start')}</g>
  <g data-k="f_l2"><rect x="560" y="620" width="800" height="110" rx="18" fill="#fff7ed"/>${tx(600,690,'+ ভ্যাট',40,C.ink,800,'start')}${lat(1320,692,'15%',56,C.o,800,'end')}</g>
  <rect x="560" y="770" width="800" height="6" rx="3" fill="#e2e8f0"/>${tx(600,860,'মোট',44,C.ink,800,'start')}${coin(1290,845,50)}</g>`,
 upd(q,lt,t,bt){rdU(q,'f_',lt,t,4);ttlU(q,'f_',lt,t);popG(q('f_r'),lt,.4,t,0,40,0,.5);popIn(q('f_l1'),pe(lt,bt(1)-.2,.4),t,1,10,0);popIn(q('f_l2'),pe(lt,bt(2)-.2,.4),t,2,10,0)}});

// 11 — fee increase March 2025
K.ep_fee2=()=>({svg:`${BG}${rd('g_')}
 <g data-k="g_n">${card(100,180,760,780,'#fff',44)}${docPage(180,230,600,520,'EPB Notice',C.bd,7)}${tx(480,850,'মার্চ ২০২৫ থেকে নতুন ফি',40,C.ink,800)}</g>
 <g data-k="g_p">${card(960,180,860,420,'#fff',44)}${lat(1390,280,'GSP certificate',44,C.ink,800)}<g data-k="g_o">${tx(1110,450,'৫০০',80,C.mute,800)}<rect x="1030" y="418" width="160" height="10" fill="${C.r}"/></g><path d="M1220 420 H1330 M1300 395 L1335 420 L1300 445" stroke="${C.ink}" stroke-width="10" fill="none"/><g data-k="g_nw">${tx(1560,460,'৬০০ টাকা',84,C.g,800)}</g></g>
 <g data-k="g_c">${card(960,650,860,310,'#eef6ff',44)}${laptop(1120,820,1.3,C.b)}${tx(1260,780,'আবেদনের আগে',36,C.mute,800,'start')}${tx(1260,850,'পোর্টালে সর্বশেষ ফি',44,C.b,800,'start')}</g>`,
 upd(q,lt,t,bt){rdU(q,'g_',lt,t,4);popG(q('g_n'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.5);popG(q('g_p'),lt,bt(1)-.8,t,1,30,0,.5);popIn(q('g_nw'),pe(lt,bt(1)-.1,.45),t,2,20,3);popG(q('g_c'),lt,bt(2)-.3,t,3,30,0,.5)}});

// 12 — point 5: right after ERC
K.ep_when=()=>({svg:`${BG}${rd('w_')}${ttl2('w_','৫','ইআরসির পরপরই',C.gd)}
 <g data-k="w_e">${ercCard(120,360,520,340)}</g>
 <path data-k="w_a" d="M680 530 H860 M820 495 L865 530 L820 565" stroke="${C.gd}" stroke-width="14" fill="none"/>
 <g data-k="w_n">${enrCard(900,360,520,340)}</g>
 <g data-k="w_s">${card(1460,330,380,620,'#e9f8ec',40)}${shipA(1650,560,.9)}${tx(1650,760,'চালান',44,C.ink,800)}${tx(1650,830,'সময়মতো',44,C.g,800)}${check(1650,900,34,C.g)}</g>
 ${kw('w_w',780,880,'তাড়াহুড়োয় আটকে থাকবে না',52,'#fff',C.gd)}`,
 upd(q,lt,t,bt){rdU(q,'w_',lt,t,5);ttlU(q,'w_',lt,t);popG(q('w_e'),lt,.4,t,0,40,2,.5);T(q('w_a'),{o:lt>bt(1)-.5?1:.12});popG(q('w_n'),lt,bt(1)-.2,t,1,40,2,.5);popG(q('w_s'),lt,bt(2)-.3,t,2,40,0,.5);kwU(q,'w_w',lt,bt(2),t)}});

// 13 — the order of steps (staircase)
K.ep_order=()=>{const S=[['Trade licence',C.b],['e-TIN',C.t],['Membership',C.p],['ERC',C.g],['EPB Enrolment',C.bd],['GSP / REX',C.o]];return{svg:`${BG}${rd('s_')}
 ${kw('s_w',520,230,'সহজ ক্রম',72,C.gd)}
 ${S.map((s,i)=>`<g data-k="s_s${i}"><rect x="${110+i*290}" y="${900-i*110}" width="270" height="${110+i*110}" rx="18" fill="${s[1]}"/>${lat(245+i*290,960-i*110,s[0],s[0].length>10?24:30,'#fff',800)}<circle cx="${245+i*290}" cy="${870-i*110}" r="26" fill="#fff"/>${tx(245+i*290,884-i*110,BN(i+1),30,s[1],800)}</g>`).join('')}`,
 upd(q,lt,t,bt){rdU(q,'s_',lt,t,5);kwU(q,'s_w',lt,.1,t);for(let i=0;i<6;i++)popG(q('s_s'+i),lt,bt(i)-.2,t,i,60,0,.45)}}};

// 14 — renewal reminder
K.ep_remind=()=>({svg:`${BG}${rd('r_')}
 <g data-k="r_p">${phone(180,170,440,820)}<rect x="200" y="300" width="400" height="200" rx="20" fill="#fff7ed" stroke="${C.o}" stroke-width="4"/>${icon('cal',260,370,60,C.o,7)}${lat(310,360,'Reminder',28,C.o,800,'start')}${lat(240,420,'Renew EPB enrolment',26,C.ink,800,'start')}${lat(240,460,'30 days left',26,C.r,800,'start')}</g>
 <g data-k="r_x">${card(780,250,1040,620,'#fff4f2',44)}<g opacity=".45">${enrCard(880,330,420,290)}</g>${stampT(1090,480,'মেয়াদোত্তীর্ণ',C.r,44)}${[['GSP',C.g],['REX',C.gd],['CO',C.b]].map((c,i)=>`<g>${chip2(1560,370+i*150,c[0],c[1])}${icon('lock',1660,330+i*150,44,C.r,8)}</g>`).join('')}${tx(1300,800,'সনদ পাওয়া বন্ধ',48,C.r,800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'r_',lt,t,5);popG(q('r_p'),lt,Math.min(bt(0)-.3,.2),t,0,40,2,.5);popG(q('r_x'),lt,bt(1)-.3,t,1,40,0,.5)}});

// 15 — Nazma succeeds
K.ep_story2=()=>({svg:`${BG}
 <g data-k="z_p">${card(100,170,600,780,'#fff',44)}${woman2(400,250,1)}${tx(400,570,'নাজমা',52,C.ink,800)}<g data-k="z_e">${enrCard(170,640,460,280,'Valid: 5 years',C.b)}</g></g>
 <g data-k="z_r">${card(780,170,520,360,'#fff',40)}${lat(1040,300,'REX',90,C.gd,800)}${tx(1040,420,'নিবন্ধিত',44,C.g,800)}${check(1240,220,34,C.g)}</g>
 <g data-k="z_d">${card(1340,170,480,360,'#e9f8ec',40)}${eu(1580,280,.7)}${lat(1580,440,'Duty benefit ✓',36,C.g,800)}</g>
 <g data-k="z_o">${card(780,580,1040,370,'#fff',40)}${person(900,620,.55,'g','z_bp')}${bub(1400,720,640,'New order: 8,000 pcs',C.b,'#fff',34,-1)}${tx(1400,860,'পরের অর্ডার',48,C.gd,800)}</g>`,
 upd(q,lt,t,bt){popG(q('z_p'),lt,.15,t,0,40,2,.5);popIn(q('z_e'),pe(lt,bt(0)-.1,.45),t,1,20,3);popG(q('z_r'),lt,bt(1)-.2,t,2,30,2,.5);popG(q('z_d'),lt,bt(2)-.2,t,3,30,2,.5);popG(q('z_o'),lt,bt(3)-.3,t,4,30,2,.5)}});

// 16 — Exportain
K.ep_brand=()=>({svg:`${BG}
 <g data-k="xb_logo"><image href="__LOGO__" x="560" y="130" width="800" height="230" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="xb_pg">${card(100,400,860,560,'#fff',40)}<rect x="100" y="400" width="860" height="86" rx="40" fill="${C.g}"/><rect x="100" y="446" width="860" height="40" fill="${C.g}"/>${lat(140,456,'Company page · Nazma Knit Exports',30,'#fff',800,'start')}${icon('shirt',200,590,90,C.b,7)}${lat(300,600,'Certificates',36,C.ink,800,'start')}
  ${[['EPB Enrolment','Verified until 2031'],['ERC','Verified'],['BKMEA membership','Verified until Jun 2027']].map((c,i)=>`<g data-k="xb_c${i}"><rect x="140" y="${680+i*88}" width="780" height="74" rx="16" fill="#f1f8f1"/>${lat(170,726+i*88,c[0],28,C.ink,800,'start')}${lat(890,726+i*88,c[1],22,C.g,800,'end')}</g>`).join('')}</g>
 <g data-k="xb_tag">${card(1020,400,800,200,C.gd,40)}${tx(1420,480,'বাংলাদেশি প্রস্তুতকারক ও রপ্তানিকারকদের',34,'#fff',800)}${lat(1290,550,'B2B',40,C.y,800)}${tx(1350,550,'মার্কেটপ্লেস',40,'#e3f8d3',800,'start')}</g>
 <g data-k="xb_by">${card(1020,640,800,320,'#fff',40)}${person(1150,680,.6,'g','xb_bp')}${bub(1520,790,460,'Certificates verified ✓',C.b,'#fff',28,-1)}${tx(1520,910,'বিদেশি ক্রেতার আস্থা বাড়ে',36,C.g,800)}</g>`,
 upd(q,lt,t,bt){const l=pe(lt,.2,.8);T(q('xb_logo'),{s:L(.5,1,eo(l))+(l>=1?Math.sin(t*1.5)*.012:0),o:cl(l*2)});popG(q('xb_pg'),lt,bt(1)-.6,t,1,40,0,.5);for(let i=0;i<3;i++){const p=pe(lt,bt(1)+i*.35,.4);T(q('xb_c'+i),{x:L(-50,0,eo(p)),o:cl(p*2)})}
  popG(q('xb_tag'),lt,bt(2)-.2,t,2,30,0,.5);popG(q('xb_by'),lt,bt(3)-.2,t,3,30,2,.5)}});

// 17 — advice
K.ep_advice=()=>({svg:`${BG}
 <g data-k="v_a">${card(140,200,760,640,'#fff',44)}${bank(520,500,1.4,C.b)}${lat(520,690,'EPB',56,C.b,800)}${tx(520,760,'রপ্তানি উন্নয়ন ব্যুরো',32,C.mute,800)}</g>
 <g data-k="v_b">${card(1020,200,760,640,'#fff',44)}${bank(1400,500,1.4,C.g)}${lat(1400,690,'AD Bank',50,C.g,800)}${tx(1400,760,'অনুমোদিত ডিলার ব্যাংক',30,C.mute,800)}</g>
 ${kw('v_w',960,960,'নির্দিষ্ট লেনদেনের আগে পরামর্শ নিন',52,'#fff',C.gd)}`,
 upd(q,lt,t,bt){popG(q('v_a'),lt,Math.min(bt(0)-.3,.2),t,0,40,2,.5);popG(q('v_b'),lt,bt(1)-.3,t,1,40,2,.5);kwU(q,'v_w',lt,bt(1)+.3,t)}});

// 18 — CTA
K.ep_cta=()=>({svg:`${BG}
 <g data-k="ct_who">${card(100,200,700,260,'#fff',44)}${bdflag(150,270,150)}${tx(560,310,'প্রস্তুতকারক বা',44,C.ink,800)}${tx(560,390,'রপ্তানিকারক?',56,C.g,800)}</g>
 <g data-k="ct_gl">${icon('globe',450,760,300,C.t,4)}${[0,1,2,3].map(i=>`<g data-k="ct_f${i}"><circle cx="0" cy="0" r="40" fill="#fff"/>${icon(['shirt','bag','box','shoe'][i],0,0,50,[C.b,C.g,C.p,C.o][i],7)}</g>`).join('')}</g>
 <g data-k="ct_lg"><image href="__LOGO__" x="1010" y="220" width="760" height="220" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="ct_bt">${card(1040,520,700,140,C.g,70)}${lat(1390,612,'Exportain.com',62,'#fff',800)}</g>
 <g data-k="ct_hd">${tap('ct_rp')}</g>
 ${kw('ct_u',1390,800,'আজই ভিজিট করুন',60,'#fff',C.o)}`,
 upd(q,lt,t,bt){popG(q('ct_who'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.5);popG(q('ct_gl'),lt,bt(1)-.4,t,1,30,0,.5);for(let i=0;i<4;i++){const p=pe(lt,bt(1)+i*.15,.5),a=i*1.57+t*.5;T(q('ct_f'+i),{x:450+Math.cos(a)*230,y:760+Math.sin(a)*200,s:L(.2,1,p),o:cl(p*2)})}
  const l=pe(lt,.4,.6);T(q('ct_lg'),{s:L(.6,1,eb(l)),o:cl(l*3)});popG(q('ct_bt'),lt,bt(2)-.4,t,2,30,0,.45);if(lt>bt(2)+.3)T(q('ct_bt'),{s:1+.04*Math.sin(t*7),o:1});
  const h=cl((lt-bt(2))/.5);T(q('ct_hd'),{x:L(1860,1700,eo(h)),y:L(760,640,eo(h)),o:cl(h*3)});const rp=((lt-bt(2))%1+1)%1;T(q('ct_rp'),{s:1+rp*1.8,o:h>=1?1-rp:0});kwU(q,'ct_u',lt,bt(2),t)}});
