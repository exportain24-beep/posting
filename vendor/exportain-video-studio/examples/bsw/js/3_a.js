// ===================== BSW 16:9 — scenes 00–09 =====================
const AG=['DGDA','EPB','BSTI','PQW','DOF','DLS','BIDA','BEPZA','BEZA','BGMEA','BKMEA','CCI&E','DoE','BTRC','DOEX','BNACWC','BAERA','BAEC','CAAB'];
const agTile=(x,y,l,on)=>`<g>${card(x,y,170,84,on?C.gd:'#fff',20)}${lat(x+85,y+54,l,l.length>5?24:30,on?'#fff':C.bd,800)}</g>`;
const winF=(x,y,w,h)=>`<g>${card(x,y,w,h,'#fff',30)}<rect x="${x}" y="${y}" width="${w}" height="80" rx="30" fill="${C.b}"/><rect x="${x}" y="${y+40}" width="${w}" height="40" fill="${C.b}"/>${lat(x+40,y+54,'Bangladesh Single Window',34,'#fff',800,'start')}${[0,1,2].map(i=>`<circle cx="${x+w-40-i*32}" cy="${y+40}" r="10" fill="#fff" opacity=".7"/>`).join('')}</g>`;
const bldg=(x,y,s,lab,col)=>`<g transform="translate(${x} ${y}) scale(${s})"><rect x="-70" y="-90" width="140" height="160" fill="${col}"/>${[0,1,2].map(r=>[0,1,2].map(c=>`<rect x="${-52+c*40}" y="${-72+r*44}" width="24" height="26" fill="#fff" opacity=".7"/>`).join('')).join('')}${lat(0,100,lab,26,C.ink,800)}</g>`;

// 00 — hook
K.bs_hook=()=>({svg:`${BG}
 <g data-k="h_c">${card(110,200,760,700,'#fff',44)}${lat(490,290,'CUSTOMS',56,C.bd,800)}${docPage(260,340,460,420,'Certificate (paper)',C.mute,6)}</g>
 <g data-k="h_s">${stampT(490,600,'গ্রহণযোগ্য নয়',C.r,58)}</g>
 ${kw('h_w0',1380,330,'কেন?',120,'#fff',C.b)}
 <g data-k="h_cal">${cal(1180,480,400,'১','জুলাই ২০২৫',C.r)}</g>
 ${kw('h_w1',1380,1010,'নিয়ম বদলে গেছে',56,'#fff',C.gd)}`,
 upd(q,lt,t,bt){popG(q('h_c'),lt,.15,t,0,40,2,.5);popIn(q('h_s'),pe(lt,bt(1)-.1,.4),t,1,0,0);kwU(q,'h_w0',lt,bt(2)-.1,t);popG(q('h_cal'),lt,bt(3)-.3,t,2,40,2,.5);kwU(q,'h_w1',lt,bt(3)+.3,t)}});

// 01 — story: Sumon, Khulna
K.bs_story=()=>({svg:`${BG}
 <g data-k="s_p">${card(100,170,560,780,'#fff',44)}${person(380,230,1,'s','s_sp')}${tx(380,560,'সুমন · খুলনা',50,C.ink,800)}${pill(380,650,'কাল্পনিক চরিত্র',C.p,32)}<g data-k="s_sh">${shrimp2(300,820,1.2)}${shrimp2(460,820,1)}</g></g>
 <g data-k="s_old">${card(740,170,1080,370,'#fff4f2',44)}${tx(800,240,'আগে',40,C.r,800,'start')}${bldg(940,370,.9,'Office 1',C.mute)}${bldg(1200,370,.9,'Office 2',C.mute)}${bldg(1460,370,.9,'Office 3',C.mute)}<path data-k="s_rt" d="M940 470 Q1070 520 1200 470 Q1330 520 1460 470" stroke="${C.r}" stroke-width="8" fill="none" stroke-dasharray="16 10"/></g>
 <g data-k="s_new">${card(740,580,1080,370,'#e9f8ec',44)}${tx(800,650,'এখন',40,C.g,800,'start')}${laptop(1060,800,1.8,C.b)}${lat(1440,770,'Bangladesh',40,C.b,800)}${lat(1440,830,'Single Window',44,C.b,800)}</g>`,
 upd(q,lt,t,bt){popG(q('s_p'),lt,.15,t,0,40,2,.5);if(lt>.8)T(q('s_p'),{y:Math.sin(lt*2.2)*10,r:Math.sin(lt*1.3)*.8,o:1});popIn(q('s_sh'),pe(lt,bt(1)-.1,.4),t,1,10,3);popG(q('s_old'),lt,bt(2)-.4,t,2,30,0,.5);popG(q('s_new'),lt,bt(3)-.2,t,3,30,0,.5);if(lt>bt(4))T(q('s_new'),{s:1+.012*Math.sin(t*4),o:1})}});

// 02 — point 1: what BSW is
K.bs_what=()=>({svg:`${BG}${rd('w_')}${ttl2('w_','১','বাংলাদেশ সিঙ্গেল উইন্ডো',C.b)}
 <g data-k="w_n">${card(100,330,600,640,'#fff',44)}${bank(400,620,1.5,C.bd)}${lat(400,800,'National Board of Revenue',30,C.bd,800)}${tx(400,860,'জাতীয় রাজস্ব বোর্ড',40,C.ink,800)}</g>
 <g data-k="w_f">${winF(780,330,1040,640)}
  ${[['Certificates','সনদ',C.g],['Licences','লাইসেন্স',C.t],['Permits','অনুমতি',C.o]].map((c,i)=>`<g data-k="w_c${i}">${card(830+i*330,460,300,360,'#f8fafc',26)}${docPage(890+i*330,490,180,200,c[0],c[2],4)}${tx(980+i*330,770,c[1],40,C.ink,800)}</g>`).join('')}
  <g data-k="w_one">${pill(1300,905,'সব এক জায়গায় · CLP',C.gd,32)}</g></g>`,
 upd(q,lt,t,bt){rdU(q,'w_',lt,t,1);ttlU(q,'w_',lt,t);popG(q('w_n'),lt,Math.min(bt(1)-.4,.7),t,0,40,2,.5);if(lt>1.4)T(q('w_n'),{y:Math.sin(lt*2)*10,o:1});popG(q('w_f'),lt,bt(2)-.6,t,1,30,0,.5);popIn(q('w_c0'),pe(lt,bt(2)-.1,.4),t,0,30,3);popIn(q('w_c1'),pe(lt,bt(2)+.4,.4),t,1,30,3);popIn(q('w_c2'),pe(lt,bt(3)-.1,.4),t,2,30,3);popG(q('w_one'),lt,bt(4)-.2,t,3,20,0,.4)}});

// 03 — how it flows
K.bs_how=()=>{const S=[['রপ্তানিকারক',C.b,'laptop'],['BSW',C.gd,'win'],['সংস্থা ✓',C.t,'bld'],['কাস্টমস',C.bd,'cust']];return{svg:`${BG}${rd('o_')}
 ${S.map((s,i)=>`<g data-k="o_s${i}">${card(110+i*450,300,360,460,'#fff',40)}<circle cx="${290+i*450}" cy="480" r="110" fill="${s[1]}"/>${s[2]=='laptop'?laptop(290+i*450,490,1,'#fff'):s[2]=='win'?`<rect x="${230+i*450}" y="420" width="120" height="120" rx="10" fill="#fff"/><path d="M${290+i*450} 420 V540 M${230+i*450} 480 H${350+i*450}" stroke="${s[1]}" stroke-width="8"/>`:s[2]=='bld'?icon('bld',290+i*450,480,110,'#fff',8):icon('doc',290+i*450,480,110,'#fff',8)}${tx(290+i*450,680,s[0],44,C.ink,800)}</g>${i<3?`<path data-k="o_a${i}" d="M${480+i*450} 530 H${550+i*450} M${525+i*450} 505 L${555+i*450} 530 L${525+i*450} 555" stroke="${C.gd}" stroke-width="10" fill="none"/>`:''}`).join('')}
 <g data-k="o_p">${card(500,830,920,170,'#fff4f2',40)}${docPage(560,850,110,130,'',C.mute,2)}${slash(615,915,70)}${tx(720,935,'আলাদা কাগজ বয়ে নেওয়ার দরকার নেই',40,C.ink,800,'start')}</g>`,
 upd(q,lt,t,bt){rdU(q,'o_',lt,t,1);const B=[bt(0)-.2,bt(0)+.6,bt(1)-.1,bt(2)-.1];for(let i=0;i<4;i++)popG(q('o_s'+i),lt,B[i],t,i,40,2,.45);for(let i=0;i<3;i++)T(q('o_a'+i),{o:lt>B[i+1]-.1?1:.12});popG(q('o_p'),lt,bt(3)-.2,t,4,30,0,.5)}}};

// 04 — point 2: mandatory since 1 July 2025
K.bs_rule=()=>({svg:`${BG}${rd('r_')}${ttl2('r_','২','১ জুলাই ২০২৫ থেকে বাধ্যতামূলক',C.r)}
 <g data-k="r_c">${cal(110,340,340,'১','জুলাই ২০২৫',C.r)}</g>
 <g data-k="r_g">${card(520,330,1300,420,'#fff',40)}${tx(1170,400,'উনিশটি সংস্থা',44,C.ink,800)}${AG.map((a,i)=>`<g data-k="r_t${i}">${agTile(560+(i%7)*180,430+Math.floor(i/7)*100,a,false)}</g>`).join('')}</g>
 <g data-k="r_x">${card(520,790,1300,200,'#fff4f2',40)}${docPage(580,810,130,160,'',C.mute,3)}${cross(645,890,46,C.r)}${lat(760,880,'Manual CLP not accepted',40,C.r,800,'start')}${tx(760,945,'কাগজের সনদ আর চলে না',38,C.ink,800,'start')}</g>`,
 upd(q,lt,t,bt){rdU(q,'r_',lt,t,2);ttlU(q,'r_',lt,t);popG(q('r_c'),lt,bt(1)-.3,t,0,40,2,.5);popG(q('r_g'),lt,bt(2)-.4,t,1,30,0,.5);for(let i=0;i<19;i++)popIn(q('r_t'+i),pe(lt,bt(2)-.2+i*.06,.25),t,i,10,0);popG(q('r_x'),lt,bt(3)-.2,t,2,30,0,.5);if(lt>bt(4))T(q('r_x'),{x:Math.sin(t*20)*cl((bt(4)+.8-lt)*2)*6,o:1})}});

// 05 — rollout across customs stations
K.bs_rollout=()=>{const P=[[560,330],[760,420],[640,560],[900,640],[820,820],[1120,760],[1020,460]];return{svg:`${BG}${rd('l_')}
 <g data-k="l_m">${card(300,170,1320,800,'#fff',44)}<path d="M600 230 Q760 200 860 300 Q1020 300 1060 420 Q1200 480 1160 620 Q1220 800 1060 860 Q980 960 860 880 Q760 940 700 840 Q560 820 560 680 Q460 560 540 440 Q500 300 600 230Z" fill="#e3f3e6" stroke="#bfe0c7" stroke-width="6"/>
  ${P.map((p,i)=>`<g data-k="l_p${i}"><circle cx="${p[0]}" cy="${p[1]}" r="26" fill="#cbd5e1" stroke="#fff" stroke-width="5"/></g><g data-k="l_q${i}"><circle cx="${p[0]}" cy="${p[1]}" r="26" fill="${C.g}" stroke="#fff" stroke-width="5"/>${check(p[0],p[1],14,C.g)}</g>`).join('')}
  ${tx(1400,420,'জুলাই',44,C.mute,800)}${tx(1400,500,'→ সেপ্টেম্বর',44,C.mute,800)}</g>
 ${kw('l_w',1400,700,'সব কাস্টমস স্টেশনে চালু',46,'#fff',C.g)}`,
 upd(q,lt,t,bt){rdU(q,'l_',lt,t,2);popG(q('l_m'),lt,.15,t,0,30,0,.5);for(let i=0;i<7;i++){const p=pe(lt,bt(0)-.2+i*.35,.3);T(q('l_q'+i),{s:L(.3,1,eb(p)),o:cl(p*3)})}kwU(q,'l_w',lt,bt(1),t)}}};

// 06 — point 3: agencies part 1
K.bs_ag1=()=>{const A=[['DGDA','ঔষধ প্রশাসন অধিদপ্তর',C.r],['EPB','রপ্তানি উন্নয়ন ব্যুরো',C.b],['BSTI','মান সনদ',C.o],['PQW','উদ্ভিদ সংগনিরোধ উইং',C.g],['DOF','মৎস্য অধিদপ্তর',C.t],['DLS','প্রাণিসম্পদ অধিদপ্তর',C.pk]];return{svg:`${BG}${rd('a_')}${ttl2('a_','৩','কোন সংস্থা?',C.t)}
 ${A.map((a,i)=>{const x=100+(i%3)*580,y=330+Math.floor(i/3)*330;return `<g data-k="a_c${i}">${card(x,y,540,290,'#fff',40)}<rect x="${x}" y="${y}" width="16" height="290" fill="${a[2]}"/>${lat(x+270,y+130,a[0],76,a[2],800)}${tx(x+270,y+220,a[1],34,C.ink,800)}</g>`}).join('')}`,
 upd(q,lt,t,bt){rdU(q,'a_',lt,t,3);ttlU(q,'a_',lt,t);for(let i=0;i<6;i++)popG(q('a_c'+i),lt,bt(i+1)-.2,t,i,40,3,.4)}}};

// 07 — agencies part 2 (all 19 shown)
K.bs_ag2=()=>{const H=['BIDA','BEPZA','BEZA','BGMEA','BKMEA','CCI&E','DoE'];return{svg:`${BG}${rd('b_')}
 ${kw('b_h',960,220,'মোট ১৯টি সংস্থা',64,C.gd)}
 <g data-k="b_g">${card(100,280,1720,700,'#fff',44)}${AG.map((a,i)=>`<g data-k="b_t${i}">${agTile(150+(i%8)*205,330+Math.floor(i/8)*130,a,false)}</g><g data-k="b_o${i}">${agTile(150+(i%8)*205,330+Math.floor(i/8)*130,a,true)}</g>`).join('')}
  ${tx(960,930,'বিএসডব্লিউর মাধ্যমে এদের সনদ, লাইসেন্স ও অনুমতি',38,C.mute,800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'b_',lt,t,3);kwU(q,'b_h',lt,.1,t);popG(q('b_g'),lt,.2,t,0,30,0,.5);for(let i=0;i<19;i++){const j=H.indexOf(AG[i]);const b=j>=0?bt(j)-.1:(j<0&&i<6?.3:bt(6)+.3+i*.05);T(q('b_o'+i),{o:cl((lt-b)/.3),s:lt>b&&lt<b+.4?1.08:1})}}}};

// 08 — more coming
K.bs_more=()=>({svg:`${BG}${rd('m_')}
 <g data-k="m_p">${card(100,200,760,700,'#fff',44)}${[0,1,2].map(i=>`<g>${card(170+i*210,330,170,84,'#f1f5f9',20)}${lat(255+i*210,384,'+',44,C.g,800)}</g>`).join('')}${tx(480,560,'আরও সংস্থা যুক্ত হচ্ছে',48,C.g,800)}${icon('cal',480,720,110,C.t,7)}</g>
 <g data-k="m_b">${browser(940,200,880,700,'bswnbr.gov.bd',C.b)}<rect x="1000" y="340" width="760" height="90" rx="45" fill="#f1f5f9" stroke="${C.b}" stroke-width="4"/>${icon('globe',1050,385,44,C.mute,6)}${lat(1090,398,'Search: shrimp → DOF',32,C.ink,800,'start')}<rect x="1000" y="470" width="760" height="110" rx="20" fill="#e9f8ec"/>${lat(1040,535,'Department of Fisheries (DOF)',32,C.g,800,'start')}${tx(1380,800,'নিজের পণ্যের সংস্থা দেখে নিন',36,C.ink,800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'m_',lt,t,3);popG(q('m_p'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.5);popG(q('m_b'),lt,bt(1)-.4,t,1,30,0,.5)}});

// 09 — point 4: less time
K.bs_time=()=>({svg:`${BG}${rd('t_')}${ttl2('t_','৪','লাভ: কম সময়',C.g)}
 <g data-k="t_c"><circle cx="360" cy="660" r="230" fill="#fff" stroke="${C.g}" stroke-width="16"/><g data-k="t_h"><rect x="-8" y="-170" width="16" height="170" rx="8" fill="${C.ink}"/></g><circle cx="360" cy="660" r="16" fill="${C.ink}"/></g>
 <g data-k="t_b">${card(720,350,1100,560,'#fff',44)}
  ${tx(780,470,'এক ঘণ্টার মধ্যে',40,C.ink,800,'start')}<rect x="780" y="500" width="980" height="70" rx="35" fill="#e2e8f0"/><rect data-k="t_b0" x="780" y="500" width="0" height="70" rx="35" fill="${C.g}"/><g data-k="t_v0">${tx(1600,550,'≈৮৬%',44,'#fff',800,'end')}</g>
  ${tx(780,680,'এক দিনের মধ্যে',40,C.ink,800,'start')}<rect x="780" y="710" width="980" height="70" rx="35" fill="#e2e8f0"/><rect data-k="t_b1" x="780" y="710" width="0" height="70" rx="35" fill="${C.t}"/><g data-k="t_v1">${tx(1700,760,'≈৯৫%',44,'#fff',800,'end')}</g>
  ${tx(1270,870,'সনদ ইস্যুর সময় (জুন ২০২৫ পর্যন্ত)',28,C.mute,700)}</g>`,
 upd(q,lt,t,bt){rdU(q,'t_',lt,t,4);ttlU(q,'t_',lt,t);popG(q('t_c'),lt,bt(1)-.4,t,0,40,0,.5);T(q('t_h'),{x:360,y:660,r:t*120,o:1});popG(q('t_b'),lt,bt(1)-.1,t,1,30,0,.5);fillTo(q('t_b0'),lt,bt(2)-.1,980*.86,1);popIn(q('t_v0'),pe(lt,bt(2)+.8,.3),t,2,0,0);fillTo(q('t_b1'),lt,bt(3)-.1,980*.95,1);popIn(q('t_v1'),pe(lt,bt(3)+.8,.3),t,3,0,0)}});
