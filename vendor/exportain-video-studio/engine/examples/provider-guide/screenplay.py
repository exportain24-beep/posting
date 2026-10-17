#!/usr/bin/env python3
"""Exportain Service Provider Guide — visual screenplay (who-scene + 20 steps + outro).
Screens recreated from docs.exportain.com/provider screenshot descriptions; callout k = spoken word that triggers it."""
F=lambda label,value='',ph='',**kw:dict(t='field',label=label,value=value,ph=ph,**kw)
SEL=lambda label,value='',**kw:dict(t='select',label=label,value=value,**kw)
TA=lambda label,value='',**kw:dict(t='textarea',label=label,value=value,**kw)
BTN=lambda text,kind='primary',**kw:dict(t='btn',text=text,kind=kind,**kw)
H=lambda text,sub='',**kw:dict(t='h',text=text,sub=sub,**kw)
ROW=lambda *items:dict(t='row',items=list(items))
N=lambda text,tone='',**kw:dict(t='note',text=text,tone=tone,**kw)
C=lambda k,id,s=0,**kw:dict(k=k,id=id,s=s,**kw)
U='provider.exportain.com'
MENU=[['Home',['Overview']],['Your services',['My Services','Freight rates']],['Work',['Leads','Offers','Service orders','Disputes']],
      ['Inbox',['Messages','Notifications','Help & support']],['Account',['Verification','Membership & Plans','Team','Settings']]]

CONFIG=dict(menu=MENU,steps=20,url=U,add_label='+ Add service',badges={'Leads':5},logo='')  # logo: pass --logo to guide_plan.py

INTRO=dict(kind='who',title='কে কোন অ্যাকাউন্ট খুলবেন?',sfx=['pop','pop2','bubble','tick'],
 callouts=[C('কে সার্ভিস প্রোভাইডার','q'),C('সার্ভিস প্রোভাইডার হয়ে','L')]+
  [C(k,f'L{i}') for i,k in enumerate(['ফ্রেইট','শিপিং','কাস্টমস','ইন্সপেকশন','সার্টিফিকেশন','বন্ডেড','প্যাকেজিং','বায়িং','ইন্সুরেন্স','ফাইন্যান্স'])]+
  [C('প্রোভাইডারে অ্যাকাউন্ট','Lok'),C('প্রোডাক্ট থাকে','R')]+[C(k,f'R{i}') for i,k in enumerate(['গার্মেন্টস','চামড়া','পাট','খাদ্যপণ্য'])]+
  [C('সেলার অ্যাকাউন্ট','Rok'),C('সার্ভিস মানে','Lg'),C('পণ্য মানে','Rg'),C('চলুন','go')])

SERV=[['Freight Forwarders','Air, sea & road cargo'],['Shipping Agents','Port & vessel agency'],['Customs Brokers (C&F Agents)','Export clearance'],
      ['Inspection & Quality Audits','Pre-shipment checks'],['Certification Bodies','Compliance & testing'],['Export Packaging','Cartons, pallets, crates']]
STEPS=[
dict(n=1,title='প্রোভাইডার অ্যাকাউন্ট খোলা',icon='rocket',url=U+'/register',side=False,
 screens=[dict(layout='center',comps=[
   dict(t='stepper',items=['Categories','Account','Verify','Done'],active=0,id='stp'),
   H('What services do you offer?','Select all that apply — you can add more later',id='q'),
   dict(t='choice',id='sv',n=2,items=SERV),
   SEL('Coverage regions','Bangladesh, Southeast Asia',id='cov'),
   BTN('Continue',id='cont')]),
  dict(layout='center',comps=[
   dict(t='stepper',items=['Categories','Account','Verify','Done'],active=1,id='stp2'),
   ROW(F('Full name','Karim Hossain',id='fn'),F('Work email','karim@karnaphulilogistics.com',id='em')),
   ROW(F('Company name','Karnaphuli Logistics Ltd.',id='co'),SEL('Country','Bangladesh',id='cty')),
   F('Password (min. 8 characters)','••••••••••',id='pw'),
   dict(t='check',label='I agree to the Terms of Use and Privacy Policy',id='tc'),
   BTN('Send Verification Code',id='svc'),
   dict(t='code',value='731804',id='code'),
   BTN('Verify & Create Account',id='vca')])],
 callouts=[C('register','stp'),C('What services','q'),C('Customs Brokers','sv.2'),C('Coverage','cov'),C('Continue','cont'),
  C('Full name','fn',1),C('Work email','em',1),C('কোম্পানির নাম','co',1),C('দেশ','cty',1),C('Password','pw',1),C('শর্তাবলিতে','tc',1),
  C('Send Verification Code','svc',1),C('ছয় সংখ্যার','code',1),C('Verify &','vca',1),C('বায়ার বা সেলার','em',1)]),
dict(n=2,title='লগইন ও পাসওয়ার্ড',icon='key',url='exportain.com/login',side=False,
 screens=[dict(layout='center',comps=[
   H('Sign in to Exportain','Each account type signs in on its own portal',id='h'),
   dict(t='choice',id='rl',items=[['Sign In as Buyer','Overseas buyers'],['Sign In as Seller','BD factories & exporters'],['Sign In as Provider','Trade service providers']]),
   F('Email','karim@karnaphulilogistics.com',id='em'),
   ROW(F('Password','••••••••••',id='pw'),BTN('Forgot?','ghost',id='fg')),
   dict(t='btns',id='bb',items=[['Sign In to Provider Center','primary'],['Continue with Google','ghost']]),
   N('Google sign-up = no company profile. Register with email for your business.','w',id='nt')]),
  dict(layout='center',comps=[
   H('Reset your password','We will send you a 6-digit code'),
   dict(t='choice',id='rc',items=[['Email','Code to your account email'],['WhatsApp (verified number)','Only if already verified']]),
   F('Account email','karim@karnaphulilogistics.com',id='ae'),
   BTN('Send code by email',id='sc'),
   dict(t='code',value='285146',id='code'),
   F('New password','••••••••••••',id='np'),
   BTN('Reset Password',id='rp')])],
 callouts=[C('লগইন পাতায়','h'),C('Sign In as Provider','rl.2'),C('ইমেইল আর','em'),C('পাসওয়ার্ড দিয়ে','pw'),C('Sign In to Provider Center','bb.0'),
  C('Continue with Google','bb.1'),C('কোম্পানি প্রোফাইল','nt'),C('Forgot?','fg'),C('Email বা','rc.0',1),C('WhatsApp','rc.1',1),C('কোড নিন','code',1),
  C('নতুন পাসওয়ার্ড','np',1),C('Reset Password','rp',1)]),
dict(n=3,title='কাজের সঠিক ক্রম',icon='grid',url=U+'/overview',active='Overview',
 screens=[dict(comps=[
   H('Getting started','Recommended order after opening your account'),
   dict(t='list',id='ls',items=[['1 · Publish each service listing','My Services → cover image, title, price, service area','Start','b'],
     ['2 · Submit trade licence for verification','Verification → only verified companies appear in the provider directory','Important','y'],
     ['3 · Add freight routes & prices','Freight rates → only for freight profiles','If freight','g'],
     ['4 · Reply to leads & send offers','Leads → Offers','Win work','b'],
     ['5 · Complete orders & get paid','Service orders → escrow & payout','Get paid','']]),
   N('New Free account: 90-day free period starts the day you register','g',id='nt')])],
 callouts=[C('এই ক্রমে','ls'),C('My Services','ls.0'),C('Verification','ls.1'),C('Freight rates','ls.2'),C('Leads','ls.3'),C('Service orders','ls.4'),C('নব্বই দিনের','nt')]),
dict(n=4,title='ড্যাশবোর্ড পরিচিতি',icon='grid',url=U+'/overview',active='Overview',
 screens=[dict(comps=[
   H('Welcome, Karnaphuli Logistics Ltd.','Plan: FREE'),
   ROW(dict(t='ring',id='ring',center='1/9',text='Verification steps',sub='1 of 9 steps · Verification Center →',pct=0),
       dict(t='btns',id='wb',items=[['Add service','primary'],['View leads','ghost']])),
   dict(t='cards',n=3,id='cards',items=[['Published services · of 3 on your plan','2'],['New leads','5'],['Open offers · 4 sent','2'],['Active service orders · 1 funds held','1'],['Unread messages · 2 chats','3']]),
   BTN('Next verification step: Mobile number →','blue',id='nv')])],
 callouts=[C('Overview','menu:Overview'),C('Jump to a page','hdr:search'),C('বেল','hdr:bell'),C('Add service','hdr:add'),
  C('রিং','ring',ring=11),C('Published services','cards.0'),C('New leads','cards.1'),C('Open offers','cards.2'),C('Active service orders','cards.3'),C('Unread messages','cards.4'),C('Next verification step','nv')]),
dict(n=5,title='My Services: সার্ভিস লিস্টিং',icon='store',url=U+'/services',active='My Services',
 screens=[dict(comps=[
   ROW(H('My Services','Each service is its own listing'),BTN('+ Add service',id='add')),
   dict(t='cards',n=3,id='cards',items=[['Active','2'],['Drafts','1'],['Unpublished','0']]),
   N('Your plan: 2 of 3 published listings used · Upgrade for more','w',id='pl'),
   dict(t='list',id='ls',items=[['Sea Freight Chattogram to Europe','USD 1,200 · Per container · Chattogram','Live','',''],
     ['Export Customs Clearance in Chattogram','Starting from BDT 8,000 · 2–4 days','Live','',''],
     ['Export Packaging','Missing: photo, price','Draft','y','Complete this draft']]),
   dict(t='btns',id='act',items=[['Edit','ghost'],['View','ghost'],['⋯  Publish · Unpublish · Archive','ghost']])])],
 callouts=[C('My Services','menu:My Services'),C('Active','cards.0'),C('Drafts','cards.1'),C('Unpublished','cards.2'),C('Your plan','pl'),
  C('Complete this draft','ls.2.b'),C('স্ট্যাটাস','ls.0'),C('Edit','act.0'),C('View','act.1'),C('তিন-ডটের','act.2')]),
dict(n=6,title='নতুন সার্ভিস: Basics',icon='box',url=U+'/services/new',active='My Services',
 screens=[dict(comps=[
   ROW(H('Add a service'),dict(t='stepper',items=['Basics','Price & area','More details'],active=0,id='stp')),
   ROW(dict(t='upload',label='Photo',sub='Square 1:1 · JPG, PNG, WebP · max 500 KB',id='ph'),
       dict(t='list',id='chk',items=[['Ready to publish?','0 of 6 done','0/6','y']])),
   SEL('Service','Customs Brokers (C&F Agents)',id='sv'),
   F('Title','Export Customs Clearance in Chattogram',id='ti'),
   TA('Description','We clear export shipments at Chattogram port within 48 hours. Price includes documentation, ASYCUDA filing and port handling...',id='ds'),
   ROW(N('How buyers see the card — live preview','',id='pv'),dict(t='btns',id='nb',items=[['Back','ghost'],['Save draft','ghost'],['Next','primary']]))])],
 callouts=[C('Add service','hdr:add'),C('তিনটি ধাপের','stp'),C('ফটো','ph'),C('Service','sv'),C('Other','sv'),C('Title','ti'),C('Description','ds'),
  C('Ready to publish','chk'),C('প্রিভিউ','pv'),C('Next','nb.2')]),
dict(n=7,title='Price & area: দাম ও এলাকা',icon='wallet',url=U+'/services/new',active='My Services',
 screens=[dict(comps=[
   ROW(H('Add a service'),dict(t='stepper',items=['Basics','Price & area','More details'],active=1,id='stp')),
   dict(t='toggles',id='tg',items=[['Contact for price — buyers request a quote',False]]),
   ROW(F('Price','8000',id='pr'),SEL('Currency','BDT',id='cu')),
   SEL('Price basis','Per shipment',id='pb'),
   F('How long it takes (optional)','2–4 days',id='hl'),
   F('Where you offer it (1–20)','Chattogram Port, Bangladesh  ·  Dhaka ICD  ·  Benapole',id='wo'),
   dict(t='btns',id='nb',items=[['Back','ghost'],['Save draft','ghost'],['Next','primary']])])],
 callouts=[C('Contact for price','tg.0',flip=True),C('Price ঘরে','pr'),C('Currency','cu'),C('Price basis','pb'),C('How long','hl'),C('Where you offer','wo')]),
dict(n=8,title='More details ও Publish',icon='star',url=U+'/services/new',active='My Services',
 screens=[dict(comps=[
   ROW(H('Add a service'),dict(t='stepper',items=['Basics','Price & area','More details'],active=2,id='stp')),
   dict(t='choice',id='dv',items=[['On site','At your location'],['Remote','Online / documents'],['At the port','Port-side work']]),
   ROW(SEL('Languages you work in','Bengali, English',id='lg'),F('Highlights (up to 6)','48-hour clearance · Door-to-door tracking',id='hi')),
   F('Licence number (if required)','CB-CTG-2024-1187',id='ln'),
   dict(t='btns',id='bt',items=[['Preview','ghost'],['Save draft','ghost'],['Publish','primary']])]),
  dict(layout='modal',comps=[
   H('🎉 Your service is live!','No approval needed — published instantly',id='live'),
   dict(t='cards',n=3,id='lim',items=[['Free · listings','3'],['Gold · listings','10'],['Platinum · listings','30']])])],
 callouts=[C('On site','dv.0'),C('Remote','dv.1'),C('At the port','dv.2'),C('Languages','lg'),C('Highlights','hi'),C('Licence number','ln'),
  C('Preview','bt.0'),C('Save draft','bt.1'),C('Publish চাপুন','bt.2'),C('লাইভ','live',1),C('Free প্ল্যানে','lim.0',1),C('Gold-এ','lim.1',1),C('Platinum-এ','lim.2',1)]),
dict(n=9,title='Verification Center',icon='shield',url=U+'/verification',active='Verification',
 screens=[dict(comps=[
   H('Verification Center','Your progress · Do this next'),
   dict(t='cards',n=3,id='tc',items=[['Personal · email, mobile, WhatsApp, identity','1/6'],['Professional · trade licence','0/2'],['Business · registration documents','0/1']]),
   ROW(dict(t='ring',id='ring',center='1/9',text='Your progress',sub='1 of 9 steps verified — a step count, not a score',pct=0),
       N('Do this next: Verify your mobile number','w',id='dn')),
   dict(t='stepper',items=['Personal','Professional','Business','Verify every step'],active=0,id='pp'),
   BTN('Take me there →','blue',id='tm')])],
 callouts=[C('মেনু থেকে','menu:Verification'),C('Personal','tc.0'),C('Professional','tc.1'),C('Business','tc.2'),C('প্রোগ্রেস রিং','ring',ring=11),
  C('Do this next','dn'),C('Take me there','tm')]),
dict(n=10,title='ইমেইল, মোবাইল ও হোয়াটসঅ্যাপ যাচাই',icon='phone',url=U+'/verification#personal',active='Verification',
 screens=[dict(comps=[
   dict(t='list',id='em',items=[['01 · Email address','karim@karnaphulilogistics.com','Verified · 1 Oct','','']]),
   ROW(F('02 · Mobile number','+880 1712 345678',id='mb'),BTN('Send code by SMS',id='sms')),
   dict(t='code',value='540921',id='code'),
   ROW(F('03 · WhatsApp number (any country)','+880 1712 345678',id='wa'),BTN('Send code by WhatsApp','blue',id='wab')),
   N('Steps 04–06 (NID/passport + selfie, owner ID, personal TIN): Ask support → support@exportain.com','',id='nt')])],
 callouts=[C('ইমেইল সাধারণত','em.0'),C('প্লাস আট আট শূন্য','mb'),C('Send code by SMS','sms'),C('ছয়টি ঘরে','code'),C('হোয়াটসঅ্যাপের জন্য','wa'),
  C('Send code by WhatsApp','wab'),C('NID','nt')]),
dict(n=11,title='বিজনেস রেজিস্ট্রেশন ও লাইসেন্স',icon='doc',url=U+'/verification#business',active='Verification',
 screens=[dict(comps=[
   H('Business registration','Must match your trade licence exactly'),
   F('Legal business name','Karnaphuli Logistics Ltd.',id='lb'),
   ROW(F('Trade licence number','TRAD/CTG/045812',id='tl'),F('Trade licence expiry date','30 Jun 2027',id='ex')),
   F('Registered address','Agrabad C/A, Chattogram',id='ra'),
   dict(t='upload',label='Trade licence (required)',sub='PDF, JPG, PNG or WEBP · up to 10 MB · private to reviewers',id='up'),
   BTN('Submit for review',id='sb')]),
  dict(layout='modal',comps=[
   H('Upload a credential document','Which document is this?'),
   dict(t='choice',id='dt',n=1,items=[['Professional Certification / Trade License',''],['Insurance Certificate',''],['Customs Broker License','']]),
   dict(t='upload',label='Choose file',sub='PDF, JPG, PNG or WebP · up to 10 MB',id='up2'),
   BTN('Submit for review',id='sb2')])],
 callouts=[C('Legal business name','lb'),C('Trade licence number','tl'),C('Registered address','ra'),C('মেয়াদ শেষের','ex'),C('Trade licence ফাইল','up'),
  C('Submit for review','sb'),C('কাস্টমস ব্রোকার','dt.2',1),C('ইন্সুরেন্স','dt.1',1),C('Upload a credential','up2',1)]),
dict(n=12,title='প্রোভাইডার ব্যাজ',icon='medal',url=U+'/verification#badges',active='Verification',
 screens=[dict(comps=[
   H('Provider badges','Earned only through verification'),
   dict(t='list',id='ls',items=[['Export Customs Clearance in Chattogram','Karnaphuli Logistics Ltd. · Chattogram','✓ Verified Provider','','View service']]),
   dict(t='badges',id='bd',items=[['Verified Provider',True],['Licence Verified',True],['Certification Verified',True],['Insurance Verified',True],['Facility Verified',False]]),
   N('Plans are not verification — Free and Platinum get the same badges for the same proof','w',id='nt')])],
 callouts=[C('ব্যাজ দেখা','ls.0'),C('Verified Provider','bd.0'),C('Licence Verified','bd.1'),C('Certification Verified','bd.2'),C('Insurance Verified','bd.3'),C('প্ল্যান কিনে','nt')]),
dict(n=13,title='Leads: সার্ভিস রিকোয়েস্ট',icon='bell',url=U+'/leads',active='Leads',
 screens=[dict(comps=[
   dict(t='tabs',id='tb',items=['All','New','Quoted','Contacted','Declined','Closed'],active=0),
   ROW(dict(t='list',id='ld',items=[['Rotterdam Textiles BV','Customs clearance · 2 × 40ft','New','b'],['Dhaka Knit Ltd.','Sea freight to Hamburg','New','b'],['Hamburg Home GmbH','Pre-shipment inspection','Quoted','g']]),
       dict(t='list',id='dt',items=[['Rotterdam Textiles BV','Service: Export customs clearance'],['Route: Chattogram → Rotterdam',''],['From listing: Export Customs Clearance in Chattogram','']])),
   TA('Your response','We can clear 2 × 40ft at Chattogram within 48 hours. Estimated BDT 16,000. We can start Monday.',id='rs'),
   dict(t='btns',id='ab',items=[['Send Response','primary'],['Mark Contacted','ghost'],['Mark Closed','ghost'],['Decline','danger']]),
   N('Free plan: replies to 15 leads per month · Gold & Platinum: unlimited','',id='nt')])],
 callouts=[C('New','tb.1'),C('একটি লিডে','ld.0'),C('Route','dt.1'),C('From listing','dt.2'),C('রেসপন্স বক্সে','rs'),C('Send Response','ab.0'),
  C('Mark Contacted','ab.1'),C('Mark Closed','ab.2'),C('Decline','ab.3'),C('পনেরোটি','nt')]),
dict(n=14,title='Offers: নির্দিষ্ট দামের অফার',icon='doc',url=U+'/offers/new',active='Offers',
 screens=[dict(comps=[
   ROW(H('Write an offer','One fixed price for one job'),BTN('Write an offer',id='wo')),
   ROW(F('Who it goes to','Rotterdam Textiles BV',id='wh'),SEL('Which service','Export Customs Clearance',id='ws')),
   F('Title','Customs clearance, 2 x 40ft, Chattogram',id='ti'),
   TA('What is included','Included: documentation, ASYCUDA filing, port handling. Not included: duties, storage charges.',id='wi'),
   ROW(F('Price','16000',id='pr'),SEL('Currency','BDT',id='cu'),SEL('How they may pay','Either',id='hp'),F('Hold this price until','30 Oct 2026',id='hd')),
   BTN('Send the offer',id='so')]),
  dict(comps=[
   H('Offers','Sent offers cannot be edited'),
   dict(t='list',id='ol',items=[['Customs clearance, 2 x 40ft, Chattogram','To: Rotterdam Textiles BV · BDT 16,000 · valid until 30 Oct','Sent','b','']]),
   dict(t='btns',id='ob',items=[['Send a new price','primary'],['Withdraw','danger']])])],
 callouts=[C('Write an offer','wo'),C('Who it goes to','wh'),C('Which service','ws'),C('Title-এ','ti'),C('What is included','wi'),C('Price আর','pr'),C('Currency','cu'),
  C('How they may pay','hp'),C('Hold this price','hd'),C('Send the offer','so'),C('পাঠানো অফার','ol.0',1),C('Send a new price','ob.0',1),C('Withdraw','ob.1',1)]),
dict(n=15,title='Freight rates: রুট ও দাম',icon='ship',url=U+'/freight-rates',active='Freight rates',
 screens=[dict(comps=[
   ROW(H('Freight rates','Routes & prices from Bangladesh'),BTN('+ Add a route',id='ar')),
   N('Freight rates need a freight profile — forwarder, logistics, shipping agent, NVOCC, consolidation, trucking. Buyers see prices only after verification.','w',id='nw'),
   dict(t='list',id='rl0',items=[['Chattogram → Rotterdam · Sea FCL','24 days · 40ft HC · USD 2,150','Hidden from buyers','g','']])]),
  dict(layout='modal',comps=[
   H('Add a route'),
   ROW(SEL('Origin port','Chattogram (BDCGP)',id='op'),SEL('Destination country','Netherlands',id='dc'),SEL('Destination port','Rotterdam',id='dp')),
   ROW(SEL('Transport mode','Sea FCL',id='tm'),F('Transit time (days)','24',id='tt')),
   ROW(SEL('Cargo type','General',id='ct'),F('Container size','40ft HC',id='cs'),F('Price','USD 2,150',id='pr'),F('Valid until','31 Dec 2026',id='vu')),
   BTN('Save route',id='sr')]),
  dict(comps=[
   H('Freight rates','Buyers see your rate next to products and in the cart'),
   dict(t='list',id='rl',items=[['Chattogram → Rotterdam · Sea FCL','24 days · 40ft HC · USD 2,150 · valid until 31 Dec','Buyers can see this','',''],
     ['Chattogram → Hamburg · Sea FCL','26 days · 20ft · USD 1,480','Buyers can see this','','']])])],
 callouts=[C('ফ্রেইট প্রোফাইলের','nw'),C('Add a route','ar'),C('Origin port','op',1),C('গন্তব্য দেশ','dc',1),C('Transport mode','tm',1),C('ট্রানজিট','tt',1),
  C('Cargo type','ct',1),C('কন্টেইনার','cs',1),C('Price আর','pr',1),C('Valid until','vu',1),C('Save route','sr',1),C('Buyers can see this','rl.0',2),C('কার্টে','rl.1',2)]),
dict(n=16,title='Service orders ও পেমেন্ট',icon='wallet',url=U+'/service-orders',active='Service orders',
 screens=[dict(comps=[
   ROW(H('Service orders','Accepted offers become orders'),BTN('Refresh','ghost',id='rf')),
   dict(t='cards',n=3,id='cards',items=[['Service orders','3'],['Money held','1'],['Waiting on you','1']]),
   dict(t='list',id='ol',items=[['SO-10482 · Customs clearance, 2 x 40ft','The customer has paid and Exportain is holding the money · Commission 5%','BDT 16,000','b','Mark work complete'],
     ['SO-10461 · Sea freight to Hamburg','You have said the work is done · waiting for customer (3 days)','USD 1,480','y',''],
     ['SO-10417 · Export packaging','Exportain has recorded the payout to you','Paid','','']]),
   dict(t='cards',n=3,id='cm',items=[['Commission · Free','5%'],['Commission · Gold','2%'],['Commission · Platinum','0%']])])],
 callouts=[C('অর্ডারটি','menu:Service orders'),C('মোট অর্ডার','cards.0'),C('Money held','cards.1'),C('Waiting on you','cards.2'),C('SO নম্বর','ol.0'),
  C('Mark work complete','ol.0.b'),C('তিন দিনে','ol.1'),C('কমিশন Free','cm.0'),C('Gold-এ','cm.1'),C('Platinum-এ','cm.2')]),
dict(n=17,title='প্ল্যান: Free, Gold ও Platinum',icon='star',url=U+'/membership',active='Membership & Plans',
 screens=[dict(comps=[
   H('Membership & Plans','This month: 2 of 3 listings · 6 of 15 lead replies'),
   dict(t='cards',n=3,id='cards',items=[['Current plan','Free'],['Commission','5%'],['Your free period · ends 9 Jan','62 days']]),
   dict(t='plans',id='pl',active=0,items=[['Free','৳0',['First 90 days','3 listings · 5% commission','15 lead replies / month','1 team member'],'Current plan'],
     ['Gold','৳599/mo',['10 listings · 2% commission','Unlimited lead replies','5 team members'],'Subscribe to Gold'],
     ['Platinum','৳1,199/mo',['30 listings · 0% commission','Unlimited lead replies','Unlimited team'],'Subscribe to Platinum']])])],
 callouts=[C('Membership & Plans','menu:Membership & Plans'),C('Current plan','cards.0'),C('Free প্ল্যান','pl.0'),C('Gold মাসে','pl.1'),C('Platinum এগারোশো','pl.2'),
  C('ফ্রি সময় শেষ','cards.2'),C('Subscribe to Gold','pl.1.b')]),
dict(n=18,title='Help & support টিকিট',icon='help',url=U+'/support',active='Help & support',
 screens=[dict(comps=[
   ROW(H('Help & support','All replies stay in one thread'),BTN('+ New ticket',id='nt')),
   dict(t='tabs',id='tb',items=['All','Waiting for you','Open','Solved'],active=0),
   dict(t='list',id='tl',items=[['EXP-SUP-2041 · Verification stuck','Updated 2h ago','Waiting for you','y',''],['EXP-SUP-1988 · No leads arriving','Updated yesterday','Open','b','']])]),
  dict(layout='modal',comps=[
   H('New ticket','Choose a topic'),
   dict(t='choice',id='tp',n=4,items=[['Account',''],['Verification',''],['Lead',''],['Payment','']]),
   F('Subject','Trade licence verification pending for 5 days',id='sj'),
   TA('Description','I submitted my trade licence on 1 Oct. I expected review in 2 days, but status still shows pending.',id='ds'),
   dict(t='upload',label='Attach a screenshot (optional)',sub='Up to 10 MB · 5 files',id='up'),
   dict(t='btns',id='bb',items=[['Next','ghost'],['Send ticket','primary']])]),
  dict(comps=[
   dict(t='tabs',id='tb2',items=['All','Waiting for you','Open','Solved'],active=0),
   dict(t='chat',id='ch',items=[['them','Support: Thanks Karim — please re-upload a clearer licence copy.'],['me','Done, uploaded now.'],['them','Verified ✓ Your business registration is active.']]),
   BTN('My problem is solved',id='ms'),
   N('Never send passwords, card numbers, bank details or ID documents in a ticket','r',id='wn')])],
 callouts=[C('New ticket','nt'),C('Account','tp.0',1),C('Payment','tp.3',1),C('Next','bb.0',1),C('Subject','sj',1),C('বিবরণে','ds',1),C('স্ক্রিনশট','up',1),
  C('Send ticket','bb.1',1),C('Waiting for you','tb2.1',2),C('My problem is solved','ms',2),C('পাসওয়ার্ড বা ব্যাংক','wn',2)]),
dict(n=19,title='মেসেজ, মিটিং ও টিম',icon='chat',url=U+'/messages',active='Messages',
 screens=[dict(comps=[
   H('Messages','Rotterdam Textiles BV'),
   dict(t='chat',id='ch',items=[['them','Can you clear 2 containers next week?'],['me','Yes — offer sent: BDT 16,000, valid until 30 Oct.'],['them','Great, let\'s have a quick call.']]),
   ROW(F('Write a message','Sharing the document checklist 📎',id='wm'),dict(t='btns',id='mb',items=[['📎 Attach','ghost'],['Propose a meeting','blue']])),
   N('Google Meet or Zoom · propose up to 3 time slots','',id='mt')]),
  dict(layout='modal',comps=[
   H('Add Team Member','They must first register with their own email'),
   F('Email','rina@karnaphulilogistics.com',id='te'),
   dict(t='toggles',id='pm',items=[['Respond to Leads',False],['Send Offers',True],['Manage Payments & Orders',False],['Edit Services',False]]),
   BTN('Send invite',id='si'),
   dict(t='cards',n=3,id='sn',items=[['Free · seats','1'],['Gold · seats','5'],['Platinum · seats','∞']])])],
 callouts=[C('Messages পাতায়','menu:Messages'),C('চ্যাট','ch'),C('ক্লিপ','mb.0'),C('Propose a meeting','mb.1'),C('Google Meet','mt'),C('Team পাতায়','menu:Team',1),
  C('ইমেইল দিন','te',1),C('Respond to Leads','pm.0',1,flip=True),C('Manage Payments','pm.2',1,flip=True),C('Free প্ল্যানে','sn.0',1),C('Gold-এ','sn.1',1),C('Platinum-এ','sn.2',1)]),
dict(n=20,title='বিরোধ, নিরাপত্তা ও সাহায্য',icon='lock',url=U+'/disputes',active='Disputes',
 screens=[dict(comps=[
   H('Dispute DSP-2207','SO-10461 · Sea freight to Hamburg'),
   N('Funds stay held until an Exportain administrator decides','w',id='nw'),
   TA('Write your reply','Shipment loaded on 12 Oct as agreed — B/L and tracking attached.',id='wr'),
   dict(t='upload',label='Add proof',sub='Chat, invoice, B/L, photos of the work',id='ap'),
   BTN('Submit',id='sb')]),
  dict(layout='center',comps=[
   H('Stay safe & get help'),
   dict(t='list',id='sl',items=[['Use a strong password','Minimum 8 characters','🔒',''],['Never share codes','Exportain never asks for them','⚠','y'],
     ['Sign in only on exportain.com','and its sub-domains','✓',''],['support@exportain.com','Email support','✉','b'],['WhatsApp +880 1351 272596','Messages only','💬','b']])])],
 callouts=[C('হোল্ডে','nw'),C('Disputes পাতায়','menu:Disputes'),C('Write your reply','wr'),C('Add proof','ap'),C('পাসওয়ার্ড রাখুন','sl.0',1),C('কোড কাউকে','sl.1',1),
  C('exportain.com-এই','sl.2',1),C('support@','sl.3',1),C('হোয়াটসঅ্যাপে মেসেজ','sl.4',1)]),
]
OUTRO=dict(kind='big',title='Provider Center গাইড সম্পূর্ণ!',sub='provider.exportain.com',sfx=['chime'])
