K.wt_drop=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="d0"><path d="M540 600 C470 720 420 800 420 880 a120 120 0 0 0 240 0 C660 800 610 720 540 600Z" fill="#3b82f6"/></g>
 <g data-k="q">${chip('star',540,1300,110,'#f59e0b')}</g>`,
 upd(q,lt,t,bt){const p0=eb(cl((lt-bt(0))/.6)),p1=eb(cl((lt-bt(1))/.5));T(q('d0'),{y:L(-300,0,eo(p0))+Math.sin(t*2)*8,s:L(.5,1,p0),o:cl(p0*2)});T(q('q'),{s:L(.3,1,p1),o:cl(p1*2)})}});
K.wt_cycle=()=>({svg:`<rect width="1080" height="1920" fill="url(#studio)"/>
 <g data-k="sun"><circle cx="300" cy="500" r="130" fill="#fbbf24"/></g><g data-k="cloud"><ellipse cx="700" cy="560" rx="220" ry="110" fill="#fff"/></g>
 <g data-k="rain">${[0,1,2,3,4].map(i=>`<rect x="${560+i*60}" y="760" width="14" height="70" rx="7" fill="#3b82f6"/>`).join('')}</g>`,
 upd(q,lt,t,bt){[['sun',0],['cloud',2],['rain',3]].forEach(([k,i])=>{const p=eb(cl((lt-bt(i))/.6));T(q(k),{y:L(120,0,eo(p)),s:L(.6,1,p),o:cl(p*2)})})}});
