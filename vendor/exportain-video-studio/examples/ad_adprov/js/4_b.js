// 03 — LIST + VERIFY
K.pv_list=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 ${kw('l_w0',540,320,'সেবা লিস্ট করুন',80,C.gd)}
 <g data-k="l_c">${card(110,400,860,880,'#fff',40)}<rect x="140" y="430" width="800" height="330" rx="24" fill="#d9eef6"/>${shipA(540,640,1.2)}
  ${lat(160,830,'C&F Agent — Chattogram Port',38,C.ink,800,'start')}<g data-k="l_p">${lat(160,900,'BDT 12,000',52,C.g,800,'start')}${lat(470,900,'/ shipment',30,C.mute,700,'start')}</g>
  <g data-k="l_a">${['Chattogram Port','Dhaka','Benapole'].map((a,i)=>pill([300,610,840][i],1010,a,C.t,26,'Pop')).join('')}${lat(160,1100,'Areas served · up to 20',24,C.mute,700,'start')}</g>
  <g data-k="l_v">${shield(820,1170,.9,C.g,'✓')}${lat(700,1185,'Verified Provider',32,C.g,800,'end')}</g></g>
 <g data-k="l_tl">${docPage(130,1340,300,360,'Trade Licence',C.bd,5)}<rect data-k="l_sc" x="130" y="1340" width="300" height="12" fill="${C.g2}" opacity=".85"/></g>
 ${kw('l_w1',720,1480,'লাইসেন্স যাচাই',56,C.ink)}${kw('l_w2',720,1630,'ভেরিফায়েড ব্যাজ',52,'#fff',C.g)}`,
 upd(q,lt,t,bt){kwU(q,'l_w0',lt,Math.min(bt(0),.1),t);popG(q('l_c'),lt,.15,t,0,60,0,.4);popIn(q('l_p'),pe(lt,.6,.35),t,1,10,0);popIn(q('l_a'),pe(lt,.9,.35),t,2,10,0);
  popG(q('l_tl'),lt,bt(1)-.3,t,3,40,0,.4);T(q('l_sc'),{y:((lt*1.2)%1)*340,o:lt>bt(1)-.3&&lt<bt(2)?1:0});kwU(q,'l_w1',lt,bt(1)-.1,t);popIn(q('l_v'),pe(lt,bt(2)-.15,.45),t,4,0,3);kwU(q,'l_w2',lt,bt(2),t)}});

// 04 — LEADS → OFFER → ORDER
K.pv_leads=()=>{const R=[['Seller · Knit factory, Gazipur','Customs clearance · 2×40ft',C.g],['Buyer · Hamburg, Germany','Pre-shipment inspection',C.b],['Seller · Jute mill, Khulna','Export packaging · 3,000 cartons',C.o]];return{svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 ${kw('d_w0',540,320,'অনুরোধ আসবে লিডে',72,C.ink)}
 <g data-k="d_in">${card(80,390,920,90,C.gd,30)}${lat(130,450,'Leads',38,'#fff',800,'start')}<circle cx="930" cy="435" r="30" fill="${C.r}"/>${lat(930,447,'3',30,'#fff',800)}</g>
 ${R.map((r,i)=>`<g data-k="d_r${i}">${card(80,510+i*180,920,160,'#fff',30)}<rect x="80" y="${510+i*180}" width="16" height="160" fill="${r[2]}"/>${lat(130,570+i*180,r[0],30,C.ink,800,'start')}${lat(130,620+i*180,r[1],26,C.mute,700,'start')}</g>`).join('')}
 <g data-k="d_bt">${card(240,1090,600,120,C.o,60)}${lat(540,1168,'Send offer',48,'#fff',800)}</g>
 <g data-k="d_hd">${tap('d_rp')}</g>
 <g data-k="d_or">${card(130,1290,820,280,'#e9f8ec',50)}${check(270,1430,62,C.g)}${lat(370,1410,'Offer accepted',48,C.g,800,'start')}${lat(370,1470,'→ Service order',36,C.ink,800,'start')}</g>
 ${confetti('d_cf',540,1430)}
 ${kw('d_w1',540,1720,'অফার পাঠান, অর্ডার নিন',62,'#fff',C.o)}`,
 upd(q,lt,t,bt){kwU(q,'d_w0',lt,Math.min(bt(0),.1),t);popG(q('d_in'),lt,.1,t,0,30,0,.35);for(let i=0;i<3;i++){const p=pe(lt,.3+i*.25,.4);T(q('d_r'+i),{x:L(700,0,eo(p)),o:cl(p*2)})}
  popG(q('d_bt'),lt,bt(1)-.5,t,1,30,0,.4);const h=cl((lt-bt(1)+.3)/.45);T(q('d_hd'),{x:L(960,790,eo(h)),y:L(1300,1150,eo(h)),o:cl(h*3)*(lt<bt(1)+1?1:0)});const rp=((lt-bt(1))%1+1)%1;T(q('d_rp'),{s:1+rp*1.8,o:lt>bt(1)?1-rp:0});
  popG(q('d_or'),lt,bt(2)-.15,t,2,30,0,.4);confU(q,'d_cf',lt,bt(2));kwU(q,'d_w1',lt,bt(1)-.1,t)}}};

// 05 — LIFETIME FREE
K.pv_free=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 ${kw('f_w0',540,520,'প্রোভাইডার অ্যাকাউন্ট',72,C.ink)}
 <g data-k="f_b"><circle cx="540" cy="920" r="260" fill="${C.g}"/><circle cx="540" cy="920" r="225" fill="none" stroke="#fff" stroke-width="8" stroke-dasharray="14 10"/>${lat(540,900,'FREE',130,'#fff',800)}${lat(540,1010,'∞',110,C.y,800)}</g>
 <g data-k="f_r"><circle cx="540" cy="920" r="300" fill="none" stroke="${C.y}" stroke-width="10" opacity=".7"/></g>
 ${kw('f_w1',540,1400,'লাইফটাইম ফ্রি',120,C.f,C.y)}
 ${confetti('f_cf',540,920)}`,
 upd(q,lt,t,bt){kwU(q,'f_w0',lt,Math.min(bt(0),.1),t);popIn(q('f_b'),pe(lt,bt(1)-.4,.5),t,0,0,0);if(lt>bt(1))T(q('f_b'),{s:1+.03*Math.sin(t*6),r:Math.sin(t*2)*3,o:1});const r=cl((lt-bt(1))/1);T(q('f_r'),{s:L(.8,1.5,eo(r)),o:r>0?1-r:0});
  kwU(q,'f_w1',lt,bt(1)-.05,t);confU(q,'f_cf',lt,bt(1))}});

// 06 — CTA
K.pv_cta=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="a_lg"><image href="__LOGO__" x="190" y="300" width="700" height="210" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="a_bt">${card(100,600,880,220,C.g,110)}${tx(540,690,'আজই যুক্ত হন',78,'#fff',800)}${tx(540,775,'সার্ভিস প্রোভাইডার হিসেবে',40,'#e3f8d3',800)}</g>
 <g data-k="a_hd">${tap('a_rp')}</g>
 <g data-k="a_url">${card(110,900,860,150,'#fff',75)}${lat(540,998,'provider.exportain.com',56,C.gd,800)}</g>
 <g data-k="a_sub">${[['১০টি ক্যাটাগরি',C.b],['ভেরিফায়েড ব্যাজ',C.t],['লাইফটাইম ফ্রি',C.o]].map((c,i)=>pill(540,1180+i*120,c[0],c[1],40)).join('')}</g>
 ${confetti('a_cf',540,710)}`,
 upd(q,lt,t,bt){const l=pe(lt,.1,.5);T(q('a_lg'),{s:L(.6,1,eb(l)),o:cl(l*3)});popIn(q('a_bt'),pe(lt,Math.min(bt(0),.3),.45),t,0,60,0);if(lt>bt(0)+.6)T(q('a_bt'),{s:1+.04*Math.sin(t*7),o:1});
  const h=cl((lt-bt(0)-.4)/.5);T(q('a_hd'),{x:L(1040,925,eo(h)),y:L(900,660,eo(h)),o:cl(h*3)});const rp=((lt-bt(0))%1+1)%1;T(q('a_rp'),{s:1+rp*1.8,o:h>=1?1-rp:0});confU(q,'a_cf',lt,bt(0)+.9);
  popG(q('a_url'),lt,bt(1)-.2,t,1,30,3,.4);for(let i=0;i<1;i++)popG(q('a_sub'),lt,bt(2)+.2,t,2,20,0,.4)}});
