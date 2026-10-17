// ===================== Dalal + Docs 16:9 — scenes 14–24 =====================
// 14 bridge (dark)
K.dl_bridge=()=>({svg:`${BG}<rect width="1920" height="1080" fill="url(#e_forest)"/>
 <g data-k="g_w">${woman2(480,470,1.3)}</g>
 ${[0,1,2,3,4].map(i=>`<g data-k="g_d${i}">${docPage(-90,-110,180,220,['ERC','e-TIN','VAT','EPB','Bank'][i],[C.o,C.gd,C.t,C.b,C.p][i],3)}</g>`).join('')}
 <g data-k="g_t">${card(900,330,920,190,C.p,50)}${tx(1360,450,'ভাগ খ',80,'#fff',800)}</g>
 ${kw('g_k',1360,680,'কাগজ গোছানোর সিস্টেম',64,C.gd,'#fff')}`,
 upd(q,lt,t,bt){popG(q('g_w'),lt,.1,t,0,40,2,.45);for(let i=0;i<5;i++){const p=pe(lt,bt(0)-.6+i*.18,.8),a=i*1.25;T(q('g_d'+i),{x:L(480+Math.cos(a)*900,330+i*80,eo(p)),y:L(470+Math.sin(a)*700,760-i*14,eo(p)),r:L(160,-8+i*4,eo(p)),s:L(1.2,.6,eo(p)),o:cl(p*3)})}popG(q('g_t'),lt,bt(1)-.2,t,1,40,2,.5);kwU(q,'g_k',lt,bt(2)-.1,t)}});

// 15 B1 folder
K.dl_folder=()=>{const F=['Trade License','e-TIN','VAT','ERC','EPB Enrolment','Bank'];return{svg:`${BG}${rd('f_','B')}${ttl2('f_','১','সব PDF এক ফোল্ডারে',C.p)}
 <g data-k="f_sc">${card(100,330,520,640,'#fff',44)}${scanner(360,520,1.2)}<g data-k="f_pg">${docPage(270,560,180,220,'',C.mute,3)}</g>${tx(360,900,'স্ক্যান → PDF',44,C.ink,800)}</g>
 <g data-k="f_fd">${card(700,330,1120,640,'#fff',44)}<g transform="translate(1260 470) scale(1.4)">${folder(-80,-56,C.o)}</g>${lat(1260,600,'Export Documents',38,C.ink,800)}
  ${F.map((f,i)=>`<g data-k="f_c${i}">${pdfF(760+(i%3)*350,660+Math.floor(i/3)*110,f)}</g>`).join('')}
  <g data-k="f_ok">${pill(1260,920,'সব এক জায়গায়',C.g,34)}</g></g>`,
 upd(q,lt,t,bt){rdU(q,'f_',lt,t,1);ttlU(q,'f_',lt,t);popG(q('f_sc'),lt,bt(0)-.4,t,0,40,2,.45);const sp=((lt-bt(0))%1.6+1.6)%1.6/1.6;T(q('f_pg'),{y:lt>bt(0)?L(-60,60,sp):0,o:lt>bt(0)?1-sp*.6:1});popG(q('f_fd'),lt,bt(1)-.3,t,1,30,0,.45);
  const B=[bt(2),bt(2)+.4,bt(3)-.5,bt(3),bt(3)+.5,bt(4)];for(let i=0;i<6;i++){const p=pe(lt,B[i]-.1,.4);T(q('f_c'+i),{x:L(-300,0,eo(p)),y:L(-120,0,eo(p)),o:cl(p*3)})}popG(q('f_ok'),lt,bt(5)-.1,t,2,20,0,.4)}}};

// 16 B1 naming
K.dl_name=()=>{const O=['scan001.pdf','IMG_2231.jpg','final final (2).pdf'],N=['TradeLicense_2027-06-30.pdf','ERC_2027-06-30.pdf','EPB_2030-12-31.pdf'];return{svg:`${BG}${rd('n_','B')}
 <g data-k="n_bx">${card(100,190,1180,800,'#fff',44)}${tx(160,270,'ফাইলের নাম',44,C.ink,800,'start')}${pill(1110,255,'উদাহরণ',C.mute,28)}
  ${[0,1,2].map(i=>`<g><rect x="150" y="${320+i*170}" width="1080" height="140" rx="22" fill="#f8fafc"/><rect x="170" y="${345+i*170}" width="70" height="90" rx="12" fill="${C.r}"/>${lat(205,400+i*170,'PDF',20,'#fff',800)}<g data-k="n_o${i}">${lat(270,403+i*170,O[i],38,C.mute,700,'start')}</g><g data-k="n_n${i}">${lat(270,403+i*170,N[i],38,C.gd,800,'start')}</g></g>`).join('')}
  <g data-k="n_rule">${card(150,830,1080,130,'#eef6ff',24)}${tx(190,910,'কাগজের নাম',36,C.b,800,'start')}${lat(450,908,'_',40,C.ink,800)}${tx(480,910,'মেয়াদ শেষের তারিখ',36,C.o,800,'start')}${lat(900,910,'.pdf',36,C.mute,800,'start')}</g></g>
 <g data-k="n_cl">${card(1360,190,460,800,C.gd,44)}<circle cx="1590" cy="520" r="150" fill="#fff"/><g data-k="n_hd"><rect x="-7" y="-120" width="14" height="120" rx="7" fill="${C.r}"/></g><circle cx="1590" cy="520" r="14" fill="${C.ink}"/>${tx(1590,800,'খুঁজতে লাগে',40,'#d9f5c4',800)}${tx(1590,880,'কয়েক সেকেন্ড',52,'#fff',800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'n_',lt,t,1);popG(q('n_bx'),lt,.15,t,0,30,0,.45);for(let i=0;i<3;i++){const p=pe(lt,bt(0)+i*.3,.4);T(q('n_o'+i),{o:1-p,x:-40*p});T(q('n_n'+i),{o:p,x:L(40,0,eo(p))})}const r=q('n_rule');popIn(r,pe(lt,bt(1)-.2,.4),t,1,20,0);if(lt>bt(2))T(r,{s:1+.012*Math.sin(t*5),o:1});
  popG(q('n_cl'),lt,bt(3)-.4,t,2,40,2,.45);T(q('n_hd'),{x:1590,y:520,r:t*360,o:1})}}};

// 17 B2 same name
K.dl_same=()=>({svg:`${BG}${rd('m_','B')}${ttl2('m_','২','নাম, ঠিকানা, বানান এক',C.p)}
 <g data-k="m_a">${card(100,320,640,520,'#fff',36)}<rect x="100" y="320" width="640" height="90" rx="36" fill="${C.b}"/><rect x="100" y="370" width="640" height="40" fill="${C.b}"/>${lat(420,380,'Trade License',38,'#fff',800)}${tx(140,480,'নাম',28,C.mute,800,'start')}<g data-k="m_an"><rect x="140" y="500" width="560" height="80" rx="16" fill="#e9f8ec"/>${lat(160,553,'Rumana Handicrafts',36,C.ink,800,'start')}</g>${tx(140,640,'ঠিকানা',28,C.mute,800,'start')}<rect x="140" y="660" width="560" height="80" rx="16" fill="#f1f5f9"/>${lat(160,713,'Zindabazar, Sylhet',32,C.ink,700,'start')}</g>
 <g data-k="m_b">${card(820,320,640,520,'#fff',36)}<rect x="820" y="320" width="640" height="90" rx="36" fill="${C.g}"/><rect x="820" y="370" width="640" height="40" fill="${C.g}"/>${lat(1140,380,'ERC',38,'#fff',800)}${tx(860,480,'নাম',28,C.mute,800,'start')}<g data-k="m_bn"><rect data-k="m_bnr" x="860" y="500" width="560" height="80" rx="16" fill="#fff4f2" stroke="${C.r}" stroke-width="5"/>${lat(880,553,'Rumana Handicraft',36,C.r,800,'start')}</g>${tx(860,640,'ঠিকানা',28,C.mute,800,'start')}<rect x="860" y="660" width="560" height="80" rx="16" fill="#f1f5f9"/>${lat(880,713,'Zindabazar, Sylhet',32,C.ink,700,'start')}</g>
 <g data-k="m_x">${card(1520,320,300,520,'#fff4f2',36)}${icon('bld',1670,480,110,C.r,7)}${icon('lock',1670,640,80,C.r,7)}${tx(1670,770,'কাজ আটকে',34,C.r,800)}</g>
 <g data-k="m_ok">${pill(780,920,'এক অক্ষরের অমিলও ঝামেলা',C.r,36)}</g>`,
 upd(q,lt,t,bt){rdU(q,'m_',lt,t,2);ttlU(q,'m_',lt,t);popG(q('m_a'),lt,bt(0)-.2,t,0,40,2,.45);popG(q('m_b'),lt,bt(1)-.2,t,1,40,2,.45);if(lt>bt(2)&&lt<bt(3))T(q('m_an'),{s:1.04,o:1});const p=pe(lt,bt(3)-.1,.3);T(q('m_bn'),{x:p>0&&p<3?Math.sin(t*30)*cl(bt(3)+.8-lt)*8:0,o:1});const r=q('m_bnr');if(r)r.setAttribute('stroke-width',lt>bt(3)-.1?5:0);
  popG(q('m_x'),lt,bt(4)-.2,t,2,40,2,.45);popG(q('m_ok'),lt,bt(4)+.4,t,3,20,0,.4)}});

// 18 B3 expiry list
K.dl_expiry=()=>{const R=[['Trade License','30 Jun 2027','1 Jun 2027'],['ERC','30 Jun 2027','1 Jun 2027'],['EPB Enrolment','31 Dec 2030','1 Dec 2030']];return{svg:`${BG}${rd('e_','B')}${ttl2('e_','৩','মেয়াদের তালিকা',C.p)}
 <g data-k="e_s">${card(100,320,1120,640,'#fff',36)}<rect x="100" y="320" width="1120" height="90" rx="36" fill="${C.g}"/><rect x="100" y="370" width="1120" height="40" fill="${C.g}"/>${lat(140,380,'Licence_Expiry.xlsx',34,'#fff',800,'start')}${pill(1110,365,'উদাহরণ',C.gd,26)}
  ${['কাগজ','মেয়াদ শেষ','রিমাইন্ডার'].map((h,i)=>`<rect x="${130+[0,400,760][i]}" y="430" width="${[380,340,340][i]}" height="80" fill="#e9f8ec"/>${tx(150+[0,400,760][i],482,h,32,C.gd,800,'start')}`).join('')}
  ${R.map((r,j)=>`<g data-k="e_r${j}">${r.map((c,i)=>`<rect x="${130+[0,400,760][i]}" y="${520+j*130}" width="${[380,340,340][i]}" height="120" fill="${j%2?'#f8fafc':'#fff'}" stroke="#e2e8f0"/>${lat(150+[0,400,760][i],592+j*130,c,32,i==2?C.o:C.ink,800,'start')}`).join('')}</g>`).join('')}</g>
 <g data-k="e_c">${cal(1300,320,520,'১','মাস আগে',C.o)}</g>
 <g data-k="e_bl"><circle cx="1800" cy="330" r="50" fill="${C.r}"/>${tx(1800,352,'!',60,'#fff',800)}</g>
 ${kw('e_k',1560,1000,'এটুকুই যথেষ্ট',48,'#fff',C.g)}`,
 upd(q,lt,t,bt){rdU(q,'e_',lt,t,3);ttlU(q,'e_',lt,t);popG(q('e_s'),lt,bt(1)-.3,t,0,30,0,.45);for(let j=0;j<3;j++)popIn(q('e_r'+j),pe(lt,bt(2)-.2+j*.3,.3),t,j,20,0);popG(q('e_c'),lt,bt(3)-.3,t,1,40,2,.45);const b=pe(lt,bt(3)+.3,.3);T(q('e_bl'),{s:L(.2,1,eb(b)),r:b>=1?Math.sin(t*14)*10:0,o:cl(b*3)});kwU(q,'e_k',lt,bt(4)-.1,t)}}};

// 19 B4 cloud backup
K.dl_cloud=()=>({svg:`${BG}${rd('k_','B')}${ttl2('k_','৪','ক্লাউড ব্যাকআপ',C.p)}
 <g data-k="k_cl">${cloudS(1000,470,1.3)}${lat(1000,500,'Google Drive',44,C.b,800)}</g>
 <g data-k="k_fd"><g transform="translate(1000 820) scale(1.3)">${folder(-80,-56,C.o)}</g></g>
 <g data-k="k_ar"><path d="M1000 720 V600" stroke="${C.b}" stroke-width="12" stroke-dasharray="20 14"/><path d="M970 630 L1000 590 L1030 630" stroke="${C.b}" stroke-width="12" fill="none"/></g>
 <g data-k="k_ph">${card(100,330,460,330,'#fff4f2',36)}<g transform="translate(330 470) rotate(-10) scale(.8)"><rect x="-70" y="-120" width="140" height="240" rx="20" fill="#0f172a"/><path d="M-50 -90 L10 0 L-30 40 L40 100" stroke="#fff" stroke-width="6" fill="none"/></g>${tx(330,630,'ফোন হারালেও',32,C.ink,800)}</g>
 <g data-k="k_lp">${card(100,690,460,300,'#fff4f2',36)}${laptop(330,830,1.1,C.mute)}<path d="M300 780 L330 810 L310 840" stroke="${C.r}" stroke-width="7" fill="none"/>${tx(330,965,'কম্পিউটার নষ্ট হলেও',30,C.ink,800)}</g>
 <g data-k="k_ok">${card(1440,400,380,460,C.gd,40)}${shield(1630,580,1.4,C.g2,'✓')}${tx(1630,780,'কাগজ নিরাপদ',40,'#fff',800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'k_',lt,t,4);ttlU(q,'k_',lt,t);popG(q('k_cl'),lt,bt(1)-.3,t,0,40,0,.45);popG(q('k_fd'),lt,bt(0)+.3,t,1,30,0,.45);const a=q('k_ar');if(a){a.querySelector('path').setAttribute('stroke-dashoffset',(t*60).toFixed(0));T(a,{o:lt>bt(2)-.1?1:0})}
  popG(q('k_ph'),lt,bt(3)-.2,t,2,40,2,.45);popG(q('k_lp'),lt,bt(4)-.2,t,3,40,2,.45);popG(q('k_ok'),lt,bt(5)-.2,t,4,40,2,.45);if(lt>bt(5)+.5)T(q('k_ok'),{y:Math.sin(t*3)*6,o:1})}});

// 20 B5 send instantly
K.dl_send=()=>({svg:`${BG}${rd('s_','B')}${ttl2('s_','৫','চাইলেই সাথে সাথে',C.p)}
 <g data-k="s_by">${card(100,330,620,300,'#fff',36)}${icon('mail',190,420,70,C.b,6)}${lat(250,410,'Buyer',36,C.b,800,'start')}${lat(150,500,'Send ERC + Trade License?',30,C.ink,800,'start')}</g>
 <g data-k="s_bk">${card(100,670,620,300,'#fff',36)}${icon('bld',190,760,70,C.g,6)}${lat(250,750,'Bank',36,C.g,800,'start')}${lat(150,840,'Need VAT registration copy',30,C.ink,800,'start')}</g>
 <g data-k="s_sr">${card(800,330,480,640,'#fff4f2',36)}<g data-k="s_mg">${mag(1040,560,1.4,C.r)}</g>${slash(1040,580,130)}${tx(1040,820,'খোঁজাখুঁজি নয়',40,C.r,800)}</g>
 <g data-k="s_pf">${pdfF(0,0,'ERC_2027-06-30',C.r,300)}</g>
 <g data-k="s_ok">${card(1360,330,460,640,C.gd,36)}${icon('check',1590,520,140,'#fff',8)}${tx(1590,720,'পাঠানো হলো',46,'#fff',800)}${lat(1590,800,'"Thanks! Quick."',30,'#d9f5c4',800)}</g>
 ${kw('s_k',960,1030,'দ্রুত উত্তর = আস্থা',48,'#fff',C.g)}`,
 upd(q,lt,t,bt){rdU(q,'s_',lt,t,5);ttlU(q,'s_',lt,t);popG(q('s_by'),lt,bt(1)-.3,t,0,30,0,.45);popG(q('s_bk'),lt,bt(1)+.2,t,1,30,0,.45);popG(q('s_sr'),lt,bt(2)-.2,t,2,40,2,.45);T(q('s_mg'),{x:Math.sin(t*2)*20,o:1});
  const p=pe(lt,bt(3),.7);T(q('s_pf'),{x:L(800,1440,eo(p)),y:L(1000,880,eo(p))-Math.sin(p*3.14)*200,s:L(.8,1,p),o:p>0&&p<1?1:0});popG(q('s_ok'),lt,bt(3)+.6,t,3,40,2,.45);kwU(q,'s_k',lt,bt(4)-.1,t)}});

// 21 story end
K.dl_story2=()=>({svg:`${BG}
 <g data-k="z_p">${card(100,170,560,800,'#fff',44)}${woman2(380,330,1.2)}${tx(380,640,'রুমানা',52,C.ink,800)}${laptop(380,830,1.4,C.b)}</g>
 <g data-k="z_f">${card(740,170,520,460,'#fff',40)}<g transform="translate(1000 330) scale(1.2)">${folder(-80,-56,C.o)}</g>${tx(1000,480,'রসিদ ও সনদ',40,C.ink,800)}${[0,1,2].map(i=>`<g data-k="z_r${i}"><rect x="${820+i*130}" y="530" width="110" height="60" rx="12" fill="#e9f8ec"/>${lat(875+i*130,570,'৳ ✓',26,C.g,800)}</g>`).join('')}</g>
 <g data-k="z_e">${card(1300,170,520,460,'#fff',40)}<rect x="1300" y="170" width="520" height="80" rx="40" fill="${C.b}"/><rect x="1300" y="210" width="520" height="40" fill="${C.b}"/>${lat(1340,225,'Buyer',30,'#fff',800,'start')}${lat(1340,330,'Can you share your',30,C.ink,800,'start')}${lat(1340,380,'ERC copy?',36,C.ink,800,'start')}<g data-k="z_at">${pdfF(1340,450,'ERC.pdf',C.r,260)}${check(1720,485,34,C.g)}</g></g>
 <g data-k="z_t">${card(740,670,1080,300,C.gd,40)}<circle cx="900" cy="820" r="90" fill="#fff"/><g data-k="z_h"><rect x="-6" y="-70" width="12" height="70" rx="6" fill="${C.r}"/></g>${tx(1300,800,'দুই মিনিটে পাঠানো',56,'#fff',800)}${tx(1300,880,'দালাল ছাড়া, রসিদসহ',38,'#d9f5c4',800)}</g>`,
 upd(q,lt,t,bt){popG(q('z_p'),lt,.1,t,0,40,2,.45);if(lt>.8)T(q('z_p'),{y:Math.sin(lt*2)*8,o:1});popG(q('z_f'),lt,bt(1)-.4,t,1,30,0,.45);for(let i=0;i<3;i++)popIn(q('z_r'+i),pe(lt,bt(1)+i*.25,.3),t,i,20,0);popG(q('z_e'),lt,bt(2)-.3,t,2,30,0,.45);popIn(q('z_at'),pe(lt,bt(3)-.2,.4),t,3,20,0);popG(q('z_t'),lt,bt(3),t,3,30,0,.45);T(q('z_h'),{x:900,y:820,r:t*240,o:1})}});

// 22 Exportain
K.dl_brand=()=>({svg:`${BG}
 <g data-k="xb_logo"><image href="__LOGO__" x="560" y="130" width="800" height="230" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="xb_pg">${card(100,400,860,560,'#fff',40)}<rect x="100" y="400" width="860" height="86" rx="40" fill="${C.g}"/><rect x="100" y="446" width="860" height="40" fill="${C.g}"/>${lat(140,456,'Company page · Rumana Handicrafts',30,'#fff',800,'start')}${mat(150,530,140,90)}${lat(320,590,'Certificates',36,C.ink,800,'start')}
  ${[['Trade License','Verified'],['ERC','Verified'],['EPB Enrolment','Verified']].map((c,i)=>`<g data-k="xb_c${i}"><rect x="140" y="${680+i*88}" width="780" height="74" rx="16" fill="#f1f8f1"/>${lat(170,726+i*88,c[0],28,C.ink,800,'start')}${lat(890,726+i*88,c[1],22,C.g,800,'end')}</g>`).join('')}</g>
 <g data-k="xb_tag">${card(1020,400,800,200,C.gd,40)}${tx(1420,480,'বাংলাদেশি প্রস্তুতকারক ও রপ্তানিকারকদের',34,'#fff',800)}${lat(1290,550,'B2B',40,C.y,800)}${tx(1350,550,'মার্কেটপ্লেস',40,'#e3f8d3',800,'start')}</g>
 <g data-k="xb_by">${card(1020,640,800,320,'#fff',40)}${person(1150,680,.6,'g','xb_bp')}${bub(1520,790,460,'Certificates verified ✓',C.b,'#fff',28,-1)}${tx(1520,910,'বিদেশি ক্রেতার আস্থা বাড়ে',36,C.g,800)}</g>`,
 upd(q,lt,t,bt){const l=pe(lt,.2,.8);T(q('xb_logo'),{s:L(.5,1,eo(l))+(l>=1?Math.sin(t*2.2)*.03:0),y:l>=1?Math.sin(t*1.8)*10:0,o:cl(l*2)});popG(q('xb_tag'),lt,Math.min(bt(1)-.3,1.2),t,1,30,0,.45);popG(q('xb_pg'),lt,bt(2)-.4,t,2,40,0,.5);for(let i=0;i<3;i++){const p=pe(lt,bt(2)+i*.35,.4);T(q('xb_c'+i),{x:L(-50,0,eo(p)),o:cl(p*2)})}popG(q('xb_by'),lt,bt(3)-.3,t,3,30,2,.45)}});

// 23 advice
K.dl_advice=()=>({svg:`${BG}
 ${kw('v_h',960,230,'ফি আর নিয়ম বদলায়',64,'#fff',C.o)}
 <g data-k="v_a">${card(140,320,500,600,'#fff',44)}${icon('bld',390,520,180,C.t,7)}${tx(390,740,'সংশ্লিষ্ট দপ্তর',42,C.t,800)}</g>
 <g data-k="v_b">${card(710,320,500,600,'#fff',44)}${bank(960,560,1.1,C.g)}${lat(960,740,'AD Bank',44,C.g,800)}${tx(960,800,'অনুমোদিত ডিলার ব্যাংক',28,C.mute,800)}</g>
 <g data-k="v_c">${card(1280,320,500,600,'#fff',44)}${person(1530,400,.7,'s','v_cp')}${tx(1530,740,'পেশাদার পরামর্শক',40,C.b,800)}</g>
 ${kw('v_w',960,1010,'নির্দিষ্ট কাজের আগে মিলিয়ে নিন',46,'#fff',C.gd)}`,
 upd(q,lt,t,bt){kwU(q,'v_h',lt,Math.min(bt(0)-.4,.2),t);const VB=[Math.min(bt(1)-.2,1),Math.min(bt(2)-.2,1.8),Math.min(bt(3)-.2,2.6)];['v_a','v_b','v_c'].forEach((k,i)=>{popG(q(k),lt,VB[i],t,i,40,2,.45);if(lt>VB[i]+.5)T(q(k),{y:Math.sin(lt*2+i*1.3)*10,o:1})});['v_a','v_b','v_c'].forEach((k,i)=>{if(lt>bt(1+i)&&lt<bt(1+i)+.6)T(q(k),{s:1.05,o:1})});kwU(q,'v_w',lt,bt(3)+.6,t)}});

// 24 CTA
K.dl_cta=()=>({svg:`${BG}
 <g data-k="ct_who">${card(100,200,700,260,'#fff',44)}${bdflag(150,270,150)}${tx(560,310,'প্রস্তুতকারক বা',44,C.ink,800)}${tx(560,390,'রপ্তানিকারক?',56,C.g,800)}</g>
 <g data-k="ct_gl">${icon('globe',450,760,300,C.t,4)}${[0,1,2,3].map(i=>`<g data-k="ct_f${i}"><circle cx="0" cy="0" r="40" fill="#fff"/>${icon(['shirt','bag','box','shoe'][i],0,0,50,[C.b,C.g,C.p,C.o][i],7)}</g>`).join('')}</g>
 <g data-k="ct_lg"><image href="__LOGO__" x="1010" y="220" width="760" height="220" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="ct_bt">${card(1040,520,700,140,C.g,70)}${lat(1390,612,'Exportain.com',62,'#fff',800)}</g>
 <g data-k="ct_hd">${tap('ct_rp')}</g>
 ${kw('ct_u',1390,800,'আজই ভিজিট করুন',60,'#fff',C.o)}`,
 upd(q,lt,t,bt){popG(q('ct_who'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.5);popG(q('ct_gl'),lt,bt(1)-.4,t,1,30,0,.5);for(let i=0;i<4;i++){const p=pe(lt,bt(1)+i*.15,.5),a=i*1.57+t*.5;T(q('ct_f'+i),{x:450+Math.cos(a)*230,y:760+Math.sin(a)*200,s:L(.2,1,p),o:cl(p*2)})}
  const l=pe(lt,.4,.6);T(q('ct_lg'),{s:L(.6,1,eb(l)),o:cl(l*3)});popG(q('ct_bt'),lt,bt(2)-.4,t,2,30,0,.45);if(lt>bt(2)+.3)T(q('ct_bt'),{s:1+.04*Math.sin(t*7),o:1});
  const h=cl((lt-bt(2))/.5);T(q('ct_hd'),{x:L(1860,1700,eo(h)),y:L(760,640,eo(h)),o:cl(h*3)});const rp=((lt-bt(2))%1+1)%1;T(q('ct_rp'),{s:1+rp*1.8,o:h>=1?1-rp:0});kwU(q,'ct_u',lt,bt(2),t)}});
