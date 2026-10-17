// ===================== Product selection 16:9 — scenes 10–18 =====================
// 10 demand
K.pd_demand=()=>({svg:`${BG}${rd('n_')}${ttl2('n_','৫','বিদেশে চাহিদা আছে?',C.gd)}
 <g data-k="n_g">${bub(400,500,460,'আমার মনে হয় চলবে…','#fff',C.mute,40,-1)}</g>
 <g data-k="n_d">${card(150,430,500,160,C.g,40)}${tx(400,530,'তথ্য দেখে যাচাই',46,'#fff',800)}</g>
 <g data-k="n_br">${browser(760,320,1060,650,'trademap.org',C.b)}${lat(1290,470,'Trade Map',80,C.b,800)}${lat(1290,540,'International Trade Centre (ITC)',32,C.mute,700)}${tx(1290,620,'আন্তর্জাতিক বাণিজ্য কেন্দ্র',38,C.ink,800)}<g data-k="n_ch">${[60,110,85,160,140,210].map((h,i)=>`<rect x="${1040+i*90}" y="${900-h}" width="60" height="${h}" rx="10" fill="${C.t}" opacity="${.5+i*.08}"/>`).join('')}</g></g>
 <g data-k="n_pop">${[0,1,2,3,4,5].map(i=>`<circle cx="${400+Math.cos(i)*200}" cy="${500+Math.sin(i)*120}" r="12" fill="${C.mute}"/>`).join('')}</g>`,
 upd(q,lt,t,bt){rdU(q,'n_',lt,t,5);ttlU(q,'n_',lt,t);const g=pe(lt,.5,.4),b=pe(lt,bt(1)+.2,.3);T(q('n_g'),{s:L(.3,1,eb(g))*(1+b*.4),o:cl(g*3)*(1-b)});T(q('n_pop'),{s:L(.5,1.6,b),o:b>0&&b<1?1-b:0});popG(q('n_d'),lt,bt(1)+.5,t,1,30,2,.45);popG(q('n_br'),lt,bt(2)-.3,t,2,30,0,.45);const c=pe(lt,bt(3),.8);T(q('n_ch'),{s:1,o:cl(c*2)})}});

// 11 trade map stats
K.pd_tmap=()=>{const S=[['২২০+','দেশ ও অঞ্চল',C.b],['≈৫,৩০০','পণ্য (এইচএস কোড)',C.t],['ফ্রি','উন্নয়নশীল দেশের জন্য',C.g]];return{svg:`${BG}${rd('m_')}
 ${S.map((s,i)=>`<g data-k="m_s${i}">${card(100+i*590,230,540,560,'#fff',44)}<rect x="${100+i*590}" y="230" width="540" height="22" rx="11" fill="${s[2]}"/>${tx(370+i*590,500,s[0],s[0].length>4?120:150,s[2],800)}${tx(370+i*590,640,s[1],40,C.ink,800)}</g>`).join('')}
 <g data-k="m_r">${card(560,840,800,140,C.gd,50)}${icon('lock',660,910,60,'#fff',7)}${tx(1000,930,'শুধু নিবন্ধন করে নিতে হয়',46,'#fff',800)}</g>`,
 upd(q,lt,t,bt){rdU(q,'m_',lt,t,5);for(let i=0;i<3;i++){popG(q('m_s'+i),lt,bt(i)-.3,t,i,40,3,.45);if(lt>bt(i)+.5)T(q('m_s'+i),{y:Math.sin(lt*2+i)*7,o:1})}popG(q('m_r'),lt,bt(3)-.2,t,3,30,0,.45)}}};

// 12 how to use
K.pd_how=()=>{const B=[['দেশ ক',380],['দেশ খ',300],['দেশ গ',230],['দেশ ঘ',170]];return{svg:`${BG}${rd('w_')}
 <g data-k="w_in">${card(100,190,1720,120,'#fff',60)}${icon('globe',180,250,60,C.b,6)}${lat(240,262,'Product / HS Code:',36,C.mute,800,'start')}<g data-k="w_hs">${lat(620,262,'6305.10  (Jute sacks & bags)',36,C.ink,800,'start')}</g>${tx(1760,262,'চিত্র উদাহরণ',28,C.mute,700,'end')}</g>
 <g data-k="w_a">${card(100,350,560,630,'#fff',40)}${tx(380,420,'সবচেয়ে বেশি আমদানি',38,C.ink,800)}${B.map((b,i)=>`<g>${tx(140,510+i*120,b[0],30,C.mute,800,'start')}<rect data-k="w_b${i}" x="260" y="${475+i*120}" width="0" height="56" rx="14" fill="${C.b}"/></g>`).join('')}</g>
 <g data-k="w_t">${card(700,350,560,630,'#fff',40)}${tx(980,420,'বাড়ছে না কমছে?',38,C.ink,800)}<path d="M760 880 H1200 M760 880 V480" stroke="#cbd5e1" stroke-width="6"/><path data-k="w_ln" d="M780 820 L880 780 L980 790 L1080 690 L1180 600" stroke="${C.g}" stroke-width="12" fill="none" stroke-linecap="round" stroke-dasharray="600" stroke-dashoffset="600"/>${tx(1180,560,'↑',70,C.g,800)}</g>
 <g data-k="w_s">${card(1300,350,520,630,'#fff',40)}${tx(1560,420,'কার কাছ থেকে কেনে?',36,C.ink,800)}${['সরবরাহকারী ১','সরবরাহকারী ২','সরবরাহকারী ৩'].map((s,i)=>`<g><rect x="1340" y="${480+i*130}" width="440" height="100" rx="20" fill="#f8fafc"/><circle cx="1400" cy="${530+i*130}" r="30" fill="${[C.o,C.t,C.p][i]}"/>${tx(1450,542+i*130,s,32,C.ink,800,'start')}</g>`).join('')}</g>`,
 upd(q,lt,t,bt){rdU(q,'w_',lt,t,5);popG(q('w_in'),lt,.1,t,0,30,0,.45);const h=pe(lt,bt(0),.6);T(q('w_hs'),{o:cl(h*3)});popG(q('w_a'),lt,bt(1)-.3,t,1,30,0,.45);for(let i=0;i<4;i++)fillTo(q('w_b'+i),lt,bt(1)+i*.15,B[i][1],.6);popG(q('w_t'),lt,bt(2)-.3,t,2,30,0,.45);const l=q('w_ln');if(l)l.setAttribute('stroke-dashoffset',(600*(1-eo(pe(lt,bt(2),1)))).toFixed(0));popG(q('w_s'),lt,bt(3)-.3,t,3,30,0,.45)}}};

// 13 EPB stats
K.pd_epb=()=>({svg:`${BG}${rd('b_')}
 <g data-k="b_c">${card(100,200,1720,780,'#fff',44)}<rect x="100" y="200" width="1720" height="110" rx="44" fill="${C.gd}"/><rect x="100" y="260" width="1720" height="50" fill="${C.gd}"/>${lat(160,272,'Export Promotion Bureau · FY 2025–26',40,'#fff',800,'start')}${tx(1760,272,'রপ্তানি উন্নয়ন ব্যুরো',36,'#d9f5c4',800,'end')}
  <g data-k="b_l">${tx(180,430,'চামড়া ও চামড়াজাত পণ্য',44,C.ink,800,'start')}${lat(180,500,'$1.23 bn',40,C.mute,800,'start')}${meter(760,420,700,70,C.o,'b_m0')}<g data-k="b_v0">${tx(1720,475,'+৭.০৯%',64,C.o,800,'end')}</g></g>
  <g data-k="b_j">${tx(180,660,'পাট ও পাটজাত পণ্য',44,C.ink,800,'start')}${lat(180,730,'$883.69 mn',40,C.mute,800,'start')}${meter(760,650,700,70,C.g,'b_m1')}<g data-k="b_v1">${tx(1720,705,'+৭.৭৫%',64,C.g,800,'end')}</g></g>
  ${tx(960,900,'সূত্র: ইপিবির রপ্তানি পরিসংখ্যান (জুলাই ২০২৫ – জুন ২০২৬)',30,C.mute,700)}</g>`,
 upd(q,lt,t,bt){rdU(q,'b_',lt,t,5);popG(q('b_c'),lt,Math.min(bt(0)-.3,.2),t,0,30,0,.45);popIn(q('b_l'),pe(lt,bt(1)-.2,.35),t,1,20,0);fillTo(q('b_m0'),lt,bt(1),700*.709,.8);popIn(q('b_v0'),pe(lt,bt(3)-.1,.35),t,2,0,0);popIn(q('b_j'),pe(lt,bt(2)-.2,.35),t,3,20,0);fillTo(q('b_m1'),lt,bt(2),700*.775,.8);popIn(q('b_v1'),pe(lt,bt(3)+.2,.35),t,4,0,0)}});

// 14 scorecard
K.pd_story2=()=>{const M=[[0,1,1,0,1,1],[1,1,1,1,1,1],[1,1,1,1,0,1]];return{svg:`${BG}
 <g data-k="z_t">${card(100,180,1720,800,'#fff',44)}${tx(160,260,'শাহেদের স্কোরকার্ড',46,C.ink,800,'start')}${pill(1700,245,'উদাহরণ',C.mute,28)}
  ${QL.map((l,i)=>`<g><rect x="${520+i*210}" y="300" width="190" height="80" rx="18" fill="#eef2f7"/>${tx(615+i*210,352,l,l.length>6?26:32,C.ink,800)}</g>`).join('')}
  ${PRD.map((p,r)=>`<g data-k="z_r${r}"><rect data-k="z_h${r}" x="130" y="${405+r*150}" width="1660" height="140" rx="24" fill="#f8fafc"/>${prodArt(p[1],210,475+r*150,.55)}${tx(300,490+r*150,p[0],38,C.ink,800,'start')}${M[r].map((v,i)=>`<g data-k="z_c${r}_${i}">${v?check(615+i*210,475+r*150,32,C.g):cross(615+i*210,475+r*150,32,C.r)}</g>`).join('')}</g>`).join('')}</g>
 <g data-k="z_w">${card(1180,870,600,96,C.g,48)}${tx(1480,934,'প্রথম পণ্য: পাটের ব্যাগ',44,'#fff',800)}</g>`,
 upd(q,lt,t,bt){popG(q('z_t'),lt,.1,t,0,30,0,.45);const R=[bt(1),bt(3),bt(2)];for(let r=0;r<3;r++)for(let i=0;i<6;i++)popIn(q('z_c'+r+'_'+i),pe(lt,R[r]-.2+i*.12,.25),t,i,0,0);
  const h0=q('z_h0'),h2=q('z_h2'),h1=q('z_h1');if(h0)h0.setAttribute('fill',lt>bt(1)+.6?'#fff4f2':'#f8fafc');if(h2)h2.setAttribute('fill',lt>bt(2)+.6?'#fff4f2':'#f8fafc');if(h1)h1.setAttribute('fill',lt>bt(4)?'#e9f8ec':'#f8fafc');
  if(lt>bt(5))T(q('z_r1'),{s:1+.015*Math.sin(t*5),o:1});popG(q('z_w'),lt,bt(5)-.2,t,1,30,2,.45)}}};

// 15 tip: stairs
K.pd_tip=()=>{const S=['একটা পণ্য','ছোট চালান','অভিজ্ঞতা','নতুন পণ্য'];return{svg:`${BG}
 <g data-k="t_x">${card(100,180,700,200,'#fff4f2',44)}${cross(200,280,44,C.r)}${tx(280,300,'শুরুতেই অনেক পণ্য নয়',44,C.r,800,'start')}</g>
 ${S.map((s,i)=>`<g data-k="t_s${i}"><rect x="${200+i*400}" y="${900-i*150}" width="380" height="${150+i*150}" rx="16" fill="${[C.b,C.t,C.g,C.gd][i]}"/>${tx(390+i*400,960-i*150,s,40,'#fff',800)}</g>`).join('')}
 <g data-k="t_p">${person(0,0,.5,'s','t_pp')}</g>`,
 upd(q,lt,t,bt){popG(q('t_x'),lt,bt(0)-.4,t,0,40,2,.45);const B=[bt(1)-.2,bt(2)-.2,bt(2)+.6,bt(3)-.2];for(let i=0;i<4;i++){const p=pe(lt,B[i],.4);T(q('t_s'+i),{y:L(200,0,eb(p)),o:cl(p*3)})}let k=0;for(let i=0;i<4;i++)if(lt>B[i]+.4)k=i;const x=390+k*400,y=900-k*150-40;T(q('t_p'),{x:x-0,y:y-30+Math.abs(Math.sin(t*4))*-10,s:1,o:lt>B[0]+.4?1:0})}}};

// 16 Exportain
K.pd_brand=()=>({svg:`${BG}
 <g data-k="xb_logo"><image href="__LOGO__" x="560" y="130" width="800" height="230" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="xb_pg">${card(100,400,860,560,'#fff',40)}<rect x="100" y="400" width="860" height="86" rx="40" fill="${C.g}"/><rect x="100" y="446" width="860" height="40" fill="${C.g}"/>${lat(140,456,'Company page · Shahed Jute Crafts',30,'#fff',800,'start')}
  ${['Jute Shopping Bag','Jute Tote Bag','Jute Pouch'].map((c,i)=>`<g data-k="xb_c${i}">${card(140+i*270,520,250,400,'#f8fafc',24)}${jutebag(265+i*270,680,.7)}${lat(265+i*270,860,c,22,C.ink,800)}</g>`).join('')}</g>
 <g data-k="xb_tag">${card(1020,400,800,200,C.gd,40)}${tx(1420,480,'বাংলাদেশি প্রস্তুতকারক ও রপ্তানিকারকদের',34,'#fff',800)}${lat(1290,550,'B2B',40,C.y,800)}${tx(1350,550,'মার্কেটপ্লেস',40,'#e3f8d3',800,'start')}</g>
 <g data-k="xb_by">${card(1020,640,800,320,'#fff',40)}${person(1150,680,.6,'g','xb_bp')}<rect x="1280" y="720" width="500" height="80" rx="40" fill="#f1f5f9" stroke="${C.b}" stroke-width="4"/>${mag(1320,760,.4,C.b)}${lat(1360,772,'jute bags supplier',30,C.ink,800,'start')}${tx(1530,900,'বিদেশি ক্রেতা সরাসরি খোঁজেন',36,C.g,800)}</g>`,
 upd(q,lt,t,bt){const l=pe(lt,.2,.8);T(q('xb_logo'),{s:L(.5,1,eo(l))+(l>=1?Math.sin(t*2.2)*.03:0),y:l>=1?Math.sin(t*1.8)*10:0,o:cl(l*2)});popG(q('xb_pg'),lt,Math.min(bt(1)-.4,1.2),t,1,40,0,.5);for(let i=0;i<3;i++)popIn(q('xb_c'+i),pe(lt,Math.min(bt(1),1.6)+i*.3,.4),t,i,20,0);
  popG(q('xb_tag'),lt,bt(2)-.3,t,2,30,0,.45);popG(q('xb_by'),lt,bt(3)-.3,t,3,30,2,.45)}});

// 17 advice
K.pd_advice=()=>({svg:`${BG}
 ${kw('v_h',960,230,'নিয়ম আর চাহিদা বদলায়',64,'#fff',C.o)}
 <g data-k="v_a">${card(140,320,500,600,'#fff',44)}${icon('globe',390,520,180,C.gd,6)}${lat(390,720,'EPB',44,C.gd,800)}${tx(390,790,'রপ্তানি উন্নয়ন ব্যুরো',32,C.mute,800)}</g>
 <g data-k="v_b">${card(710,320,500,600,'#fff',44)}${icon('bld',960,520,180,C.t,7)}${tx(960,740,'সংশ্লিষ্ট দপ্তর',42,C.t,800)}</g>
 <g data-k="v_c">${card(1280,320,500,600,'#fff',44)}${bank(1530,560,1.1,C.g)}${lat(1530,740,'AD Bank',44,C.g,800)}${tx(1530,800,'অনুমোদিত ডিলার ব্যাংক',28,C.mute,800)}</g>
 ${kw('v_w',960,1010,'নির্দিষ্ট পণ্যের আগে মিলিয়ে নিন',46,'#fff',C.gd)}`,
 upd(q,lt,t,bt){kwU(q,'v_h',lt,Math.min(bt(0)-.4,.2),t);const VB=[Math.min(bt(1)-.2,1),Math.min(bt(2)-.2,1.8),Math.min(bt(3)-.2,2.6)];['v_a','v_b','v_c'].forEach((k,i)=>{popG(q(k),lt,VB[i],t,i,40,2,.45);if(lt>VB[i]+.5)T(q(k),{y:Math.sin(lt*2+i*1.3)*10,s:lt>bt(1+i)&&lt<bt(1+i)+.6?1.05:1,o:1})});kwU(q,'v_w',lt,bt(3)+.6,t)}});

// 18 CTA
K.pd_cta=()=>({svg:`${BG}
 <g data-k="ct_who">${card(100,200,700,260,'#fff',44)}${bdflag(150,270,150)}${tx(560,310,'প্রস্তুতকারক বা',44,C.ink,800)}${tx(560,390,'রপ্তানিকারক?',56,C.g,800)}</g>
 <g data-k="ct_gl">${icon('globe',450,760,300,C.t,4)}${[0,1,2,3].map(i=>`<g data-k="ct_f${i}"><circle cx="0" cy="0" r="40" fill="#fff"/>${icon(['shirt','bag','box','shoe'][i],0,0,50,[C.b,C.g,C.p,C.o][i],7)}</g>`).join('')}</g>
 <g data-k="ct_lg"><image href="__LOGO__" x="1010" y="220" width="760" height="220" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="ct_bt">${card(1040,520,700,140,C.g,70)}${lat(1390,612,'Exportain.com',62,'#fff',800)}</g>
 <g data-k="ct_hd">${tap('ct_rp')}</g>
 ${kw('ct_u',1390,800,'আজই ভিজিট করুন',60,'#fff',C.o)}`,
 upd(q,lt,t,bt){popG(q('ct_who'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.5);popG(q('ct_gl'),lt,bt(1)-.4,t,1,30,0,.5);for(let i=0;i<4;i++){const p=pe(lt,bt(1)+i*.15,.5),a=i*1.57+t*.5;T(q('ct_f'+i),{x:450+Math.cos(a)*230,y:760+Math.sin(a)*200,s:L(.2,1,p),o:cl(p*2)})}
  const l=pe(lt,.4,.6);T(q('ct_lg'),{s:L(.6,1,eb(l)),o:cl(l*3)});popG(q('ct_bt'),lt,bt(2)-.4,t,2,30,0,.45);if(lt>bt(2)+.3)T(q('ct_bt'),{s:1+.04*Math.sin(t*7),o:1});
  const h=cl((lt-bt(2))/.5);T(q('ct_hd'),{x:L(1860,1700,eo(h)),y:L(760,640,eo(h)),o:cl(h*3)});const rp=((lt-bt(2))%1+1)%1;T(q('ct_rp'),{s:1+rp*1.8,o:h>=1?1-rp:0});kwU(q,'ct_u',lt,bt(2),t)}});
