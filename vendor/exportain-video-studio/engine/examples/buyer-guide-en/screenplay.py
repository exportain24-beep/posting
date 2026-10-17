#!/usr/bin/env python3
"""Exportain Buyer Guide (English, international) — hook + 17 steps + outro.
Screens recreated from docs.exportain.com/buyer; callout k = exact spoken words that trigger each action."""
F=lambda label,value='',ph='',**kw:dict(t='field',label=label,value=value,ph=ph,**kw)
SEL=lambda label,value='',**kw:dict(t='select',label=label,value=value,**kw)
TA=lambda label,value='',**kw:dict(t='textarea',label=label,value=value,**kw)
BTN=lambda text,kind='primary',**kw:dict(t='btn',text=text,kind=kind,**kw)
H=lambda text,sub='',**kw:dict(t='h',text=text,sub=sub,**kw)
ROW=lambda *items:dict(t='row',items=list(items))
N=lambda text,tone='',**kw:dict(t='note',text=text,tone=tone,**kw)
C=lambda k,id,s=0,**kw:dict(k=k,id=id,s=s,**kw)
U='buyer.exportain.com'
MENU=[['Sourcing',['Overview','My RFQs','Requests','Messages']],['Orders',['My Orders','Funds Holds','Disputes']],
      ['Trade services',['Find services','Service Offers','Service Orders']],
      ['Account',['Saved Items','Notifications','Help & support','Company Profile','Verification Center','Badges','Settings']]]
CONFIG=dict(lang='en',menu=MENU,steps=17,url=U,add_label='+ Post a Buying Requirement',badges={'My RFQs':2,'Requests':1},
            search='Search products & suppliers…')

INTRO=dict(kind='hook',title='Welcome',sfx=['swoosh','boom','sparkle','pop','pop2','bubble','ding','rise','pop','pop2','pop','chime'],
 hook=dict(l1='Source directly from',l2='Bangladesh',pill="One of the world's largest garment exporters",
   cards=[['Verified factories','shield','#1f8a3a'],['No middlemen','team','#e8590c',True],['$0 membership fees','wallet','#7048e8'],['Funds held safely','lock','#1971c2']],
   stay='In the next few minutes, you will',
   road=[['Find suppliers','search','#1f8a3a'],['Compare quotes','scale','#7048e8'],['Track your order','ship','#1971c2']],
   tag='Buyer Guide  ·  buyer.exportain.com'),
 callouts=[C('What if','h1'),C('Bangladesh','h2'),C('garment','pill'),C('verified factories','c0'),C('middlemen','c1'),C('membership','c2'),
  C('held safely','c3'),C('Stay with me','stay'),C('find suppliers','r0'),C('compare competing','r1'),C('track your order','r2'),C('Welcome to Exportain','logo')])

STEPS=[
dict(n=1,title='Create your buyer account',icon='rocket',url=U+'/register',side=False,
 screens=[dict(layout='center',comps=[
   H('Create your buyer account','Takes about 2 minutes · No card needed',id='h'),
   ROW(F('Full name','Laura Schmidt',id='fn'),F('Work email','laura@nordtextil.de',id='em')),
   F('Company name','Nordtextil GmbH',id='co'),
   ROW(SEL('Country','Germany',id='cty'),F('City','Hamburg',id='ci')),
   F('Password (min. 8 characters)','••••••••••',id='pw'),
   dict(t='check',label='I agree to the Terms of Use and Privacy Policy',id='tc'),
   BTN('Send Verification Code →',id='svc'),
   dict(t='code',value='604918',id='code'),
   BTN('Verify & Create Account',id='vca')])],
 callouts=[C('buyer.exportain.com/register','h'),C('Full name','fn'),C('Work email','em'),C('Company name','co'),C('Country','cty'),C('City','ci'),
  C('Password','pw'),C('Terms of Use','tc'),C('Send Verification Code','svc'),C('six-digit code','code'),C('Verify and Create Account','vca'),C('one email','em')]),
dict(n=2,title='Sign in & reset your password',icon='key',url='exportain.com/login',side=False,
 screens=[dict(layout='center',comps=[
   H('Sign in to Exportain','Each account type signs in on its own portal'),
   dict(t='choice',id='rl',items=[['Sign In as Buyer','For buyer accounts'],['Sign In as Seller','Bangladeshi exporters'],['Sign In as Provider','Trade service providers']]),
   F('Email','laura@nordtextil.de',id='em'),
   ROW(F('Password','••••••••••',id='pw'),BTN('Forgot?','ghost',id='fg')),
   dict(t='btns',id='bb',items=[['Sign In to Dashboard','primary'],['Continue with Google','ghost']]),
   N('Google sign-up creates no company — add it later in Company Profile','w',id='nt')]),
  dict(layout='center',comps=[
   H('Reset your password','We will send you a 6-digit code'),
   dict(t='choice',id='rc',items=[['Email','Code to your account email'],['WhatsApp (verified number)','Only if already verified']]),
   F('Account email','laura@nordtextil.de',id='ae'),
   BTN('Send code by email',id='sc'),
   dict(t='code',value='381640',id='code'),
   F('New Password','••••••••••••',id='np'),
   BTN('Reset Password',id='rp')])],
 callouts=[C('Sign In as Buyer','rl.0'),C('Enter your email','em'),C('password, then','pw'),C('Sign In to Dashboard','bb.0'),C('Continue with Google','bb.1'),
  C('does not create a company','nt'),C('Click Forgot','fg'),C('Email or WhatsApp','rc.0',1),C('request a code','sc',1),C('six-digit code','code',1),
  C('new password','np',1),C('Reset Password','rp',1)]),
dict(n=3,title='Your first steps',icon='grid',url=U+'/overview',active='Overview',
 screens=[dict(comps=[
   H('Getting started','The fastest path to your first order'),
   dict(t='list',id='ls',items=[['1 · Complete your Company Profile','Required before you can post an RFQ','Start here','b'],
     ['2 · Verify mobile (WhatsApp) & card','Earn trust badges automatically','Trust','g'],
     ['3 · Find products & suppliers','Search exportain.com, check supplier badges','Discover','g'],
     ['4 · Send an order request or post an RFQ','From your cart, or one requirement to many suppliers','Request','g'],
     ['5 · Compare quotations & accept one','Accepting creates an order','Decide','g'],
     ['6 · Track shipments & pay into Funds Holds','Money held on Exportain until you confirm','Receive','g']]),
   N('Buyers pay no membership fees · No usage limits','g',id='nt')])],
 callouts=[C('Company Profile','ls.0'),C('verify your mobile','ls.1'),C('find products','ls.2'),C('order request','ls.3'),C('Compare the quotations','ls.4'),
  C('follow your shipment','ls.5'),C('no membership fees','nt')]),
dict(n=4,title='Your Buyer Desk',icon='grid',url=U+'/overview',active='Overview',
 screens=[dict(comps=[
   H('Welcome back, Laura','Nordtextil GmbH · Hamburg, Germany'),
   dict(t='badges',id='bd',n=4,items=[['Buyer Email Verified',True],['Buyer Mobile Verified',True],['Payment Verified',False],['Business Verified',False]]),
   N('Your badges: 2 of 8 earned · Next: Payment Verified','',id='bn'),
   dict(t='cards',n=4,id='cards',items=[['Active RFQs','2'],['Quotes received','5'],['Open inquiries','3'],['Active orders','1']]),
   dict(t='cards',n=4,id='c2',items=[['Saved products','14'],['Saved suppliers','6'],['Unread notifications','4'],['Profile strength','80%']])])],
 callouts=[C('Overview','menu:Overview'),C('Post a Buying Requirement','hdr:add'),C('Your badges','bd'),C('Active RFQs','cards.0'),C('Quotes received','cards.1'),
  C('Open inquiries','cards.2'),C('Active orders','cards.3'),C('Use Search','hdr:search'),C('bell','hdr:bell')]),
dict(n=5,title='Complete your company profile',icon='store',url=U+'/company',active='Company Profile',
 screens=[dict(comps=[
   ROW(H('Company Profile','Suppliers quote companies, not individuals'),F('Company ID','EXP-C-48213   ⧉ Copy',id='cid')),
   F('Company Name *','Nordtextil GmbH',id='cn'),
   ROW(SEL('Country *','Germany',id='cty'),F('City *','Hamburg',id='ci')),
   F('Address','Spaldingstraße 160, 20097 Hamburg',id='ad'),
   ROW(F('Registration Number','HRB 145872',id='rn'),F('Website','www.nordtextil.de',id='ws')),
   F('Company email','sourcing@nordtextil.de',id='ce'),
   ROW(N('Suppliers never see your company email','',id='nt'),BTN('Save Changes',id='sv'))])],
 callouts=[C('Open Company Profile','menu:Company Profile'),C('Company ID','cid'),C('Company Name','cn'),C('Country and','cty'),C('City. For','ci'),
  C('Address','ad'),C('Registration Number','rn'),C('Website or','ws'),C('Company email','ce'),C('never see','nt'),C('Save Changes','sv')]),
dict(n=6,title='Find products',icon='search',url='exportain.com/search?q=t-shirt',side=False,
 screens=[dict(comps=[
   dict(t='sitebar',id='sb',value='t-shirt'),
   dict(t='tabs',id='tb',items=['Products (248)','Suppliers (36)','RFQs (12)'],active=0),
   dict(t='choice',id='fl',n=3,items=[['Exportain Verified','Verified suppliers only'],['Samples available','Order a sample first'],['OEM / ODM capable','Your brand, your design']]),
   dict(t='pcards',id='pc',items=[
     dict(icon='shirt',c1='#9fc5f8',c2='#3b82c4',cat='Apparel › T-shirts',title='Cotton Crew Neck T-Shirt, 180 GSM',sup='Dhaka Knit Ltd.',ver=True,moq='MOQ 500 pieces',price='$2.60 / pc · FOB'),
     dict(icon='shirt',c1='#ffc9a9',c2='#e8590c',cat='Apparel › Polo shirts',title='Pique Polo Shirt, 220 GSM',sup='Chittagong Apparels',ver=True,moq='MOQ 1,000 pieces',price='$4.10 / pc · FOB'),
     dict(icon='sack',c1='#d8f5a2',c2='#5c940d',cat='Jute › Bags',title='Natural Jute Shopping Bag',sup='Golden Fibre Co.',ver=False,moq='MOQ 2,000 pieces',price='$1.10 / pc · FOB')])]),
  dict(comps=[
   dict(t='sitebar',id='sb2',value='t-shirt'),
   dict(t='pdp',id='pd',icon='shirt',c1='#9fc5f8',c2='#3b82c4',sup='Dhaka Knit Ltd. · Gazipur, Bangladesh',title='Cotton Crew Neck T-Shirt, 180 GSM',
        price='$2.60 / piece',sub='Unit price, FOB · Minimum order 500 Pieces',qty='1,000',total='$2,600',
        specs=['Lead time: 30 days · Port of loading: Chattogram','100% combed cotton · Sizes S–XXL · OEKO-TEX certified'])])],
 callouts=[C('search box','sb'),C('Products,','tb.0'),C('Suppliers and','tb.1'),C('RFQs. Use','tb.2'),C('Exportain Verified','fl.0'),C('samples','fl.1'),
  C('OEM','fl.2'),C('product card','pc.0'),C('product page','pd.im',1),C('quantity','pd.qty',1),C('Add to cart','pd.cart',1),C('Request quote','pd.rfq',1),
  C('Contact','pd.contact',1),C('heart','pd.save',1)]),
dict(n=7,title='Read supplier trust badges',icon='shield',url='exportain.com/suppliers/dhaka-knit',side=False,
 screens=[dict(comps=[
   H('Dhaka Knit Ltd.','Manufacturer · Gazipur, Bangladesh · Gold member'),
   dict(t='badges',id='bd',items=[['Exportain Verified',True],['Export Verified',True],['Factory Verified',True],['Trading Company Verified',False],['Trusted Trader',True]]),
   N('Gold & Platinum = a paid plan, not verification','w',id='n1'),
   N('Badges show what was checked — always review samples and documents yourself','',id='n2')])],
 callouts=[C('Exportain Verified','bd.0'),C('Export Verified','bd.1'),C('Factory Verified','bd.2'),C('Trading Company Verified','bd.3'),C('Trusted Trader','bd.4'),
  C('Gold and Platinum','n1'),C('review samples','n2')]),
dict(n=8,title='Send order requests',icon='cart',url='exportain.com/cart',side=False,
 screens=[dict(comps=[
   H('Your cart','2 suppliers · nothing is charged'),
   dict(t='list',id='ls',items=[['Cotton Crew Neck T-Shirt, 180 GSM','Dhaka Knit Ltd. · 1,000 pcs · $2.60 FOB','','','Choose port: Chattogram ▾'],
     ['Natural Jute Shopping Bag','Golden Fibre Co. · 2,000 pcs · $1.10 FOB','','','Choose port: Mongla ▾']]),
   ROW(SEL('Ship to','Germany',id='st'),BTN('Send order request',id='sor')),
   N('No money is taken — each supplier receives a separate request','g',id='nm')]),
  dict(comps=[
   H('Requests','Order requests and questions, with supplier replies'),
   dict(t='list',id='rq',items=[['🛒 Order request · Dhaka Knit Ltd.','Sent today','Replied','b',''],['💬 Question · Golden Fibre Co.','"Do you offer custom printing?"','Awaiting reply','y','']]),
   dict(t='list',id='rd',items=[['Listed price when sent','$2.60 / pc FOB'],['Loading port','Chattogram'],['Destination','Germany · Hamburg'],['Supplier reply','"We can confirm 1,000 pcs in 30 days. Quotation to follow."']]),
   N('An order request is not an order — accept a quotation to create one','w',id='nt')])],
 callouts=[C('Add products','ls.0'),C('Choose port','ls.0.b'),C('Ship to','st'),C('Send order request','sor'),C('no money','nm'),C('Requests','rq.0',1),
  C('listed price','rd.0',1),C('loading port','rd.1',1),C('destination, and','rd.2',1),C('supplier reply','rd.3',1),C('not an order','nt',1)]),
dict(n=9,title='Post an RFQ',icon='doc',url='exportain.com/rfqs/new',side=False,
 screens=[dict(comps=[
   dict(t='stepper',id='stp',items=['Sourcing','Requirements','Quantity','Delivery','Compliance','Preferences'],active=0),
   ROW(F("What are you sourcing?",'100% cotton crew-neck T-shirt, 180 GSM, custom print',id='ws'),SEL('Category','Apparel › T-shirts',id='cat')),
   TA('Specifications','Combed cotton jersey, 180 GSM · Sizes S–XL (20/30/30/20) · Pantone colours · Polybag per piece, 50 pcs per carton · Woven label',id='sp'),
   ROW(F('Quantity','10,000',id='q'),SEL('Unit','Pieces',id='u'),F('Target unit price','2.40',id='tp'),SEL('Currency','USD',id='cu')),
   ROW(SEL('Destination country','Germany',id='dc'),F('Destination port','Hamburg',id='dp'),SEL('Incoterm','FOB',id='inc')),
   ROW(F('Required certifications','OEKO-TEX, GOTS',id='rc'),F('Quotation deadline','30 Nov 2026',id='qd')),
   BTN('Publish RFQ',id='pub')])],
 callouts=[C('Post a Buying Requirement','stp'),C('What are you sourcing','ws'),C('Category','cat'),C('Specifications','sp'),C('Quantity and','q'),C('Unit, and','u'),
  C('Target unit price','tp'),C('Destination country','dc'),C('port and','dp'),C('Incoterm','inc'),C('Required certifications','rc'),C('Quotation deadline','qd'),C('Publish RFQ','pub')]),
dict(n=10,title='Compare & counter quotations',icon='scale',url=U+'/rfqs/RFQ-20931',active='My RFQs',
 screens=[dict(comps=[
   H('Cotton crew-neck T-shirts · 10,000 pcs','Quotations received: 3 · Edit RFQ'),
   dict(t='table',id='tb',w='1.55fr .95fr 1fr .9fr .85fr .75fr 1.15fr .95fr',
        cols=['Supplier','Unit price','Total','Min. order','Lead time','Incoterm','Payment terms','Valid until'],
        rows=[['Chittagong Apparels','$2.55','$25,500','2,000','40 days','FOB','30% / 70% B/L','20 Nov'],
              ['Dhaka Knit Ltd.','$2.35','$23,500','500','35 days','FOB','30% / 70% B/L','25 Nov'],
              ['Savar Textiles','$2.48','$24,800','1,000','45 days','FOB','LC at sight','18 Nov']],low=[1,1]),
   dict(t='list',id='qc',items=[['Dhaka Knit Ltd. · Exportain Verified · Factory Verified','$2.35 / pc · 35 days · valid until 25 Nov','Round 1','b','']]),
   dict(t='btns',id='qa',items=[['Accept','primary'],['Counter','blue'],['Decline','danger'],['Negotiation history','ghost']])]),
  dict(layout='modal',comps=[
   H('Counter-offer','Dhaka Knit Ltd.'),
   ROW(F('Unit price (USD)','2.25',id='up'),F('Lead time (days)','30',id='lt')),
   F('Your offer is valid until','28 Nov 2026',id='vu'),
   TA('Note (optional)','We can confirm 10,000 pcs at $2.25 with 30-day delivery.',id='nn'),
   BTN('Send counter-offer',id='sco'),
   N('Every round is saved in Negotiation history','',id='nh')])],
 callouts=[C('My RFQs','menu:My RFQs'),C('Compare quotations','tb'),C('Lowest','tb.1.1'),C('Lead time','tb.1.4'),C('Minimum order','tb.1.3'),C('Incoterm','tb.1.5'),
  C('Payment terms','tb.1.6'),C('Counter','qa.1'),C('Unit price','up',1),C('Lead time in days','lt',1),C('valid, then','vu',1),C('Send counter-offer','sco',1),C('Negotiation history','nh',1)]),
dict(n=11,title='Accept or decline',icon='star',url=U+'/rfqs/RFQ-20931',active='My RFQs',
 screens=[dict(comps=[
   H('Cotton crew-neck T-shirts · 10,000 pcs','Supplier replied to your counter'),
   dict(t='list',id='qc',items=[['Dhaka Knit Ltd. · current terms','$2.30 / pc · 32 days · FOB Chattogram · 30% / 70% against B/L','Round 3','b','']]),
   dict(t='btns',id='qa',items=[['Accept','primary'],['Counter','blue'],['Decline','danger'],['Negotiation history','ghost']])]),
  dict(layout='modal',comps=[
   H('Accept this quotation?'),
   dict(t='table',id='sm',w='1fr 1.3fr',cols=['Term','Value'],rows=[['Price','$2.30 / pc (USD)'],['Quantity','10,000 pieces'],['Lead time','32 days'],['Incoterm','FOB Chattogram'],['Payment terms','30% / 70% against B/L'],['Order total','$23,000']]),
   dict(t='btns',id='ab',items=[['Accept and create order','primary'],['Cancel','ghost']])]),
  dict(layout='modal',comps=[
   H('✓ Order created','EXP-ORD-10293 · Dhaka Knit Ltd.'),
   BTN('Open the order',id='oo'),
   N('An RFQ can be awarded only once','w',id='aw')]),
  dict(layout='center',comps=[
   H('Decline quotation','Savar Textiles'),
   dict(t='choice',id='rs',n=3,items=[['Price',''],['Lead time',''],['Minimum order quantity',''],['Terms',''],['Other','']]),
   TA('Note (optional, up to 500 characters)','Thank you — we have awarded this RFQ to another supplier.',id='dn'),
   BTN('Decline quotation','danger',id='dq')])],
 callouts=[C('click Accept','qa.0'),C('Review the summary','sm',1),C('Order total','sm.5',1),C('Accept and create order','ab.0',1),C('Open the order','oo',2),
  C('awarded only once','aw',2),C('Click Decline','rs',3),C('Price or','rs.0',3),C('Lead time, and','rs.1',3),C('Decline quotation','dq',3)]),
dict(n=12,title='Track orders & shipments',icon='ship',url=U+'/orders',active='My Orders',
 screens=[dict(comps=[
   H('My Orders'),
   dict(t='tabs',id='tb',items=['Active','Completed'],active=0),
   dict(t='list',id='ol',items=[['EXP-ORD-10293 · Dhaka Knit Ltd.','10,000 pcs · $23,000 · FOB Chattogram','Confirmed','b','Not Booked']])]),
  dict(comps=[
   H('Order EXP-ORD-10293','Status: In transit · Dhaka Knit Ltd. · 10,000 pcs · FOB · Hamburg'),
   dict(t='timeline',id='tl',items=[['Booked','doc'],['Departed','ship'],['In transit','plane'],['Arrived at destination','anchor'],['Import customs clearance','stamp'],['Delivered','box']]),
   dict(t='list',id='sd',items=[['Carrier','Maersk Line'],['Tracking / B/L number','MAEU 264819370'],['Estimated arrival','Hamburg · 24 Dec 2026']])])],
 callouts=[C('My Orders','menu:My Orders'),C('Active and Completed','tb'),C('order number','ol.0'),C('Not Booked','ol.0.b'),C('timeline','tl',1),
  C('Booked,','tl.0',1),C('Departed','tl.1',1),C('In transit','tl.2',1),C('Arrived at destination','tl.3',1),C('Import customs clearance','tl.4',1),
  C('Delivered','tl.5',1),C('carrier','sd.0',1),C('bill of lading','sd.1',1)]),
dict(n=13,title='Funds Holds: pay safely',icon='lock',url=U+'/funds-holds',active='Funds Holds',
 screens=[dict(comps=[
   H('Funds Holds','Money held on Exportain — the supplier is paid only after clearance and your confirmation'),
   dict(t='list',id='hl',items=[['Hold FH-2207 · Order EXP-ORD-10293','30% advance for production · requested by Dhaka Knit Ltd.','Awaiting your payment','y','Pay $6,900']])]),
  dict(layout='modal',comps=[
   H('Pay $6,900','Secure card payment'),
   F('Card number','4242 4242 4242 4242',id='cn'),
   ROW(F('Expiry','08 / 29',id='ex'),F('CVC','•••',id='cv')),
   BTN('Pay now',id='pn')]),
  dict(comps=[
   H('Hold FH-2207 · $6,900','Clearance filed by the seller'),
   dict(t='timeline',id='ft',done=1,items=[['Paid','wallet'],['Held — awaiting seller clearance','lock'],['Clearance filed — confirm completion','stamp'],['Released to seller','bank']]),
   dict(t='btns',id='fb',items=[['Mark trade complete','primary'],['Raise a dispute','danger']]),
   N('No extra fee — you pay exactly the hold amount','g',id='nf')])],
 callouts=[C('Open Funds Holds','menu:Funds Holds'),C('Awaiting your payment','hl.0'),C('click Pay','hl.0.b'),C('enter your card','cn',1),C('not paid yet','ft.1',2),
  C('file export clearance','ft.2',2),C('Mark trade complete','fb.0',2),C('Raise a dispute','fb.1',2),C('no extra fee','nf',2)]),
dict(n=14,title='Verification & buyer badges',icon='shield',url=U+'/verification',active='Verification Center',
 screens=[dict(comps=[
   H('Verification Center','1 of 3 checks done'),
   dict(t='list',id='vl',items=[['Email Address','laura@nordtextil.de · earns Buyer Email Verified','Verified','',''],
     ['Mobile number (WhatsApp)','Earns Buyer Mobile Verified','','','Verify WhatsApp'],
     ['Payment card','Stripe checks the card for $0 · earns Payment Verified','','','Verify card']])]),
  dict(layout='modal',comps=[
   H('Verify WhatsApp','A 6-digit code will arrive on WhatsApp'),
   ROW(SEL('Country code','+49 Germany',id='cc'),F('Mobile number','151 2345 6789',id='mn')),
   BTN('Send code via WhatsApp',id='sc'),
   dict(t='code',value='275301',id='code'),
   N('Resend in 0:59 · code valid for 10 minutes','',id='rs')]),
  dict(comps=[
   H('Your badges','3 of 8 earned · awarded automatically'),
   dict(t='badges',id='bg',n=4,items=[['Buyer Mobile Verified',True],['Buyer Email Verified',True],['Payment Verified',True],['Business Verified',False],
     ['Frequent Buyer',False],['Verified Buyer',False],['RFQ Buyer',True],['Trusted Buyer',False]]),
   N('Suppliers see your badges next to your name on RFQs, requests, orders and messages','',id='nb')])],
 callouts=[C('Verification Center','menu:Verification Center'),C('email is already','vl.0'),C('Verify WhatsApp','vl.1.b'),C('country code','cc',1),
  C('Send code via WhatsApp','sc',1),C('six digits','code',1),C('Buyer Mobile Verified','bg.0',2),C('Payment Verified','bg.2',2),C('Business Verified','bg.3',2),
  C('Frequent Buyer','bg.4',2),C('Verified Buyer and','bg.5',2),C('Trusted Buyer','bg.7',2),C('automatically','nb',2)]),
dict(n=15,title='Book trade services',icon='truck',url=U+'/services',active='Find services',
 screens=[dict(comps=[
   ROW(F('Search services','Sea freight Chattogram to Hamburg',id='ss'),SEL('Service','Freight Forwarders (12)',id='sf')),
   dict(t='pcards',id='sv',btns=['Request this service','View'],items=[
     dict(icon='ship',c1='#a5d8ff',c2='#1971c2',cat='Freight Forwarders',title='Sea Freight Chattogram → Europe',sup='Karnaphuli Logistics',ver=True,moq='24–28 days · per container',price='From $2,150'),
     dict(icon='stamp',c1='#d0bfff',c2='#7048e8',cat='Customs Brokers',title='Export Customs Clearance, Chattogram',sup='Port City C&F',ver=True,moq='2–4 days · per shipment',price='From $180'),
     dict(icon='search',c1='#96f2d7',c2='#0b7285',cat='Inspection & Quality Audits',title='Pre-shipment Inspection (AQL 2.5)',sup='QC Bangla Ltd.',ver=False,moq='1 day · per inspection',price='From $220')])]),
  dict(layout='modal',comps=[
   H('Request a service','Sea Freight Chattogram → Europe · Karnaphuli Logistics'),
   TA('What do you need?','1 × 40ft HC, 10,000 cartons of T-shirts, ready 15 Dec. Please quote FOB Chattogram to Hamburg.',id='wn'),
   ROW(F('Origin','Chattogram',id='or'),F('Destination','Hamburg',id='de')),
   BTN('Send request',id='sr')]),
  dict(comps=[
   H('Service Offers','Accepting creates a service order — Exportain holds the money until you confirm'),
   dict(t='list',id='of',items=[['Sea freight 1 × 40ft HC · Chattogram → Hamburg','Service $2,150 · VAT $0 · Total $2,150 · valid until 30 Nov','Awaiting your decision','y','Accept this offer']])]),
  dict(comps=[
   H('Service Orders'),
   dict(t='list',id='so',items=[['SO-10522 · Sea freight to Hamburg','Accepted — awaiting payment · $2,150','Card','b','Pay online']]),
   dict(t='btns',id='sb',items=[['Confirm the work is done','primary'],['Dispute — the work is not done','danger']]),
   N('Not confirmed within 3 days? An Exportain admin reviews it — money is never released automatically','',id='nt')])],
 callouts=[C('Open Find services','menu:Find services'),C('search box','ss'),C('Service filter','sf'),C('Request this service','sv.0.b0'),C('What do you need','wn',1),
  C('Send request','sr',1),C('Service Offers','menu:Service Offers',2),C('Accept this offer','of.0.b',2),C('Service Orders','menu:Service Orders',3),C('Pay online','so.0.b',3),
  C('Confirm the work is done','sb.0',3),C('open a dispute','sb.1',3)]),
dict(n=16,title='Messages & meetings',icon='chat',url=U+'/messages',active='Messages',
 screens=[dict(comps=[
   ROW(F('Search conversations','Dhaka Knit',id='se'),dict(t='toggles',id='un',items=[['Unread only',False]])),
   dict(t='chat',id='ch',items=[['them','Dhaka Knit: Lab dips are ready — sharing photos today.'],['me','Great. Can we confirm 32 days lead time in writing?'],['them','Confirmed: 32 days from approval of the pre-production sample.']]),
   ROW(F('Write a message','Thanks — please also send the packing list draft.',id='wm'),dict(t='btns',id='mb',items=[['Send','primary'],['Propose a meeting','blue']])),
   N('You can edit your own message for 2 minutes · messages cannot be deleted','',id='ed')]),
  dict(layout='modal',comps=[
   H('Propose a meeting','Dhaka Knit Ltd.'),
   dict(t='choice',id='mt',items=[['Google Meet',''],['Zoom','']]),
   dict(t='list',id='ts',items=[['Tue 18 Nov · 10:00 CET','30 min'],['Wed 19 Nov · 09:30 CET','30 min'],['Thu 20 Nov · 14:00 CET','30 min']]),
   BTN('Send proposal',id='sp'),
   N('Keep prices, dates and payment terms in Exportain messages — your evidence in a dispute','w',id='ev')])],
 callouts=[C('Open Messages','menu:Messages'),C('search box','se'),C('Unread only','un.0',flip=True),C('reply box','wm'),C('edit your own message','ed'),
  C('Propose a meeting','mb.1'),C('Google Meet','mt.0',1),C('Zoom','mt.1',1),C('three time slots','ts',1),C('evidence','ev',1)]),
dict(n=17,title='Support, disputes & safety',icon='help',url=U+'/support',active='Help & support',
 screens=[dict(comps=[
   ROW(H('Help & support','All replies stay on the ticket'),BTN('+ New ticket',id='nt')),
   dict(t='tabs',id='tb',items=['Open','Waiting for you','Resolved','Closed','All'],active=0),
   dict(t='list',id='tl',items=[['EXP-SUP-3108 · Quotation cannot be accepted','Updated 1h ago','In progress','b',''],['EXP-SUP-2977 · Payment question','Updated 2 days ago','Resolved','','']])]),
  dict(layout='modal',comps=[
   H('New ticket','Step 1 of 4 · What do you need help with?'),
   dict(t='choice',id='hc',n=3,items=[['Payments',''],['Quotations',''],['Supplier safety','']]),
   F('Subject','Funds hold payment shows as not recorded',id='sj'),
   dict(t='upload',label='Add a screenshot (optional)',sub='Images, PDF, Word, Excel · up to 10 MB · 5 files',id='up'),
   BTN('Send ticket',id='st')]),
  dict(comps=[
   dict(t='tabs',id='tb2',items=['Open','Waiting for you','Resolved','Closed','All'],active=0),
   dict(t='chat',id='ch',items=[['them','Support: Thanks Laura — your payment is now confirmed on hold FH-2207.'],['me','Perfect, thank you!']]),
   BTN('My problem is solved',id='ms')]),
  dict(layout='center',comps=[
   H('Stay safe'),
   dict(t='list',id='sf',items=[['Never share passwords, codes or card details','Exportain never asks for them','⚠','y'],
     ['support@exportain.com','Email support any time','✉','b'],['WhatsApp +880 1351 272596','Messages only','💬','b']])])],
 callouts=[C('Help and support','menu:Help & support'),C('New ticket','nt'),C('what you need help with','hc',1),C('describe the problem','sj',1),C('screenshot','up',1),
  C('Send ticket','st',1),C('Waiting for you','tb2.1',2),C('My problem is solved','ms',2),C('Never share','sf.0',3),C('support@exportain.com','sf.1',3),C('WhatsApp message','sf.2',3)]),
]
OUTRO=dict(kind='big',title='Start sourcing today',sub='buyer.exportain.com',sfx=['chime'])
