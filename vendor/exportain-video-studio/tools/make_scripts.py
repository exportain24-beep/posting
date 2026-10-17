"""Write <prefix>_voiceover.txt (one ElevenLabs prompt) and <prefix>_script.md from
narration.json + meta.json in the project dir.
meta.json keys: title, prefix, length_bn (e.g. "প্রায় চার মিনিট"), acronyms (Bangla list shown in the
header), idea, audience, story, order, vis {scene_id: visual description}, verified [markdown bullets],
sources [urls].   Usage: python3 make_scripts.py <project_dir>"""
import json,re,sys,os
P=sys.argv[1] if len(sys.argv)>1 else '.'
n=json.load(open(os.path.join(P,'narration.json'),encoding='utf-8'))
m=json.load(open(os.path.join(P,'meta.json'),encoding='utf-8'))
for x in n:
    t=re.sub(r'\[.*?\]','',x['text'])
    assert '/' not in t, f"slash in {x['id']}"
    assert not re.search('[A-Za-z]',t), f"Latin letters in voice text {x['id']} - write them in Bangla"
chars=sum(len(re.sub(r'\[.*?\]\s*','',x['text'])) for x in n)
hdr=f"""EXPORTAIN — {m['title']} ({m.get('format','১৬:৯')}) — সম্পূর্ণ বাংলা ভয়েসওভার (এক প্রম্পট)
Voice: Debashish · Model: eleven_v4

কীভাবে ব্যবহার করবেন
• START আর END লাইনের মাঝের সবটুকু একসাথে ElevenLabs-এ একটি প্রম্পট হিসেবে পেস্ট করুন।
• দৃশ্যগুলোর মাঝে <break time="2.0s" /> = ২ সেকেন্ডের বিরতি। এই বিরতি দেখেই অডিওকে {len(n)}টি দৃশ্যে ভাগ করা হবে।
• সব সংক্ষিপ্ত রূপ বাংলা হরফে, কোথাও স্ল্যাশ নেই ({m.get('acronyms','')}); পর্দায় এগুলো ইংরেজিতে দেখানো হবে।
• শেষ লাইন CTA ("…এক্সপোর্টেইন ডট কম")। আলাদা আউটরো লাইন নেই।
• মোট প্রায় {chars:,} অক্ষর (ট্যাগ ছাড়া) → ভয়েস {m.get('length_bn','')}।

===== START =====

"""
body='\n\n<break time="2.0s" />\n\n'.join(x['text'] for x in n)
open(os.path.join(P,m['prefix']+'_voiceover.txt'),'w',encoding='utf-8').write(hdr+body+'\n\n===== END =====\n')
vis=m.get('vis',{})
rows='\n'.join(f"| {x['id'][:2]} | {x['text']} | {vis.get(x['id'],'')} |" for x in n)
md=f"""# Exportain — {m['title']} ({m.get('format','১৬:৯')})

মূল ভাবনা: {m.get('idea','')} · দর্শক: {m.get('audience','')} · ভয়েস: Debashish (eleven_v4)
গল্প: {m.get('story','')} {m.get('order','')} আলাদা আউটরো লাইন নেই।

| # | ন্যারেশন (ভয়েস) | ভিজ্যুয়াল ({m.get('format','১৬:৯')}) |
|---|---|---|
{rows}

## গবেষণায় যা যাচাই হলো
""" + '\n'.join('- '+v for v in m.get('verified',[])) + "\n\n## তথ্যসূত্র\n" + '\n'.join('- '+s for s in m.get('sources',[])) + '\n'
open(os.path.join(P,m['prefix']+'_script.md'),'w',encoding='utf-8').write(md)
est=chars*0.0858
print('wrote',m['prefix']+'_voiceover.txt',m['prefix']+'_script.md',chars,'chars  ->  est. video %d:%02d (incl. 2 s breaks)'%(est//60,est%60))
