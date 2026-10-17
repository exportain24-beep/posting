// ===================== Seller ad 16:9 — kinetic type + product UI (1920×1080) =====================
const BG=`<rect width="1920" height="1080" fill="url(#studio)"/>`;
const kw=(id,x,y,txt,size,col,hl,f='B')=>`<g data-k="${id}">${hl?`<rect x="${x-txt.length*size*.29-24}" y="${y-size*.95}" width="${txt.length*size*.58+48}" height="${size*1.3}" rx="${size*.3}" fill="${hl}"/>`:''}${f=='L'?lat(x,y,txt,size,col,800):tx(x,y,txt,size,col,800)}</g>`;
const kwU=(q,id,lt,b,t)=>{const e=q(id);if(!e)return;if(lt<b){T(e,{o:0,s:.6});return}const p=cl((lt-b)/.42);T(e,{s:L(.55,1,eb(p)),o:cl(p*3),y:L(30,0,eo(p))})};
const confetti=(id,cx,cy)=>`<g data-k="${id}">${Array.from({length:18},(_,i)=>`<rect data-k="${id}${i}" x="${cx-7}" y="${cy-7}" width="14" height="${i%2?14:22}" rx="3" fill="${[C.y,C.g2,C.o,C.t,C.b,C.r][i%6]}"/>`).join('')}</g>`;
const confU=(q,id,lt,b)=>{const p=cl((lt-b)/1.4);for(let i=0;i<18;i++){const a=i/18*6.283+.3,r=L(0,240+(i%3)*60,eo(p));T(q(id+i),{x:Math.cos(a)*r,y:Math.sin(a)*r*.7+p*p*120,r:p*360*(i%2?1:-1),o:p>0?1-p*p:0})}};
const tap=(id)=>`<circle cx="0" cy="0" r="34" fill="#ffffff" opacity=".85" stroke="${C.ink}" stroke-width="6"/><circle data-k="${id}" cx="0" cy="0" r="34" fill="none" stroke="#fff" stroke-width="6"/>`;

// 00 — HOOK
K.ad_hook=()=>({svg:`${BG}
 <g data-k="h_c">${cert(150,190,620,440,'Export Course',C.y)}${tx(460,460,'সার্টিফিকেট',42,C.ink,800)}${check(670,560,42,C.g)}</g>
 <g data-k="h_in">${card(220,730,480,120,'#ffffff22',60)}${icon('mail',300,790,70,'#fff',7)}${lat(520,810,'0 orders',48,'#fff',800)}</g>
 ${kw('h_w0',1320,300,'এক্সপোর্ট কোর্স',96,'#fff')}${kw('h_w1',1320,470,'শেষ?',140,C.g2)}
 ${kw('h_w2',1320,700,'বায়ার',150,C.f,C.y)}${kw('h_w3',1320,900,'কোথায়?',130,'#fff')}`,
 upd(q,lt,t,bt){const c=cl(lt/.5);T(q('h_c'),{y:L(-700,0,eb(c)),r:L(-8,-3,c)+Math.sin(t*2),o:1});kwU(q,'h_w0',lt,Math.min(bt(0),.3),t);kwU(q,'h_w1',lt,bt(1)-.05,t);
  kwU(q,'h_w2',lt,bt(2)-.05,t);kwU(q,'h_w3',lt,bt(3)-.05,t);if(lt>bt(3)+.4)T(q('h_w3'),{r:Math.sin(t*9)*4,o:1});popG(q('h_in'),lt,bt(3)+.2,t,0,20,0,.4)}});

// 01 — PAIN
K.ad_pain=()=>{const S=[['L/C',C.b],['Incoterms',C.t],['Shipping',C.o]];return{svg:`${BG}
 ${S.map((s,i)=>`<g data-k="p_s${i}">${card(110+i*330,160,300,160,'#fff',36)}${lat(260+i*330,255,s[0],42,s[1],800)}<g data-k="p_k${i}">${check(380+i*330,180,30,C.g)}</g></g>`).join('')}
 ${kw('p_w0',580,470,'সব শিখেছেন',96,C.gd)}
 ${kw('p_w1',580,760,'প্রথম অর্ডার?',100,'#fff',C.r)}
 <g data-k="p_ph">${phone(1180,140,380,800)}<rect x="1200" y="210" width="340" height="80" fill="${C.b}"/>${lat(1230,262,'Inbox',34,'#fff',800,'start')}${[0,1,2].map(i=>`<rect x="1220" y="${320+i*120}" width="300" height="96" rx="14" fill="#f1f5f9"/>`).join('')}${lat(1370,760,'No orders yet',32,C.mute,800)}</g>
 <g data-k="p_clk"><circle cx="1720" cy="380" r="100" fill="#fff" stroke="${C.ink}" stroke-width="10"/><g data-k="p_hand"><rect x="-5" y="-78" width="10" height="78" rx="5" fill="${C.r}"/></g></g>`,
 upd(q,lt,t,bt){for(let i=0;i<3;i++){popIn(q('p_s'+i),pe(lt,Math.min(bt(i)-.15,.1+i*.3),.4),t,i,40,2);popIn(q('p_k'+i),pe(lt,bt(i)+.1,.3),t,i,0,0)}kwU(q,'p_w0',lt,bt(3)-.1,t);
  popG(q('p_ph'),lt,bt(4)-.4,t,3,40,0,.5);popIn(q('p_clk'),pe(lt,bt(4)-.2,.4),t,4,0,0);T(q('p_hand'),{x:1720,y:380,r:t*240,o:1});kwU(q,'p_w1',lt,bt(5)-.15,t);if(lt>bt(5)+.4)T(q('p_w1'),{x:Math.sin(t*25)*cl((bt(5)+1-lt)*2)*10,o:1})}}};

// 02 — REVEAL
K.ad_reveal=()=>({svg:`${BG}<rect data-k="r_fl" width="1920" height="1080" fill="#fff"/>
 ${kw('r_w0',960,170,'এখানেই',70,C.mute)}
 <g data-k="r_ring"><circle cx="960" cy="340" r="230" fill="none" stroke="${C.g2}" stroke-width="10" opacity=".5"/><circle cx="960" cy="340" r="310" fill="none" stroke="${C.g}" stroke-width="6" opacity=".3"/></g>
 <g data-k="r_logo"><image href="__LOGO__" x="510" y="215" width="900" height="260" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="r_gl">${icon('globe',380,780,280,C.t,4)}${[[C.o,140,560],[C.b,620,560],[C.g,700,700]].map((a,i)=>`<path data-k="r_a${i}" d="M390 790 Q${(390+a[1])/2} ${a[2]-160} ${a[1]} ${a[2]}" stroke="${a[0]}" stroke-width="8" fill="none" stroke-dasharray="900" stroke-dashoffset="900"/>`).join('')}<circle cx="405" cy="805" r="16" fill="#f42a41"/></g>
 ${kw('r_w1',1260,640,'বাংলাদেশি প্রস্তুতকারক ও রপ্তানিকারকদের',46,C.ink)}
 ${kw('r_w2',1260,760,'আন্তর্জাতিক',72,C.b)}
 <g data-k="r_w3"><rect x="870" y="830" width="780" height="120" rx="32" fill="${C.gd}"/>${lat(1040,915,'B2B',76,C.y,800)}${tx(1360,915,'মার্কেটপ্লেস',76,'#fff',800)}</g>`,
 upd(q,lt,t,bt){T(q('r_fl'),{o:1-cl(lt/.5)});kwU(q,'r_w0',lt,Math.min(bt(0),.3),t);const l=pe(lt,bt(1)-.15,.7);T(q('r_logo'),{s:L(.4,1,eb(l))+(l>=1?Math.sin(t*1.6)*.015:0),o:cl(l*3)});
  const r=cl((lt-bt(1))/1.2);T(q('r_ring'),{s:L(.3,1.2,eo(r)),o:r>0?1-r*.6:0});popG(q('r_gl'),lt,bt(1)+.5,t,1,30,0,.5);for(let i=0;i<3;i++){const e=q('r_a'+i);if(e)e.setAttribute('stroke-dashoffset',900*(1-eio(cl((lt-bt(1)-.8-i*.2)/.9))))}
  kwU(q,'r_w1',lt,bt(2)-.1,t);kwU(q,'r_w2',lt,bt(3)-.1,t);kwU(q,'r_w3',lt,bt(4)-.1,t)}});

// 03 — SETUP
K.ad_setup=()=>({svg:`${BG}
 <g data-k="s_f">${badge(230,230,100,C.o,'FREE',48)}</g>${kw('s_w0',700,250,'ফ্রি প্ল্যানে শুরু',72,C.gd)}
 <g data-k="s_ph">${phone(120,370,400,680)}<rect x="140" y="440" width="360" height="66" fill="${C.g}"/>${lat(320,484,'seller.exportain.com',24,'#fff',800)}
  ${field(160,560,320,'Company name',C.g,'s_fd0')}${field(160,640,320,'Email',C.g,'s_fd1')}<g data-k="s_bt">${card(160,730,320,76,C.g,38)}${lat(320,780,'Create seller account',22,'#fff',800)}</g>
  <g data-k="s_ok">${check(320,900,54,C.g)}${lat(320,1000,'Account ready',28,C.g,800)}</g></g>
 <g data-k="s_cp">${card(580,370,440,560,'#fff',30)}<rect x="580" y="370" width="440" height="150" rx="30" fill="${C.t}"/><rect x="580" y="470" width="440" height="50" fill="${C.t}"/><circle cx="650" cy="530" r="50" fill="#fff" stroke="${C.t}" stroke-width="6"/>${icon('bld',650,530,60,C.gd,6)}${lat(720,570,'Company page',28,C.ink,800,'start')}
  ${[0,1,2].map(i=>`<rect x="${605+i*135}" y="640" width="120" height="96" rx="10" fill="${['#cfe9d4','#fde68a','#bfdbfe'][i]}"/>${factB(665+i*135,700,.18,C.mute)}`).join('')}${tx(800,800,'কারখানার ছবি · ঠিকানা',26,C.mute,800)}</g>
 ${[['shirt',C.b,'Knit polo'],['bag',C.g,'Jute tote'],['box',C.o,'Ceramics']].map((p,i)=>`<g data-k="s_p${i}">${card(1080+i*265,420,245,330,'#fff',30)}${icon(p[0],1202+i*265,540,130,p[1],7)}${lat(1202+i*265,670,p[2],30,C.ink,800)}${lat(1202+i*265,715,'MOQ · Price',22,C.mute,700)}</g>`).join('')}
 <g data-k="s_lb">${tx(1480,850,'পণ্য লিস্ট করুন',52,C.gd,800)}</g>`,
 upd(q,lt,t,bt){popIn(q('s_f'),pe(lt,Math.min(bt(0),.2),.45),t,0,0,3);if(lt>.6)T(q('s_f'),{r:Math.sin(t*3)*6,o:1});kwU(q,'s_w0',lt,Math.min(bt(0),.3),t);popG(q('s_ph'),lt,bt(1)-.4,t,1,40,0,.5);
  fillTo(q('s_fd0'),lt,bt(1)-.2,320,.4);fillTo(q('s_fd1'),lt,bt(1)+.1,320,.4);T(q('s_bt'),{s:lt>bt(1)+.5&&lt<bt(1)+.8?.93:1,o:1});popIn(q('s_ok'),pe(lt,bt(1)+.8,.35),t,2,0,0);
  popG(q('s_cp'),lt,bt(2)-.2,t,3,40,0,.5);for(let i=0;i<3;i++)popIn(q('s_p'+i),pe(lt,bt(3)-.1+i*.18,.4),t,i,60,3);popG(q('s_lb'),lt,bt(3)+.3,t,4,20,0,.4)}});
