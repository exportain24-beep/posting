// ===================== ERC rules 16:9 — scenes 00–10 =====================
// 00 — hook
K.er_hook=()=>({svg:`${BG}
 <g data-k="h_c">${ercCard(110,190,640,460)}</g><g data-k="h_st">${stampT(430,450,'বাতিল?',C.r,64)}</g>
 ${kw('h_w0',1320,260,'ইআরসি হাতে পেলেই',72,C.ink)}${kw('h_w1',1320,400,'যেকোনো পণ্য রপ্তানি?',72,C.b)}
 ${kw('h_w2',1320,610,'না।',150,'#fff',C.r)}
 <g data-k="h_s">${['নিষিদ্ধ পণ্য','শর্তসাপেক্ষ পণ্য','হস্তান্তর নয়'].map((s,i)=>pill([1000,1320,1640][i],820,s,[C.r,C.o,C.t][i],34)).join('')}${tx(1320,930,'সনদের সাথে আসে কিছু শর্ত',40,C.mute,800)}</g>`,
 upd(q,lt,t,bt){popG(q('h_c'),lt,.15,t,0,50,2,.5);kwU(q,'h_w0',lt,Math.min(bt(0),.3),t);kwU(q,'h_w1',lt,bt(1)-.1,t);kwU(q,'h_w2',lt,bt(2)-.1,t);if(lt>bt(2)+.4)T(q('h_w2'),{r:Math.sin(t*8)*3,o:1});
  popG(q('h_s'),lt,bt(3)-.2,t,1,30,0,.5);popIn(q('h_st'),pe(lt,bt(4)-.1,.4),t,2,0,0)}});

// 01 — story: Jewel from Cumilla
K.er_story=()=>({svg:`${BG}
 <g data-k="s_p">${card(100,170,620,760,'#fff',44)}${person(410,230,1.05,'s','s_sp')}${tx(410,560,'জুয়েল · কুমিল্লা',52,C.ink,800)}${pill(410,650,'কাল্পনিক চরিত্র',C.p,32)}</g>
 <g data-k="s_e">${ercCard(170,720,480,180)}${check(620,740,30,C.g)}</g>
 <g data-k="s_f">${card(820,230,980,360,'#fff',44)}${person(950,270,.55,'n','s_fp')}${bub(1340,350,720,'পাটবীজ পাঠাও, দ্রুত লাভ!',C.o,'#fff',44,-1)}${tx(1340,520,'বন্ধুর পরামর্শ',34,C.mute,800)}</g>
 <g data-k="s_q">${card(820,660,980,280,'#eef6ff',44)}${tx(1310,790,'আসল নিয়ম কী?',72,C.b,800)}${tx(1310,870,'চলুন দেখি',40,C.mute,800)}</g>`,
 upd(q,lt,t,bt){popG(q('s_p'),lt,.15,t,0,50,2,.5);popG(q('s_e'),lt,bt(1)-.2,t,1,30,3,.5);popG(q('s_f'),lt,bt(2)-.3,t,2,40,0,.5);popG(q('s_q'),lt,bt(3)-.2,t,3,30,2,.5)}});

// 02 — conditions printed on the certificate
K.er_cert=()=>{const R=[['Prohibited goods cannot be exported.','নিষিদ্ধ পণ্য রপ্তানি করা যাবে না',C.r],['Controlled goods: follow the Export Policy.','নিয়ন্ত্রিত পণ্যে নীতির শর্ত মানতে হবে',C.o],['This certificate cannot be transferred.','সনদ হস্তান্তর করা যাবে না',C.t]];return{svg:`${BG}
 <g data-k="c_d">${card(220,150,1480,880,'#fffbeb',30)}<rect x="240" y="170" width="1440" height="840" rx="20" fill="none" stroke="#c9a227" stroke-width="5"/>
  <rect x="240" y="170" width="1440" height="110" rx="20" fill="${C.g}"/><rect x="240" y="240" width="1440" height="40" fill="${C.g}"/>${lat(960,240,'EXPORT REGISTRATION CERTIFICATE',46,'#fff',800)}
  ${lat(300,340,'Office of the Chief Controller of Imports & Exports',28,C.mute,700,'start')}<rect x="300" y="370" width="700" height="14" rx="7" fill="#e7dcb8"/>
  ${lat(300,450,'Conditions',34,C.ink,800,'start')}
  ${R.map((r,i)=>`<g data-k="c_r${i}"><rect x="290" y="${480+i*165}" width="1340" height="145" rx="20" fill="#fff" stroke="${r[2]}" stroke-width="5"/><circle cx="350" cy="${552+i*165}" r="30" fill="${r[2]}"/>${lat(350,563+i*165,String(i+1),30,'#fff',800)}${lat(410,540+i*165,r[0],34,C.ink,800,'start')}${tx(410,595+i*165,r[1],34,r[2],800,'start')}</g>`).join('')}</g>
 <g data-k="c_z">${kw('c_zz',1500,440,'সনদের গায়েই লেখা',40,'#fff',C.gd)}</g>`,
 upd(q,lt,t,bt){popG(q('c_d'),lt,.15,t,0,40,0,.5);kwU(q,'c_zz',lt,bt(0)-.1,t);for(let i=0;i<3;i++){popG(q('c_r'+i),lt,bt(i+1)-.2,t,i,20,0,.5);if(lt>bt(i+1)&&lt<bt(i+1)+.8)T(q('c_r'+i),{s:1+.02*Math.sin((lt-bt(i+1))*12),o:1})}}}};

// 03 — point 1: prohibited
K.er_ban=()=>({svg:`${BG}${rd('b_')}${ttl2('b_','১','রপ্তানি নিষিদ্ধ পণ্য',C.r)}
 <g data-k="b_bk">${card(100,330,760,620,'#fff',40)}<rect x="160" y="380" width="300" height="420" rx="16" fill="${C.gd}"/>${lat(310,520,'Export',40,'#fff',800)}${lat(310,575,'Policy',40,'#fff',800)}${lat(310,650,'2024–27',44,C.y,800)}
  <g data-k="b_pg"><rect x="480" y="380" width="330" height="420" rx="16" fill="#fff7f6" stroke="${C.r}" stroke-width="5"/>${tx(645,450,'পরিশিষ্ট-১',36,C.r,800)}${tx(645,500,'রপ্তানি নিষিদ্ধ',32,C.ink,800)}${[0,1,2,3,4].map(i=>`<rect x="510" y="${540+i*44}" width="270" height="14" rx="7" fill="#f3c6c6"/>`).join('')}</g>${tx(480,890,'রপ্তানি নীতি ২০২৪–২৭',36,C.mute,800)}</g>
 <g data-k="b_w"><rect x="1500" y="330" width="60" height="620" rx="12" fill="${C.r}"/>${Array.from({length:6},(_,i)=>`<rect x="1500" y="${350+i*100}" width="60" height="16" fill="#fff" opacity=".5"/>`).join('')}</g>
 <g data-k="b_e">${ercCard(1000,480,420,300)}</g>
 <g data-k="b_x">${cross(1530,640,60,C.r)}${kw('b_t',1300,920,'ইআরসি থাকলেও না',56,'#fff',C.r)}</g>`,
 upd(q,lt,t,bt){rdU(q,'b_',lt,t,1);ttlU(q,'b_',lt,t);popG(q('b_bk'),lt,.5,t,0,40,0,.5);popIn(q('b_pg'),pe(lt,bt(1)-.2,.5),t,1,0,0);popG(q('b_w'),lt,bt(1)+.4,t,2,0,0,.4);
  const k=cl((lt-bt(2)+.2)/.6);T(q('b_e'),{x:L(-300,0,eo(k))+(k>=1?-Math.abs(Math.sin((lt-bt(2))*10))*20*cl(1.5-(lt-bt(2))):0),o:cl(k*3)});popIn(q('b_x'),pe(lt,bt(2)+.3,.4),t,3,0,0);kwU(q,'b_t',lt,bt(2)+.3,t)}});

// 04 — the list
K.er_list=()=>{const I=[[gun(0,0,1.2),'অস্ত্র ও গোলাবারুদ'],[radio(0,0,1),'তেজস্ক্রিয় পদার্থ'],[vase(0,0,1),'প্রত্নতাত্ত্বিক নিদর্শন'],[skull(0,0,1),'মানুষের কঙ্কাল'],[seeds(0,0,1),'পাটবীজ'],[shrimp2(0,0,1),'নির্দিষ্ট আকারের ছোট চিংড়ি'],[rice(0,0,1),'সাধারণ চাল*']];return{svg:`${BG}${rd('l_')}${ttl2('l_','১','তালিকায় যা আছে',C.r)}
 ${I.map((it,i)=>{const r=Math.floor(i/4),c=i%4,x=(r==0?110:310)+c*430,y=320+r*360;return `<g data-k="l_i${i}">${card(x,y,400,330,'#fff',36)}<g transform="translate(${x+200} ${y+130})">${it[0]}</g>${tx(x+200,y+285,it[1],it[1].length>16?28:34,C.ink,800)}<g data-k="l_s${i}">${slash(x+200,y+130,90)}</g></g>`}).join('')}
 ${tx(1700,1050,'* সরকারি পর্যায় ও সুগন্ধি চাল ছাড়া',24,C.mute,700,'end')}`,
 upd(q,lt,t,bt){rdU(q,'l_',lt,t,1);ttlU(q,'l_',lt,t);for(let i=0;i<7;i++){popG(q('l_i'+i),lt,bt(i)-.25,t,i,30,2,.45);popIn(q('l_s'+i),pe(lt,bt(i)+.25,.3),t,i,0,0)}}}};

// 05 — Jewel's shipment stopped
K.er_jewel=()=>({svg:`${BG}
 <g data-k="j_p">${card(100,170,520,640,'#fff',44)}${person(360,230,.95,'s','j_sp')}${tx(360,560,'জুয়েল',52,C.ink,800)}${kw('j_w0',360,700,'পরামর্শ ভুল',52,'#fff',C.r)}</g>
 <g data-k="j_g">${card(700,170,1120,640,'#fff',44)}<rect x="1300" y="300" width="40" height="420" fill="#475569"/><rect x="1290" y="290" width="60" height="30" rx="8" fill="#475569"/>
  <g data-k="j_bar"><rect x="1320" y="420" width="440" height="34" rx="12" fill="${C.r}"/>${[0,1,2,3].map(i=>`<rect x="${1360+i*100}" y="420" width="44" height="34" fill="#fff"/>`).join('')}</g>${lat(1540,380,'CUSTOMS',44,C.bd,800)}
  <g data-k="j_t"><rect x="760" y="560" width="440" height="160" rx="16" fill="${C.b}"/><rect x="1200" y="610" width="110" height="110" rx="12" fill="${C.bd}"/><circle cx="850" cy="740" r="36" fill="#1f2937"/><circle cx="1220" cy="740" r="36" fill="#1f2937"/>${seeds(980,520,1.1)}${lat(980,660,'Jute seed',32,'#fff',800)}</g>
  <g data-k="j_h">${stampT(1540,620,'HOLD',C.r,70)}</g></g>
 ${kw('j_w1',960,960,'চালান কাস্টমসেই আটকে যাবে',64,'#fff',C.gd)}`,
 upd(q,lt,t,bt){popG(q('j_p'),lt,.15,t,0,40,2,.5);kwU(q,'j_w0',lt,bt(0)-.1,t);popG(q('j_g'),lt,.4,t,1,30,0,.5);const k=cl((lt-.6)/(bt(1)-.6));T(q('j_t'),{x:L(-260,0,eo(k)),o:1});popIn(q('j_h'),pe(lt,bt(1),.4),t,2,0,0);kwU(q,'j_w1',lt,bt(1)+.2,t);if(lt>bt(2))T(q('j_t'),{x:Math.sin(t*20)*cl((bt(2)+.6-lt)*2)*6,o:1})}});

// 06 — point 2: conditional
K.er_cond=()=>({svg:`${BG}${rd('d_')}${ttl2('d_','২','শর্তসাপেক্ষ পণ্য',C.o)}
 <g data-k="d_g">${card(100,330,1720,640,'#fff',44)}<rect x="900" y="380" width="40" height="540" fill="#a16207"/><g data-k="d_dr"><rect x="940" y="420" width="420" height="460" rx="16" fill="${C.y}"/>${Array.from({length:5},(_,i)=>`<rect x="${980+i*70}" y="440" width="24" height="420" rx="10" fill="#fde68a"/>`).join('')}${icon('lock',1150,650,120,C.ink,8)}</g>
  <g data-k="d_k"><circle cx="0" cy="0" r="44" fill="none" stroke="${C.g}" stroke-width="16"/><rect x="40" y="-10" width="200" height="20" rx="8" fill="${C.g}"/><rect x="200" y="10" width="20" height="34" fill="${C.g}"/>${tx(140,-30,'অনুমতি / সনদ',34,C.g,800)}</g>
  <g data-k="d_c">${carton(600,700,1.3)}</g></g>
 ${kw('d_w',1250,940,'অনুমতি বা বিশেষ সনদ নিয়ে রপ্তানি',44,'#fff',C.o)}`,
 upd(q,lt,t,bt){rdU(q,'d_',lt,t,2);ttlU(q,'d_',lt,t);popG(q('d_g'),lt,.4,t,0,30,0,.5);popIn(q('d_c'),pe(lt,bt(1)-.3,.5),t,1,20,2);const k=cl((lt-bt(2)+.4)/.8);T(q('d_k'),{x:L(300,880,eio(k)),y:650,o:cl(k*4)*(1-cl((lt-bt(2)-.7)/.4))});
  const o=eio(cl((lt-bt(2)-.5)/.8));T(q('d_dr'),{y:L(0,-160,o),o:1-o});T(q('d_c'),{x:L(0,920,eio(cl((lt-bt(2)-1.2)/1.2))),o:1});kwU(q,'d_w',lt,bt(2)-.1,t)}});

// 07 — examples
K.er_examples=()=>{const E=[[leaf2(0,0,1.3),'বন্যপ্রাণী ও তালিকাভুক্ত গাছ','CITES + Licence',C.g],[fish2(0,0,1.1),'হিমায়িত মাছ','DoF quality certificate',C.b],[mango(0,0,1.4),'কৃষিপণ্য','Phytosanitary certificate',C.o]];return{svg:`${BG}${rd('x_')}${ttl2('x_','২','কোন পণ্যে কোন সনদ',C.o)}
 ${E.map((e,i)=>`<g data-k="x_c${i}">${card(100+i*580,330,540,560,'#fff',40)}<circle cx="${370+i*580}" cy="500" r="120" fill="#f1f8f6"/><g transform="translate(${370+i*580} 500)">${e[0]}</g>${tx(370+i*580,700,e[1],e[1].length>14?32:40,C.ink,800)}<rect x="${150+i*580}" y="750" width="440" height="90" rx="45" fill="${e[3]}"/>${lat(370+i*580,808,e[2],e[2].length>18?26:32,'#fff',800)}</g>`).join('')}
 <g data-k="x_b">${pill(960,980,'মান সনদ: BSTI বা নির্দিষ্ট দপ্তর',C.bd,36)}</g>`,
 upd(q,lt,t,bt){rdU(q,'x_',lt,t,2);ttlU(q,'x_',lt,t);for(let i=0;i<3;i++)popG(q('x_c'+i),lt,bt(i)-.25,t,i,40,3,.5);popG(q('x_b'),lt,bt(3)-.2,t,3,20,0,.5)}}};

// 08 — customs hub HS lookup
K.er_hub=()=>({svg:`${BG}${rd('u_')}${ttl2('u_','২','যাচাইয়ের সহজ উপায়',C.o)}
 <g data-k="u_b">${browser(100,320,1720,700,'hub.bangladeshcustoms.gov.bd',C.bd)}${lat(160,460,'Import Export Hub · Export requirements',36,C.ink,800,'start')}
  <rect x="160" y="500" width="900" height="90" rx="45" fill="#f1f5f9" stroke="${C.bd}" stroke-width="4"/>${lat(200,558,'HS code:',32,C.mute,800,'start')}<clipPath id="u_cp"><rect data-k="u_tw" x="350" y="510" width="0" height="70"/></clipPath><g clip-path="url(#u_cp)">${lat(350,558,'1209.99 — Jute seed',34,C.ink,800,'start')}</g>
  <g data-k="u_s"><rect x="160" y="630" width="1600" height="120" rx="20" fill="#fff4f2" stroke="${C.r}" stroke-width="5"/>${lat(200,700,'Status:',34,C.mute,800,'start')}${lat(360,700,'Export prohibited — Export Policy 2024-27',36,C.r,800,'start')}</g>
  <g data-k="u_q"><rect x="160" y="780" width="1600" height="190" rx="20" fill="#f1f8f1"/>${lat(200,840,'Requirements',32,C.ink,800,'start')}${['Phytosanitary certificate','Seed certification','Ministry permission'].map((r,i)=>pill([420,870,1300][i],915,r,C.t,26,'Pop')).join('')}</g></g>`,
 upd(q,lt,t,bt){rdU(q,'u_',lt,t,2);ttlU(q,'u_',lt,t);popG(q('u_b'),lt,bt(0)-.4,t,0,40,0,.5);const tw=q('u_tw');if(tw)tw.setAttribute('width',660*cl((lt-bt(1)+.2)/1));popG(q('u_s'),lt,bt(2)-.2,t,1,20,0,.5);popG(q('u_q'),lt,bt(3)-.2,t,2,20,0,.5)}});

// 09 — point 3: fraud / false info
K.er_fraud=()=>{const R=[['ভুল তথ্য দিলে','False information'],['জালিয়াতি করে অনুমতি','Fraudulent licence / permit'],['আমদানি-রপ্তানি বা বৈদেশিক মুদ্রার নিয়ম ভঙ্গ','Rule violation']];return{svg:`${BG}${rd('f_')}${ttl2('f_','৩','জালিয়াতি বা ভুল তথ্য',C.b)}
 ${R.map((r,i)=>`<g data-k="f_r${i}">${card(100,330+i*200,980,170,'#fff',36)}${cross(180,415+i*200,40,C.r)}${tx(250,410+i*200,r[0],r[0].length>24?34:42,C.ink,800,'start')}${lat(250,455+i*200,r[1],24,C.mute,700,'start')}</g>`).join('')}
 <g data-k="f_e">${ercCard(1200,340,560,400)}</g><g data-k="f_s">${stampT(1480,560,'স্থগিত / বাতিল',C.r,56)}</g>
 ${kw('f_w',1480,880,'নিবন্ধনের ঝুঁকি',56,'#fff',C.r)}`,
 upd(q,lt,t,bt){rdU(q,'f_',lt,t,3);ttlU(q,'f_',lt,t);popG(q('f_e'),lt,.5,t,0,40,2,.5);for(let i=0;i<3;i++)slideG(q('f_r'+i),lt,bt(i+1)-.3,-160,t,i);popIn(q('f_s'),pe(lt,bt(4)-.1,.4),t,1,0,0);kwU(q,'f_w',lt,bt(4)+.2,t)}}};

// 10 — misdeclaration
K.er_misdec=()=>{const F=[['Item','Knit T-shirt',false],['Quantity','10,000 pcs',true],['Unit value','USD 0.40',true]];return{svg:`${BG}${rd('m_')}
 <g data-k="m_l">${card(100,170,780,180,'#fff',40)}${tx(140,250,'সনদেও লেখা:',36,C.mute,800,'start')}${lat(140,310,'Fraud, forgery & misdeclaration are punishable',28,C.r,800,'start')}</g>
 <g data-k="m_s">${stampT(700,470,'শাস্তিযোগ্য',C.r,56)}</g>
 <g data-k="m_b">${docPage(100,560,780,470,'Shipping Bill',C.bd,0)}${F.map((f,i)=>`<g data-k="m_f${i}"><rect x="140" y="${650+i*120}" width="700" height="96" rx="14" fill="${f[2]?'#fff4f2':'#f1f5f9'}" ${f[2]?`stroke="${C.r}" stroke-width="4"`:''}/>${lat(170,708+i*120,f[0],28,C.mute,800,'start')}${lat(810,708+i*120,f[1],32,f[2]?C.r:C.ink,800,'end')}</g>`).join('')}</g>
 <g data-k="m_c">${card(1000,240,820,720,'#fff',44)}${factB(1410,560,1.2,C.bd)}${tx(1410,760,'পুরো ব্যবসা ঝুঁকিতে',52,C.r,800)}<g data-k="m_rp"><circle cx="1410" cy="520" r="200" fill="none" stroke="${C.r}" stroke-width="8"/></g></g>`,
 upd(q,lt,t,bt){rdU(q,'m_',lt,t,3);popG(q('m_l'),lt,bt(0)-.3,t,0,30,0,.5);popIn(q('m_s'),pe(lt,bt(1)-.1,.4),t,1,0,0);popG(q('m_b'),lt,bt(1)+.4,t,2,40,0,.5);for(let i=0;i<3;i++)popIn(q('m_f'+i),pe(lt,bt(2)-.2+i*.3,.35),t,i,10,0);
  popG(q('m_c'),lt,bt(3)-.4,t,3,40,0,.5);const r=((lt-bt(3))%1.2+1.2)%1.2/1.2;T(q('m_rp'),{s:.6+r*.9,o:lt>bt(3)?1-r:0})}}};
