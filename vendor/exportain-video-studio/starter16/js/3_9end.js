// ===== Reusable closing scenes (edit company name / product cards per topic) =====
// 16 Exportain
// Edit these two per topic (company name of the story character + 3 items shown on the company page)
const BRAND_CO='Rumana Handicrafts';
const BRAND_ITEMS=[['Trade License','Verified'],['ERC','Verified'],['EPB Enrolment','Verified']];
K.PFX_brand=()=>({svg:`${BG}
 <g data-k="xb_logo"><image href="__LOGO__" x="560" y="130" width="800" height="230" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="xb_pg">${card(100,400,860,560,'#fff',40)}<rect x="100" y="400" width="860" height="86" rx="40" fill="${C.g}"/><rect x="100" y="446" width="860" height="40" fill="${C.g}"/>${lat(140,456,'Company page · '+BRAND_CO,30,'#fff',800,'start')}${icon('bld',200,580,80,C.g,7)}${lat(270,592,'Certificates',36,C.ink,800,'start')}
  ${BRAND_ITEMS.map((c,i)=>`<g data-k="xb_c${i}"><rect x="140" y="${680+i*88}" width="780" height="74" rx="16" fill="#f1f8f1"/>${lat(170,726+i*88,c[0],28,C.ink,800,'start')}${lat(890,726+i*88,c[1],22,C.g,800,'end')}</g>`).join('')}</g>
 <g data-k="xb_tag">${card(1020,400,800,200,C.gd,40)}${tx(1420,480,'বাংলাদেশি প্রস্তুতকারক ও রপ্তানিকারকদের',34,'#fff',800)}${lat(1290,550,'B2B',40,C.y,800)}${tx(1350,550,'মার্কেটপ্লেস',40,'#e3f8d3',800,'start')}</g>
 <g data-k="xb_by">${card(1020,640,800,320,'#fff',40)}${person(1150,680,.6,'g','xb_bp')}${bub(1520,790,460,'Certificates verified ✓',C.b,'#fff',28,-1)}${tx(1520,910,'বিদেশি ক্রেতার আস্থা বাড়ে',36,C.g,800)}</g>`,
 // keys expected: 4 (e.g. ["এক্সপোর্টেইনে","কোম্পানির পাতায়","বিটুবি মার্কেটপ্লেস","বিদেশি ক্রেতা…"]) — retime as needed
 upd(q,lt,t,bt){const l=pe(lt,.2,.8);T(q('xb_logo'),{s:L(.5,1,eo(l))+(l>=1?Math.sin(t*2.2)*.03:0),y:l>=1?Math.sin(t*1.8)*10:0,o:cl(l*2)});popG(q('xb_pg'),lt,Math.min(bt(1)-.4,1.2),t,1,40,0,.5);for(let i=0;i<3;i++){const p=pe(lt,Math.min(bt(1),1.6)+i*.35,.4);T(q('xb_c'+i),{x:L(-50,0,eo(p)),o:cl(p*2)})}
  popG(q('xb_tag'),lt,bt(2)-.3,t,2,30,0,.45);popG(q('xb_by'),lt,bt(3)-.3,t,3,30,2,.45)}});

// 17 advice
K.PFX_advice=()=>({svg:`${BG}
 ${kw('v_h',960,230,'নিয়ম আর চাহিদা বদলায়',64,'#fff',C.o)}
 <g data-k="v_a">${card(140,320,500,600,'#fff',44)}${icon('globe',390,520,180,C.gd,6)}${lat(390,720,'EPB',44,C.gd,800)}${tx(390,790,'রপ্তানি উন্নয়ন ব্যুরো',32,C.mute,800)}</g>
 <g data-k="v_b">${card(710,320,500,600,'#fff',44)}${icon('bld',960,520,180,C.t,7)}${tx(960,740,'সংশ্লিষ্ট দপ্তর',42,C.t,800)}</g>
 <g data-k="v_c">${card(1280,320,500,600,'#fff',44)}${bank(1530,560,1.1,C.g)}${lat(1530,740,'AD Bank',44,C.g,800)}${tx(1530,800,'অনুমোদিত ডিলার ব্যাংক',28,C.mute,800)}</g>
 ${kw('v_w',960,1010,'নির্দিষ্ট পণ্যের আগে মিলিয়ে নিন',46,'#fff',C.gd)}`,
 upd(q,lt,t,bt){kwU(q,'v_h',lt,Math.min(bt(0)-.4,.2),t);const VB=[Math.min(bt(1)-.2,1),Math.min(bt(2)-.2,1.8),Math.min(bt(3)-.2,2.6)];['v_a','v_b','v_c'].forEach((k,i)=>{popG(q(k),lt,VB[i],t,i,40,2,.45);if(lt>VB[i]+.5)T(q(k),{y:Math.sin(lt*2+i*1.3)*10,s:lt>bt(1+i)&&lt<bt(1+i)+.6?1.05:1,o:1})});kwU(q,'v_w',lt,bt(3)+.6,t)}});

// 18 CTA
K.PFX_cta=()=>({svg:`${BG}
 <g data-k="ct_who">${card(100,200,700,260,'#fff',44)}${bdflag(150,270,150)}${tx(560,310,'প্রস্তুতকারক বা',44,C.ink,800)}${tx(560,390,'রপ্তানিকারক?',56,C.g,800)}</g>
 <g data-k="ct_gl">${icon('globe',450,760,300,C.t,4)}${[0,1,2,3].map(i=>`<g data-k="ct_f${i}"><circle cx="0" cy="0" r="40" fill="#fff"/>${icon(['shirt','bag','box','shoe'][i],0,0,50,[C.b,C.g,C.p,C.o][i],7)}</g>`).join('')}</g>
 <g data-k="ct_lg"><image href="__LOGO__" x="1010" y="220" width="760" height="220" preserveAspectRatio="xMidYMid meet"/></g>
 <g data-k="ct_bt">${card(1040,520,700,140,C.g,70)}${lat(1390,612,'Exportain.com',62,'#fff',800)}</g>
 <g data-k="ct_hd">${tap('ct_rp')}</g>
 ${kw('ct_u',1390,800,'আজই ভিজিট করুন',60,'#fff',C.o)}`,
 upd(q,lt,t,bt){popG(q('ct_who'),lt,Math.min(bt(0)-.2,.2),t,0,40,2,.5);popG(q('ct_gl'),lt,bt(1)-.4,t,1,30,0,.5);for(let i=0;i<4;i++){const p=pe(lt,bt(1)+i*.15,.5),a=i*1.57+t*.5;T(q('ct_f'+i),{x:450+Math.cos(a)*230,y:760+Math.sin(a)*200,s:L(.2,1,p),o:cl(p*2)})}
  const l=pe(lt,.4,.6);T(q('ct_lg'),{s:L(.6,1,eb(l)),o:cl(l*3)});popG(q('ct_bt'),lt,bt(2)-.4,t,2,30,0,.45);if(lt>bt(2)+.3)T(q('ct_bt'),{s:1+.04*Math.sin(t*7),o:1});
  const h=cl((lt-bt(2))/.5);T(q('ct_hd'),{x:L(1860,1700,eo(h)),y:L(760,640,eo(h)),o:cl(h*3)});const rp=((lt-bt(2))%1+1)%1;T(q('ct_rp'),{s:1+rp*1.8,o:h>=1?1-rp:0});kwU(q,'ct_u',lt,bt(2),t)}});
