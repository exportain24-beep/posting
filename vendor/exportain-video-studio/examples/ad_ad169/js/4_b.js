// 04 — RFQ
K.ad_rfq=()=>{const R=[['DE','Germany','5,000 knit polos',C.b],['AE','UAE','2,000 jute bags',C.t],['US','USA','800 ceramic mugs',C.o]];return{svg:`${BG}
 ${kw('q_w0',520,220,'বিদেশি বায়ারের',72,C.ink)}${kw('q_w1',520,400,'RFQ',130,'#fff',C.b,'L')}
 ${R.map((r,i)=>`<g data-k="q_r${i}">${card(1000,150+i*220,840,180,'#fff',36)}<circle cx="1100" cy="${240+i*220}" r="50" fill="${r[3]}"/>${lat(1100,254+i*220,r[0],36,'#fff',800)}${lat(1180,225+i*220,'RFQ · '+r[1],36,C.ink,800,'start')}${lat(1180,280+i*220,r[2],30,C.mute,700,'start')}<g data-k="q_m${i}x">${pill(1700,250+i*220,'Matched ✓',C.g,26,'Pop')}</g></g>`).join('')}
 <g data-k="q_bt">${card(220,540,600,120,C.o,60)}${lat(520,618,'Send quotation',44,'#fff',800)}</g>
 <g data-k="q_hd">${tap('q_rp')}</g>
 <g data-k="q_or">${card(160,740,720,240,'#e9f8ec',50)}${check(290,860,60,C.g)}${lat(380,845,'Order created',52,C.g,800,'start')}${tx(380,920,'অর্ডার নিশ্চিত',36,C.ink,800,'start')}</g>
 ${confetti('q_cf',520,860)}`,
 upd(q,lt,t,bt){kwU(q,'q_w0',lt,Math.min(bt(0),.25),t);kwU(q,'q_w1',lt,bt(1)-.1,t);for(let i=0;i<3;i++){const p=pe(lt,bt(0)+.2+i*.3,.45);T(q('q_r'+i),{x:L(900,0,eo(p)),o:cl(p*2)});popIn(q('q_m'+i+'x'),pe(lt,bt(2)+i*.15,.3),t,i,0,0)}
  const h=cl((lt-bt(3)+.3)/.5);T(q('q_hd'),{x:L(960,760,eo(h)),y:L(760,600,eo(h)),o:cl(h*3)*(lt<bt(3)+1?1:0)});const rp=((lt-bt(3))%1+1)%1;T(q('q_rp'),{s:1+rp*1.8,o:lt>bt(3)?1-rp:0});
  T(q('q_bt'),{s:lt>bt(3)&&lt<bt(3)+.25?.92:1,o:lt>bt(3)-.5?1:.16});popG(q('q_or'),lt,bt(4)-.1,t,4,30,0,.45);confU(q,'q_cf',lt,bt(4))}}};

// 05 — TRUST
K.ad_trust=()=>({svg:`${BG}
 <g data-k="t_c">${cert(120,140,520,380,'ISO 9001',C.b)}<rect data-k="t_sc" x="120" y="140" width="520" height="14" fill="${C.g2}" opacity=".8"/></g>
 <g data-k="t_v">${shield(800,320,1.5,C.g,'✓')}${lat(800,500,'Verified',42,C.g,800)}</g>
 ${kw('t_w0',480,680,'ভেরিফায়েড ব্যাজ',80,'#fff',C.g)}
 <g data-k="t_p">${card(1040,140,800,380,'#fff',44)}${bank(1200,370,.85,C.gd)}<g data-k="t_tk"><circle cx="1520" cy="320" r="110" fill="${C.y}"/>${tx(1520,365,'৳',130,C.f,800)}</g>${lat(1730,310,'Payout',34,C.ink,800)}${lat(1730,360,'BDT',44,C.gd,800)}</g>
 ${kw('t_w1',1440,640,'পেমেন্ট টাকায়',80,C.gd)}
 <g data-k="t_cal">${Array.from({length:7},(_,i)=>`<g data-k="t_d${i}">${card(1020+i*120,730,105,130,i==6?C.g:'#fff',20)}${tx(1072+i*120,818,BN(i+1),52,i==6?'#fff':C.ink,800)}</g>`).join('')}</g>
 ${kw('t_w2',1440,960,'সাত দিনের মধ্যে',60,C.ink)}`,
 upd(q,lt,t,bt){popG(q('t_c'),lt,.15,t,0,40,2,.4);const sc=(lt*.9)%1;T(q('t_sc'),{y:sc*360,o:lt<bt(1)?1:0});popIn(q('t_v'),pe(lt,bt(1)-.2,.45),t,1,0,3);kwU(q,'t_w0',lt,bt(1),t);
  popG(q('t_p'),lt,bt(2)-.4,t,2,40,0,.4);if(lt>bt(2))T(q('t_tk'),{y:Math.sin(t*4)*8,s:1+.04*Math.sin(t*4),o:1});kwU(q,'t_w1',lt,bt(2)-.1,t);for(let i=0;i<7;i++)popIn(q('t_d'+i),pe(lt,bt(3)-.2+i*.1,.25),t,i,20,0);kwU(q,'t_w2',lt,bt(3)+.3,t)}});

// 06 — SHIFT
K.ad_shift=()=>({svg:`${BG}
 ${kw('c_w0',520,240,'যা শিখেছেন,',72,C.mute)}${kw('c_w1',520,380,'এবার কাজে লাগান',86,C.gd)}
 ${kw('c_w2',520,620,'ক্লাসরুম থেকে',76,C.ink)}${kw('c_w3',520,800,'সরাসরি বিশ্ববাজারে',80,'#fff',C.t)}
 <g data-k="c_rm">${card(1000,140,840,600,'#fff',44)}<rect x="1050" y="190" width="480" height="280" rx="16" fill="#1f4d3a"/>${lat(1290,290,'Export 101',48,'#e3f8d3',800)}${lat(1290,355,'L/C · Incoterms · Shipping',24,'#bde5a8',700)}${tx(1290,560,'ক্লাসরুম',44,C.ink,800)}
  <rect x="1580" y="190" width="220" height="500" rx="12" fill="#e9f8f6"/>${shipA(1690,560,.52)}<g data-k="c_dr"><rect x="1580" y="190" width="220" height="500" rx="12" fill="#7c4a12"/><circle cx="1770" cy="440" r="12" fill="${C.y}"/></g></g>
 <g data-k="c_gl">${icon('globe',1180,900,170,C.t,5)}${shipA(1560,920,.8)}</g>`,
 upd(q,lt,t,bt){kwU(q,'c_w0',lt,Math.min(bt(0),.2),t);kwU(q,'c_w1',lt,bt(1)-.1,t);popG(q('c_rm'),lt,.3,t,0,40,0,.45);const k=eio(cl((lt-bt(1)-.2)/.9));T(q('c_dr'),{x:L(0,-190,k),o:1-k*.95});
  kwU(q,'c_w2',lt,bt(2)-.1,t);popG(q('c_gl'),lt,bt(3)-.4,t,1,30,3,.45);kwU(q,'c_w3',lt,bt(3)-.05,t)}});

// 07 — CTA
K.ad_cta=()=>({svg:`${BG}
 ${kw('a_w0',960,170,'আজই',100,C.o)}
 <g data-k="a_lg"><image href="__LOGO__" x="610" y="200" width="700" height="210" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="a_bt">${card(470,450,980,200,C.g,100)}${tx(960,540,'ফ্রি সেলার অ্যাকাউন্ট',70,'#fff',800)}${tx(960,620,'খুলুন',50,'#e3f8d3',800)}</g>
 <g data-k="a_hd">${tap('a_rp')}</g>
 <g data-k="a_url">${card(640,700,640,130,'#fff',65)}${lat(960,787,'Exportain.com',62,C.gd,800)}</g>
 <g data-k="a_sub">${lat(960,890,'seller.exportain.com',36,C.mute,800)}${[['ফ্রি প্ল্যান',C.o],['বিদেশি বায়ার',C.b],['টাকায় পেমেন্ট',C.g]].map((c,i)=>pill([620,960,1300][i],990,c[0],c[1],32)).join('')}</g>
 ${confetti('a_cf',960,560)}`,
 upd(q,lt,t,bt){kwU(q,'a_w0',lt,Math.min(bt(0),.15),t);const l=pe(lt,.3,.5);T(q('a_lg'),{s:L(.6,1,eb(l)),o:cl(l*3)});popIn(q('a_bt'),pe(lt,bt(1)-.25,.45),t,0,60,0);if(lt>bt(1)+.5)T(q('a_bt'),{s:1+.03*Math.sin(t*7),o:1});
  const h=cl((lt-bt(1)-.4)/.5);T(q('a_hd'),{x:L(1500,1360,eo(h)),y:L(760,600,eo(h)),o:cl(h*3)});const rp=((lt-bt(1))%1+1)%1;T(q('a_rp'),{s:1+rp*1.8,o:h>=1?1-rp:0});confU(q,'a_cf',lt,bt(1)+.9);popG(q('a_url'),lt,bt(2)-.2,t,1,30,3,.4);popG(q('a_sub'),lt,bt(2)+.4,t,2,20,0,.4)}});
