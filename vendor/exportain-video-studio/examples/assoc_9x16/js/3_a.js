// ===================== Chamber vs association — art + scenes 00–10 =====================
const fishA=(x,y,s=1,col='#7aa7c7')=>`<g transform="translate(${x} ${y}) scale(${s})"><path d="M-90 0 Q-30 -52 50 -14 L96 -46 L86 0 L96 46 L50 14 Q-30 52 -90 0Z" fill="${col}"/><circle cx="-56" cy="-8" r="8" fill="#0f172a"/><path d="M-20 -28 Q0 0 -20 28" stroke="#fff" stroke-width="5" fill="none" opacity=".6"/></g>`;
const shrimp=(x,y,s=1)=>`<g transform="translate(${x} ${y}) scale(${s})"><path d="M60 -30 Q90 20 40 50 Q-10 70 -50 40 L-80 60 L-70 20 L-90 0 L-50 10 Q-10 30 20 10 Q40 -6 30 -30Z" fill="#f28c5a"/>${[0,1,2].map(i=>`<path d="M${-10+i*22} ${36-i*10} q6 -14 0 -26" stroke="#fff" stroke-width="4" fill="none" opacity=".7"/>`).join('')}<path d="M55 -28 q30 -40 70 -36 M50 -24 q40 -20 70 0" stroke="#c2410c" stroke-width="3" fill="none"/></g>`;
const leafB=(x,y,s=1)=>`<g transform="translate(${x} ${y}) scale(${s})"><path d="M0 110 Q-110 30 -80 -50 Q-50 -110 0 -70 Q50 -110 80 -50 Q110 30 0 110Z" fill="#3f9b2f"/><path d="M0 -70 V110 M0 0 L-50 -30 M0 30 L50 0 M0 60 L-40 40" stroke="#bde5a8" stroke-width="6" fill="none"/></g>`;
const spool=(x,y,s=1,col=C.o)=>`<g transform="translate(${x} ${y}) scale(${s})"><rect x="-60" y="-90" width="120" height="22" rx="6" fill="#a16207"/><rect x="-60" y="68" width="120" height="22" rx="6" fill="#a16207"/><rect x="-46" y="-68" width="92" height="136" fill="${col}"/>${[0,1,2,3,4,5].map(i=>`<path d="M-46 ${-56+i*22} L46 ${-46+i*22}" stroke="#fff" stroke-width="4" opacity=".5"/>`).join('')}</g>`;
const gavel=(x,y,s=1)=>`<g transform="translate(${x} ${y}) scale(${s})"><rect x="-90" y="70" width="180" height="30" rx="8" fill="#7c4a12"/><g transform="rotate(-30)"><rect x="-70" y="-40" width="140" height="56" rx="12" fill="#92400e"/><rect x="-10" y="16" width="20" height="130" rx="8" fill="#b45309"/></g></g>`;
const stepRow=(x,y,w,txt,col,id,hl)=>`<g data-k="${id}"><rect x="${x}" y="${y}" width="${w}" height="78" rx="16" fill="${hl?'#e9f8ec':'#f4f7f9'}" ${hl?`stroke="${col}" stroke-width="5"`:''}/>${lat(x+30,y+50,txt,28,hl?col:C.mute,800,'start')}</g>`;

// 00 — hook: which membership? two signs
K.as_hook=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="hk_e">${card(90,290,900,330,'#fff',40)}${cert(130,330,300,250,'ERC',C.g)}${tx(470,420,'ইআরসির জন্য',44,C.ink,800,'start')}${tx(470,500,'সদস্যপদ লাগবে',52,C.g,800,'start')}${check(900,460,38,C.g)}</g>
 <g data-k="hk_q">${tx(540,800,'কোনটা?',96,C.r,800)}</g>
 <rect x="526" y="840" width="28" height="700" rx="10" fill="#7c5a32"/>
 <g data-k="hk_a"><path d="M190 900 H520 V1060 H190 L130 980Z" fill="${C.b}"/>${tx(345,1000,'জেলা চেম্বার',46,'#fff',800)}</g>
 <g data-k="hk_b"><path d="M560 1120 H960 L1020 1200 L960 1280 H560Z" fill="${C.g}"/>${tx(780,1190,'পণ্যভিত্তিক',36,'#e3f8d3',800)}${tx(780,1250,'অ্যাসোসিয়েশন',40,'#fff',800)}</g>
 <g data-k="hk_c">${card(140,1560,800,190,'#fff4f2',40)}${coin(270,1655,58)}${coin(370,1655,58)}${tx(640,1640,'ভুল বাছলে',36,C.mute,800)}${tx(640,1705,'খরচ দুইবার',50,C.r,800)}</g>`,
 upd(q,lt,t,bt){popG(q('hk_e'),lt,.2,t,0,40,2);popG(q('hk_q'),lt,bt(1)-.2,t,1,30,0,.6);if(lt>bt(1)+.6)T(q('hk_q'),{s:1+.05*Math.sin(t*4),o:1});
  slideG(q('hk_a'),lt,bt(2)-.1,-160,t,2);slideG(q('hk_b'),lt,bt(3)-.1,160,t,3);popG(q('hk_c'),lt,bt(4)-.2,t,4,40,0,.6);if(lt>bt(4)+.6)T(q('hk_c'),{x:Math.sin(t*22)*cl((bt(4)+1.4-lt)*2)*8,o:1})}});

// 01 — story: Rakib from Jashore
K.as_story=()=>{const P=[['shirt',C.b],['shoe',C.o],['bag',C.g],['box',C.t],['doc',C.p]];return{svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="st_p">${card(60,290,960,520,'#fff',40)}${person(260,390,.92,'s','st_sp')}${pill(260,750,'রাকিব · যশোর',C.t,40)}${tx(700,760,'কাল্পনিক চরিত্র',28,C.mute,700)}</g>
 <g data-k="st_v">${basket(720,560,1.25)}${tx(720,700,'সবজি রপ্তানি',40,C.g,800)}</g>
 <g data-k="st_c"><rect x="80" y="860" width="920" height="140" rx="26" fill="#fff"/>${tx(130,950,'চেম্বার সদস্য সনদ',42,C.ink,800,'start')}${check(920,930,36,C.g)}</g>
 <g data-k="st_a"><rect x="80" y="1030" width="920" height="140" rx="26" fill="#fff4f2" stroke="${C.r}" stroke-width="5" stroke-dasharray="16 10"/>${tx(130,1120,'অ্যাসোসিয়েশনের সনদও?',42,C.r,800,'start')}${tx(920,1125,'?',70,C.r,800,'middle','Pop')}</g>
 <g data-k="st_g">${card(80,1230,920,500,'#fff',40)}${tx(540,1320,'কোন পণ্যে কোনটা?',52,C.gd,800)}${P.map((p,i)=>`<g data-k="st_i${i}"><circle cx="${170+i*185}" cy="1500" r="78" fill="${p[1]}" opacity=".14"/>${icon(p[0],170+i*185,1500,110,p[1],7)}</g>`).join('')}${tx(540,1665,'পোশাক · চামড়া · সবজি · মাছ · সফটওয়্যার',30,C.mute,800)}</g>`,
 upd(q,lt,t,bt){popG(q('st_p'),lt,.2,t,0,50,2);popG(q('st_v'),lt,bt(1)-.2,t,1,40,3);popG(q('st_c'),lt,bt(2)-.2,t,2,30,0);popG(q('st_a'),lt,bt(3)-.2,t,3,30,0);if(lt>bt(3)+.6)T(q('st_a'),{x:Math.sin(t*20)*cl((bt(3)+1.3-lt)*2)*6,o:1});
  popG(q('st_g'),lt,bt(4)-.4,t,4,40,0);for(let i=0;i<5;i++)popIn(q('st_i'+i),pe(lt,bt(4)+i*.18,.4),t,i,20,4)}}};

// 02 — point 1: garments (BGMEA woven, BKMEA knit) + UD
K.as_rmg=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>${road5('a1_')}
 ${ttl('a1_','১','পোশাক',C.b)}
 <g data-k="a1_w">${card(80,600,450,420,'#fff',36)}${icon('shirt',305,730,180,C.b,6)}${tx(305,880,'ওভেন পোশাক',34,C.mute,800)}${pill(305,965,'BGMEA',C.b,44,'Pop')}</g>
 <g data-k="a1_k">${card(550,600,450,420,'#fff',36)}${icon('shirt',775,730,180,C.o,9)}${tx(775,880,'নিট পোশাক',34,C.mute,800)}${pill(775,965,'BKMEA',C.o,44,'Pop')}</g>
 <g data-k="a1_f">${card(80,1070,920,660,'#eef6ff',40)}${tx(540,1150,'প্রতিটি অর্ডারে ইউডি',42,C.ink,800)}
  <g data-k="a1_o">${docPage(120,1200,230,300,'Order',C.b,5)}</g>
  <g data-k="a1_u"><circle cx="540" cy="1350" r="100" fill="${C.gd}"/>${lat(540,1370,'UD',64,'#fff',800)}${tx(540,1500,'ইউটিলাইজেশন ডিক্লারেশন',26,C.mute,800)}</g>
  <g data-k="a1_b">${carton(840,1330,1.05,'#d9a55c','#b9853d','#e9c287','BOND')}${tx(840,1500,'শুল্কমুক্ত কাঁচামাল',28,C.mute,800)}</g>
  <path data-k="a1_r1" d="M370 1350 H420" stroke="${C.ink}" stroke-width="10"/><path data-k="a1_r2" d="M660 1350 H720" stroke="${C.ink}" stroke-width="10"/>
  <g data-k="a1_x">${pill(540,1640,'→ রপ্তানির পোশাকে ব্যবহার',C.g,38)}</g></g>`,
 upd(q,lt,t,bt){road5Upd(q,'a1_',lt,t,1,0);popIn(q('a1_tt'),pe(lt,.2,.6),t,0,40,2);popG(q('a1_w'),lt,bt(1)-.2,t,1,40,3);popG(q('a1_k'),lt,bt(2)-.2,t,2,40,3);
  popG(q('a1_f'),lt,bt(3)-.5,t,3,30,0);popIn(q('a1_o'),pe(lt,bt(3),.5),t,4,20,0);T(q('a1_r1'),{o:lt>bt(4)?1:.15});popIn(q('a1_u'),pe(lt,bt(4)-.1,.6),t,5,0,3);T(q('a1_r2'),{o:lt>bt(5)?1:.15});popIn(q('a1_b'),pe(lt,bt(5),.6),t,6,20,3);popG(q('a1_x'),lt,bt(5)+1.2,t,7,20,3,.6)}});

// 03 — 5% cash support needs membership
K.as_rmg2=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>${road5('a2_')}
 <g data-k="a2_y">${card(80,410,920,420,'#fff',40)}${spool(240,600,1.1,C.o)}${spool(400,620,.9,C.t)}<rect x="520" y="500" width="400" height="220" rx="18" fill="${C.b}" opacity=".85"/>${[0,1,2,3,4].map(i=>`<path d="M520 ${530+i*40} H920" stroke="#fff" stroke-width="5" opacity=".35"/>`).join('')}${lat(720,630,'Made in BD',40,'#fff',800)}${tx(540,790,'দেশি সুতা ও কাপড়',40,C.ink,800)}</g>
 <g data-k="a2_p"><circle cx="300" cy="1060" r="160" fill="${C.g}"/><circle cx="300" cy="1060" r="134" fill="none" stroke="#fff" stroke-width="6" stroke-dasharray="10 8"/>${tx(300,1090,'৫%',110,'#fff',800)}${card(500,950,500,220,'#fff',36)}${tx(750,1040,'নগদ সহায়তা',46,C.g,800)}${tx(750,1110,'অর্থবছর ২০২৬-২৭',32,C.mute,800)}</g>
 <g data-k="a2_c">${card(80,1290,920,440,'#fff',40)}${tx(540,1370,'শর্ত: সদস্যপদ',42,C.ink,800)}
  ${['BGMEA','BKMEA'].map((l,i)=>`<g data-k="a2_c${i}">${pill(200+i*230,1490,l,[C.b,C.o][i],40,'Pop')}</g>`).join('')}<g data-k="a2_c2">${pill(770,1490,'সংশ্লিষ্ট সংগঠন',C.t,32)}</g>
  <g data-k="a2_ok">${check(300,1630,40,C.g)}${tx(370,1645,'সদস্য হলে তবেই আবেদন',38,C.g,800,'start')}</g></g>`,
 upd(q,lt,t,bt){road5Upd(q,'a2_',lt,t,1,0);popG(q('a2_y'),lt,.2,t,0,40,2);popG(q('a2_p'),lt,bt(1)-.2,t,1,40,3);if(lt>bt(1)+.6)T(q('a2_p'),{s:1+.02*Math.sin(t*3),o:1});
  popG(q('a2_c'),lt,bt(2)-.5,t,2,30,0);for(let i=0;i<3;i++)popIn(q('a2_c'+i),pe(lt,bt(2)+i*.4,.45),t,i,20,3);popG(q('a2_ok'),lt,bt(3),t,3,20,0,.6)}});

// 04 — leather & footwear: LFMEAB
K.as_leather=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>${road5('a3_')}
 <g data-k="a3_b">${card(80,410,450,460,'#fff',40)}${bagL(305,640,1.15)}${tx(305,830,'চামড়াজাত পণ্য',36,C.ink,800)}</g>
 <g data-k="a3_s">${card(550,410,450,460,'#fff',40)}${icon('shoe',775,620,230,'#7c4a12',8)}${tx(775,830,'জুতা',40,C.ink,800)}</g>
 <g data-k="a3_l">${card(80,920,920,320,'#7c4a12',44)}${lat(540,1090,'LFMEAB',120,'#fff',800)}${tx(540,1190,'চামড়া খাতের অ্যাসোসিয়েশন',36,'#fde6c8',800)}</g>
 <g data-k="a3_n">${card(80,1290,920,420,'#fff',40)}${['Leathergoods & Footwear','Manufacturers & Exporters','Association of Bangladesh'].map((l,i)=>`<g data-k="a3_n${i}">${lat(540,1400+i*100,l,44,[C.pk,C.ink,C.mute][i],800)}</g>`).join('')}</g>`,
 upd(q,lt,t,bt){road5Upd(q,'a3_',lt,t,1,0);popG(q('a3_b'),lt,.2,t,0,40,3);popG(q('a3_s'),lt,bt(1)-.2,t,1,40,3);popG(q('a3_l'),lt,bt(2)-.2,t,2,40,0,.6);if(lt>bt(2)+.6)T(q('a3_l'),{s:1+.015*Math.sin(t*3),o:1});
  popG(q('a3_n'),lt,bt(3)-.3,t,3,30,0);for(let i=0;i<3;i++){const p=pe(lt,bt(3)+i*.7,.5);T(q('a3_n'+i),{x:L(-60,0,eo(p)),o:cl(p*2)})}}});

// 05 — point 2: fruits & vegetables: BFVAPEA
K.as_veg=()=>{const S=['DCCI Membership','Export Registration (ERC)','Production contract','BFVAPEA Membership','Phytosanitary certificate'];return{svg:`<rect width="1080" height="1920" fill="url(#studio)"/>${road5('b1_')}
 ${ttl('b1_','২','সবজি ও ফল',C.t)}
 <g data-k="b1_v">${card(80,600,920,330,'#fff',40)}${basket(250,780,1.3)}${mango(430,790,.9)}${lat(720,780,'BFVAPEA',80,C.t,800)}${tx(720,860,'সবজি ও ফল রপ্তানিকারকদের সংগঠন',28,C.mute,800)}</g>
 <g data-k="b1_e">${browser(80,980,920,760,'bangladesh.eregulations.org',C.t)}${lat(130,1110,'Exporting fresh vegetables',34,C.ink,800,'start')}
  ${S.map((s,i)=>stepRow(130,1150+i*104,820,(i+1)+'. '+s,C.t,'b1_s'+i,i==3)).join('')}</g>
 <g data-k="b1_k">${check(900,1505,34,C.g)}</g>`,
 upd(q,lt,t,bt){road5Upd(q,'b1_',lt,t,2,0);popIn(q('b1_tt'),pe(lt,.2,.6),t,0,40,2);popG(q('b1_v'),lt,bt(1)-.3,t,1,40,3);popG(q('b1_e'),lt,bt(2)-.3,t,2,30,0);
  for(let i=0;i<5;i++){const p=pe(lt,bt(2)+.1+i*.2,.35);T(q('b1_s'+i),{x:L(-40,0,eo(p)),o:cl(p*2)})}if(lt>bt(3))T(q('b1_s3'),{s:1+.02*Math.sin(t*5),o:1});popIn(q('b1_k'),pe(lt,bt(3)+.1,.4),t,3,0,0)}}};

// 06 — software: BASIS
K.as_basis=()=>{const B=[['সদস্যপদ বাধ্যতামূলক',C.r],['কর সুবিধা',C.g],['দরপত্র',C.b]];return{svg:`<rect width="1080" height="1920" fill="url(#studio)"/>${road5('b2_')}
 <g data-k="b2_l">${card(80,410,920,470,'#fff',40)}${laptop(330,640,1.7,C.b)}${lat(760,620,'BASIS',100,C.b,800)}${tx(760,710,'সফটওয়্যার ও আইটি সেবা',32,C.mute,800)}</g>
 ${B.map((b,i)=>`<g data-k="b2_c${i}">${card(80,930+i*230,920,200,'#fff',36)}<circle cx="190" cy="${1030+i*230}" r="58" fill="${b[1]}"/>${i==0?icon('lock',190,1030+i*230,70,'#fff',8):i==1?tx(190,1055+i*230,'৳',64,'#fff',800):icon('doc',190,1030+i*230,70,'#fff',8)}${tx(290,1050+i*230,b[0],48,C.ink,800,'start')}</g>`).join('')}
 <g data-k="b2_s">${tx(540,1690,'সূত্র: বাণিজ্য সংগঠন অধিদপ্তর, ২০১৯',28,C.mute,700)}</g>`,
 upd(q,lt,t,bt){road5Upd(q,'b2_',lt,t,2,0);popG(q('b2_l'),lt,.2,t,0,40,3);for(let i=0;i<3;i++)slideG(q('b2_c'+i),lt,bt(i+1)-.2,-140,t,i);popG(q('b2_s'),lt,bt(1)+.8,t,3,10,0,.6)}}};

// 07 — point 3: frozen fish: BFFEA
K.as_fish=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>${road5('c1_')}
 ${ttl('c1_','৩','হিমায়িত মাছ ও চিংড়ি',C.o)}
 <g data-k="c1_f">${card(80,600,920,340,'#e7f5fb',40)}${fishA(280,740,1.3,'#5b8db3')}<g data-k="c1_sh">${shrimp(560,760,1.1)}</g>${[0,1,2,3,4].map(i=>`<path d="M${130+i*190} 900 l12 -20 l12 20Z" fill="#bfe3f2"/>`).join('')}<g data-k="c1_b">${lat(840,780,'BFFEA',70,C.o,800)}</g></g>
 <g data-k="c1_d">${card(80,990,920,740,'#fff',40)}${tx(540,1070,'নগদ সহায়তার আবেদন',42,C.ink,800)}
  <g data-k="c1_d0">${cert(130,1120,380,300,'BFFEA সনদ',C.o)}</g><g data-k="c1_d1">${docPage(570,1120,380,300,'DoF Licence',C.b,4)}${tx(760,1460,'মৎস্য অধিদপ্তর',30,C.mute,800)}</g>
  <g data-k="c1_c">${coin(380,1600,60)}${tx(470,1615,'= আবেদন সম্পূর্ণ',40,C.g,800,'start')}</g></g>`,
 upd(q,lt,t,bt){road5Upd(q,'c1_',lt,t,3,0);popIn(q('c1_tt'),pe(lt,.2,.6),t,0,40,2);popG(q('c1_f'),lt,.6,t,1,40,0);popG(q('c1_sh'),lt,bt(1)-.2,t,2,20,4);popG(q('c1_b'),lt,bt(2)-.2,t,3,20,3);
  popG(q('c1_d'),lt,bt(3)-.4,t,4,30,0);popIn(q('c1_d0'),pe(lt,bt(3)+.2,.5),t,5,20,0);popG(q('c1_d1'),lt,bt(4)-.1,t,6,20,0,.6);popG(q('c1_c'),lt,bt(4)+.9,t,7,20,3,.5)}});

// 08 — jute goods: BJGEA
K.as_jute=()=>{const S=['DCCI Membership','ERC','Jute Goods Exporter Licence','BJGEA Membership','EPB Enrolment'];return{svg:`<rect width="1080" height="1920" fill="url(#studio)"/>${road5('c2_')}
 <g data-k="c2_j">${card(80,410,920,440,'#fff',40)}${jutebag(270,640,1.05)}${lat(720,620,'BJGEA',100,C.juteD,800)}</g>
 <g data-k="c2_n">${tx(720,710,'পাটপণ্য রপ্তানিকারকদের',32,C.ink,800)}${tx(720,760,'সংগঠন',32,C.ink,800)}</g>
 <g data-k="c2_e">${browser(80,900,920,830,'bangladesh.eregulations.org',C.juteD)}${lat(130,1030,'Exporting jute goods',34,C.ink,800,'start')}
  ${S.map((s,i)=>stepRow(130,1070+i*104,820,(i+1)+'. '+s,i==2?C.b:C.juteD,'c2_s'+i,i==2||i==3)).join('')}
  <g data-k="c2_t">${tx(540,1660,'পাট অধিদপ্তরের লাইসেন্স + BJGEA সনদ',32,C.gd,800)}</g></g>`,
 upd(q,lt,t,bt){road5Upd(q,'c2_',lt,t,3,0);popG(q('c2_j'),lt,.2,t,0,40,3);popG(q('c2_n'),lt,bt(1)-.2,t,1,20,0,.6);popG(q('c2_e'),lt,bt(2)-.4,t,2,30,0);
  for(let i=0;i<5;i++){const p=pe(lt,bt(2)+i*.2,.35);T(q('c2_s'+i),{x:L(-40,0,eo(p)),o:cl(p*2)})}if(lt>bt(2)+1.2)T(q('c2_s3'),{s:1+.015*Math.sin(t*5),o:1});if(lt>bt(3))T(q('c2_s2'),{s:1+.015*Math.sin(t*5+1),o:1});popG(q('c2_t'),lt,bt(3)+.3,t,3,20,0,.6)}}};

// 09 — point 4: services beyond the certificate
K.as_serv=()=>{const S=[['ইউডি সনদ','doc',C.b],['প্রণোদনার প্রত্যয়ন','check',C.g],['বাজার তথ্য','globe',C.t],['প্রশিক্ষণ','star',C.o],['প্রতিনিধিত্ব','chat',C.gd]];const pos=[[290,1250],[790,1250],[290,1480],[790,1480],[540,1700]];return{svg:`<rect width="1080" height="1920" fill="url(#studio)"/>${road5('d1_')}
 ${ttl('d1_','৪','অ্যাসোসিয়েশনের সেবা',C.g)}
 <g data-k="d1_h">${bank(540,880,1.35,C.gd)}${tx(540,1010,'অ্যাসোসিয়েশন',38,C.gd,800)}</g>
 <g data-k="d1_c">${cert(80,640,250,190,'সনদ',C.t)}<g data-k="d1_x">${tx(205,880,'শুধু এটা নয়',30,C.r,800)}</g></g>
 ${S.map((s,i)=>`<g data-k="d1_s${i}">${card(pos[i][0]-230,pos[i][1]-90,460,180,'#fff',36)}<circle cx="${pos[i][0]-140}" cy="${pos[i][1]}" r="56" fill="${s[2]}"/>${i==0?lat(pos[i][0]-140,pos[i][1]+14,'UD',40,'#fff',800):icon(s[1],pos[i][0]-140,pos[i][1],66,'#fff',8)}${tx(pos[i][0]+40,pos[i][1]+14,s[0],s[0].length>12?28:38,C.ink,800)}</g>`).join('')}`,
 upd(q,lt,t,bt){road5Upd(q,'d1_',lt,t,4,0);popIn(q('d1_tt'),pe(lt,.2,.6),t,0,40,2);popG(q('d1_h'),lt,.6,t,1,40,3);popG(q('d1_c'),lt,bt(1)-.2,t,2,30,3);popG(q('d1_x'),lt,bt(1)+.5,t,3,10,0,.5);
  for(let i=0;i<5;i++)popG(q('d1_s'+i),lt,bt(i+2)-.15,t,i,40,3,.6)}}};

// 10 — UD facts
K.as_ud=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>${road5('d2_')}
 <g data-k="d2_a">${card(80,410,920,560,'#fff',40)}${lat(170,470,'BGMEA',36,C.b,800,'start')}${tx(910,480,'প্রতি মাসে',34,C.mute,800,'end')}
  ${Array.from({length:12},(_,i)=>`<g data-k="d2_f${i}">${icon('bld',170+(i%6)*148,600+Math.floor(i/6)*130,100,C.b,6)}</g>`).join('')}
  <g data-k="d2_n">${tx(540,920,'≈ ১,৭০০ কারখানা পায় ইউডি',48,C.gd,800)}</g></g>
 <g data-k="d2_c">${cal(100,1030,260,'১','সেপ ২০২৫',C.r)}${tx(400,1140,'থেকে নতুন নিয়ম',40,C.ink,800,'start')}</g>
 <g data-k="d2_u">${card(80,1330,920,410,'#fff',40)}<rect x="80" y="1330" width="920" height="80" rx="40" fill="${C.gd}"/><rect x="80" y="1370" width="920" height="40" fill="${C.gd}"/>${lat(130,1385,'UD Application',32,'#fff',800,'start')}
  ${field(130,1460,820,'কাঁচামাল','#94a3b8','d2_w0')}<g data-k="d2_p"><rect x="120" y="1545" width="840" height="150" rx="20" fill="#fff4f2" stroke="${C.r}" stroke-width="5"/>${lat(160,1610,'Unit price',40,C.r,800,'start')}${tx(160,1665,'বাধ্যতামূলক',32,C.r,800,'start')}${lat(920,1630,'$ 0.00',44,C.ink,800,'end')}</g></g>`,
 upd(q,lt,t,bt){road5Upd(q,'d2_',lt,t,4,0);popG(q('d2_a'),lt,.2,t,0,40,0);for(let i=0;i<12;i++)popIn(q('d2_f'+i),pe(lt,bt(0)+i*.1,.3),t,i,10,0);popG(q('d2_n'),lt,bt(1)-.1,t,1,20,0,.6);
  popG(q('d2_c'),lt,bt(2)-.2,t,2,30,3);popG(q('d2_u'),lt,bt(2)+.8,t,3,30,0);fillTo(q('d2_w0'),lt,bt(2)+1.3,820);popG(q('d2_p'),lt,bt(3)-.1,t,4,10,0,.5);if(lt>bt(3)+.6)T(q('d2_p'),{s:1+.02*Math.sin(t*6),o:1})}});
