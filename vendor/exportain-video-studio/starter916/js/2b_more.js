// ===================== Compliance — scenes 00–09 =====================
function badge(x,y,r,col,txt,size=40,f='Pop'){return `<g><circle cx="${x}" cy="${y}" r="${r}" fill="${col}"/><circle cx="${x}" cy="${y}" r="${r*.84}" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="6 6"/>${tx(x,y+size*.35,txt,size,'#fff',800,'middle',f)}</g>`}
function gate(x,y,w,h,col){return `<g><rect x="${x}" y="${y}" width="22" height="${h}" fill="${col}"/><rect x="${x+w-22}" y="${y}" width="22" height="${h}" fill="${col}"/><rect x="${x}" y="${y}" width="${w}" height="40" rx="8" fill="${col}"/></g>`}

const pill=(x,y,l,c,s=36,f='B',fg='#fff')=>chipT(x,y,l,c,s,f,fg);
