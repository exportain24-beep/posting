// ===================== ERC rules 16:9 — scenes 11–20 =====================
// 11 — reasons communicated, review possible
K.er_hear=()=>({svg:`${BG}${rd('h2_')}
 <g data-k="h2_n">${docPage(140,260,560,640,'Notice',C.b,6)}${tx(420,820,'কারণসহ লিখিত নোটিশ',38,C.ink,800)}</g>
 <path data-k="h2_a" d="M760 580 H1060 M1020 545 L1065 580 L1020 615" stroke="${C.gd}" stroke-width="14" fill="none"/>
 <g data-k="h2_r">${docPage(1120,260,620,640,'Review application',C.g,6)}${tx(1430,820,'পুনর্বিবেচনার আবেদন',38,C.g,800)}${check(1660,330,40,C.g)}</g>
 ${kw('h2_w',960,990,'নিজের কথা বলার সুযোগ আছে',52,'#fff',C.gd)}`,
 upd(q,lt,t,bt){rdU(q,'h2_',lt,t,3);popG(q('h2_n'),lt,Math.min(bt(0)-.3,.3),t,0,40,2,.5);T(q('h2_a'),{o:lt>bt(1)-.4?1:.12});popG(q('h2_r'),lt,bt(1)-.2,t,1,40,2,.5);kwU(q,'h2_w',lt,bt(1)+.5,t)}});

// 12 — point 4: not transferable
K.er_transfer=()=>({svg:`${BG}${rd('t_')}${ttl2('t_','৪','ইআরসি হস্তান্তরযোগ্য নয়',C.t)}
 <g data-k="t_a">${card(100,340,520,600,'#fff',40)}${person(360,390,.85,'s','t_ap')}${tx(360,700,'সনদধারী',40,C.ink,800)}</g>
 <g data-k="t_b">${card(1300,340,520,600,'#fff',40)}${person(1560,390,.85,'n','t_bp')}${tx(1560,700,'অন্য কেউ',40,C.ink,800)}</g>
 <g data-k="t_e">${ercCard(700,480,420,280)}</g>
 <g data-k="t_l"><rect x="1150" y="520" width="110" height="100" rx="16" fill="${C.r}"/><path d="M1170 520 V480 Q1205 440 1240 480 V520" stroke="${C.r}" stroke-width="16" fill="none"/>${lat(1205,590,'✕',44,'#fff',800)}</g>
 ${kw('t_w',960,1000,'অনুমতি ছাড়া হস্তান্তর নয়',56,'#fff',C.t)}`,
 upd(q,lt,t,bt){rdU(q,'t_',lt,t,4);ttlU(q,'t_',lt,t);popG(q('t_a'),lt,.4,t,0,40,2,.5);popG(q('t_b'),lt,.7,t,1,40,2,.5);const k=cl((lt-1)/1.2);T(q('t_e'),{x:L(-200,120,eo(k))-(lt>bt(0)+.3?Math.min(1,(lt-bt(0)-.3)*2)*120:0),o:cl(k*3)});popIn(q('t_l'),pe(lt,bt(0)+.2,.4),t,2,0,0);kwU(q,'t_w',lt,bt(1)-.1,t)}});

// 13 — renting an ERC is dangerous
K.er_rent=()=>({svg:`${BG}${rd('n_')}
 <g data-k="n_c">${card(100,180,760,420,'#fff',40)}${carton(300,400,1.4,'#d9a55c','#b9853d','#e9c287','OTHER')}<g data-k="n_l">${ercCard(470,300,340,220)}</g>${tx(480,560,'অন্যের পণ্য, আপনার ইআরসি',36,C.ink,800)}</g>
 <g data-k="n_r">${card(100,650,760,320,'#fff4f2',40)}<rect x="180" y="720" width="600" height="120" rx="20" fill="${C.o}"/>${tx(480,800,'ইআরসি ভাড়া',52,'#fff',800)}${slash(480,780,150)}</g>
 <g data-k="n_d">${card(980,180,840,790,'#fff',44)}${shield(1400,400,1.6,C.r,'!')}${tx(1400,640,'চালানে গোলমাল হলে',44,C.ink,800)}${kw('n_w',1400,780,'দায় সনদধারীর',72,'#fff',C.r)}</g>`,
 upd(q,lt,t,bt){rdU(q,'n_',lt,t,4);popG(q('n_c'),lt,Math.min(bt(0)-.3,.3),t,0,40,2,.5);popG(q('n_r'),lt,bt(1)-.2,t,1,30,0,.5);popG(q('n_d'),lt,bt(2)-.2,t,2,40,0,.5);kwU(q,'n_w',lt,bt(3)-.1,t)}});

// 14 — update on changes
K.er_update=()=>({svg:`${BG}${rd('p_')}
 <g data-k="p_s">${card(100,200,760,560,'#fff',40)}<rect x="160" y="260" width="640" height="130" rx="16" fill="${C.bd}"/><g data-k="p_o">${lat(480,345,'Jewel Trading',48,'#cfe3f3',800)}</g><g data-k="p_nw">${lat(480,345,'Jewel Jute Exports Ltd',42,'#fff',800)}</g>
  ${['নাম','ঠিকানা','মালিকানা'].map((s,i)=>pill([250,480,710][i],480,s,[C.b,C.t,C.o][i],34)).join('')}${tx(480,620,'কিছু বদলালে',40,C.ink,800)}</g>
 <path data-k="p_a" d="M900 480 H1060 M1020 445 L1065 480 L1020 515" stroke="${C.gd}" stroke-width="14" fill="none"/>
 <g data-k="p_o2">${card(1100,200,720,560,'#fff',40)}${bank(1460,470,1.3,C.bd)}${lat(1460,640,'CCI&E',48,C.bd,800)}${tx(1460,700,'প্রধান নিয়ন্ত্রকের দপ্তর',30,C.mute,800)}</g>
 ${kw('p_w',960,900,'সনদ হালনাগাদ ✓',64,'#fff',C.g)}`,
 upd(q,lt,t,bt){rdU(q,'p_',lt,t,4);popG(q('p_s'),lt,.2,t,0,40,2,.5);const k=cl((lt-bt(0)-.4)/.5);T(q('p_o'),{o:1-k});T(q('p_nw'),{o:k});T(q('p_a'),{o:lt>bt(1)-.4?1:.12});popG(q('p_o2'),lt,bt(1)-.2,t,1,40,2,.5);kwU(q,'p_w',lt,bt(2)-.1,t)}});

// 15 — point 5: no fear
K.er_calm=()=>{const P=['shirt','shoe','bag','box','cart','star'];return{svg:`${BG}${rd('k_')}${ttl2('k_','৫','আইন মানলে ভয় নেই',C.g)}
 <g data-k="k_r">${card(100,340,380,600,'#fff4f2',40)}${tx(290,460,'নিষিদ্ধ',44,C.r,800)}<rect x="210" y="520" width="160" height="160" rx="20" fill="${C.r}" opacity=".85"/>${tx(290,620,'ছোট',44,'#fff',800)}${tx(290,800,'তালিকা',40,C.mute,800)}</g>
 <g data-k="k_g">${card(540,340,1280,600,'#e9f8ec',40)}${tx(1180,430,'বেশির ভাগ পণ্যই রপ্তানিযোগ্য',52,C.g,800)}${P.map((p,i)=>`<g data-k="k_p${i}"><circle cx="${700+i*190}" cy="640" r="80" fill="#fff"/>${icon(p,700+i*190,640,100,[C.b,C.o,C.g,C.p,C.t,C.y][i],7)}</g>`).join('')}${tx(1180,830,'পোশাক · চামড়া · পাটপণ্য · হস্তশিল্প · খাদ্য',36,C.ink,800)}</g>
 ${kw('k_w',960,1020,'ভয়ের কিছু নেই',48,'#fff',C.g)}`,
 upd(q,lt,t,bt){rdU(q,'k_',lt,t,5);ttlU(q,'k_',lt,t);kwU(q,'k_w',lt,bt(1)-.1,t);popG(q('k_r'),lt,bt(2)-.3,t,0,40,0,.5);popG(q('k_g'),lt,bt(3)-.4,t,1,40,0,.5);for(let i=0;i<6;i++)popIn(q('k_p'+i),pe(lt,bt(3)+i*.12,.3),t,i,20,4)}}};

// 16 — three habits
K.er_habits=()=>{const H=[['এইচএস কোড যাচাই','HS code check','globe'],['আগেই অনুমতি','Permit first','lock'],['সঠিক তথ্য','Correct data','check']];return{svg:`${BG}${rd('g_')}
 ${kw('g_w',960,240,'তিনটি অভ্যাস',80,C.gd)}
 ${H.map((h,i)=>`<g data-k="g_h${i}">${card(100+i*590,330,540,620,'#fff',44)}<circle cx="${370+i*590}" cy="520" r="110" fill="${[C.b,C.o,C.g][i]}"/>${icon(h[2],370+i*590,520,120,'#fff',8)}${tx(370+i*590,730,h[0],46,C.ink,800)}${lat(370+i*590,790,h[1],28,C.mute,700)}<g data-k="g_k${i}">${check(370+i*590,880,44,C.g)}</g></g>`).join('')}`,
 upd(q,lt,t,bt){rdU(q,'g_',lt,t,5);kwU(q,'g_w',lt,Math.min(bt(0),.3),t);for(let i=0;i<3;i++){popG(q('g_h'+i),lt,Math.min(bt(i+1)-.5,.6+i*.6),t,i,40,3,.5);popIn(q('g_k'+i),pe(lt,bt(i+1)+.2,.35),t,i,0,0)}}}};

// 17 — Jewel now exports jute bags
K.er_jewel2=()=>({svg:`${BG}
 <g data-k="w_p">${card(100,170,560,760,'#fff',44)}${person(380,230,.95,'s','w_sp')}${tx(380,560,'জুয়েল',52,C.ink,800)}${jutebag(380,760,.7)}</g>
 <g data-k="w_s">${card(720,170,1100,760,'#eef6ff',44)}${shipA(1270,560,1.8)}<rect x="720" y="680" width="1100" height="250" fill="#9fd3e8" opacity=".5"/></g>
 <g data-k="w_k">${card(1080,740,400,120,C.g,60)}${lat(1280,818,'Cleared ✓',52,'#fff',800)}</g>
 ${kw('w_w',960,1020,'কাগজ ঠিক, চালান নিশ্চিন্ত',52,'#fff',C.gd)}`,
 upd(q,lt,t,bt){popG(q('w_p'),lt,.15,t,0,40,2,.5);popG(q('w_s'),lt,Math.min(bt(0),.5),t,1,30,0,.5);popIn(q('w_k'),pe(lt,bt(1),.4),t,2,0,3);kwU(q,'w_w',lt,bt(2)-.2,t)}});

// 18 — Exportain
K.er_brand=()=>({svg:`${BG}
 <g data-k="xb_logo"><image href="__LOGO__" x="560" y="130" width="800" height="230" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="xb_pg">${card(100,400,860,560,'#fff',40)}<rect x="100" y="400" width="860" height="86" rx="40" fill="${C.g}"/><rect x="100" y="446" width="860" height="40" fill="${C.g}"/>${lat(140,456,'Company page · Jewel Jute Exports',30,'#fff',800,'start')}${jutebag(220,600,.5)}${lat(330,580,'Certificates',36,C.ink,800,'start')}
  ${[['ERC','Verified'],['Chamber membership','Verified until Jun 2027'],['Trade licence','Verified']].map((c,i)=>`<g data-k="xb_c${i}"><rect x="140" y="${680+i*88}" width="780" height="74" rx="16" fill="#f1f8f1"/>${lat(170,726+i*88,c[0],28,C.ink,800,'start')}${lat(890,726+i*88,c[1],22,C.g,800,'end')}</g>`).join('')}</g>
 <g data-k="xb_tag">${card(1020,400,800,200,C.gd,40)}${tx(1420,480,'বাংলাদেশি প্রস্তুতকারক ও রপ্তানিকারকদের',34,'#fff',800)}${lat(1290,550,'B2B',40,C.y,800)}${tx(1350,550,'মার্কেটপ্লেস',40,'#e3f8d3',800,'start')}</g>
 <g data-k="xb_by">${card(1020,640,800,320,'#fff',40)}${person(1150,680,.6,'g','xb_bp')}${bub(1520,790,460,'Certificates verified ✓',C.b,'#fff',28,-1)}${tx(1520,910,'ক্রেতার আস্থা বাড়ে',36,C.g,800)}</g>`,
 upd(q,lt,t,bt){const l=pe(lt,.2,.8);T(q('xb_logo'),{s:L(.5,1,eo(l))+(l>=1?Math.sin(t*1.5)*.012:0),o:cl(l*2)});popG(q('xb_pg'),lt,bt(1)-.6,t,1,40,0,.5);for(let i=0;i<3;i++){const p=pe(lt,bt(1)+i*.35,.4);T(q('xb_c'+i),{x:L(-50,0,eo(p)),o:cl(p*2)})}
  popG(q('xb_tag'),lt,bt(2)-.2,t,2,30,0,.5);popG(q('xb_by'),lt,bt(3)-.2,t,3,30,2,.5)}});

// 19 — get advice
K.er_advice=()=>({svg:`${BG}
 <g data-k="v_a">${card(140,200,760,640,'#fff',44)}${bank(520,500,1.4,C.bd)}${lat(520,690,'CCI&E',50,C.bd,800)}${tx(520,760,'আমদানি ও রপ্তানি প্রধান নিয়ন্ত্রকের দপ্তর',28,C.mute,800)}</g>
 <g data-k="v_b">${card(1020,200,760,640,'#fff',44)}${bank(1400,500,1.4,C.g)}${lat(1400,690,'AD Bank',50,C.g,800)}${tx(1400,760,'অনুমোদিত ডিলার ব্যাংক',30,C.mute,800)}</g>
 ${kw('v_w',960,960,'নির্দিষ্ট লেনদেনের আগে পরামর্শ নিন',52,'#fff',C.gd)}`,
 upd(q,lt,t,bt){popG(q('v_a'),lt,Math.min(bt(0)-.3,.2),t,0,40,2,.5);popG(q('v_b'),lt,bt(1)-.3,t,1,40,2,.5);kwU(q,'v_w',lt,bt(1)+.3,t)}});

// 20 — CTA
K.er_cta=()=>({svg:`${BG}
 <g data-k="ct_who">${card(100,200,700,260,'#fff',44)}${bdflag(150,270,150)}${tx(560,310,'প্রস্তুতকারক বা',44,C.ink,800)}${tx(560,390,'রপ্তানিকারক?',56,C.g,800)}</g>
 <g data-k="ct_gl">${icon('globe',450,760,300,C.t,4)}${[0,1,2,3].map(i=>`<g data-k="ct_f${i}"><circle cx="0" cy="0" r="40" fill="#fff"/>${icon(['shirt','bag','box','shoe'][i],0,0,50,[C.b,C.g,C.p,C.o][i],7)}</g>`).join('')}</g>
 <g data-k="ct_lg"><image href="__LOGO__" x="1010" y="220" width="760" height="220" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="ct_bt">${card(1040,520,700,140,C.g,70)}${lat(1390,612,'Exportain.com',62,'#fff',800)}</g>
 <g data-k="ct_hd">${tap('ct_rp')}</g>
 ${kw('ct_u',1390,800,'আজই ভিজিট করুন',60,'#fff',C.o)}`,
 upd(q,lt,t,bt){popG(q('ct_who'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.5);popG(q('ct_gl'),lt,bt(1)-.4,t,1,30,0,.5);for(let i=0;i<4;i++){const p=pe(lt,bt(1)+i*.15,.5),a=i*1.57+t*.5;T(q('ct_f'+i),{x:450+Math.cos(a)*230,y:760+Math.sin(a)*200,s:L(.2,1,p),o:cl(p*2)})}
  const l=pe(lt,.4,.6);T(q('ct_lg'),{s:L(.6,1,eb(l)),o:cl(l*3)});popG(q('ct_bt'),lt,bt(2)-.4,t,2,30,0,.45);if(lt>bt(2)+.3)T(q('ct_bt'),{s:1+.04*Math.sin(t*7),o:1});
  const h=cl((lt-bt(2))/.5);T(q('ct_hd'),{x:L(1860,1700,eo(h)),y:L(760,640,eo(h)),o:cl(h*3)});const rp=((lt-bt(2))%1+1)%1;T(q('ct_rp'),{s:1+rp*1.8,o:h>=1?1-rp:0});kwU(q,'ct_u',lt,bt(2),t)}});
