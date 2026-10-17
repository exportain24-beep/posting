#!/usr/bin/env bash
set -e; cd "$(dirname "$0")"; SK=${SK:-__ENGINE__}
cat js/*.js > scenes.js
python3 $SK/scripts/topic_build.py --project . --logo assets/logo.png --brand Exportain --url Exportain.com --endcard 2.5 "$@"
python3 - <<'PY'
import json
p='scenes.html'; s=open(p,encoding='utf-8').read()
css="""@font-face{font-family:B;src:url('__FONTDIR__/NotoSansBengali-Regular.ttf');font-weight:400}
@font-face{font-family:B;src:url('__FONTDIR__/NotoSansBengali-SemiBold.ttf');font-weight:600}
@font-face{font-family:B;src:url('__FONTDIR__/NotoSansBengali-Bold.ttf');font-weight:700}
@font-face{font-family:B;src:url('__FONTDIR__/NotoSansBengali-ExtraBold.ttf');font-weight:800}
@font-face{font-family:Inter;src:url('__FONTDIR__/Inter.ttf');font-weight:100 900}
@font-face{font-family:Pop;src:url('__FONTDIR__/Poppins-Medium.ttf');font-weight:500}
@font-face{font-family:Pop;src:url('__FONTDIR__/Poppins-SemiBold.ttf');font-weight:600}
@font-face{font-family:Pop;src:url('__FONTDIR__/Poppins-Bold.ttf');font-weight:700}
@font-face{font-family:Pop;src:url('__FONTDIR__/Poppins-ExtraBold.ttf');font-weight:800}
#badge{height:4.6%!important;background:transparent!important;box-shadow:none!important;padding:0!important}
#badge img{filter:drop-shadow(0 3px 8px rgba(0,60,16,.18))}
"""
a="T(o.q('cam'),{s:1+.05*es(cl(lt/Math.max(dur,1)))});"; assert a in s
s=s.replace(a,"T(o.q('cam'),{s:1.03+.045*es(cl(lt/Math.max(dur,1))),x:Math.sin(lt*.42)*12,y:Math.cos(lt*.33)*14});")
s=s.replace("o.sc.kind==='logo_reveal'","(o.sc.kind==='logo_reveal'||o.sc.kind==='pv_none')")
s=s.replace('<style>','<style>'+css,1)
G='<linearGradient id="e_mint" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="#f3fcf4"/><stop offset="1" stop-color="#b9e6c2"/></linearGradient><linearGradient id="e_lime" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="#f7fde9"/><stop offset="1" stop-color="#c9ed9c"/></linearGradient><linearGradient id="e_sea" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="#ecf8f7"/><stop offset="1" stop-color="#a3dcd7"/></linearGradient><linearGradient id="e_gold" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="#fffae6"/><stop offset="1" stop-color="#f8dc8c"/></linearGradient><linearGradient id="e_sky" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="#eef5fa"/><stop offset="1" stop-color="#b3d0e6"/></linearGradient><linearGradient id="e_forest" x1="0" y1="0" x2=".4" y2="1"><stop offset="0" stop-color="#003c10"/><stop offset=".55" stop-color="#005a1e"/><stop offset="1" stop-color="#0e6e3a"/></linearGradient><linearGradient id="e_deep" x1="0" y1="0" x2=".4" y2="1"><stop offset="0" stop-color="#003c10"/><stop offset="1" stop-color="#0b3b5c"/></linearGradient>'
a='<linearGradient id="studio"'; assert a in s; s=s.replace(a,G+a,1)

a='<div id="end"><div class="ring r1"></div><div class="ring r2"></div><div class="lw"><img class="lg"><div class="shine"><i></i></div></div></div>'
assert a in s
s=s.replace(a,a[:-6]+'<div class="tgl"><span style="font-family:Pop;font-weight:700">provider.exportain.com</span></div></div>',1)
s=s.replace('<style>','<style>#end .tgl{position:absolute;left:0;right:0;top:61%;text-align:center;font-family:B;font-weight:700;font-size:40px;color:#005a1e}',1)
open(p,'w',encoding='utf-8').write(s)
pl=json.load(open('plan.json',encoding='utf-8')); pl['intro']=False; json.dump(pl,open('plan.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('9:16 template ready')
PY
