(function(){const N=22,AC=['#ffffff','#d9f5c4','#fde68a','#bfe8c6','#ffffff'];
 const AMB=Array.from({length:N},(_,i)=>`<circle data-k="amb${i}" cx="0" cy="0" r="${8+(i*37%34)}" fill="${AC[i%5]}" opacity="${.16+(i%4)*.05}"/>`).join('');
 for(const name of Object.keys(K)){if(!name.startsWith('ad_'))continue;const f=K[name];
  K[name]=()=>{const k=f();k.svg=k.svg.replace(/(<rect[^>]*\/>)/,'$1<g>'+AMB+'</g>');const u=k.upd;
   k.upd=function(q,lt,t,bt){for(let i=0;i<N;i++){const sp=26+(i*13%34);let y=((i*577)%1080-t*sp)%1180;if(y<-100)y+=1180;
     T(q('amb'+i),{x:(i*263)%1920+Math.sin(t*.55+i)*50,y:y,s:1+Math.sin(t*.9+i)*.18})}u.call(this,q,lt,t,bt)};return k}}})();
