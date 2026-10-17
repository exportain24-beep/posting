// ===================== Dalal + Docs 16:9 — scenes 00–13 =====================
// 00 hook
K.dl_hook=()=>({svg:`${BG}
 <g data-k="h_l">${card(80,170,820,620,'#fff',44)}<g data-k="h_b">${brk(650,380,1.15)}</g>${tx(650,700,'দালাল',44,C.ink,800)}</g>
 ${[0,1,2].map(i=>`<g data-k="h_m${i}">${cash(0,0,1)}</g>`).join('')}
 <g data-k="h_r">${card(180,820,620,150,'#fff4f2',40)}${tx(440,912,'রসিদ?',56,C.ink,800)}${cross(640,895,40,C.r)}</g>
 <g data-k="h_e">${card(1000,170,840,330,'#fff',44)}<rect x="1000" y="170" width="840" height="80" rx="44" fill="${C.b}"/><rect x="1000" y="210" width="840" height="40" fill="${C.b}"/>${lat(1050,225,'From: Buyer',30,'#fff',800,'start')}${lat(1060,330,'Please send your ERC copy today.',36,C.ink,800,'start')}${lat(1060,400,'Thanks!',32,C.mute,700,'start')}</g>
 <g data-k="h_p">${[0,1,2,3,4].map(i=>`<g transform="rotate(${[-14,9,-5,16,-9][i]} ${1240+i*60} ${740})">${docPage(1140+i*60,590,200,250,'',[C.o,C.t,C.p,C.b,C.mute][i],3)}</g>`).join('')}</g>
 ${kw('h_q',1420,960,'কোথায় গেল কাগজটা?',46,'#fff',C.r)}
 ${kw('h_w',960,560,'আজ দুটো সমাধান',90,'#fff',C.gd)}`,
 upd(q,lt,t,bt){popG(q('h_l'),lt,.1,t,0,40,2,.45);for(let i=0;i<3;i++){const p=pe(lt,bt(0)+i*.25,.6);T(q('h_m'+i),{x:L(-150,600,eo(p)),y:L(500,470,eo(p))-Math.sin(p*3.14)*120,r:p*200,o:p>0&&p<1?1:0})}
  popG(q('h_r'),lt,bt(1)-.1,t,1,30,0,.45);popG(q('h_e'),lt,bt(2)-.3,t,2,30,0,.45);popG(q('h_p'),lt,bt(3)-.4,t,3,30,0,.45);if(lt>bt(3))T(q('h_p'),{x:Math.sin(t*18)*cl((bt(3)+1-lt))*8,o:1});kwU(q,'h_q',lt,bt(3)+.2,t);
  const w=pe(lt,bt(4)-.1,.5);T(q('h_w'),{s:L(.3,1,eb(w)),o:cl(w*3)});for(const k of ['h_l','h_r','h_e','h_p','h_q'])if(w>0)fadeMul(q(k),1-w*.75)}});

// 01 story
K.dl_story=()=>({svg:`${BG}
 <g data-k="s_p">${card(100,170,560,800,'#fff',44)}${woman2(380,330,1.2)}${tx(380,640,'রুমানা · সিলেট',50,C.ink,800)}${pill(380,720,'কাল্পনিক চরিত্র',C.p,32)}<g data-k="s_mt">${mat(190,770,380,130)}${tx(380,955,'শীতলপাটি',30,C.mute,800)}</g></g>
 <g data-k="s_b">${card(1240,170,580,560,'#fff',44)}${brk(1530,330,1)}${tx(1530,640,'দালাল',44,C.ink,800)}</g>
 <g data-k="s_f">${docPage(0,0,180,220,'Files',C.o,4)}</g>
 <g data-k="s_c">${card(740,770,1080,200,'#fff4f2',40)}${tx(800,850,'খরচ',40,C.r,800,'start')}${meter(920,815,820,50,C.r,'s_mt2')}${tx(800,930,'কাগজ রইল অন্যের হাতে',36,C.ink,800,'start')}${icon('lock',1500,915,60,C.r,7)}</g>`,
 upd(q,lt,t,bt){popG(q('s_p'),lt,.1,t,0,40,2,.45);if(lt>.8)T(q('s_p'),{y:Math.sin(lt*2)*8,o:1});popIn(q('s_mt'),pe(lt,bt(1)-.1,.4),t,1,20,0);popG(q('s_b'),lt,bt(2)-.3,t,1,40,2,.45);
  const f=pe(lt,bt(2),.9);T(q('s_f'),{x:L(560,1440,eo(f)),y:L(380,330,eo(f))-Math.sin(f*3.14)*120,r:f*8,s:L(1,.6,f),o:f>0?1:0});
  popG(q('s_c'),lt,bt(3)-.3,t,2,30,0,.45);fillTo(q('s_mt2'),lt,bt(3),720,1.6)}});

// 02 two parts
K.dl_parts=()=>({svg:`${BG}
 ${kw('p_h',960,230,'আজ দুই ভাগে',72,C.gd)}
 <g data-k="p_a">${card(120,320,800,620,'#fff',50)}<rect x="120" y="320" width="800" height="120" rx="50" fill="${C.o}"/><rect x="120" y="390" width="800" height="50" fill="${C.o}"/>${tx(520,405,'ভাগ ক',56,'#fff',800)}${brk(520,580,.85)}${slash(520,640,190)}${tx(520,880,'দালাল ছাড়া লাইসেন্স',50,C.ink,800)}</g>
 <g data-k="p_b">${card(1000,320,800,620,'#fff',50)}<rect x="1000" y="320" width="800" height="120" rx="50" fill="${C.p}"/><rect x="1000" y="390" width="800" height="50" fill="${C.p}"/>${tx(1400,405,'ভাগ খ',56,'#fff',800)}<g transform="translate(1400 640) scale(1.6)">${folder(-80,-56,C.o)}</g>${tx(1400,880,'কাগজ গোছানোর সিস্টেম',50,C.ink,800)}</g>`,
 upd(q,lt,t,bt){kwU(q,'p_h',lt,.1,t);popG(q('p_a'),lt,bt(1)-.3,t,0,40,2,.45);popG(q('p_b'),lt,bt(2)-.3,t,1,40,2,.45)}});

// 03 A1 cost
K.dl_cost=()=>{const R=[['সরকারি ফি',C.g,300],['দালালের চার্জ',C.r,420],['যাতায়াত ও যোগাযোগ',C.o,220]];return{svg:`${BG}${rd('c_','A')}${ttl2('c_','১','দালালে খরচ বাড়ে',C.r)}
 <g data-k="c_bx">${card(100,320,1100,660,'#fff',44)}${tx(160,400,'আপনার মোট খরচ',40,C.ink,800,'start')}
  ${R.map((r,i)=>`<g data-k="c_r${i}">${tx(160,500+i*130,r[0],36,C.ink,800,'start')}${meter(560,465+i*130,560,56,r[1],'c_m'+i)}</g>`).join('')}
  <rect x="160" y="860" width="960" height="6" rx="3" fill="#e2e8f0"/>${tx(160,930,'মোট',40,C.ink,800,'start')}${meter(560,895,560,56,C.ink,'c_tot')}</g>
 <g data-k="c_ar">${card(1280,320,540,660,'#fff4f2',44)}${tx(1550,520,'↑',200,C.r,800)}${tx(1550,720,'খরচ বাড়ে',56,C.r,800)}${tx(1550,800,'হয়রানিও বাড়ে',40,C.ink,800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'c_',lt,t,1);ttlU(q,'c_',lt,t);popG(q('c_bx'),lt,bt(1)-.4,t,0,30,0,.45);const B=[bt(2),bt(3),bt(4)];for(let i=0;i<3;i++){popIn(q('c_r'+i),pe(lt,B[i]-.3,.3),t,i,20,0);fillTo(q('c_m'+i),lt,B[i],R[i][2],.7)}
  const tot=(lt>B[0]?R[0][2]*cl((lt-B[0])/.7):0)+(lt>B[1]?R[1][2]*cl((lt-B[1])/.7):0)*.25+(lt>B[2]?R[2][2]*cl((lt-B[2])/.7):0)*.25;const e=q('c_tot');if(e)setW(e,Math.min(560,tot*1.0));popG(q('c_ar'),lt,bt(1),t,1,40,2,.45);if(lt>bt(1)+.5)T(q('c_ar'),{y:Math.sin(t*3)*6,o:1})}}};

// 04 A1 no learning
K.dl_learn=()=>{const E=[['নবায়ন',C.b],['ঠিকানা বদল',C.t],['নতুন সনদ',C.p]];return{svg:`${BG}${rd('l_','A')}
 <g data-k="l_a">${card(100,200,620,780,'#fff',44)}${tx(410,290,'আপনার শেখা',46,C.ink,800)}<circle cx="410" cy="560" r="190" fill="none" stroke="#e2e8f0" stroke-width="40"/><circle data-k="l_g" cx="410" cy="560" r="190" fill="none" stroke="${C.r}" stroke-width="40" stroke-dasharray="0 1200" transform="rotate(-90 410 560)"/>${tx(410,600,'০%',110,C.r,800)}${tx(410,880,'কিছুই শেখা হয় না',44,C.r,800)}</g>
 <g data-k="l_b">${card(800,200,1020,780,'#fff',44)}<g data-k="l_bk">${brk(1310,520,1)}</g>${tx(1310,800,'আবার দালালের কাছে',44,C.ink,800)}</g>
 ${E.map((e,i)=>`<g data-k="l_e${i}">${pill(0,0,e[0],e[1],34)}</g>`).join('')}
 ${kw('l_k',1310,920,'প্রতিবার নতুন খরচ',44,'#fff',C.r)}`,
 upd(q,lt,t,bt){rdU(q,'l_',lt,t,1);popG(q('l_a'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.45);const g=q('l_g');if(g)g.setAttribute('stroke-dasharray',`${(12+Math.sin(t*5)*6).toFixed(1)} 1200`);if(lt>bt(1))T(q('l_a'),{s:1+.015*Math.sin(t*6),o:1});
  popG(q('l_b'),lt,bt(1)+.2,t,1,40,2,.45);const P=[[960,330],[1660,330],[1000,680]];for(let i=0;i<3;i++){const p=pe(lt,bt(2+i)-.1,.5),k=((lt-bt(2+i))%2.4+2.4)%2.4/2.4;T(q('l_e'+i),{x:P[i][0]+(lt>bt(2+i)+.5?Math.sin(t*2+i)*8:0),y:P[i][1],s:L(.3,1,eb(p)),o:cl(p*3)})}kwU(q,'l_k',lt,bt(5),t)}}};

// 05 A2 e-TIN
K.dl_etin=()=>({svg:`${BG}${rd('e_','A')}${ttl2('e_','২','নিজেই অনলাইনে',C.r)}
 <g data-k="e_br">${browser(100,320,1040,660,'secure.incometax.gov.bd',C.gd)}${lat(620,460,'e-TIN Registration',48,C.gd,800)}${tx(620,520,'ই টিআইএন · করদাতা শনাক্তকরণ নম্বর',32,C.mute,800)}
  ${field(200,600,840,'NID / Passport',C.g,'e_f0')}${field(200,720,840,'Mobile number',C.g,'e_f1')}<g data-k="e_bt">${card(420,830,400,90,C.g,45)}${lat(620,888,'Register',34,'#fff',800)}</g></g>
 <g data-k="e_c">${card(1220,320,600,500,'#fffbeb',36)}<rect x="1236" y="336" width="568" height="468" rx="26" fill="none" stroke="#c9a227" stroke-width="4"/>${lat(1520,420,'e-TIN Certificate',40,C.ink,800)}<rect x="1300" y="470" width="260" height="14" rx="7" fill="#e7dcb8"/><rect x="1300" y="510" width="200" height="14" rx="7" fill="#e7dcb8"/><rect x="1300" y="550" width="230" height="14" rx="7" fill="#e7dcb8"/>${qr(1590,600,170)}${check(1360,700,44,C.g)}</g>
 <g data-k="e_z">${card(1220,850,600,130,C.gd,40)}${tx(1520,935,'সরকারি ফি: ০ টাকা',50,'#fff',800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'e_',lt,t,2);ttlU(q,'e_',lt,t);popG(q('e_br'),lt,Math.min(bt(2)-.4,.9),t,0,30,0,.45);if(lt>1.5)T(q('e_br'),{y:Math.sin(lt*2)*8,o:1});fillTo(q('e_f0'),lt,bt(3),840,.8);fillTo(q('e_f1'),lt,bt(3)+.6,840,.8);T(q('e_bt'),{s:lt>bt(4)-.3&&lt<bt(4)-.05?.93:1,o:1});popG(q('e_c'),lt,bt(4)-.1,t,1,40,3,.5);popG(q('e_z'),lt,bt(5)-.2,t,2,30,0,.45);if(lt>bt(5)+.4)T(q('e_z'),{s:1+.025*Math.sin(t*6),o:1})}});

// 06 A2 ERC
K.dl_erc=()=>({svg:`${BG}${rd('r_','A')}
 <g data-k="r_c">${ercCard(100,200,600,440)}${tx(400,720,'ইআরসি · রপ্তানি নিবন্ধন সনদ',38,C.ink,800)}</g>
 <g data-k="r_b">${browser(780,200,1040,520,'olm.ccie.gov.bd',C.b)}${lat(1300,330,'Online Licensing Module',44,C.b,800)}${lat(1300,385,'Office of the CCI&E',30,C.mute,700)}
  ${['New ERC','Renewal','Fee payment'].map((l,i)=>`<g data-k="r_i${i}">${card(840+i*320,450,290,200,'#f1f5f9',24)}${icon(['doc','cal','check'][i],985+i*320,520,80,[C.b,C.t,C.g][i],7)}${lat(985+i*320,620,l,28,C.ink,800)}</g>`).join('')}</g>
 <g data-k="r_p">${card(780,770,1040,200,'#e9f8ec',40)}${icon('lock',880,870,80,C.g,7)}${lat(960,850,'Sonali Payment Gateway',40,C.g,800,'start')}${tx(960,920,'ফি দেওয়া যায় অনলাইনেই',36,C.ink,800,'start')}${check(1740,870,44,C.g)}</g>`,
 upd(q,lt,t,bt){rdU(q,'r_',lt,t,2);popG(q('r_c'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.45);popG(q('r_b'),lt,bt(1)-.3,t,1,30,0,.45);for(let i=0;i<3;i++)popIn(q('r_i'+i),pe(lt,bt(2)-.2+i*.25,.35),t,i,20,0);popG(q('r_p'),lt,bt(3)-.3,t,2,30,0,.45)}});

// 07 A2 BSW + EPB
K.dl_bsw=()=>{const G=[['e-TIN','আয়কর বিভাগ',C.gd,'secure.incometax.gov.bd'],['ERC','সিসিআইই',C.b,'olm.ccie.gov.bd'],['BSW','১৯টি সংস্থার সনদ',C.t,'bswnbr.gov.bd'],['EPB Enrolment','রপ্তানি উন্নয়ন ব্যুরো',C.o,'ems.epb.gov.bd']];return{svg:`${BG}${rd('b_','A')}
 ${G.map((g,i)=>{const x=100+(i%2)*880,y=200+Math.floor(i/2)*390;return `<g data-k="b_g${i}">${card(x,y,840,350,'#fff',40)}<rect x="${x}" y="${y}" width="18" height="350" fill="${g[2]}"/>${lat(x+60,y+120,g[0],g[0].length>6?60:80,g[2],800,'start')}${tx(x+60,y+200,g[1],38,C.ink,800,'start')}${lat(x+60,y+280,g[3],28,C.mute,700,'start')}<g data-k="b_k${i}">${check(x+740,y+100,50,C.g)}</g></g>`}).join('')}
 ${kw('b_w',960,1010,'সবই অনলাইনে',52,'#fff',C.g)}`,
 upd(q,lt,t,bt){rdU(q,'b_',lt,t,2);const B=[.1,.35,bt(0)-.2,bt(2)-.2];for(let i=0;i<4;i++){popG(q('b_g'+i),lt,B[i],t,i,40,2,.45);popIn(q('b_k'+i),pe(lt,i<2?.9+i*.2:B[i]+.8,.35),t,i,0,0)}kwU(q,'b_w',lt,bt(3),t)}}};

// 08 A3 citizen charter
K.dl_fee=()=>{const R=[['ERC নিবন্ধন','৭ দিন*','নির্ধারিত'],['ERC নবায়ন','৩ দিন*','নির্ধারিত'],['EPB এনরোলমেন্ট','—','নির্ধারিত']];return{svg:`${BG}${rd('f_','A')}${ttl2('f_','৩','ফি আগে নিজে দেখুন',C.t)}
 <g data-k="f_bd">${card(100,320,1300,660,'#fff',44)}<rect x="100" y="320" width="1300" height="110" rx="44" fill="${C.t}"/><rect x="100" y="390" width="1300" height="40" fill="${C.t}"/>${lat(160,392,'Citizen Charter',44,'#fff',800,'start')}${tx(1340,392,'সিটিজেন চার্টার',40,'#fff',800,'end')}
  ${['সেবা','সময়','ফি'].map((h,i)=>`<g data-k="f_h${i}"><rect x="${140+[0,600,920][i]}" y="460" width="${[560,300,400][i]}" height="80" rx="16" fill="#e6f4f1"/>${tx(160+[0,600,920][i],515,h,38,C.t,800,'start')}</g>`).join('')}
  ${[0,1,2].map(r=>`<g data-k="f_r${r}"><rect x="140" y="${570+r*120}" width="1220" height="100" rx="16" fill="#f8fafc"/>${[0,1,2].map(c=>`<rect x="${170+[0,600,920][c]}" y="${605+r*120}" width="${[360,180,240][c]}" height="30" rx="15" fill="#cbd5e1"/>`).join('')}</g>`).join('')}</g>
 <g data-k="f_m">${card(1460,320,360,660,'#fff',44)}<g data-k="f_mg">${mag(1640,600,1.6,C.t)}</g>${tx(1640,860,'নিজে মিলিয়ে নিন',36,C.ink,800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'f_',lt,t,3);ttlU(q,'f_',lt,t);popG(q('f_bd'),lt,bt(2)-.4,t,0,30,0,.45);for(let i=0;i<3;i++){popIn(q('f_h'+i),pe(lt,bt(3+i)-.15,.3),t,i,10,0);popIn(q('f_r'+i),pe(lt,bt(2)+.2+i*.2,.3),t,i,20,0)}
  for(let i=0;i<3;i++){const h=q('f_h'+i);if(h&&lt>bt(3+i))T(h,{s:lt<bt(3+i)+.8?1.06:1,o:1})}popG(q('f_m'),lt,bt(1)-.2,t,1,40,2,.45);T(q('f_mg'),{x:Math.sin(t*1.6)*30,y:Math.cos(t*1.3)*20,o:1})}}};

// 09 A3 where
K.dl_where=()=>({svg:`${BG}${rd('w_','A')}
 <g data-k="w_a">${browser(100,200,840,560,'olm.ccie.gov.bd',C.b)}${lat(520,330,'Fees & Notices',44,C.b,800)}${[0,1,2].map(i=>`<g><rect x="160" y="${400+i*100}" width="720" height="76" rx="16" fill="#f1f5f9"/>${icon('doc',210,438+i*100,44,C.b,6)}<rect x="260" y="${428+i*100}" width="${[420,360,300][i]}" height="22" rx="11" fill="#cbd5e1"/></g>`).join('')}</g>
 <g data-k="w_b">${browser(980,200,840,560,'bangladesh.eregulations.org',C.t)}${lat(1400,330,'Step by step',44,C.t,800)}${[0,1,2,3].map(i=>`<g data-k="w_s${i}"><circle cx="1080" cy="${420+i*85}" r="30" fill="${C.t}"/>${lat(1080,432+i*85,String(i+1),30,'#fff',800)}<rect x="1130" y="${408+i*85}" width="${[560,480,520,420][i]}" height="24" rx="12" fill="#cbd5e1"/></g>`).join('')}</g>
 <g data-k="w_n">${card(560,800,800,180,'#fffbeb',40)}${icon('cal',660,890,80,C.o,7)}${tx(740,880,'ফি মাঝে মাঝে বদলায়',38,C.ink,800,'start')}${tx(740,940,'সর্বশেষ নোটিশটাই দেখুন',38,C.o,800,'start')}</g>`,
 upd(q,lt,t,bt){rdU(q,'w_',lt,t,3);popG(q('w_a'),lt,Math.min(bt(0)-.3,.2),t,0,30,0,.45);popG(q('w_b'),lt,bt(1)-.2,t,1,30,0,.45);for(let i=0;i<4;i++)popIn(q('w_s'+i),pe(lt,bt(2)+i*.25,.3),t,i,20,0);popG(q('w_n'),lt,bt(3)-.2,t,2,30,0,.45);if(lt>bt(4))T(q('w_n'),{s:1+.02*Math.sin(t*6),o:1})}});

// 10 A4 receipt
K.dl_receipt=()=>({svg:`${BG}${rd('x_','A')}${ttl2('x_','৪','রসিদ ছাড়া টাকা নয়',C.g)}
 <g data-k="x_c">${card(100,320,520,640,'#fff4f2',44)}${cash(360,520,1.5)}${slash(360,520,150)}${tx(360,780,'রসিদ নেই?',48,C.r,800)}${tx(360,850,'টাকা নয়',48,C.ink,800)}</g>
 <g data-k="x_ph">${phone(700,300,380,680)}<g data-k="x_ok"><circle cx="890" cy="500" r="80" fill="${C.g}"/>${check(890,500,50,C.g)}${lat(890,640,'Payment',34,C.ink,800)}${lat(890,685,'Successful',34,C.g,800)}</g></g>
 <g data-k="x_r">${card(1160,320,660,640,'#fff',36)}<path d="M1160 930 ${Array.from({length:11},(_,i)=>`l30 30 l30 -30`).join(' ')}" fill="none"/>${lat(1490,420,'RECEIPT',52,C.ink,800)}${tx(1490,480,'রসিদ',34,C.mute,800)}
  <g data-k="x_no"><rect x="1220" y="530" width="540" height="90" rx="16" fill="#e9f8ec"/>${lat(1250,590,'Challan No: ••••••',34,C.g,800,'start')}</g>
  <rect x="1220" y="650" width="400" height="20" rx="10" fill="#e2e8f0"/><rect x="1220" y="690" width="300" height="20" rx="10" fill="#e2e8f0"/>
  <g data-k="x_dl">${card(1300,780,380,110,C.b,55)}${icon('arrow',1370,835,56,'#fff',8)}${lat(1530,850,'Download',34,'#fff',800)}</g></g>`,
 upd(q,lt,t,bt){rdU(q,'x_',lt,t,4);ttlU(q,'x_',lt,t);popG(q('x_c'),lt,bt(1)-.3,t,0,40,2,.45);popG(q('x_ph'),lt,bt(2)-.4,t,1,30,0,.45);popIn(q('x_ok'),pe(lt,bt(2)+.2,.4),t,1,0,0);popG(q('x_r'),lt,bt(3)-.4,t,2,30,0,.45);popIn(q('x_no'),pe(lt,bt(3),.35),t,2,10,0);popG(q('x_dl'),lt,bt(4)-.2,t,3,20,0,.4);if(lt>bt(4)+.4)T(q('x_dl'),{y:Math.abs(Math.sin(t*4))*-8,o:1})}});

// 11 A4 stop
K.dl_stop=()=>{const M=['দ্রুত করে দেব!','একটু বাড়তি দিন…','রসিদ লাগবে না'];return{svg:`${BG}${rd('s_','A')}
 <g data-k="s_bk">${card(100,200,520,780,'#fff',44)}${brk(360,420,1.2)}${tx(360,780,'দালাল',44,C.ink,800)}</g>
 ${M.map((m,i)=>`<g data-k="s_m${i}">${bub(980,300+i*170,620,m,'#fff',C.ink,40,-1)}</g>`).join('')}
 <g data-k="s_st">${octo(1560,560,220)}${lat(1560,545,'STOP',90,'#fff',800)}${tx(1560,630,'থামুন',56,'#fff',800)}</g>
 <g data-k="s_pr">${card(700,830,700,150,C.gd,40)}${shield(800,905,.7,C.g2,'✓')}${tx(1100,925,'রসিদ মানে প্রমাণ',48,'#fff',800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'s_',lt,t,4);popG(q('s_bk'),lt,.1,t,0,40,2,.45);for(let i=0;i<3;i++)popG(q('s_m'+i),lt,bt(i)-.2,t,i,20,0,.35);const s=pe(lt,bt(3)-.1,.4);T(q('s_st'),{s:L(2.2,1,eb(s))+(s>=1?.03*Math.sin(t*8):0),r:L(-20,0,eo(s)),o:cl(s*3)});if(s>0)for(let i=0;i<3;i++)fadeMul(q('s_m'+i),1-s*.6);popG(q('s_pr'),lt,bt(4)-.2,t,3,30,0,.45)}}};

// 12 A5 professionals
K.dl_pro=()=>{const P=[['C&F Agent','লাইসেন্সপ্রাপ্ত, কাস্টমস খালাস','truck',C.b],['Lawyer','আইনজীবী','doc',C.p],['Chartered Accountant','চার্টার্ড অ্যাকাউন্ট্যান্ট','star',C.t],['AD Bank','এডি ব্যাংক','bld',C.g]];return{svg:`${BG}${rd('o_','A')}${ttl2('o_','৫','পেশাদার পরামর্শ নিন',C.gd)}
 <g data-k="o_x">${card(1300,170,520,110,'#fff4f2',36)}${tx(1500,243,'দালাল নয়',44,C.r,800)}${cross(1370,225,32,C.r)}</g>
 ${P.map((p,i)=>`<g data-k="o_c${i}">${card(100+i*440,330,410,640,'#fff',40)}<circle cx="${305+i*440}" cy="500" r="110" fill="${p[3]}" opacity=".14"/>${icon(p[2],305+i*440,500,120,p[3],7)}${lat(305+i*440,700,p[0],p[0].length>12?28:40,p[3],800)}${tx(305+i*440,780,p[1],p[1].length>16?26:34,C.ink,800)}${check(305+i*440,880,34,C.g)}</g>`).join('')}`,
 upd(q,lt,t,bt){rdU(q,'o_',lt,t,5);ttlU(q,'o_',lt,t);popG(q('o_x'),lt,bt(1)-.1,t,0,30,0,.4);for(let i=0;i<4;i++)popG(q('o_c'+i),lt,bt(2+i)-.25,t,i,40,3,.45)}}};

// 13 A5 difference
K.dl_diff=()=>{const R=['লিখিত ফি আগে','রসিদ','কাজ বুঝিয়ে দেন'];return{svg:`${BG}${rd('d_','A')}
 <g data-k="d_t">${card(100,190,1200,640,'#fff',44)}<rect x="560" y="210" width="340" height="100" rx="24" fill="#fff4f2"/>${tx(730,278,'দালাল',44,C.r,800)}<rect x="930" y="210" width="340" height="100" rx="24" fill="#e9f8ec"/>${tx(1100,278,'পেশাদার',44,C.g,800)}
  ${R.map((r,i)=>`<g data-k="d_r${i}"><rect x="130" y="${340+i*160}" width="1140" height="140" rx="20" fill="#f8fafc"/>${tx(160,425+i*160,r,42,C.ink,800,'start')}${cross(730,410+i*160,40,C.r)}<g data-k="d_k${i}">${check(1100,410+i*160,40,C.g)}</g></g>`).join('')}</g>
 <g data-k="d_h">${card(1360,190,460,640,C.gd,44)}${icon('phone',1590,360,120,'#fff',7)}${lat(1590,520,'BSW Hotline',40,'#d9f5c4',800)}${lat(1590,640,'16139',100,'#fff',800)}${tx(1590,740,'বিএসডব্লিউ সাহায্য',34,'#d9f5c4',800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'d_',lt,t,5);popG(q('d_t'),lt,Math.min(bt(0)-.3,.2),t,0,30,0,.45);for(let i=0;i<3;i++){popIn(q('d_r'+i),pe(lt,bt(1+i)-.25,.3),t,i,20,0);popIn(q('d_k'+i),pe(lt,bt(1+i)+.1,.35),t,i,0,0)}popG(q('d_h'),lt,bt(4)-.3,t,1,40,2,.45);if(lt>bt(4)+.5)T(q('d_h'),{r:Math.sin(t*9)*1.2,o:1})}}};
