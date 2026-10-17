// ===================== EPB enrolment 16:9 — scenes 00–09 =====================
const enrCard=(x,y,w,h,sub='Enrolment Certificate',col=C.b)=>`<g>${card(x,y,w,h,'#f4f9ff',24)}<rect x="${x+14}" y="${y+14}" width="${w-28}" height="${h-28}" rx="14" fill="none" stroke="${col}" stroke-width="4" stroke-dasharray="10 6"/><rect x="${x+14}" y="${y+14}" width="${w-28}" height="${h*.24}" rx="14" fill="${col}"/>${lat(x+w/2,y+14+h*.16,'EPB',Math.min(60,h*.17),'#fff',800)}${lat(x+w/2,y+h*.47,sub,Math.min(28,w*.05),C.ink,800)}<rect x="${x+w*.15}" y="${y+h*.57}" width="${w*.5}" height="12" rx="6" fill="#cfe0f0"/><rect x="${x+w*.15}" y="${y+h*.65}" width="${w*.35}" height="12" rx="6" fill="#cfe0f0"/><circle cx="${x+w-78}" cy="${y+h-78}" r="42" fill="${col}" opacity=".9"/><circle cx="${x+w-78}" cy="${y+h-78}" r="30" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="6 5"/></g>`;
const chip2=(x,y,l,col)=>`<g>${card(x-110,y-46,220,92,col,46)}${lat(x,y+14,l,l.length>5?28:36,'#fff',800)}</g>`;
const eu=(x,y,s=1)=>`<g transform="translate(${x} ${y}) scale(${s})"><rect x="-90" y="-60" width="180" height="120" rx="10" fill="#1f3a93"/>${Array.from({length:12},(_,i)=>{const a=i/12*6.283;return `<circle cx="${Math.cos(a)*38}" cy="${Math.sin(a)*38}" r="6" fill="#ffcc00"/>`}).join('')}</g>`;

// 00 — hook
K.ep_hook=()=>({svg:`${BG}
 <g data-k="h_o">${docPage(110,180,360,440,'Order',C.b,6)}${check(420,210,34,C.g)}</g>
 <g data-k="h_e">${ercCard(520,240,420,300)}${check(900,270,34,C.g)}</g>
 <g data-k="h_g">${card(1020,200,800,420,'#fff',40)}${lat(1420,300,'GSP certificate',52,C.ink,800)}<rect x="1100" y="350" width="640" height="200" rx="24" fill="#fff4f2" stroke="${C.r}" stroke-width="5"/>${cross(1220,450,50,C.r)}${tx(1480,470,'আটকে গেল',56,C.r,800)}</g>
 <g data-k="h_n">${enrCard(560,690,800,330)}</g>
 ${kw('h_w',1580,860,'কারণ?',80,'#fff',C.b)}`,
 upd(q,lt,t,bt){popG(q('h_o'),lt,Math.min(bt(0)-.2,.15),t,0,40,2,.5);popG(q('h_e'),lt,bt(1)-.2,t,1,40,2,.5);popG(q('h_g'),lt,bt(2)-.2,t,2,30,0,.5);if(lt>bt(3))T(q('h_g'),{x:Math.sin(t*22)*cl((bt(3)+.8-lt)*2)*8,o:1});
  kwU(q,'h_w',lt,bt(3)+.2,t);popIn(q('h_n'),pe(lt,bt(4)-.2,.6),t,3,60,3)}});

// 01 — story: Nazma, Savar
K.ep_story=()=>({svg:`${BG}
 <g data-k="s_p">${card(100,170,600,780,'#fff',44)}${woman2(400,250,1)}${tx(400,570,'নাজমা · সাভার',52,C.ink,800)}${tx(400,640,'নিট পোশাক',36,C.mute,800)}${pill(400,730,'কাল্পনিক চরিত্র',C.p,32)}</g>
 <g data-k="s_m">${card(780,170,1040,420,'#fff',44)}${eu(920,300,.9)}${shipA(1400,420,1.1)}${tx(1300,540,'ইউরোপে প্রথম চালান',44,C.ink,800)}</g>
 <g data-k="s_b">${card(780,630,1040,320,'#eef6ff',44)}${person(900,660,.55,'g','s_bp')}${bub(1400,760,700,'Proof of origin for GSP?',C.b,'#fff',36,-1)}${tx(1400,890,'বায়ার চাইছেন উৎসের প্রমাণ',36,C.ink,800)}</g>
 <g data-k="s_k">${pill(400,860,'লাগবে ইপিবির নিবন্ধন',C.gd,34)}</g>`,
 upd(q,lt,t,bt){popG(q('s_p'),lt,.15,t,0,40,2,.5);popG(q('s_m'),lt,bt(1)-.3,t,1,40,0,.5);popG(q('s_b'),lt,bt(2)-.3,t,2,30,2,.5);popG(q('s_k'),lt,bt(3)-.1,t,3,20,0,.5)}});

// 02 — what is EPB enrolment
K.ep_what=()=>({svg:`${BG}
 <g data-k="w_b">${card(100,170,800,800,'#fff',44)}${bank(500,520,1.8,C.b)}${lat(500,760,'Export Promotion Bureau',40,C.b,800)}${tx(500,830,'রপ্তানি উন্নয়ন ব্যুরো',48,C.ink,800)}</g>
 <g data-k="w_l">${card(980,170,840,380,'#fff',44)}${lat(1040,240,'Exporters register',34,C.mute,800,'start')}${[0,1,2].map(i=>`<g data-k="w_r${i}"><rect x="1040" y="${280+i*80}" width="720" height="64" rx="14" fill="${i==2?'#e9f8ec':'#f1f5f9'}"/>${lat(1070,322+i*80,['Rahim Leather Ltd','Karim Jute Co','Nazma Knit Exports'][i],28,i==2?C.g:C.ink,800,'start')}${i==2?check(1720,312+i*80,22,C.g):''}</g>`).join('')}</g>
 <g data-k="w_c">${enrCard(1060,600,680,380)}</g>`,
 upd(q,lt,t,bt){popG(q('w_b'),lt,Math.min(bt(0)-.3,.2),t,0,40,2,.5);popG(q('w_l'),lt,bt(1)-.6,t,1,30,0,.5);for(let i=0;i<3;i++)popIn(q('w_r'+i),pe(lt,bt(1)-.4+i*.3,.35),t,i,10,0);popIn(q('w_c'),pe(lt,bt(2)-.2,.6),t,2,60,3)}});

// 03 — point 1: no enrolment, no services
K.ep_need=()=>{const S=[['GSP',C.g],['CO',C.b],['SAFTA',C.t],['SAPTA',C.o],['APTA',C.p],['REX',C.gd]];const P=[[560,330],[960,250],[1360,330],[1360,830],[960,910],[560,830]];return{svg:`${BG}${rd('n_')}${ttl2('n_','১','কেন লাগে',C.b)}
 <g data-k="n_c">${enrCard(760,430,400,290)}</g><g data-k="n_gr"><rect x="760" y="430" width="400" height="290" rx="24" fill="#94a3b8" opacity=".55"/>${tx(960,600,'মেয়াদোত্তীর্ণ',40,'#fff',800)}</g>
 ${S.map((s,i)=>`<g data-k="n_s${i}">${chip2(P[i][0]+(i<3?0:0),P[i][1]+100,s[0],s[1])}<g data-k="n_l${i}">${icon('lock',P[i][0]+90,P[i][1]+60,50,C.r,8)}</g></g>`).join('')}
 ${kw('n_w',960,1010,'কোনো সেবাই নয়',48,'#fff',C.r)}`,
 upd(q,lt,t,bt){rdU(q,'n_',lt,t,1);ttlU(q,'n_',lt,t);popG(q('n_c'),lt,.4,t,0,40,0,.5);for(let i=0;i<6;i++){popG(q('n_s'+i),lt,bt(i+2)-.15,t,i,20,3,.4);popIn(q('n_l'+i),pe(lt,bt(8)-.2+i*.08,.3),t,i,0,0)}
  T(q('n_gr'),{o:cl((lt-bt(1))/.6)*(lt<bt(1)+2.2?1:1)});kwU(q,'n_w',lt,bt(8),t)}}};

// 04 — why it matters: duty
K.ep_why=()=>({svg:`${BG}${rd('y_')}
 <g data-k="y_a">${card(100,180,820,780,'#e9f8ec',44)}${enrCard(300,230,420,280)}${tx(510,600,'সনদ থাকলে',44,C.ink,800)}<g data-k="y_a1">${lat(510,760,'0%',150,C.g,800)}${tx(510,860,'শুল্ক ছাড় বা কম শুল্ক',40,C.g,800)}</g></g>
 <g data-k="y_b">${card(1000,180,820,780,'#fff4f2',44)}<g opacity=".4">${enrCard(1200,230,420,280)}</g>${cross(1410,370,70,C.r)}${tx(1410,600,'সনদ না থাকলে',44,C.ink,800)}<g data-k="y_b1">${tx(1410,760,'পুরো শুল্ক',100,C.r,800)}</g><g data-k="y_b2">${docPage(1500,800,180,140,'Order',C.mute,2)}</g></g>`,
 upd(q,lt,t,bt){rdU(q,'y_',lt,t,1);popG(q('y_a'),lt,.2,t,0,40,0,.5);popIn(q('y_a1'),pe(lt,bt(0)-.1,.5),t,1,30,3);popG(q('y_b'),lt,bt(1)+.3,t,2,40,0,.5);popIn(q('y_b1'),pe(lt,bt(2)-.1,.5),t,3,30,0);
  const f=cl((lt-bt(3))/1.2);T(q('y_b2'),{x:L(0,320,eio(f)),y:L(0,-700,eio(f)),r:f*40,o:1-f})}});

// 05 — REX in EU
K.ep_rex=()=>({svg:`${BG}${rd('x_')}
 <g data-k="x_e">${card(100,180,700,780,'#fff',44)}${eu(450,380,1.6)}${tx(450,620,'ইউরোপের জিএসপি',48,C.ink,800)}</g>
 <g data-k="x_d">${card(880,180,940,330,'#fff',44)}<ellipse cx="1060" cy="290" rx="90" ry="30" fill="${C.b}"/><rect x="970" y="290" width="180" height="120" fill="${C.b}"/><ellipse cx="1060" cy="410" rx="90" ry="30" fill="${C.bd}"/>${lat(1060,365,'REX',40,'#fff',800)}${tx(1220,330,'রেক্স পদ্ধতি',52,C.ink,800,'start')}${lat(1220,400,'Registered Exporter System',28,C.mute,700,'start')}</g>
 <g data-k="x_s">${card(880,550,940,200,'#fff',40)}${docPage(920,575,140,150,'',C.g,3)}${lat(1100,640,'Statement on origin',38,C.g,800,'start')}${tx(1100,700,'রপ্তানিকারকের নিজের ঘোষণা',32,C.ink,800,'start')}</g>
 <g data-k="x_r">${card(880,790,940,170,C.gd,40)}${check(960,875,40,C.g2)}${tx(1030,890,'আগে ইপিবির মাধ্যমে রেক্সে নিবন্ধন',40,'#fff',800,'start')}</g>`,
 upd(q,lt,t,bt){rdU(q,'x_',lt,t,1);popG(q('x_e'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.5);popG(q('x_d'),lt,bt(1)-.2,t,1,30,0,.5);popG(q('x_s'),lt,bt(2)-.2,t,2,30,0,.5);popG(q('x_r'),lt,bt(3)-.2,t,3,30,0,.5)}});

// 06 — point 2: 1–5 year term
K.ep_term=()=>({svg:`${BG}${rd('t_')}${ttl2('t_','২','মেয়াদ এক থেকে পাঁচ বছর',C.t)}
 <g data-k="t_c">${cal(110,340,300,'২০২৩','থেকে',C.t)}${tx(260,720,'আগে: এক বছর',36,C.mute,800)}</g>
 <g data-k="t_s">${card(500,360,1320,380,'#fff',44)}<rect x="600" y="540" width="1120" height="20" rx="10" fill="#e2e8f0"/><rect data-k="t_f" x="600" y="540" width="0" height="20" rx="10" fill="${C.t}"/>
  ${[1,2,3,4,5].map(i=>`<g data-k="t_y${i}"><circle cx="${600+(i-1)*280}" cy="550" r="40" fill="#fff" stroke="${C.t}" stroke-width="8"/>${tx(600+(i-1)*280,568,BN(i),40,C.t,800)}${tx(600+(i-1)*280,650,'বছর',28,C.mute,800)}</g>`).join('')}<g data-k="t_h"><circle cx="0" cy="0" r="30" fill="${C.t}"/></g></g>
 <g data-k="t_d">${card(500,790,1320,190,'#eef9f6',40)}${icon('cal',600,885,80,C.t,7)}${tx(680,900,'মেয়াদ গোনা হয় ইস্যু বা নবায়নের দিন থেকে',42,C.ink,800,'start')}</g>`,
 upd(q,lt,t,bt){rdU(q,'t_',lt,t,2);ttlU(q,'t_',lt,t);popG(q('t_c'),lt,bt(1)-.3,t,0,40,2,.5);popG(q('t_s'),lt,bt(2)-.6,t,1,30,0,.5);const k=eio(cl((lt-bt(2))/1.6));setW(q('t_f'),1120*k);T(q('t_h'),{x:600+1120*k,y:550,o:lt>bt(2)?1:0});
  for(let i=1;i<=5;i++)T(q('t_y'+i),{s:k*4>=i-1?1.08:1,o:1});popG(q('t_d'),lt,bt(3)-.2,t,2,30,0,.5)}});

// 07 — online on EMS
K.ep_online=()=>({svg:`${BG}${rd('o_')}
 <g data-k="o_l">${laptop(960,560,4.2,C.b)}</g>
 <g data-k="o_u">${card(560,320,800,90,'#fff',45)}${lat(960,378,'ems.epb.gov.bd',44,C.b,800)}</g>
 <g data-k="o_b">${card(620,620,320,90,C.g,45)}${lat(780,678,'Apply',36,'#fff',800)}${card(980,620,320,90,C.o,45)}${lat(1140,678,'Renew',36,'#fff',800)}</g>
 ${kw('o_w',960,960,'আবেদন ও নবায়ন, দুটোই অনলাইনে',52,'#fff',C.gd)}`,
 upd(q,lt,t,bt){rdU(q,'o_',lt,t,2);popG(q('o_l'),lt,.15,t,0,40,0,.5);popG(q('o_u'),lt,bt(1)-.4,t,1,20,0,.4);popG(q('o_b'),lt,bt(1)+.2,t,2,20,3,.4);kwU(q,'o_w',lt,Math.min(bt(0),.5),t)}});

// 08 — documents
K.ep_docs=()=>{const D=[['ট্রেড লাইসেন্স','Trade licence',C.b],['ই টিন','e-TIN',C.t],['ইআরসি','ERC',C.g],['ভ্যাট নিবন্ধন','VAT',C.o],['সদস্য সনদ','Membership',C.p]];return{svg:`${BG}${rd('d_')}
 ${kw('d_w',960,230,'সাধারণত যা লাগে',64,C.gd)}
 ${D.map((d,i)=>`<g data-k="d_d${i}">${card(90+i*352,320,330,560,'#fff',36)}${docPage(150+i*352,370,210,280,d[1],d[2],5)}${tx(255+i*352,740,d[0],38,C.ink,800)}<g data-k="d_k${i}">${check(255+i*352,820,36,C.g)}</g></g>`).join('')}`,
 upd(q,lt,t,bt){rdU(q,'d_',lt,t,2);kwU(q,'d_w',lt,.15,t);for(let i=0;i<5;i++){popG(q('d_d'+i),lt,Math.min(bt(i)-.3,.4+i*.35),t,i,40,3,.45);popIn(q('d_k'+i),pe(lt,bt(i)+.1,.3),t,i,0,0)}}}};

// 09 — point 3: less hassle
K.ep_easy=()=>({svg:`${BG}${rd('e_')}${ttl2('e_','৩','প্রতি বছরের ঝামেলা কম',C.g)}
 <g data-k="e_a">${card(100,330,820,640,'#fff4f2',44)}${tx(510,410,'আগে',44,C.r,800)}${[0,1,2,3,4].map(i=>`<g data-k="e_c${i}">${cal(140+i*150,480,130,BN(2019+i).slice(2),'নবায়ন',C.r)}</g>`).join('')}${tx(510,760,'প্রতি বছর আবেদন, লাইন, কাগজ',36,C.ink,800)}</g>
 <g data-k="e_b">${card(1000,330,820,640,'#e9f8ec',44)}${tx(1410,410,'এখন',44,C.g,800)}${enrCard(1180,460,460,290,'Valid: 5 years',C.g)}${tx(1410,840,'একবার আবেদন, পাঁচ বছর নিশ্চিন্ত',36,C.g,800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'e_',lt,t,3);ttlU(q,'e_',lt,t);popG(q('e_a'),lt,bt(1)-.4,t,0,40,0,.5);for(let i=0;i<5;i++)popIn(q('e_c'+i),pe(lt,bt(1)-.2+i*.15,.3),t,i,20,0);popG(q('e_b'),lt,bt(2)-.3,t,1,40,0,.5);if(lt>bt(3))T(q('e_b'),{s:1+.015*Math.sin(t*4),o:1})}});
