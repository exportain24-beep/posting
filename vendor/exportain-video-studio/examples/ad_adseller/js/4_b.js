// 04 — RFQ: buyers' RFQs matched to you → quotation → order
K.ad_rfq=()=>{const R=[['#000','#dd0000','#ffce00','Germany','5,000 knit polos'],['#00732f','#fff','#000','UAE','2,000 jute bags'],['#b22234','#fff','#3c3b6e','USA','800 ceramic mugs']];return{svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 ${kw('q_w0',540,360,'বিদেশি বায়ারের',64,C.ink)}${kw('q_w1',540,490,'RFQ',110,'#fff',C.b,'L')}
 ${R.map((r,i)=>`<g data-k="q_r${i}">${card(80,600+i*200,920,170,'#fff',36)}<circle cx="170" cy="${685+i*200}" r="46" fill="${[C.b,C.t,C.o][i]}"/>${lat(170,700+i*200,['DE','AE','US'][i],34,'#fff',800)}${lat(250,670+i*200,'RFQ · '+r[3],34,C.ink,800,'start')}${lat(250,720+i*200,r[4],28,C.mute,700,'start')}<g data-k="q_m${i}0">${pill(860,690+i*200,'Matched ✓',C.g,26,'Pop')}</g></g>`).join('')}
 <g data-k="q_bt">${card(240,1250,600,120,C.o,60)}${lat(540,1328,'Send quotation',44,'#fff',800)}</g>
 <g data-k="q_hd"><circle cx="0" cy="0" r="34" fill="#ffffff" opacity=".85" stroke="${C.ink}" stroke-width="6"/><circle data-k="q_rp" cx="0" cy="0" r="34" fill="none" stroke="#fff" stroke-width="6"/></g>
 <g data-k="q_or">${card(160,1440,760,260,'#e9f8ec',50)}${check(300,1570,60,C.g)}${lat(400,1555,'Order created',52,C.g,800,'start')}${tx(400,1630,'অর্ডার নিশ্চিত',36,C.ink,800,'start')}</g>
 ${confetti('q_cf',540,1560)}`,
 upd(q,lt,t,bt){kwU(q,'q_w0',lt,Math.min(bt(0),.25),t);kwU(q,'q_w1',lt,bt(1)-.1,t);for(let i=0;i<3;i++){const p=pe(lt,bt(0)+.2+i*.3,.45);T(q('q_r'+i),{x:L(700,0,eo(p)),o:cl(p*2)});popIn(q('q_m'+i+'0'),pe(lt,bt(2)+i*.15,.3),t,i,0,0)}
  popG(q('q_bt'),lt,bt(3)-.5,t,3,30,0,.4);const h=cl((lt-bt(3)+.3)/.5);T(q('q_hd'),{x:L(980,790,eo(h)),y:L(1500,1310,eo(h)),o:cl(h*3)*(lt<bt(3)+1?1:0)});const rp=((lt-bt(3))%1+1)%1;T(q('q_rp'),{s:1+rp*1.8,o:lt>bt(3)?1-rp:0});T(q('q_bt'),{s:lt>bt(3)&&lt<bt(3)+.25?.92:1,o:lt>bt(3)-.5?1:.16});
  popG(q('q_or'),lt,bt(4)-.1,t,4,30,0,.45);confU(q,'q_cf',lt,bt(4))}}};

// 05 — TRUST: verified badge, taka payout within 7 days
K.ad_trust=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="t_c">${cert(140,300,520,400,'ISO 9001',C.b)}<rect data-k="t_sc" x="140" y="300" width="520" height="14" fill="${C.g2}" opacity=".8"/></g>
 <g data-k="t_v">${shield(820,500,1.6,C.g,'✓')}${lat(820,690,'Verified',44,C.g,800)}</g>
 ${kw('t_w0',540,850,'ভেরিফায়েড ব্যাজ',76,'#fff',C.g)}
 <g data-k="t_p">${card(80,960,920,420,'#fff',44)}${bank(250,1200,.9,C.gd)}<g data-k="t_tk"><circle cx="640" cy="1150" r="110" fill="${C.y}"/>${tx(640,1195,'৳',130,C.f,800)}</g>${lat(850,1150,'Payout',36,C.ink,800)}${lat(850,1200,'BDT',44,C.gd,800)}</g>
 ${kw('t_w1',540,1490,'পেমেন্ট টাকায়',76,C.gd)}
 <g data-k="t_cal">${Array.from({length:7},(_,i)=>`<g data-k="t_d${i}">${card(95+i*130,1580,115,140,i==6?C.g:'#fff',20)}${tx(152+i*130,1675,BN(i+1),56,i==6?'#fff':C.ink,800)}</g>`).join('')}</g>
 ${kw('t_w2',540,1830,'সাত দিনের মধ্যে',56,C.ink)}`,
 upd(q,lt,t,bt){popG(q('t_c'),lt,.15,t,0,40,2,.4);const sc=(lt*0.9)%1;T(q('t_sc'),{y:sc*380,o:lt<bt(1)?1:0});popIn(q('t_v'),pe(lt,bt(1)-.2,.45),t,1,0,3);kwU(q,'t_w0',lt,bt(1),t);
  popG(q('t_p'),lt,bt(2)-.4,t,2,40,0,.4);if(lt>bt(2))T(q('t_tk'),{y:Math.sin(t*4)*8,s:1+.04*Math.sin(t*4),o:1});kwU(q,'t_w1',lt,bt(2)-.1,t);for(let i=0;i<7;i++)popIn(q('t_d'+i),pe(lt,bt(3)-.2+i*.1,.25),t,i,20,0);kwU(q,'t_w2',lt,bt(3)+.3,t)}});

// 06 — SHIFT: from classroom to world market
K.ad_shift=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 ${kw('c_w0',540,360,'যা শিখেছেন,',70,C.mute)}${kw('c_w1',540,480,'এবার কাজে লাগান',84,C.gd)}
 <g data-k="c_rm">${card(80,560,920,700,'#fff',44)}<rect x="140" y="620" width="520" height="300" rx="16" fill="#1f4d3a"/>${lat(400,720,'Export 101',48,'#e3f8d3',800)}${lat(400,790,'L/C · Incoterms · Shipping',26,'#bde5a8',700)}${tx(400,1000,'ক্লাসরুম',44,C.ink,800)}
  <rect x="720" y="620" width="230" height="560" rx="12" fill="#e9f8f6"/>${shipA(835,1050,.55)}<g data-k="c_dr"><rect x="720" y="620" width="230" height="560" rx="12" fill="#7c4a12"/><circle cx="920" cy="900" r="12" fill="${C.y}"/></g></g>
 ${kw('c_w2',540,1360,'ক্লাসরুম থেকে',72,C.ink)}
 <g data-k="c_gl">${icon('globe',300,1600,200,C.t,5)}${shipA(720,1620,.9)}</g>
 ${kw('c_w3',540,1810,'সরাসরি বিশ্ববাজারে',76,'#fff',C.t)}`,
 upd(q,lt,t,bt){kwU(q,'c_w0',lt,Math.min(bt(0),.2),t);kwU(q,'c_w1',lt,bt(1)-.1,t);popG(q('c_rm'),lt,.3,t,0,40,0,.45);const k=eio(cl((lt-bt(1)-.2)/.9));T(q('c_dr'),{x:L(0,-200,k),o:1-k*.95});
  kwU(q,'c_w2',lt,bt(2)-.1,t);popG(q('c_gl'),lt,bt(3)-.4,t,1,30,3,.45);kwU(q,'c_w3',lt,bt(3)-.05,t)}});

// 07 — CTA
K.ad_cta=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 ${kw('a_w0',540,400,'আজই',110,C.o)}
 <g data-k="a_lg"><image href="__LOGO__" x="190" y="470" width="700" height="210" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="a_bt">${card(100,760,880,220,C.g,110)}${tx(540,850,'ফ্রি সেলার অ্যাকাউন্ট',64,'#fff',800)}${tx(540,935,'খুলুন',52,'#e3f8d3',800)}</g>
 <g data-k="a_hd"><circle cx="0" cy="0" r="34" fill="#ffffff" opacity=".85" stroke="${C.ink}" stroke-width="6"/><circle data-k="a_rp" cx="0" cy="0" r="34" fill="none" stroke="#fff" stroke-width="6"/></g>
 <g data-k="a_url">${card(190,1080,700,140,'#fff',70)}${lat(540,1172,'Exportain.com',64,C.gd,800)}</g>
 <g data-k="a_sub">${lat(540,1300,'seller.exportain.com',38,C.mute,800)}${[['ফ্রি প্ল্যান',C.o],['বিদেশি বায়ার',C.b],['টাকায় পেমেন্ট',C.g]].map((c,i)=>pill([200,540,860][i],1440,c[0],c[1],30)).join('')}</g>
 ${confetti('a_cf',540,870)}`,
 upd(q,lt,t,bt){kwU(q,'a_w0',lt,Math.min(bt(0),.15),t);const l=pe(lt,.3,.5);T(q('a_lg'),{s:L(.6,1,eb(l)),o:cl(l*3)});popIn(q('a_bt'),pe(lt,bt(1)-.25,.45),t,0,60,0);if(lt>bt(1)+.5)T(q('a_bt'),{s:1+.04*Math.sin(t*7),o:1});
  const h=cl((lt-bt(1)-.4)/.5);T(q('a_hd'),{x:L(1000,860,eo(h)),y:L(1150,900,eo(h)),o:cl(h*3)});const rp=((lt-bt(1))%1+1)%1;T(q('a_rp'),{s:1+rp*1.8,o:h>=1?1-rp:0});confU(q,'a_cf',lt,bt(1)+.9);popG(q('a_url'),lt,bt(2)-.2,t,1,30,3,.4);popG(q('a_sub'),lt,bt(2)+.4,t,2,20,0,.4)}});
