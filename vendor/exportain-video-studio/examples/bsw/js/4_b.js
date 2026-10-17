// ===================== BSW 16:9 — scenes 10–18 =====================
// 10 — less cost, less face-to-face
K.bs_cost=()=>{const R=[['কম খরচ','coin'],['কম যাতায়াত','route'],['কম মুখোমুখি লেনদেন','face'],['স্বচ্ছতা বাড়ে','glass']];return{svg:`${BG}${rd('c_')}
 ${R.map((r,i)=>`<g data-k="c_r${i}">${card(100+i*440,300,410,560,'#fff',40)}<circle cx="${305+i*440}" cy="500" r="120" fill="${[C.o,C.r,C.b,C.g][i]}" opacity=".15"/>${r[1]=='coin'?coin(305+i*440,500,80):r[1]=='route'?`${icon('truck',305+i*440,500,130,C.r,7)}${slash(305+i*440,500,100)}`:r[1]=='face'?`${person(250+i*440,420,.35,'s','c_fp'+i)}${person(360+i*440,420,.35,'n','c_fq'+i)}${slash(305+i*440,500,100)}`:`${shield(305+i*440,500,1.1,C.g,'✓')}`}${tx(305+i*440,720,r[0],r[0].length>12?32:42,C.ink,800)}</g>`).join('')}`,
 upd(q,lt,t,bt){rdU(q,'c_',lt,t,4);for(let i=0;i<4;i++)popG(q('c_r'+i),lt,bt(i)-.25,t,i,40,3,.45)}}};

// 11 — 5 lakh milestone
K.bs_mile=()=>({svg:`${BG}${rd('k_')}
 <g data-k="k_c">${card(360,220,1200,640,'#fff',50)}${tx(960,360,'সেপ্টেম্বর ২০২৫',48,C.mute,800)}<g data-k="k_n">${tx(960,600,'৫,০০,০০০',200,C.gd,800)}</g>${tx(960,760,'সনদ ইস্যুর মাইলফলক',52,C.ink,800)}</g>
 <g data-k="k_f">${Array.from({length:16},(_,i)=>`<rect data-k="k_f${i}" x="953" y="533" width="14" height="${i%2?14:22}" rx="3" fill="${[C.y,C.g2,C.o,C.t,C.b,C.r][i%6]}"/>`).join('')}</g>`,
 upd(q,lt,t,bt){rdU(q,'k_',lt,t,4);popG(q('k_c'),lt,Math.min(bt(0)-.2,.15),t,0,40,0,.5);popIn(q('k_n'),pe(lt,bt(1)-.2,.5),t,1,30,0);const p=cl((lt-bt(1))/1.4);for(let i=0;i<16;i++){const a=i/16*6.283;T(q('k_f'+i),{x:Math.cos(a)*L(0,520,eo(p)),y:Math.sin(a)*L(0,300,eo(p))+p*p*120,r:p*360,o:p>0?1-p*p:0})}}});

// 12 — point 5: register with BIN
K.bs_reg=()=>({svg:`${BG}${rd('g_')}${ttl2('g_','৫','প্রথম কাজ: নিবন্ধন',C.gd)}
 <g data-k="g_b">${browser(100,330,960,660,'bswnbr.gov.bd',C.b)}${lat(580,480,'Bangladesh Single Window',44,C.b,800)}<g data-k="g_btn">${card(380,560,400,100,C.g,50)}${lat(580,623,'Create Account',36,'#fff',800)}</g>${field(200,740,760,'Business Identification Number (BIN)',C.g,'g_fd')}</g>
 <g data-k="g_hd">${tap('g_rp')}</g>
 <g data-k="g_bin">${card(1140,380,680,420,C.gd,44)}${lat(1480,500,'BIN',110,'#fff',800)}${tx(1480,610,'ব্যবসায় শনাক্তকরণ নম্বর',40,'#d9f5c4',800)}${lat(1480,700,'000123456-0101',40,C.y,800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'g_',lt,t,5);ttlU(q,'g_',lt,t);popG(q('g_b'),lt,bt(1)-.3,t,0,40,0,.5);const h=cl((lt-bt(2)+.4)/.5);T(q('g_hd'),{x:L(900,700,eo(h)),y:L(760,640,eo(h)),o:cl(h*3)*(lt<bt(2)+1?1:0)});const rp=((lt-bt(2))%1+1)%1;T(q('g_rp'),{s:1+rp*1.8,o:lt>bt(2)?1-rp:0});
  T(q('g_btn'),{s:lt>bt(2)&&lt<bt(2)+.25?.94:1,o:1});popG(q('g_bin'),lt,bt(3)-.4,t,1,40,2,.5);fillTo(q('g_fd'),lt,bt(3),760,.8)}});

// 13 — steps: OTP, company, owner, password
K.bs_steps=()=>{const S=[['OTP','ওটিপি · বিআইএনের মোবাইলে','phone',C.b],['Company info','কোম্পানির তথ্য মিলিয়ে নিন','bld',C.t],['Owner info','মালিকের তথ্য','star',C.o],['Password','ইমেইল লিংকে পাসওয়ার্ড','lock',C.g]];return{svg:`${BG}${rd('p_')}
 ${S.map((s,i)=>`<g data-k="p_s${i}">${card(100+i*440,300,410,620,'#fff',40)}<circle cx="${305+i*440}" cy="430" r="44" fill="${s[3]}"/>${tx(305+i*440,448,BN(i+1),48,'#fff',800)}${icon(s[2],305+i*440,600,120,s[3],7)}${lat(305+i*440,760,s[0],38,s[3],800)}${tx(305+i*440,830,s[1],s[1].length>18?26:30,C.ink,800)}</g>${i<3?`<path d="M${515+i*440} 600 H${535+i*440}" stroke="${C.gd}" stroke-width="8"/>`:''}`).join('')}`,
 upd(q,lt,t,bt){rdU(q,'p_',lt,t,5);for(let i=0;i<4;i++)popG(q('p_s'+i),lt,Math.min(bt(i)-.3,.3+i*.5),t,i,40,3,.45)}}};

// 14 — keep VAT/BIN and mobile updated
K.bs_tip=()=>({svg:`${BG}${rd('v_')}
 <g data-k="v_a">${card(140,220,760,640,'#fff',44)}${docPage(310,280,420,420,'VAT / BIN',C.o,6)}${tx(520,780,'ভ্যাট নিবন্ধন হালনাগাদ',42,C.ink,800)}${check(780,300,40,C.g)}</g>
 <g data-k="v_b">${card(1020,220,760,640,'#fff',44)}${phone(1240,270,320,520)}<rect x="1258" y="400" width="284" height="120" rx="16" fill="#e9f8ec"/>${lat(1400,470,'+880 1•••',30,C.g,800)}${tx(1400,820,'মোবাইল নম্বর চালু রাখুন',40,C.ink,800)}${check(1660,300,40,C.g)}</g>`,
 upd(q,lt,t,bt){rdU(q,'v_',lt,t,5);popG(q('v_a'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.5);popG(q('v_b'),lt,bt(1)-.3,t,1,40,2,.5)}});

// 15 — Sumon now
K.bs_story2=()=>({svg:`${BG}
 <g data-k="z_p">${card(100,170,560,780,'#fff',44)}${person(380,230,1,'s','z_sp')}${tx(380,560,'সুমন',52,C.ink,800)}${laptop(380,770,1.5,C.b)}</g>
 <g data-k="z_c">${card(740,170,1080,380,'#e9f8ec',44)}${docPage(800,200,240,320,'DOF',C.t,4)}${check(1010,230,36,C.g)}${tx(1120,330,'মৎস্য অধিদপ্তরের সনদ',44,C.ink,800,'start')}${tx(1120,410,'অনলাইনেই',56,C.g,800,'start')}</g>
 <g data-k="z_s">${card(740,590,1080,360,'#eef6ff',44)}${shipA(1100,800,1.3)}${slash(1560,770,90)}${icon('truck',1560,770,110,C.r,7)}${tx(1560,920,'অফিসে দৌড় নেই',34,C.ink,800)}</g>`,
 upd(q,lt,t,bt){popG(q('z_p'),lt,.15,t,0,40,2,.5);popG(q('z_c'),lt,bt(0)-.4,t,1,30,2,.5);popG(q('z_s'),lt,bt(1)-.3,t,2,30,0,.5)}});

// 16 — Exportain
K.bs_brand=()=>({svg:`${BG}
 <g data-k="xb_logo"><image href="__LOGO__" x="560" y="130" width="800" height="230" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="xb_pg">${card(100,400,860,560,'#fff',40)}<rect x="100" y="400" width="860" height="86" rx="40" fill="${C.g}"/><rect x="100" y="446" width="860" height="40" fill="${C.g}"/>${lat(140,456,'Company page · Sumon Sea Foods',30,'#fff',800,'start')}${shrimp2(210,600,.8)}${lat(310,600,'Certificates',36,C.ink,800,'start')}
  ${[['DOF health certificate','Verified'],['ERC','Verified'],['EPB Enrolment','Verified until 2031']].map((c,i)=>`<g data-k="xb_c${i}"><rect x="140" y="${680+i*88}" width="780" height="74" rx="16" fill="#f1f8f1"/>${lat(170,726+i*88,c[0],28,C.ink,800,'start')}${lat(890,726+i*88,c[1],22,C.g,800,'end')}</g>`).join('')}</g>
 <g data-k="xb_tag">${card(1020,400,800,200,C.gd,40)}${tx(1420,480,'বাংলাদেশি প্রস্তুতকারক ও রপ্তানিকারকদের',34,'#fff',800)}${lat(1290,550,'B2B',40,C.y,800)}${tx(1350,550,'মার্কেটপ্লেস',40,'#e3f8d3',800,'start')}</g>
 <g data-k="xb_by">${card(1020,640,800,320,'#fff',40)}${person(1150,680,.6,'g','xb_bp')}${bub(1520,790,460,'Certificates verified ✓',C.b,'#fff',28,-1)}${tx(1520,910,'বিদেশি ক্রেতার আস্থা বাড়ে',36,C.g,800)}</g>`,
 upd(q,lt,t,bt){const l=pe(lt,.2,.8);T(q('xb_logo'),{s:L(.5,1,eo(l))+(l>=1?Math.sin(t*1.5)*.012:0),o:cl(l*2)});popG(q('xb_pg'),lt,bt(1)-.6,t,1,40,0,.5);for(let i=0;i<3;i++){const p=pe(lt,bt(1)+i*.35,.4);T(q('xb_c'+i),{x:L(-50,0,eo(p)),o:cl(p*2)})}
  popG(q('xb_tag'),lt,bt(2)-.2,t,2,30,0,.5);popG(q('xb_by'),lt,bt(3)-.2,t,3,30,2,.5)}});

// 17 — advice
K.bs_advice=()=>({svg:`${BG}
 <g data-k="v2_a">${card(140,200,500,640,'#fff',44)}${bank(390,480,1.1,C.bd)}${lat(390,660,'Customs',44,C.bd,800)}${tx(390,720,'কাস্টমস',34,C.mute,800)}</g>
 <g data-k="v2_c">${card(710,200,500,640,'#fff',44)}${icon('bld',960,450,180,C.t,7)}${tx(960,660,'সংশ্লিষ্ট সংস্থা',40,C.t,800)}</g>
 <g data-k="v2_b">${card(1280,200,500,640,'#fff',44)}${bank(1530,480,1.1,C.g)}${lat(1530,660,'AD Bank',44,C.g,800)}${tx(1530,720,'অনুমোদিত ডিলার ব্যাংক',28,C.mute,800)}</g>
 ${kw('v2_w',960,960,'নির্দিষ্ট লেনদেনের আগে পরামর্শ নিন',52,'#fff',C.gd)}`,
 upd(q,lt,t,bt){popG(q('v2_a'),lt,Math.min(bt(0)-.3,.2),t,0,40,2,.5);popG(q('v2_c'),lt,bt(0)+.4,t,1,40,2,.5);popG(q('v2_b'),lt,bt(1)-.3,t,2,40,2,.5);kwU(q,'v2_w',lt,bt(1)+.3,t)}});

// 18 — CTA
K.bs_cta=()=>({svg:`${BG}
 <g data-k="ct_who">${card(100,200,700,260,'#fff',44)}${bdflag(150,270,150)}${tx(560,310,'প্রস্তুতকারক বা',44,C.ink,800)}${tx(560,390,'রপ্তানিকারক?',56,C.g,800)}</g>
 <g data-k="ct_gl">${icon('globe',450,760,300,C.t,4)}${[0,1,2,3].map(i=>`<g data-k="ct_f${i}"><circle cx="0" cy="0" r="40" fill="#fff"/>${icon(['shirt','bag','box','shoe'][i],0,0,50,[C.b,C.g,C.p,C.o][i],7)}</g>`).join('')}</g>
 <g data-k="ct_lg"><image href="__LOGO__" x="1010" y="220" width="760" height="220" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="ct_bt">${card(1040,520,700,140,C.g,70)}${lat(1390,612,'Exportain.com',62,'#fff',800)}</g>
 <g data-k="ct_hd">${tap('ct_rp')}</g>
 ${kw('ct_u',1390,800,'আজই ভিজিট করুন',60,'#fff',C.o)}`,
 upd(q,lt,t,bt){popG(q('ct_who'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.5);popG(q('ct_gl'),lt,bt(1)-.4,t,1,30,0,.5);for(let i=0;i<4;i++){const p=pe(lt,bt(1)+i*.15,.5),a=i*1.57+t*.5;T(q('ct_f'+i),{x:450+Math.cos(a)*230,y:760+Math.sin(a)*200,s:L(.2,1,p),o:cl(p*2)})}
  const l=pe(lt,.4,.6);T(q('ct_lg'),{s:L(.6,1,eb(l)),o:cl(l*3)});popG(q('ct_bt'),lt,bt(2)-.4,t,2,30,0,.45);if(lt>bt(2)+.3)T(q('ct_bt'),{s:1+.04*Math.sin(t*7),o:1});
  const h=cl((lt-bt(2))/.5);T(q('ct_hd'),{x:L(1860,1700,eo(h)),y:L(760,640,eo(h)),o:cl(h*3)});const rp=((lt-bt(2))%1+1)%1;T(q('ct_rp'),{s:1+rp*1.8,o:h>=1?1-rp:0});kwU(q,'ct_u',lt,bt(2),t)}});
