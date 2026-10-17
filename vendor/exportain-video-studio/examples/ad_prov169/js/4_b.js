// 03 — LIST + VERIFY
K.pv_list=()=>({svg:`${BG}
 <g data-k="l_c">${card(110,130,820,880,'#fff',40)}<rect x="140" y="160" width="760" height="320" rx="24" fill="#d9eef6"/>${shipA(520,360,1.15)}
  ${lat(160,550,'C&F Agent — Chattogram Port',36,C.ink,800,'start')}<g data-k="l_p">${lat(160,620,'BDT 12,000',50,C.g,800,'start')}${lat(460,620,'/ shipment',30,C.mute,700,'start')}</g>
  <g data-k="l_a">${['Chattogram Port','Dhaka','Benapole'].map((a,i)=>pill([300,590,800][i],720,a,C.t,26,'Pop')).join('')}${lat(160,810,'Areas served · up to 20',24,C.mute,700,'start')}</g>
  <g data-k="l_v">${shield(800,900,.85,C.g,'✓')}${lat(690,915,'Verified Provider',32,C.g,800,'end')}</g></g>
 ${kw('l_w0',1420,220,'সেবা লিস্ট করুন',80,C.gd)}
 <g data-k="l_tl">${docPage(1010,340,250,320,'Trade Licence',C.bd,5)}<rect data-k="l_sc" x="1010" y="340" width="250" height="12" fill="${C.g2}" opacity=".85"/></g>
 ${kw('l_w1',1570,520,'লাইসেন্স যাচাই',58,C.ink)}${kw('l_w2',1420,840,'ভেরিফায়েড ব্যাজ',64,'#fff',C.g)}`,
 upd(q,lt,t,bt){kwU(q,'l_w0',lt,Math.min(bt(0),.1),t);popG(q('l_c'),lt,.15,t,0,60,0,.4);popIn(q('l_p'),pe(lt,.6,.35),t,1,10,0);popIn(q('l_a'),pe(lt,.9,.35),t,2,10,0);
  popG(q('l_tl'),lt,bt(1)-.3,t,3,40,0,.4);T(q('l_sc'),{y:((lt*1.2)%1)*300,o:lt>bt(1)-.3&&lt<bt(2)?1:0});kwU(q,'l_w1',lt,bt(1)-.1,t);popIn(q('l_v'),pe(lt,bt(2)-.15,.45),t,4,0,3);kwU(q,'l_w2',lt,bt(2),t)}});

// 04 — LEADS → OFFER → ORDER
K.pv_leads=()=>{const R=[['Seller · Knit factory, Gazipur','Customs clearance · 2×40ft',C.g],['Buyer · Hamburg, Germany','Pre-shipment inspection',C.b],['Seller · Jute mill, Khulna','Export packaging · 3,000 cartons',C.o]];return{svg:`${BG}
 ${kw('d_w0',520,190,'অনুরোধ আসবে লিডে',72,C.ink)}
 <g data-k="d_in">${card(100,250,840,90,C.gd,30)}${lat(150,310,'Leads',38,'#fff',800,'start')}<circle cx="880" cy="295" r="30" fill="${C.r}"/>${lat(880,307,'3',30,'#fff',800)}</g>
 ${R.map((r,i)=>`<g data-k="d_r${i}">${card(100,370+i*190,840,165,'#fff',30)}<rect x="100" y="${370+i*190}" width="16" height="165" fill="${r[2]}"/>${lat(150,435+i*190,r[0],30,C.ink,800,'start')}${lat(150,485+i*190,r[1],26,C.mute,700,'start')}</g>`).join('')}
 <g data-k="d_bt">${card(1120,200,600,120,C.o,60)}${lat(1420,278,'Send offer',48,'#fff',800)}</g>
 <g data-k="d_hd">${tap('d_rp')}</g>
 <g data-k="d_or">${card(1040,400,760,270,'#e9f8ec',50)}${check(1180,535,62,C.g)}${lat(1280,515,'Offer accepted',48,C.g,800,'start')}${lat(1280,575,'→ Service order',36,C.ink,800,'start')}</g>
 ${confetti('d_cf',1420,535)}
 ${kw('d_w1',1420,860,'অফার পাঠান, অর্ডার নিন',62,'#fff',C.o)}`,
 upd(q,lt,t,bt){kwU(q,'d_w0',lt,Math.min(bt(0),.1),t);popG(q('d_in'),lt,.1,t,0,30,0,.35);for(let i=0;i<3;i++){const p=pe(lt,.3+i*.25,.4);T(q('d_r'+i),{x:L(-700,0,eo(p)),o:cl(p*2)})}
  popG(q('d_bt'),lt,bt(1)-.5,t,1,30,0,.4);const h=cl((lt-bt(1)+.3)/.45);T(q('d_hd'),{x:L(1800,1660,eo(h)),y:L(420,260,eo(h)),o:cl(h*3)*(lt<bt(1)+1?1:0)});const rp=((lt-bt(1))%1+1)%1;T(q('d_rp'),{s:1+rp*1.8,o:lt>bt(1)?1-rp:0});
  popG(q('d_or'),lt,bt(2)-.15,t,2,30,0,.4);confU(q,'d_cf',lt,bt(2));kwU(q,'d_w1',lt,bt(1)-.1,t)}}};

// 05 — LIFETIME FREE
K.pv_free=()=>({svg:`${BG}
 ${kw('f_w0',600,420,'প্রোভাইডার অ্যাকাউন্ট',76,C.ink)}
 ${kw('f_w1',600,660,'লাইফটাইম ফ্রি',124,C.f,C.y)}
 <g data-k="f_b"><circle cx="1420" cy="540" r="260" fill="${C.g}"/><circle cx="1420" cy="540" r="225" fill="none" stroke="#fff" stroke-width="8" stroke-dasharray="14 10"/>${lat(1420,520,'FREE',130,'#fff',800)}${lat(1420,630,'∞',110,C.y,800)}</g>
 <g data-k="f_r"><circle cx="1420" cy="540" r="300" fill="none" stroke="${C.y}" stroke-width="10" opacity=".7"/></g>
 ${confetti('f_cf',1420,540)}`,
 upd(q,lt,t,bt){kwU(q,'f_w0',lt,Math.min(bt(0),.1),t);popIn(q('f_b'),pe(lt,bt(1)-.4,.5),t,0,0,0);if(lt>bt(1))T(q('f_b'),{s:1+.03*Math.sin(t*6),r:Math.sin(t*2)*3,o:1});const r=cl((lt-bt(1))/1);T(q('f_r'),{s:L(.8,1.5,eo(r)),o:r>0?1-r:0});
  kwU(q,'f_w1',lt,bt(1)-.05,t);confU(q,'f_cf',lt,bt(1))}});

// 06 — CTA
K.pv_cta=()=>({svg:`${BG}
 <g data-k="a_lg"><image href="__LOGO__" x="660" y="120" width="600" height="180" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="a_bt">${card(470,340,980,210,C.g,105)}${tx(960,430,'আজই যুক্ত হন',80,'#fff',800)}${tx(960,510,'সার্ভিস প্রোভাইডার হিসেবে',40,'#e3f8d3',800)}</g>
 <g data-k="a_hd">${tap('a_rp')}</g>
 <g data-k="a_url">${card(530,600,860,140,'#fff',70)}${lat(960,693,'provider.exportain.com',56,C.gd,800)}</g>
 <g data-k="a_sub">${[['১০টি ক্যাটাগরি',C.b],['ভেরিফায়েড ব্যাজ',C.t],['লাইফটাইম ফ্রি',C.o]].map((c,i)=>pill([500,960,1420][i],880,c[0],c[1],34)).join('')}</g>
 ${confetti('a_cf',960,445)}`,
 upd(q,lt,t,bt){const l=pe(lt,.1,.5);T(q('a_lg'),{s:L(.6,1,eb(l)),o:cl(l*3)});popIn(q('a_bt'),pe(lt,Math.min(bt(0),.3),.45),t,0,60,0);if(lt>bt(0)+.6)T(q('a_bt'),{s:1+.03*Math.sin(t*7),o:1});
  const h=cl((lt-bt(0)-.4)/.5);T(q('a_hd'),{x:L(1540,1410,eo(h)),y:L(640,420,eo(h)),o:cl(h*3)});const rp=((lt-bt(0))%1+1)%1;T(q('a_rp'),{s:1+rp*1.8,o:h>=1?1-rp:0});confU(q,'a_cf',lt,bt(0)+.9);
  popG(q('a_url'),lt,bt(1)-.2,t,1,30,3,.4);popG(q('a_sub'),lt,bt(2)+.2,t,2,20,0,.4)}});
