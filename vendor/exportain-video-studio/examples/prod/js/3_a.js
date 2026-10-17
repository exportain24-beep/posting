// ===================== Product selection 16:9 — scenes 00–09 =====================
const PRD=[['তাজা আম','m',C.o],['পাটের ব্যাগ','j',C.g],['বাঁশের হস্তশিল্প','b',C.t]];
const prodArt=(k,x,y,s=1)=>k=='m'?mango(x,y,1.4*s):k=='j'?jutebag(x,y,.75*s):basket(x,y,.9*s);
const QL=['পুঁজি','জ্ঞান','নিয়ম','টেকসই','সোর্সিং','চাহিদা'];

// 00 hook
K.pd_hook=()=>{const O=[['shirt',C.b],['m',C.o],['j',C.g],['fish',C.t],['b',C.p]];return{svg:`${BG}
 <g data-k="h_q"><circle cx="960" cy="520" r="210" fill="#fff" stroke="${C.gd}" stroke-width="14"/>${tx(960,610,'?',260,C.gd,800)}</g>
 ${O.map((o,i)=>`<g data-k="h_o${i}"><circle cx="0" cy="0" r="90" fill="#fff"/>${o[0]=='shirt'?icon('shirt',0,0,100,o[1],7):o[0]=='fish'?fish2(0,0,.8):prodArt(o[0],0,0,.8)}</g>`).join('')}
 <g data-k="h_x">${card(1340,700,480,280,'#fff4f2',40)}${carton(1500,840,1)}${cross(1700,800,50,C.r)}${tx(1580,950,'প্রথম চালানেই আটকে',32,C.r,800)}</g>
 <g data-k="h_t">${card(560,820,800,170,C.gd,50)}${tx(960,930,'৫টি প্রশ্নে সঠিক পণ্য',62,'#fff',800)}</g>`,
 upd(q,lt,t,bt){popG(q('h_q'),lt,.1,t,0,40,0,.45);T(q('h_q'),{s:1+.03*Math.sin(t*3),o:1});for(let i=0;i<5;i++){const a=i*1.2566+t*.6,p=pe(lt,.2+i*.15,.5),r=L(80,360,eo(p));T(q('h_o'+i),{x:960+Math.cos(a)*r*1.25,y:520+Math.sin(a)*r*.85,s:L(.2,1,p),o:cl(p*3)})}
  popG(q('h_x'),lt,bt(1),t,1,40,2,.45);if(lt>bt(2))T(q('h_x'),{x:Math.sin(t*22)*cl(bt(2)+.8-lt)*8,o:1});popG(q('h_t'),lt,bt(3)-.2,t,2,30,0,.45)}}};

// 01 story
K.pd_story=()=>({svg:`${BG}
 <g data-k="s_p">${card(100,170,520,800,'#fff',44)}${person(360,250,1,'s','s_pp')}${tx(360,600,'শাহেদ · রংপুর',48,C.ink,800)}${pill(360,680,'কাল্পনিক চরিত্র',C.p,32)}<g data-k="s_q">${tx(360,850,'কোন পণ্য?',56,C.o,800)}</g></g>
 ${PRD.map((p,i)=>`<g data-k="s_c${i}">${card(700+i*380,170,350,520,'#fff',40)}<circle cx="${875+i*380}" cy="370" r="130" fill="${p[2]}" opacity=".14"/>${prodArt(p[1],875+i*380,370)}${tx(875+i*380,600,p[0],p[0].length>10?34:42,C.ink,800)}</g>`).join('')}
 <g data-k="s_g">${card(700,730,1110,240,'#fff',36)}${QL.map((l,i)=>`<g>${pill(800+i*178,800,l,'#94a3b8',26)}<rect x="${750+i*178}" y="860" width="100" height="70" rx="16" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="3" stroke-dasharray="8 6"/></g>`).join('')}</g>`,
 upd(q,lt,t,bt){popG(q('s_p'),lt,.1,t,0,40,2,.45);if(lt>.8)T(q('s_p'),{y:Math.sin(lt*2)*8,o:1});popIn(q('s_q'),pe(lt,bt(1),.4),t,1,10,0);for(let i=0;i<3;i++){popG(q('s_c'+i),lt,bt(2+i)-.2,t,i,40,3,.45)}popG(q('s_g'),lt,bt(5)-.3,t,3,30,0,.45)}});

// 02 capital
K.pd_capital=()=>{const S=[['পণ্য কেনা',C.b],['স্যাম্পল',C.t],['প্যাকেজিং',C.o],['পরিবহন',C.p],['টাকা আসা পর্যন্ত অপেক্ষা',C.r]];return{svg:`${BG}${rd('c_')}${ttl2('c_','১','পুঁজি কত?',C.b)}
 <g data-k="c_w">${card(100,330,560,640,'#fff',44)}<rect x="200" y="460" width="360" height="240" rx="40" fill="${C.gd}"/><rect x="420" y="530" width="160" height="100" rx="30" fill="${C.g}"/><circle cx="470" cy="580" r="18" fill="#fff"/>${tx(380,620,'৳',120,'#fff',800)}${tx(380,850,'আপনার পুঁজি',44,C.ink,800)}</g>
 ${S.map((s,i)=>`<g data-k="c_s${i}">${card(760,860-i*130,1060,110,'#fff',28)}<rect x="760" y="${860-i*130}" width="20" height="110" fill="${s[1]}"/>${tx(820,928-i*130,s[0],40,C.ink,800,'start')}${i==4?icon('cal',1740,915-i*130,60,s[1],6):coin(1740,915-i*130,30)}</g>`).join('')}`,
 upd(q,lt,t,bt){rdU(q,'c_',lt,t,1);ttlU(q,'c_',lt,t);popG(q('c_w'),lt,.4,t,0,40,2,.45);for(let i=0;i<5;i++){const p=pe(lt,bt(1+i)-.15,.4);T(q('c_s'+i),{y:L(-300,0,eb(p)),o:cl(p*3)})}}}};

// 03 knowledge
K.pd_know=()=>{const K3=[['মান যাচাই','mag',C.b],['ভালো মাল কোথায়','mappin',C.t],['দামের ওঠানামা','chart',C.o]];return{svg:`${BG}${rd('k_')}
 <g data-k="k_p">${card(100,190,560,780,'#fff',44)}${person(380,260,1,'s','k_pp')}${tx(380,620,'কতটা জানি?',48,C.ink,800)}${meter(170,700,420,50,C.g,'k_m')}${tx(380,820,'জ্ঞানের মিটার',34,C.mute,800)}</g>
 ${K3.map((k,i)=>`<g data-k="k_c${i}">${card(740+i*370,190,340,480,'#fff',40)}<circle cx="${910+i*370}" cy="370" r="110" fill="${k[2]}" opacity=".14"/>${k[1]=='mag'?mag(910+i*370,360,1.1,k[2]):k[1]=='chart'?`<path d="M${830+i*370} 420 L${880+i*370} 340 L${930+i*370} 390 L${990+i*370} 300" stroke="${k[2]}" stroke-width="12" fill="none" stroke-linecap="round"/>`:icon('mappin',910+i*370,370,130,k[2],7)}${tx(910+i*370,580,k[0],k[0].length>10?34:40,C.ink,800)}</g>`).join('')}
 <g data-k="k_b">${card(740,730,1080,240,C.gd,40)}${tx(1280,830,'যে পণ্য চেনেন',52,'#fff',800)}${tx(1280,910,'সেখান থেকেই শুরু নিরাপদ',42,'#d9f5c4',800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'k_',lt,t,1);popG(q('k_p'),lt,.1,t,0,40,2,.45);fillTo(q('k_m'),lt,bt(1),420*.8,bt(4)-bt(1));for(let i=0;i<3;i++)popG(q('k_c'+i),lt,bt(1+i)-.2,t,i,40,3,.45);popG(q('k_b'),lt,bt(4)-.2,t,3,30,0,.45)}}};

// 04 rules
K.pd_rules=()=>({svg:`${BG}${rd('r_')}${ttl2('r_','২','নিষেধাজ্ঞা আছে কি?',C.r)}
 <g data-k="r_bk">${card(100,330,560,640,'#fff',44)}<rect x="200" y="400" width="360" height="460" rx="20" fill="${C.gd}"/><rect x="200" y="400" width="40" height="460" fill="${C.f}"/>${lat(400,560,'Export',44,'#fff',800)}${lat(400,620,'Policy',44,'#fff',800)}${lat(400,700,'2024–27',40,C.y,800)}${tx(380,930,'রপ্তানি নীতি',40,C.ink,800)}</g>
 <g data-k="r_lst">${card(740,330,1080,640,'#fff4f2',44)}${tx(800,410,'রপ্তানি নিষিদ্ধ (উদাহরণ)',42,C.r,800,'start')}
  <g data-k="r_t0">${card(800,460,440,440,'#fff',36)}${seeds(1020,620,1.5)}${slash(1020,620,140)}${tx(1020,840,'পাটবীজ',46,C.ink,800)}</g>
  <g data-k="r_t1">${card(1320,460,440,440,'#fff',36)}${rice(1540,620,1.5)}${slash(1540,620,140)}${tx(1540,820,'সাধারণ চাল',44,C.ink,800)}${tx(1540,870,'(সুগন্ধি চাল ছাড়া)',28,C.mute,800)}</g></g>`,
 upd(q,lt,t,bt){rdU(q,'r_',lt,t,2);ttlU(q,'r_',lt,t);popG(q('r_bk'),lt,Math.min(bt(1)-.3,.9),t,0,40,2,.45);if(lt>1.5)T(q('r_bk'),{y:Math.sin(lt*2)*10,r:Math.sin(lt*1.4)*1.2,o:1});popG(q('r_lst'),lt,bt(2)-.3,t,1,30,0,.45);popG(q('r_t0'),lt,bt(3)-.2,t,2,40,3,.45);popG(q('r_t1'),lt,bt(4)-.2,t,3,40,3,.45)}});

// 05 special certificates
K.pd_special=()=>({svg:`${BG}${rd('x_')}
 ${kw('x_h',480,230,'বিশেষ সনদ লাগে',56,'#fff',C.t)}
 <g data-k="x_a">${card(100,300,420,520,'#fff',40)}${leaf2(310,460,1.3)}${lat(310,640,'Phytosanitary',34,C.g,800)}${tx(310,700,'উদ্ভিদ সংগনিরোধ',32,C.ink,800)}${tx(310,760,'ফল · সবজি',30,C.mute,800)}</g>
 <g data-k="x_b">${card(560,300,420,520,'#fff',40)}${fish2(770,460,1.2)}${lat(770,640,'DOF Health Cert.',32,C.b,800)}${tx(770,700,'মৎস্য অধিদপ্তর',32,C.ink,800)}${tx(770,760,'মাছ',30,C.mute,800)}</g>
 <g data-k="x_br">${browser(1040,200,780,620,'hub.bangladeshcustoms.gov.bd',C.bd)}${lat(1430,330,'Import Export Hub',40,C.bd,800)}<rect x="1100" y="380" width="660" height="90" rx="45" fill="#f1f5f9" stroke="${C.bd}" stroke-width="4"/>${icon('globe',1150,425,44,C.mute,6)}${lat(1200,438,'HS Code: ',32,C.mute,800,'start')}<g data-k="x_hs">${lat(1370,438,'0804.50',34,C.ink,800,'start')}</g>
  <g data-k="x_rs"><rect x="1100" y="510" width="660" height="80" rx="18" fill="#e9f8ec"/>${lat(1130,560,'Export: allowed',30,C.g,800,'start')}<rect x="1100" y="610" width="660" height="80" rx="18" fill="#fffbeb"/>${lat(1130,660,'Requires: Phytosanitary Cert.',30,C.o,800,'start')}${tx(1430,770,'চিত্র উদাহরণ',26,C.mute,700)}</g></g>
 ${kw('x_k',960,960,'এইচএস কোড = আন্তর্জাতিক পণ্য শ্রেণি নম্বর',44,'#fff',C.gd)}`,
 upd(q,lt,t,bt){rdU(q,'x_',lt,t,2);kwU(q,'x_h',lt,Math.min(bt(0)-.2,.2),t);popG(q('x_a'),lt,Math.min(bt(1)-.2,1.0),t,0,40,2,.45);popG(q('x_b'),lt,Math.min(bt(2)-.2,1.8),t,1,40,2,.45);['x_a','x_b'].forEach((k,i)=>{if(lt>2.4)T(q(k),{y:Math.sin(lt*2+i*1.5)*10,s:lt>bt(1+i)&&lt<bt(1+i)+.6?1.05:1,o:1})});popG(q('x_br'),lt,bt(3)-.3,t,2,30,0,.45);const p=pe(lt,bt(3)+.1,.6);T(q('x_hs'),{o:cl(p*3)});kwU(q,'x_k',lt,bt(3)+.2,t);popIn(q('x_rs'),pe(lt,bt(4)-.1,.4),t,3,20,0)}});

// 06 perishable
K.pd_perish=()=>{const D=['#f59e0b','#eab308','#a16207','#78350f'];return{svg:`${BG}${rd('p_')}${ttl2('p_','৩','পচনশীল কি?',C.o)}
 <g data-k="p_tl">${card(100,330,900,640,'#fff',44)}${tx(150,410,'তাজা আম: দিন যত যায়',38,C.ink,800,'start')}<path d="M180 640 H920" stroke="#cbd5e1" stroke-width="8"/>${D.map((c,i)=>`<g data-k="p_m${i}"><circle cx="${230+i*230}" cy="560" r="80" fill="${c}"/>${tx(230+i*230,720,'দিন '+BN([1,3,5,7][i]),34,C.mute,800)}</g>`).join('')}${tx(550,870,'কয়েক দিনেই নষ্ট হতে পারে',42,C.r,800)}</g>
 ${[['ঠান্ডা সংরক্ষণ','box',C.b],['দ্রুত পরিবহন','truck',C.t],['বিমান খরচ ↑','plane',C.r]].map((r,i)=>`<g data-k="p_n${i}">${card(1060,330+i*220,760,190,'#fff',36)}<circle cx="1160" cy="${425+i*220}" r="62" fill="${r[2]}" opacity=".15"/>${r[1]=='plane'?plane(1160,425+i*220,.42,r[2]):icon(r[1],1160,425+i*220,80,r[2],7)}${tx(1260,440+i*220,r[0],42,C.ink,800,'start')}</g>`).join('')}`,
 upd(q,lt,t,bt){rdU(q,'p_',lt,t,3);ttlU(q,'p_',lt,t);popG(q('p_tl'),lt,Math.min(bt(1)-.4,.9),t,0,30,0,.45);if(lt>1.5)T(q('p_tl'),{y:Math.sin(lt*2)*8,o:1});for(let i=0;i<4;i++)popIn(q('p_m'+i),pe(lt,bt(1)+i*.3,.35),t,i,10,0);for(let i=0;i<3;i++)popG(q('p_n'+i),lt,bt(2+i)-.2,t,i,40,2,.45)}}};

// 07 durable
K.pd_durable=()=>({svg:`${BG}${rd('d_')}
 <g data-k="d_a">${card(100,200,900,560,'#fff',44)}${jutebag(330,460,1)}${basket(720,480,1.4)}${check(900,260,40,C.g)}${tx(550,700,'টেকসই পণ্য',52,C.g,800)}</g>
 <g data-k="d_c">${cal(1080,200,360,'✓','মাস পেরোলেও',C.g)}</g>
 <g data-k="d_s">${card(1060,600,760,380,'#eef6ff',40)}${shipA(1440,800,1.3)}${tx(1440,940,'সমুদ্রপথেও চলে',40,C.b,800)}</g>
 ${kw('d_k',550,880,'নতুনদের জন্য সহজ শুরু',48,'#fff',C.g)}`,
 upd(q,lt,t,bt){rdU(q,'d_',lt,t,3);popG(q('d_a'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.45);kwU(q,'d_k',lt,bt(0)+.3,t);popG(q('d_c'),lt,bt(1)-.2,t,1,40,2,.45);popG(q('d_s'),lt,bt(2)-.3,t,2,30,0,.45);if(lt>bt(2))T(q('d_s'),{y:Math.sin(t*2)*6,o:1})}});

// 08 sourcing
K.pd_source=()=>({svg:`${BG}${rd('o_')}${ttl2('o_','৪','নিয়মিত সোর্সিং?',C.g)}
 <g data-k="o_cv">${card(100,330,1100,640,'#fff',44)}<rect x="150" y="720" width="1000" height="40" rx="20" fill="#475569"/>${[0,1,2,3,4,5,6,7,8].map(i=>`<circle cx="${190+i*115}" cy="740" r="12" fill="#94a3b8"/>`).join('')}<g data-k="o_bg">${[0,1,2,3,4,5].map(i=>`<g transform="translate(${i*220} 0)">${jutebag(0,610,.6)}</g>`).join('')}</g>${tx(650,880,'একই মান · বারবার',44,C.ink,800)}</g>
 ${['একই মান','সময়মতো','দরকারি পরিমাণ'].map((l,i)=>`<g data-k="o_k${i}">${card(1260,330+i*220,560,190,'#fff',36)}${check(1350,425+i*220,40,C.g)}${tx(1420,440+i*220,l,44,C.ink,800,'start')}</g>`).join('')}`,
 upd(q,lt,t,bt){rdU(q,'o_',lt,t,4);ttlU(q,'o_',lt,t);popG(q('o_cv'),lt,bt(0)+.3,t,0,30,0,.45);const g=q('o_bg');if(g)T(g,{x:((t*120)%220)-60,o:1});for(let i=0;i<3;i++)popG(q('o_k'+i),lt,bt(1+i)-.2,t,i,40,2,.45)}});

// 09 reorder
K.pd_reorder=()=>({svg:`${BG}${rd('e_')}
 <g data-k="e_o1">${card(100,200,520,300,'#fff',36)}${lat(150,270,'Order #1',36,C.b,800,'start')}${carton(280,410,.8)}${tx(470,420,'ছোট',40,C.ink,800)}</g>
 <g data-k="e_o2">${card(100,540,520,430,'#e9f8ec',36)}${lat(150,610,'Order #2',36,C.g,800,'start')}${carton(230,800,.9)}${carton(360,800,.9)}${carton(295,730,.9)}${tx(530,700,'আরও বড়',40,C.g,800)}</g>
 <g data-k="e_x0">${card(700,200,500,180,'#fff4f2',36)}${cross(780,290,36,C.r)}${tx(840,305,'মৌসুম শেষ',44,C.r,800,'start')}</g>
 <g data-k="e_x1">${card(700,420,500,180,'#fff4f2',36)}${cross(780,510,36,C.r)}${tx(840,525,'কারিগর নেই',44,C.r,800,'start')}</g>
 <g data-k="e_n">${card(700,640,1120,330,'#fff',40)}${tx(1260,710,'২–৩ জন নির্ভরযোগ্য সরবরাহকারী',42,C.gd,800)}${[0,1,2].map(i=>`<g>${factB(900+i*360,860,.45,[C.b,C.t,C.p][i])}<path d="M${900+i*360} 760 Q1260 700 1260 760" stroke="${C.g}" stroke-width="0" fill="none"/></g>`).join('')}</g>
 <g data-k="e_b">${card(1260,200,560,400,'#fff',36)}${person(1400,250,.6,'g','e_bp')}${bub(1600,360,320,'Reorder!',C.b,'#fff',36,-1)}${tx(1540,540,'বায়ার খুশি',40,C.g,800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'e_',lt,t,4);popG(q('e_b'),lt,.1,t,0,40,2,.45);popG(q('e_o1'),lt,Math.min(bt(0)-.3,.5),t,1,40,2,.45);popG(q('e_o2'),lt,bt(1)-.2,t,2,40,2,.45);popG(q('e_x0'),lt,bt(2)-.2,t,3,40,2,.45);popG(q('e_x1'),lt,bt(3)-.2,t,4,40,2,.45);for(const k of ['e_x0','e_x1'])if(lt>bt(4))fadeMul(q(k),.45);popG(q('e_n'),lt,bt(4)-.2,t,5,30,0,.45)}});
