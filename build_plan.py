#!/usr/bin/env python3
"""Builds the 1,000-Short master plan (plan.json + Exportain_1000_Shorts_Plan.xlsx).

Input : rows.json (1,000 researched YouTube keywords) + final_pool.json (replacement candidates)
Output: plan.json  — one entry per Short in publish order, with slot time, clean SEO keyword, language,
        cluster, unique subtopic, hook format, visual world, draft title, tags, hashtags.
Scripts are NOT pre-written here: each one is researched and written on production day (SHORTS_TASK.md),
so facts are current and every Short actually answers its keyword.
"""
import json, re, sys, collections
from datetime import datetime, timedelta, timezone

SCR = sys.argv[1]
OUT = sys.argv[2]
rows = json.load(open(f"{SCR}/rows.json", encoding="utf-8"))
pool = json.load(open(f"{SCR}/final_pool.json", encoding="utf-8"))
BN = re.compile(r"[ঀ-৿]")

# ------------------------------------------------------------------ 1. drop junk, restore fixable, add replacements
JUNK = re.compile(r"(বায়ারের ধান|বায়ার ক্রপ|মন্টুর|হাত বায়ার|demon slayer|export option|kivabe khele|dropshipping|dealers for|pune|ahmedabad|"
    r"chennai|after 12th|malayalam|hai ki nahin|ielts|work permit|question paper|paper solution|\bdj\b|ডাকি|পেঁয়াজ রপ্তানি বন্ধ|"
    r"x bangladesh|via bangladesh|by bangladesh|kaise kare|bangla bangla|খেলে কি হয়|লাভ স্টোরি|বায়ারের$|বিদেশি বায়ার বায়ারের|"
    r"ফ্রেইট ফরোয়ার্ডিং জুতা|savar roptani|export processor|online booking|lc খুলতে কি সরকার|ইংরেজি কি|লেখার নিয়ম|তৈরির পদ্ধতি|"
    r"ব্যবসা ব্যবসা|এলসি কি জুতা|এলসি কি ফল|এলসি করার নিয়ম ফল|আমা$|কি রকম|marketing executive|এক্সপোর্ট বাজার বিডি|ব্যবসায়ী$|"
    r"নিয়ম নিয়ম|এর কাজ কি$|লাইসেন্স জুতা|কিভাবে জুতা|ইআরসি লাইসেন্স জুতা|রপ্তানি করার নিয়ম জুতা|export lc bangladesh export|"
    r"erc license bangladesh license|registration certificate bangladesh registration|bangladesh in bangladesh|bank bangladesh$|"
    r"dhaka bangladesh$|export documents y |india bangladesh rice export|usa from bangladesh to india|europe bangladesh to india|"
    r"usa bangladesh to india|europe from bangladesh to india|food report|garments home|garments work|garments a business|"
    r"export bangla work|export business bangla business$|which export buyers|can i export buyers|why export buyers|কিভাবে এক্সপোর্ট দাম|"
    r"লাইসেন্স লাভ|লাইসেন্স ইনকাম|এলসি কি ইনকাম|এলসি কি লাভ|এলসি করার নিয়ম ইনকাম|এলসি করার নিয়ম দাম|এক্সপোর্ট চালু|"
    r"ইমপোর্ট এক্সপোর্ট জুতা|ব্যবসা জুতা$|কৃষি পণ্য রপ্তানি জুতা|কৃষি পণ্য রপ্তানি পণ্য|বিদেশে পণ্য রপ্তানি পণ্য|রপ্তানি পণ্য আমদানি|"
    r"বায়ার এর কাজ|বায়ার তৈরির|swagger|waikiki|aktu|\bmba\b|executive|specialist|documentary|gobar|coffee|cow dung|ড্রপশিপিং|"
    r"bank of bangladesh|marketing important questions|export lc bangladesh ki$|export lc bangladesh quality|lc bangladesh border|"
    r"payment bangladesh ki$|documents bangladesh ki$|incentive bangladesh ki$|foreign buyers bangladesh ki$|foreign buyers bangladesh kaj|"
    r"registration certificate bangladesh ki$|registration certificate bangladesh quality|registration certificate bangladesh sample|"
    r"registration certificate bangladesh wholesale|registration certificate bangladesh online shop|documents bangladesh quality|"
    r"documents bangladesh work|documents bangladesh wholesale|lc bangladesh wholesale|license bangladesh wholesale|"
    r"usa bangladesh work|europe bangladesh work|usa bangladesh quality|europe bangladesh quality|usa bangladesh border|"
    r"europe bangladesh border|incentive bangladesh work|incentive bangladesh experience|lc bangladesh products|lc bangladesh market|"
    r"documents bangladesh market|business bangla quality|import bangla quality|business bangla problem|export business bangla company)")
RESTORE = {"lc কিভাবে খুলতে হয়": "এলসি কিভাবে খুলতে হয়"}

keep, seen = [], set()
for r in rows:
    k = r["keyword"]
    if k in RESTORE:
        r = {**r, "keyword": RESTORE[k]}
    elif JUNK.search(k):
        continue
    if r["keyword"] in seen:
        continue
    seen.add(r["keyword"]); keep.append(r)
# replacements: best unused pool keywords (already scored), same junk filter
cluster_of = {r["keyword"]: r for r in rows}
need = 1000 - len(keep)
for p in pool:
    if need <= 0:
        break
    k = p["keyword"]
    if k in seen or JUNK.search(k) or len(k.split()) < 2:
        continue
    seen.add(k)
    keep.append({"keyword": k, "lang": "Bangla" if BN.search(k) else "English", "cluster": None,
                 "tier": p["tier"], "opp": 55.0, "source": p["source"], "replacement": True})
    need -= 1
assert len(keep) == 1000, len(keep)

# ------------------------------------------------------------------ 2. clean SEO keyword + language (Banglish -> Bangla)
BANGLISH = {   # Banglish keyword -> natural Bangla search phrase (owner: Banglish videos are made in Bangla)
    "export license kivabe korbo bangladesh": "এক্সপোর্ট লাইসেন্স কিভাবে করবো",
    "export license kivabe korbo video bangla": "এক্সপোর্ট লাইসেন্স কিভাবে করবো",
    "export license kivabe korbo bangla": "এক্সপোর্ট লাইসেন্স কিভাবে করবো বাংলা",
    "export license kivabe korbo bengali": "এক্সপোর্ট লাইসেন্স করার নিয়ম",
    "export license kivabe korbo dhaka": "ঢাকায় এক্সপোর্ট লাইসেন্স কিভাবে করবো",
    "export license kivabe korbo 2023": "এক্সপোর্ট লাইসেন্স কিভাবে করবো ২০২৬",
    "export license kivabe korbo": "এক্সপোর্ট লাইসেন্স কিভাবে করবো",
    "export license bangladesh kivabe korbo": "বাংলাদেশে এক্সপোর্ট লাইসেন্স কিভাবে করবো",
    "export license bangladesh dam koto": "এক্সপোর্ট লাইসেন্সের দাম কত",
    "export license bangladesh koto taka": "এক্সপোর্ট লাইসেন্স করতে কত টাকা লাগে",
    "export lc bangladesh koto": "এক্সপোর্ট এলসি খরচ কত",
    "export lc bangladesh rate koto": "এক্সপোর্ট এলসির চার্জ কত",
    "export payment bangladesh koto taka": "এক্সপোর্ট পেমেন্টে কত টাকা চার্জ",
    "export payment bangladesh kivabe korbo": "এক্সপোর্ট পেমেন্ট কিভাবে নেবো",
    "export documents bangladesh koto": "এক্সপোর্ট ডকুমেন্টস খরচ কত",
    "export documents bangladesh ki ki lage": "এক্সপোর্ট করতে কি কি ডকুমেন্টস লাগে",
    "erc license bangladesh koto": "ইআরসি লাইসেন্স খরচ কত",
    "erc license bangladesh taka": "ইআরসি লাইসেন্স করতে কত টাকা লাগে",
    "erc license bangladesh koto taka": "ইআরসি লাইসেন্স কত টাকা",
    "erc license bangladesh price koto": "ইআরসি লাইসেন্সের দাম কত",
    "buyer kivabe pabo bengali": "বায়ার কিভাবে পাবো",
    "buyer kivabe pabo bangladesh": "বাংলাদেশ থেকে বিদেশি বায়ার কিভাবে পাবো",
    "buyer kivabe pabo bangla": "এক্সপোর্ট বায়ার কিভাবে পাবো",
    "bideshe product export bangladesh": "বিদেশে পণ্য এক্সপোর্ট",
    "bideshe product export bangla": "বিদেশে পণ্য রপ্তানি কিভাবে করবো",
    "bideshe product export dhaka": "ঢাকা থেকে বিদেশে পণ্য এক্সপোর্ট",
    "bideshe product export price": "বিদেশে পণ্য রপ্তানির খরচ",
    "bideshe product exporter": "বিদেশে পণ্য রপ্তানিকারক হবেন কিভাবে",
    "bideshe product export video in bangladesh": "বাংলাদেশ থেকে বিদেশে পণ্য রপ্তানি",
    "bideshe product export from bangladesh": "বাংলাদেশ থেকে বিদেশে পণ্য রপ্তানি",
    "bideshe product export quality bangladesh": "বিদেশে রপ্তানির মানের পণ্য",
    "bideshe product export and price": "বিদেশে পণ্য রপ্তানি ও দাম ঠিক করা",
    "export business kivabe korbo": "এক্সপোর্ট ব্যবসা কিভাবে করবো",
    "export import business kivabe korbo": "এক্সপোর্ট ইমপোর্ট ব্যবসা কিভাবে করবো",
    "export import business kivabe bangladesh": "বাংলাদেশে এক্সপোর্ট ইমপোর্ট ব্যবসা কিভাবে করবো",
    "export import business kivabe in bengali": "এক্সপোর্ট ইমপোর্ট ব্যবসা কিভাবে শুরু করবো",
    "export kivabe korbo": "এক্সপোর্ট কিভাবে করবো",
    "kivabe export korbo": "কিভাবে এক্সপোর্ট করবো",
    "export business kivabe shuru korbo bangla": "এক্সপোর্ট ব্যবসা কিভাবে শুরু করবো",
    "export business kivabe shuru korbo bengali": "নতুনদের এক্সপোর্ট ব্যবসা শুরু",
    "export business kivabe shuru korbo bangladesh": "বাংলাদেশে এক্সপোর্ট ব্যবসা কিভাবে শুরু করবো",
    "export business kivabe shuru korbo video bangla": "এক্সপোর্ট ব্যবসা শুরুর ধাপ",
    "export to usa from bangladesh koto taka": "বাংলাদেশ থেকে আমেরিকায় এক্সপোর্ট খরচ কত",
    "export to europe from bangladesh koto taka": "বাংলাদেশ থেকে ইউরোপে এক্সপোর্ট খরচ কত",
    "export to europe from bangladesh koto": "ইউরোপে পণ্য পাঠাতে কত খরচ",
    "export to usa bangladesh koto taka": "আমেরিকায় পণ্য পাঠাতে কত টাকা লাগে",
    "export to europe bangladesh koto taka": "ইউরোপে রপ্তানি করতে কত টাকা লাগে",
    "export to europe bangladesh koto": "ইউরোপে এক্সপোর্ট খরচ",
    "buying house bangladesh kivabe korbo": "বায়িং হাউস কিভাবে খুলবো",
    "cnf মানে কি": "সিএন্ডএফ মানে কি",
    "lc মানে কি": "এলসি মানে কি",
    "এলসি করার নিয়ম ও কি": "এলসি কী ও করার নিয়ম",
}
# English tails that are autocomplete noise: strip them (the core keyword stays first)
EN_TAIL = re.compile(r"\s+(wholesale market|wholesale|market price|market|online shop|online order|online registration|"
                     r"online payment|online class|online business|online|full details|details|guidelines|guide|company ltd|"
                     r"company|overseas bank|overseas|bank account|bank|business idea|easy way|easy|quick guide|full process|"
                     r"process|procedure|explanation|in bangladesh|in bd|bangla|bengali|how to make|step by step|small business|"
                     r"for beginners|registration|requirements|documents|document|list|ki ki lage|apply online|to dubai|to japan|"
                     r"to canada|to india|to italy|without credit card|without bank account|without investment|license|"
                     r"products|work|ship|which country|2025|2023)$")
EN_COST = re.compile(r"\s+(low price|with price|price|low cost|cost)$")
BN_TAIL = re.compile(r"\s+(দাম|লাভ|ইনকাম|আয়|সরকার|শুরু|শুল্ক|ফল|আম|মানে কি|করবো কিভাবে|কি)$")


def clean(kw, lang):
    k = kw.strip()
    if k in BANGLISH:
        return BANGLISH[k], "Bangla", True
    if BN.search(k):
        if re.search(r"[a-z]", k):                       # mixed: Latin acronym inside Bangla
            k = (k.replace("lc", "এলসি").replace("cnf", "সিএন্ডএফ").replace("erc", "ইআরসি"))
        return re.sub(r"\s+", " ", k), "Bangla", False
    if re.search(r"\b(kivabe|korbo|koto|taka|shuru|pabo|bideshe|dam)\b", k):
        return k, "Bangla", True                          # any Banglish not in the map: runner writes it in Bangla
    base = k
    cost = bool(EN_COST.search(base))
    base = EN_COST.sub("", base)
    for _ in range(3):
        nb = EN_TAIL.sub("", base)
        if nb == base or len(nb.split()) < 2:
            break
        base = nb
    if cost and not re.search(r"cost|price", base):
        base += " cost"
    return re.sub(r"\s+", " ", base), "English", False


# ------------------------------------------------------------------ 3. cluster (for replacements) + topic banks
def cluster_for(k):
    rules = [
        ("Export surplus / পাইকারি মার্কেট", r"(পাইকারি|চেনার উপায়|নিউ মার্কেট|কম দামে|surplus|export (jacket|jeans|pant|shirt|shoes|clothes)|kapda market|paikari)"),
        ("License & Registration (IRC/ERC)", r"(irc|erc|license|licence|registration|লাইসেন্স|certificate)"),
        ("Payment & LC", r"(\blc\b|এলসি|payment|পেমেন্ট|finance)"),
        ("Buyer Finding", r"(buyer|বায়ার|order)"),
        ("Shipping, CNF & Documents", r"(document|shipping|freight|cnf|c&f|সিএন্ডএফ|ফ্রেইট|container|customs|cargo|logistic|dispatch|billing|packing|lcl)"),
        ("Sourcing Agent & Buying House", r"(sourcing|buying house|বায়িং)"),
        ("Course & Training", r"(course|training|tutorial|masterclass)"),
        ("Cost, Capital & Profit", r"(cost|price|profit|income|invest|money|margin|খরচ|টাকা|দাম|লাভ)"),
        ("Destination Markets", r"(usa|europe|america|আমেরিকা|ইউরোপ|dubai|japan|canada|india|ভারত)"),
        ("Product-wise Export", r"(garment|jute|shrimp|mango|potato|vegetable|fruit|rice|leather|handicraft|food|fish|crab|granite|pomegranate|পোশাক|চাল|মাছ|সবজি|আলু|পাট)"),
        ("Export Ideas & Products List", r"(idea|product|item|পণ্য)"),
        ("Basics & Concepts", r"(what is|meaning|মানে|কি$|কাকে বলে)"),
        ("How to Start Export Business", r"(how|start|step|beginner|process|procedure|শুরু|কিভাবে)"),
    ]
    for name, rx in rules:
        if re.search(rx, k, re.I):
            return name
    return "Bangladesh Export Overview"


# Unique subtopics per cluster ("English topic | বাংলা টপিক"). The runner researches each one fresh.
BANK = {
 "License & Registration (IRC/ERC)": [
  "What an ERC is and who needs one|ইআরসি কী, কার লাগে", "ERC vs IRC: the difference|ইআরসি আর আইআরসির পার্থক্য",
  "Documents you need before applying for ERC|ইআরসির আগে যে কাগজগুলো লাগে", "Why the trade licence comes first|কেন আগে ট্রেড লাইসেন্স",
  "e-TIN and BIN for a new exporter|নতুন রপ্তানিকারকের ই-টিআইএন আর বিআইএন", "Chamber or association membership for ERC|ইআরসির জন্য চেম্বার বা অ্যাসোসিয়েশন সদস্যপদ",
  "Applying for ERC online (CCI&E)|অনলাইনে ইআরসি আবেদন (সিসিআইঅ্যান্ডই)", "Where to check the latest ERC fee|ইআরসির সর্বশেষ ফি কোথায় দেখবেন",
  "ERC renewal: when and how|ইআরসি নবায়ন কখন ও কিভাবে", "Why your AD bank matters|এডি ব্যাংক কেন জরুরি",
  "EPB registration and what it unlocks|ইপিবি নিবন্ধনে কী সুবিধা", "Product-specific permits before export|পণ্যভিত্তিক অনুমতিপত্র",
  "Proprietorship or company for exporting?|রপ্তানির জন্য প্রোপ্রাইটরশিপ নাকি কোম্পানি", "Common ERC application mistakes|ইআরসি আবেদনের সাধারণ ভুল",
  "How long getting an ERC takes|ইআরসি পেতে কত দিন লাগে", "Is ERC needed to send a sample?|স্যাম্পল পাঠাতে কি ইআরসি লাগে",
  "Legal ways to export without your own ERC|নিজের ইআরসি ছাড়া রপ্তানির বৈধ উপায়", "IRC basics for importers|আমদানিকারকের আইআরসি",
  "Registering a buying house|বায়িং হাউস নিবন্ধন", "Freight forwarder licence basics|ফ্রেইট ফরোয়ার্ডার লাইসেন্সের মূল কথা",
  "C&F agent licence basics|সিএন্ডএফ এজেন্ট লাইসেন্সের মূল কথা", "Checklist before you apply|আবেদনের আগে চেকলিস্ট",
  "ERC categories by export value|রপ্তানি মূল্য অনুযায়ী ইআরসির ক্যাটাগরি", "Keeping licences up to date|লাইসেন্স হালনাগাদ রাখার নিয়ম",
  "Bangladesh Single Window (BSW) explained|বাংলাদেশ সিঙ্গেল উইন্ডো কী", "Getting a trade licence online|অনলাইনে ট্রেড লাইসেন্স",
  "Phytosanitary certificate for agro exports|কৃষিপণ্যে ফাইটোস্যানিটারি সনদ", "Garments: BGMEA/BKMEA membership and UD|পোশাকে বিজিএমইএ/বিকেএমইএ সদস্যপদ ও ইউডি",
  "Fish exports: Department of Fisheries licence|মাছ রপ্তানিতে মৎস্য অধিদপ্তরের লাইসেন্স", "What changes when your business grows|ব্যবসা বড় হলে লাইসেন্সে কী বদলায়"],
 "Payment & LC": [
  "What a letter of credit (LC) is|এলসি আসলে কী", "The four parties in an LC|এলসির চার পক্ষ", "Sight LC vs usance LC|সাইট এলসি বনাম ইউজান্স এলসি",
  "Confirmed LC: when you need it|কনফার্মড এলসি কখন দরকার", "LC discrepancies that block payment|যে ভুলে এলসির টাকা আটকে যায়",
  "Documents presented under an LC|এলসিতে যে ডকুমেন্ট জমা দিতে হয়", "Advance payment (TT) pros and cons|অগ্রিম টিটি পেমেন্টের সুবিধা-ঝুঁকি",
  "Documents against payment (D/P)|ডকুমেন্টস অ্যাগেইনস্ট পেমেন্ট", "Documents against acceptance (D/A)|ডকুমেন্টস অ্যাগেইনস্ট অ্যাকসেপ্টেন্স",
  "Open account terms: the risk|ওপেন অ্যাকাউন্টের ঝুঁকি", "Bringing export proceeds home on time|রপ্তানি আয় সময়মতো দেশে আনা",
  "The EXP form explained|ইএক্সপি ফর্ম কী", "ERQ account basics|ইআরকিউ অ্যাকাউন্ট কী", "Bank charges on export payments|রপ্তানি পেমেন্টে ব্যাংক চার্জ",
  "Checklist when you receive an LC|এলসি হাতে পেলে যা মিলিয়ে দেখবেন", "Back-to-back LC|ব্যাক টু ব্যাক এলসি", "Master LC|মাস্টার এলসি",
  "Proforma invoice before the LC|এলসির আগে প্রোফর্মা ইনভয়েস", "How Incoterms affect payment|ইনকোটার্মস আর পেমেন্টের সম্পর্ক",
  "Red flags of a fake LC|ভুয়া এলসি চেনার উপায়", "How the money reaches your account (SWIFT)|সুইফটে টাকা কিভাবে আসে",
  "Exchange rate and your export price|বিনিময় হার আর রপ্তানি মূল্য", "Safest payment terms for a first order|প্রথম অর্ডারে নিরাপদ পেমেন্ট শর্ত",
  "LC expiry and latest shipment date|এলসির মেয়াদ আর শেষ শিপমেন্ট তারিখ", "LC amendment|এলসি সংশোধন", "Partial shipment under an LC|এলসিতে আংশিক শিপমেন্ট",
  "UCP 600 in one minute|ইউসিপি ছয়শো এক মিনিটে", "Bill of exchange (draft)|বিল অব এক্সচেঞ্জ", "Export cash incentive basics|রপ্তানিতে নগদ সহায়তা"],
 "Buyer Finding": [
  "B2B marketplaces for first buyers|প্রথম বায়ার পেতে বিটুবি মার্কেটপ্লেস", "Finding buyers on LinkedIn|লিংকডইনে বায়ার খোঁজা",
  "Trade fairs that bring buyers|যে মেলায় বায়ার আসে", "EPB support for fairs|মেলায় ইপিবির সহায়তা",
  "Bangladesh missions' commercial wings|দূতাবাসের কমার্শিয়াল উইং", "Searching importers on Google the smart way|গুগলে আমদানিকারক খোঁজার কৌশল",
  "Using trade data to find buyers|ট্রেড ডেটা দিয়ে বায়ার খোঁজা", "The first email to a buyer|বায়ারকে প্রথম ইমেইল",
  "Follow-up without being annoying|বিরক্ত না করে ফলো আপ", "Sample policy that wins orders|যে স্যাম্পল নীতিতে অর্ডার আসে",
  "Talking price with a buyer|বায়ারের সাথে দাম নিয়ে কথা", "Checking if a buyer is real|বায়ার আসল কিনা যাচাই",
  "Answering an RFQ fast|আরএফকিউ-এর দ্রুত উত্তর", "A product catalogue buyers read|বায়ার যে ক্যাটালগ পড়ে",
  "Product photos that sell abroad|বিদেশে বিক্রি করা পণ্যের ছবি", "MOQ: how to set it|এমওকিউ কিভাবে ঠিক করবেন",
  "Reply speed and trust|দ্রুত উত্তর আর আস্থা", "Business etiquette with foreign buyers|বিদেশি বায়ারের সাথে আচরণ",
  "Professional WhatsApp for export|এক্সপোর্টে পেশাদার হোয়াটসঅ্যাপ", "Virtual factory tour on video call|ভিডিও কলে কারখানা দেখানো",
  "Certifications buyers ask for|বায়াররা যে সার্টিফিকেট চায়", "Building trust before the first order|প্রথম অর্ডারের আগে আস্থা তৈরি",
  "Listing on Exportain|এক্সপোর্টেইনে পণ্য তালিকাভুক্তি", "Negotiation basics|দরকষাকষির মূল কৌশল", "Handling a buyer's 'no'|বায়ার না বললে কী করবেন",
  "Turning one order into repeat orders|এক অর্ডারকে বারবার অর্ডারে রূপ দেওয়া", "Talking to a buyer on a call|কলে বায়ারের সাথে কথা",
  "Getting a first export order|প্রথম এক্সপোর্ট অর্ডার পাওয়া"],
 "Shipping, CNF & Documents": [
  "Commercial invoice|কমার্শিয়াল ইনভয়েস", "Packing list|প্যাকিং লিস্ট", "Bill of lading|বিল অব লেডিং", "Air waybill|এয়ার ওয়েবিল",
  "Certificate of origin|সার্টিফিকেট অব অরিজিন", "GSP and the EU REX system|জিএসপি আর ইইউর রেক্স", "Bill of export|বিল অব এক্সপোর্ট",
  "Phytosanitary certificate|ফাইটোস্যানিটারি সার্টিফিকেট", "Fumigation certificate|ফিউমিগেশন সার্টিফিকেট", "Insurance certificate|ইন্স্যুরেন্স সার্টিফিকেট",
  "Pre-shipment inspection|প্রি-শিপমেন্ট ইন্সপেকশন", "HS code: why it matters|এইচএস কোড কেন জরুরি", "FOB vs CIF|এফওবি বনাম সিআইএফ",
  "EXW and DAP explained|এক্স ওয়ার্কস আর ডিএপি", "What a C&F agent does|সিএন্ডএফ এজেন্টের কাজ", "What a freight forwarder does|ফ্রেইট ফরোয়ার্ডারের কাজ",
  "FCL vs LCL|এফসিএল বনাম এলসিএল", "Air freight vs sea freight|এয়ার নাকি সি ফ্রেইট", "Container sizes|কনটেইনারের সাইজ",
  "Chattogram port export flow|চট্টগ্রাম বন্দরে রপ্তানির ধাপ", "Land port exports via Benapole|বেনাপোল স্থলবন্দর দিয়ে রপ্তানি",
  "Customs clearance step by step|কাস্টমস ক্লিয়ারেন্সের ধাপ", "ASYCUDA World in simple words|অ্যাসাইকুডা ওয়ার্ল্ড সহজ ভাষায়",
  "Shipping marks on cartons|কার্টনের শিপিং মার্ক", "Export-standard packaging|রপ্তানি মানের প্যাকেজিং", "Sending samples by courier|কুরিয়ারে স্যাম্পল পাঠানো",
  "What decides your freight cost|কী দেখে ফ্রেইট খরচ ঠিক হয়", "Transit time planning|ট্রানজিট টাইম পরিকল্পনা", "Bonded warehouse basics|বন্ডেড ওয়্যারহাউসের মূল কথা",
  "VGM: container weight rule|ভিজিএম: কনটেইনারের ওজনের নিয়ম"],
 "Sourcing Agent & Buying House": [
  "What a buying house actually does|বায়িং হাউস আসলে কী করে", "Sourcing agent vs buying house|সোর্সিং এজেন্ট বনাম বায়িং হাউস",
  "How buying houses earn (commission)|বায়িং হাউসের আয় কিভাবে", "Starting a buying house: first steps|বায়িং হাউস শুরুর প্রথম ধাপ",
  "Merchandiser's daily work|মার্চেন্ডাইজারের কাজ", "Factory compliance audits|কারখানার কমপ্লায়েন্স অডিট", "Tech pack basics|টেক প্যাক কী",
  "Sampling stages in garments|পোশাকে স্যাম্পলিংয়ের ধাপ", "Quality inspection (AQL)|মান পরিদর্শন (একিউএল)", "Order follow-up timeline|অর্ডার ফলো আপের টাইমলাইন",
  "Choosing a reliable factory|নির্ভরযোগ্য কারখানা বাছাই", "Costing a garment order|পোশাক অর্ডারের কস্টিং"],
 "Course & Training": [
  "What to learn first as a new exporter|নতুন রপ্তানিকারক আগে কী শিখবেন", "Free export learning resources|বিনামূল্যে রপ্তানি শেখার উৎস",
  "How to judge an export course|এক্সপোর্ট কোর্স যাচাইয়ের উপায়", "Skills every exporter needs|রপ্তানিকারকের জরুরি দক্ষতা",
  "Learn by doing: a 30-day plan|৩০ দিনের শেখার পরিকল্পনা", "Export marketing in simple words|সহজ ভাষায় এক্সপোর্ট মার্কেটিং",
  "Export marketing plan basics|এক্সপোর্ট মার্কেটিং প্ল্যান", "Export documentation: what to practise|ডকুমেন্টেশন অনুশীলন"],
 "Cost, Capital & Profit": [
  "Cost breakdown of a first shipment|প্রথম চালানের খরচের হিসাব", "How to calculate an FOB price|এফওবি দাম হিসাবের নিয়ম",
  "Hidden costs new exporters miss|নতুনদের চোখ এড়ানো খরচ", "Profit margin in export|রপ্তানিতে লাভের মার্জিন",
  "Starting with small capital|কম পুঁজিতে শুরু", "The 'no investment' export myth|বিনা পুঁজিতে রপ্তানির ভুল ধারণা",
  "Sample cost: who pays?|স্যাম্পলের খরচ কে দেবে", "Packaging cost and price|প্যাকেজিং খরচ আর দাম", "Bank charges in your costing|কস্টিংয়ে ব্যাংক চার্জ",
  "Payment terms and cash flow|পেমেন্ট শর্ত আর নগদ প্রবাহ", "MOQ and working capital|এমওকিউ আর চলতি মূলধন", "A simple export costing sheet|সহজ কস্টিং শিট",
  "Writing a price quotation|প্রাইস কোটেশন লেখা", "Licence and registration cost: where to check|লাইসেন্স খরচ কোথায় দেখবেন",
  "Cash incentive and your margin|নগদ সহায়তা আর মার্জিন", "Discounts without losing money|লোকসান ছাড়া ছাড় দেওয়া"],
 "Destination Markets": [
  "Exporting to the USA: first checks|আমেরিকায় রপ্তানির আগে যা দেখবেন", "Food exports to the USA: FDA basics|আমেরিকায় খাদ্য রপ্তানিতে এফডিএ",
  "Exporting to the EU: duty-free access|ইউরোপে শুল্কমুক্ত সুবিধা", "EU buyer expectations|ইউরোপের বায়ারের প্রত্যাশা",
  "Exporting to the UK|যুক্তরাজ্যে রপ্তানি", "Exporting to Japan|জাপানে রপ্তানি", "Exporting to Canada|কানাডায় রপ্তানি",
  "Exporting to India by land port|স্থলবন্দর দিয়ে ভারতে রপ্তানি", "Exporting to the Middle East|মধ্যপ্রাচ্যে রপ্তানি",
  "Exporting to China|চীনে রপ্তানি", "How to choose your first market|প্রথম বাজার বাছাই", "Shipping cost to the USA vs Europe|আমেরিকা বনাম ইউরোপ শিপিং খরচ"],
 "Product-wise Export": [],     # filled from the keyword's own product
 "Export Ideas & Products List": [
  "Bangladesh's top export products|বাংলাদেশের প্রধান রপ্তানি পণ্য", "Low-capital export ideas|কম পুঁজির রপ্তানি আইডিয়া",
  "Emerging export products|সম্ভাবনাময় নতুন রপ্তানি পণ্য", "Agro export ideas|কৃষিপণ্য রপ্তানির আইডিয়া", "Handicraft export ideas|হস্তশিল্প রপ্তানির আইডিয়া",
  "Choosing a beginner-friendly product|নতুনদের জন্য সহজ পণ্য", "Checking demand before you choose|পণ্য বাছাইয়ের আগে চাহিদা যাচাই",
  "Using Trade Map for product ideas|ট্রেড ম্যাপে পণ্যের আইডিয়া", "Products from your own district|নিজের জেলার পণ্য দিয়ে রপ্তানি",
  "Eco-friendly products buyers want|পরিবেশবান্ধব পণ্যের চাহিদা"],
 "Basics & Concepts": [
  "What export means|রপ্তানি মানে কী", "Import vs export|আমদানি আর রপ্তানির পার্থক্য", "Deemed export|প্রচ্ছন্ন রপ্তানি",
  "Re-export port|পুনঃরপ্তানি বন্দর", "What EPB does|ইপিবি কী করে", "EPZ and BEPZA|ইপিজেড আর বেপজা",
  "Export duty explained|রপ্তানি শুল্ক", "Bangladesh's biggest export sector|বাংলাদেশের প্রধান রপ্তানি খাত", "Export earnings and the fiscal year|রপ্তানি আয় আর অর্থবছর",
  "Manufacturer-exporter vs merchant exporter|প্রস্তুতকারক বনাম মার্চেন্ট রপ্তানিকারক"],
 "How to Start Export Business": [
  "The 7-step export roadmap|রপ্তানির সাত ধাপের রোডম্যাপ", "Your first 30 days as an exporter|রপ্তানিকারক হিসেবে প্রথম ৩০ দিন",
  "Beginner mistakes to avoid|নতুনদের সাধারণ ভুল", "Starting export from home|ঘরে বসে রপ্তানি শুরু", "Exporting as a small business|ছোট ব্যবসা থেকে রপ্তানি",
  "Women entrepreneurs in export|নারী উদ্যোক্তাদের রপ্তানি", "Choosing your first product|প্রথম পণ্য বাছাই", "From registration to first shipment|নিবন্ধন থেকে প্রথম চালান",
  "Online tools for a new exporter|নতুন রপ্তানিকারকের অনলাইন টুল", "What a new exporter should never promise|নতুনরা যে প্রতিশ্রুতি দেবেন না"],
 "Bangladesh Export Overview": [
  "Bangladesh export earnings: the latest numbers|বাংলাদেশের রপ্তানি আয়ের সর্বশেষ চিত্র", "Top export destinations|প্রধান রপ্তানি গন্তব্য",
  "LDC graduation and exporters|এলডিসি উত্তরণ আর রপ্তানিকারক", "Why diversify beyond garments|পোশাকের বাইরে বৈচিত্র্য কেন",
  "Government support for exporters|রপ্তানিকারকের সরকারি সহায়তা", "Skills that make exporters succeed|সফল রপ্তানিকারকের দক্ষতা",
  "Export myths in Bangladesh|রপ্তানি নিয়ে প্রচলিত ভুল ধারণা", "What buyers think of Bangladesh|বাংলাদেশ নিয়ে বায়ারদের ধারণা",
  "Digital tools changing export|রপ্তানি বদলে দেওয়া ডিজিটাল টুল", "Exporter vs manufacturer vs trader|রপ্তানিকারক, প্রস্তুতকারক, ট্রেডার",
  "Export fairs in Dhaka|ঢাকার রপ্তানি মেলা", "Why export at all|কেন রপ্তানি করবেন"],
 "Export surplus / পাইকারি মার্কেট": [
  "What 'export surplus' really means|এক্সপোর্ট সারপ্লাস আসলে কী", "How to check export-quality stitching|এক্সপোর্ট কোয়ালিটি সেলাই চেনা",
  "Reading labels and size tags|লেবেল আর সাইজ ট্যাগ দেখে চেনা", "Stock lot business basics|স্টক লট ব্যবসার মূল কথা",
  "Wholesale buying tips|পাইকারি কেনার টিপস", "Fake 'export quality' warning signs|ভুয়া এক্সপোর্ট কোয়ালিটি চেনার উপায়",
  "Pricing surplus for resale|সারপ্লাস পণ্যের দাম ঠিক করা", "From buying surplus to making your own export|সারপ্লাস কেনা থেকে নিজের রপ্তানি"],
}
PRODUCTS = [("garment", "Garments|পোশাক"), ("t shirt|t-shirt|টি শার্ট", "T-shirts|টি শার্ট"), ("textile|kapda|কাপড়", "Textiles|কাপড়"),
            ("jute bag", "Jute bags|পাটের ব্যাগ"), ("jute|পাট", "Jute goods|পাটপণ্য"), ("shrimp|চিংড়ি", "Shrimp|চিংড়ি"),
            ("crab|কাঁকড়া", "Crab|কাঁকড়া"), ("eel|কুচিয়া", "Eel (kuchia)|কুঁচিয়া"), ("ইলিশ", "Hilsa|ইলিশ"), ("আইশ|scale", "Fish scales|মাছের আঁশ"),
            ("fish|মাছ", "Fish|মাছ"), ("mango|(?<![\u0980-\u09FF])আম(?![\u0980-\u09FF])|আমের", "Mango|আম"), ("potato|আলু", "Potato|আলু"), ("vegetable|সবজি", "Vegetables|সবজি"),
            ("banana|(?<![\u0980-\u09FF])কলা(?![\u0980-\u09FF])", "Banana|কলা"), ("coconut", "Coconut|নারকেল"), ("pomegranate", "Fruit|ফল"), ("fruit|(?<![\u0980-\u09FF])ফল(?![\u0980-\u09FF])", "Fruit|ফল"),
            ("rice|(?<![\u0980-\u09FF])চাল(?![\u0980-\u09FF])", "Rice|চাল"), ("onion|pyaj", "Onion|পেঁয়াজ"), ("leather|চামড়া", "Leather|চামড়া"), ("shoe|জুতা", "Footwear|জুতা"),
            ("handicraft", "Handicrafts|হস্তশিল্প"), ("furniture", "Furniture|আসবাব"), ("mushroom|মাশরুম", "Mushroom|মাশরুম"),
            ("কচুরিপানা", "Water hyacinth crafts|কচুরিপানার পণ্য"), ("pharma|medicine", "Medicine|ওষুধ"), ("granite", "Stone|পাথর"),
            ("food", "Food products|খাদ্যপণ্য"), ("agri|কৃষি", "Agro products|কৃষিপণ্য"), ("জ্যাকেট|jacket|হুডি|শীতের", "Winter wear|শীতের পোশাক"), ("পোশাক|গার্মেন্টস|clothes|clothing|apparel", "Garments|পোশাক")]
PRODUCT_ANGLES = ["How to start exporting {p}|{bp} রপ্তানি কিভাবে শুরু করবেন", "Documents and permits for {p}|{bp} রপ্তানির কাগজ ও অনুমতি",
                  "Finding buyers for {p}|{bp} এর বিদেশি বায়ার খোঁজা", "Packaging and quality for {p}|{bp} এর প্যাকেজিং ও মান",
                  "Pricing {p} for export|রপ্তানির জন্য {bp} এর দাম ঠিক করা", "Best markets for {p}|{bp} এর সেরা বাজার"]
HOOKS = ["3 quick steps|৩টি দ্রুত ধাপ", "The mistake most beginners make|নতুনরা যে ভুল করে", "Myth vs fact|ভুল ধারণা বনাম সত্য",
         "One number that surprises people|একটি চমকে দেওয়া সংখ্যা", "Question → straight answer|প্রশ্ন → সরাসরি উত্তর",
         "Save-this checklist|সেভ করে রাখার চেকলিস্ট", "Before vs after|আগে বনাম পরে", "15-second story|১৫ সেকেন্ডের গল্প",
         "Did you know?|জানতেন কি?", "A vs B|এটা নাকি ওটা", "Explain like I'm new|একদম নতুনদের মতো করে", "Stop doing this|এটা আর করবেন না"]
WORLDS = ["port and container ship|বন্দর আর কনটেইনার জাহাজ", "world map with flight and sea routes|বিশ্ব মানচিত্রে রুট",
          "desk with documents flying into folders|টেবিলে কাগজ ফোল্ডারে ঢুকছে", "phone chat with a foreign buyer|ফোনে বিদেশি বায়ারের চ্যাট",
          "calculator and price tags|ক্যালকুলেটর আর দামের ট্যাগ", "factory line with cartons|কারখানার লাইনে কার্টন", "bank vault and money flow|ব্যাংক আর টাকার প্রবাহ",
          "checklist board with ticks|টিক দেওয়া চেকলিস্ট বোর্ড", "split screen before/after|আগে-পরে স্প্লিট স্ক্রিন", "counter and bar chart|কাউন্টার আর বার চার্ট",
          "quiz cards flipping|উল্টানো কুইজ কার্ড", "district map of Bangladesh|বাংলাদেশের জেলা মানচিত্র"]

# ------------------------------------------------------------------ 4. assign cluster, subtopic, hook, world
used_sub = collections.Counter()
for r in keep:
    r["cluster"] = r.get("cluster") or cluster_for(r["keyword"])
    r["seo_kw"], r["lang"], r["banglish"] = clean(r["keyword"], r["lang"])

by_cluster = collections.defaultdict(list)
for r in sorted(keep, key=lambda x: -x.get("opp", 0)):
    if r["cluster"] in ("Bangladesh Export Overview", "Export Ideas & Products List", "How to Start Export Business", "Basics & Concepts") \
            and any(re.search(rx, r["keyword"], re.I) for rx, _ in PRODUCTS):
        r["cluster"] = "Product-wise Export"
    by_cluster[r["cluster"]].append(r)

# keyword -> specific subtopic triggers (searched across ALL banks, so the Short answers what was searched)
TRIG = [
 (r"incentive|নগদ সহায়তা", "Export cash incentive basics"), (r"শুল্ক|duty", "Export duty explained"),
 (r"প্রচ্ছন্ন|deemed", "Deemed export"), (r"পুনঃরপ্তানি|re-?export", "Re-export port"),
 (r"bepza|epz|প্রক্রিয়াকরণ এলাকা|ইপিজেড", "EPZ and BEPZA"), (r"উন্নয়ন ব্যুরো|\bepb\b", "What EPB does"),
 (r"earning|আয়ের প্রধান|রপ্তানি আয়|export report|export 2025", "Bangladesh export earnings: the latest numbers"),
 (r"প্রধান রপ্তানি পণ্য|তালিকা|list|which product|কি কি পণ্য|export items|export products of", "Bangladesh's top export products"),
 (r"মানে কি|meaning|কাকে বলে|what is export$|রপ্তানি কি$|রপ্তানি কী$|এক্সপোর্ট কি$|এক্সপোর্ট মানে", "What export means"),
 (r"আমদানি ও রপ্তানি|আমদানি রপ্তানি কি|what is (export )?import|import and export|export and import", "Import vs export"),
 (r"irc", "ERC vs IRC: the difference"), (r"renew", "ERC renewal: when and how"),
 (r"কি কি লাগে|requirements|documents?$(?<=license bangladesh documents)|what.*need", "Documents you need before applying for ERC"),
 (r"freight.*(cost|price)|ফ্রেইট.*দাম", "What decides your freight cost"), (r"how to export from bangladesh|how to export products|export kivabe|এক্সপোর্ট কিভাবে|কিভাবে এক্সপোর্ট", "The 7-step export roadmap"),
 (r"(erc|ইআরসি|license|licence|লাইসেন্স|registration certificate).*(cost|price|দাম|টাকা|খরচ|koto)", "Where to check the latest ERC fee"),
 (r"(erc|ইআরসি).*online|apply|license.*online", "Applying for ERC online (CCI&E)"),
 (r"ট্রেড লাইসেন্স|trade license", "Why the trade licence comes first"), (r"without license|লাইসেন্স ছাড়া", "Legal ways to export without your own ERC"),
 (r"buying house.*(licen|regist)", "Registering a buying house"), (r"freight.*licen|freight.*regist", "Freight forwarder licence basics"),
 (r"সি এন্ড এফ লাইসেন্স|c&f.*licen|cnf.*licen", "C&F agent licence basics"), (r"garments? export license", "Garments: BGMEA/BKMEA membership and UD"),
 (r"কৃষি পণ্য রপ্তানি লাইসেন্স", "Phytosanitary certificate for agro exports"),
 (r"এলসি কিভাবে খুলতে|lc process|lc export procedure|against lc", "Checklist when you receive an LC"),
 (r"এলসি করার নিয়ম|এলসি কি$|এলসি মানে|lc মানে|what is lc|export lc$|lc for export", "What a letter of credit (LC) is"),
 (r"lc.*(cost|koto|charge|rate|খরচ|চার্জ)", "Bank charges on export payments"), (r"payment.*(bank|overseas|online)", "How the money reaches your account (SWIFT)"),
 (r"payment method|payment terms|payment process", "Safest payment terms for a first order"), (r"lc documentation|lc.*document", "Documents presented under an LC"),
 (r"linkedin", "Finding buyers on LinkedIn"), (r"online.*buyer|buyers online", "B2B marketplaces for first buyers"),
 (r"convince|কথা বলতে", "Talking to a buyer on a call"), (r"first export order|export order|orders?", "Getting a first export order"),
 (r"চায়না বায়ার", "Checking if a buyer is real"), (r"buyer.*(bank account|credit card|without investment)", "Building trust before the first order"),
 (r"commercial invoice|billing", "Commercial invoice"), (r"packing", "Packing list"), (r"bill of lading|lading", "Bill of lading"),
 (r"air (export|cargo)|air export shipment", "Air freight vs sea freight"), (r"sea export|container", "Container sizes"),
 (r"customs", "Customs clearance step by step"), (r"\blcl\b", "FCL vs LCL"), (r"courier", "Sending samples by courier"),
 (r"cnf|c&f|সিএন্ডএফ", "What a C&F agent does"), (r"freight|ফ্রেইট", "What a freight forwarder does"),
 (r"shipment process|shipping process|shipping documentation|export shipping", "Customs clearance step by step"),
 (r"(documents?|documentation).*(list|related|all)|export documents$|export related", "Commercial invoice"),
 (r"t shirt buying|garments buying house", "What a buying house actually does"), (r"buying house.*course|buying house course", "Merchandiser's daily work"),
 (r"best buying house|top buying", "Choosing a reliable factory"), (r"sourcing agent", "Sourcing agent vs buying house"),
 (r"free.*course|course free", "Free export learning resources"), (r"course|training", "How to judge an export course"),
 (r"marketing (plan|strategy|objectives)", "Export marketing plan basics"), (r"export marketing|marketing for export|fob export marketing", "Export marketing in simple words"),
 (r"book", "What to learn first as a new exporter"), (r"profit|লাভ|margin", "Profit margin in export"), (r"income|ইনকাম|আয়$", "Profit margin in export"),
 (r"without investment|without money|low investment|কম পুঁজি|minimum investment|capital", "Starting with small capital"),
 (r"(usa|america|আমেরিকা).*(cost|price|koto|টাকা|খরচ)", "Shipping cost to the USA vs Europe"),
 (r"(europe|ইউরোপ).*(cost|price|koto|টাকা|খরচ)", "Shipping cost to the USA vs Europe"),
 (r"food.*usa|usa.*food", "Food exports to the USA: FDA basics"), (r"usa|america|আমেরিকা", "Exporting to the USA: first checks"),
 (r"europe|ইউরোপ|italy", "Exporting to the EU: duty-free access"), (r"india|ভারত", "Exporting to India by land port"),
 (r"dubai", "Exporting to the Middle East"), (r"japan", "Exporting to Japan"), (r"canada", "Exporting to Canada"),
 (r"idea|আইডিয়া", "Low-capital export ideas"), (r"women", "Women entrepreneurs in export"), (r"from home|home$", "Starting export from home"),
 (r"step by step|a to z|full process|procedure|process", "The 7-step export roadmap"), (r"beginner|নতুন", "Beginner mistakes to avoid"),
 (r"online", "Online tools for a new exporter"), (r"small business|ছোট", "Exporting as a small business"),
 (r"চেনার উপায়|quality", "How to check export-quality stitching"), (r"surplus|সারপ্লাস", "What 'export surplus' really means"),
]
ALL = {s.split("|")[0]: (c, s) for c, b in BANK.items() for s in b}

for c, lst in by_cluster.items():
    bank = BANK.get(c) or []
    for i, r in enumerate(lst):
        k = r["keyword"].lower()
        if c == "Product-wise Export":
            p = next((v for rx, v in PRODUCTS if re.search(rx, k, re.I)), "Export products|রপ্তানি পণ্য")
            pe, pb = p.split("|")
            n = used_sub[p]; used_sub[p] += 1
            a = PRODUCT_ANGLES[n % len(PRODUCT_ANGLES)]
            if re.search(r"document|permit", k): a = PRODUCT_ANGLES[1]
            elif re.search(r"buyer", k): a = PRODUCT_ANGLES[2]
            elif re.search(r"packing|quality", k): a = PRODUCT_ANGLES[3]
            pel = pe if pe in ("Hilsa",) else pe[0].lower() + pe[1:]
            r["subtopic"] = a.split("|")[0].format(p=pel) + "|" + a.split("|")[1].format(bp=pb)
            r["sub_round"] = n // len(PRODUCT_ANGLES)
            continue
        hit = next((sub for rx, sub in TRIG if re.search(rx, k, re.I) and sub in ALL), None)
        if hit:
            # a strongly matching subtopic; if it is already used a lot, use the least-used sibling in the same bank
            hc, hs = ALL[hit]
            if used_sub[hs] >= 6:
                sib = BANK[hc]
                hs = min(sib, key=lambda s: (used_sub[s], sib.index(s)))
            r["subtopic"] = hs
        else:
            r["subtopic"] = min(bank, key=lambda s: (used_sub[s], bank.index(s)))
        r["sub_round"] = used_sub[r["subtopic"]]; used_sub[r["subtopic"]] += 1

# ------------------------------------------------------------------ 5. publish order: spread clusters evenly, best first
order, buckets = [], {c: list(v) for c, v in by_cluster.items()}
weights = {c: len(v) for c, v in buckets.items()}
credit = {c: 0.0 for c in buckets}
last = None
while any(buckets.values()):
    for c in credit:
        if buckets[c]:
            credit[c] += weights[c]
    cands = sorted((c for c in buckets if buckets[c]), key=lambda c: -credit[c])
    pick = next((c for c in cands if c != last), cands[0])
    credit[pick] -= sum(weights[c] for c in buckets if buckets[c]) or 1
    order.append(buckets[pick].pop(0)); last = pick

# avoid same subtopic within 21 videos (swap forward)
for i in range(len(order)):
    for j in range(i + 1, min(i + 60, len(order))):
        window = {o["subtopic"] for o in order[max(0, i - 21):i]}
        if order[i]["subtopic"] not in window:
            break
        order[i], order[j] = order[j], order[i]

# ------------------------------------------------------------------ 6. slots, IDs, titles, tags
TZ = timezone(timedelta(hours=6))
start = datetime(2026, 10, 28, tzinfo=TZ)
SLOTS = [(6, 0), (15, 0), (20, 0)]
EXID = {r["keyword"]: f"EX-{i + 1:04d}" for i, r in enumerate(rows)}
CL_TAGS = {
 "License & Registration (IRC/ERC)": (["#ExportLicense", "#ERC"], ["#এক্সপোর্টলাইসেন্স", "#ইআরসি"]),
 "Payment & LC": (["#LetterOfCredit", "#ExportPayment"], ["#এলসি", "#এক্সপোর্টপেমেন্ট"]),
 "Buyer Finding": (["#ExportBuyers", "#FindBuyers"], ["#বিদেশিবায়ার", "#বায়ার"]),
 "Shipping, CNF & Documents": (["#ExportDocuments", "#Shipping"], ["#এক্সপোর্টডকুমেন্ট", "#শিপিং"]),
 "Sourcing Agent & Buying House": (["#BuyingHouse", "#Sourcing"], ["#বায়িংহাউস", "#সোর্সিং"]),
 "Course & Training": (["#ExportCourse", "#LearnExport"], ["#এক্সপোর্টকোর্স", "#রপ্তানিশিখুন"]),
 "Cost, Capital & Profit": (["#ExportCost", "#ExportProfit"], ["#রপ্তানিখরচ", "#ব্যবসারলাভ"]),
 "Destination Markets": (["#ExportMarkets", "#GlobalTrade"], ["#বিদেশেরবাজার", "#বৈশ্বিকবাণিজ্য"]),
 "Product-wise Export": (["#ExportProducts", "#MadeInBangladesh"], ["#রপ্তানিপণ্য", "#মেইডইনবাংলাদেশ"]),
 "Export Ideas & Products List": (["#ExportIdeas", "#BusinessIdeas"], ["#রপ্তানিআইডিয়া", "#ব্যবসারআইডিয়া"]),
 "Basics & Concepts": (["#ExportBasics", "#ImportExport"], ["#রপ্তানি", "#আমদানিরপ্তানি"]),
 "How to Start Export Business": (["#StartExporting", "#ExportBusiness"], ["#এক্সপোর্টব্যবসা", "#রপ্তানিব্যবসা"]),
 "Bangladesh Export Overview": (["#BangladeshExport", "#ExportBusiness"], ["#বাংলাদেশেররপ্তানি", "#এক্সপোর্টব্যবসা"]),
 "Export surplus / পাইকারি মার্কেট": (["#ExportSurplus", "#Wholesale"], ["#এক্সপোর্টসারপ্লাস", "#পাইকারি"]),
}


def title_case(s):
    small = {"a", "an", "and", "or", "for", "of", "to", "in", "on", "from", "the", "vs", "with", "by"}
    keep_up = {"bd": "BD", "lc": "LC", "erc": "ERC", "irc": "IRC", "usa": "USA", "uk": "UK", "c&f": "C&F", "cnf": "CNF", "epz": "EPZ",
               "fob": "FOB", "lcl": "LCL", "bepza": "BEPZA", "(bepza)": "(BEPZA)", "(epz)": "(EPZ)"}
    out = []
    for i, w in enumerate(s.split()):
        lw = w.lower()
        out.append(keep_up.get(lw) or (lw if (i and lw in small) else lw[:1].upper() + lw[1:]))
    return " ".join(out)


def tags_for(r):
    k, kw = r["keyword"], r["seo_kw"]
    en_core = ["export business bangladesh", "how to export from bangladesh", "export import business", "exportain"]
    bn_core = ["রপ্তানি ব্যবসা", "এক্সপোर्ट ব্যবসা".replace("र", "র"), "আমদানি রপ্তানি", "এক্সপোর্টেইন"]
    t = [kw, k] + ([r["subtopic"].split("|")[0].lower(), r["subtopic"].split("|")[1]])
    t += bn_core + en_core if r["lang"] == "Bangla" else en_core + bn_core
    t += ["youtube shorts", "shorts"]
    out, total = [], 0
    for x in t:
        x = re.sub(r"[<>#,]", "", x).strip()
        if x and x.lower() not in [o.lower() for o in out] and total + len(x) + 1 <= 440:
            out.append(x); total += len(x) + 1
    return out


plan = []
for n, r in enumerate(order):
    day, s = divmod(n, 3)
    hh, mm = SLOTS[s]
    slot = start + timedelta(days=day, hours=hh, minutes=mm)
    en_sub, bn_sub = r["subtopic"].split("|")
    hook_en, hook_bn = HOOKS[(n * 5 + r.get("sub_round", 0) * 7) % len(HOOKS)].split("|")
    world_en, world_bn = WORLDS[(n * 7 + 3) % len(WORLDS)].split("|")
    lang = r["lang"]
    if lang == "Bangla":
        title = f"{r['seo_kw']} | {bn_sub}"
    else:
        title = f"{title_case(r['seo_kw'])}: {en_sub}"
    if len(title) > 90:
        title = title[:88].rsplit(" ", 1)[0]
    ht = CL_TAGS[r["cluster"]][1 if lang == "Bangla" else 0]
    hashtags = ["#Shorts"] + ht + (["#রপ্তানি", "#Exportain"] if lang == "Bangla" else ["#BangladeshExport", "#Exportain"])
    plan.append({
        "n": n + 1, "id": f"sh-{n + 1:04d}", "ex_id": EXID.get(r["keyword"], "NEW"), "slot": slot.isoformat(),
        "lang": lang, "keyword": r["keyword"], "seo_keyword": r["seo_kw"], "banglish_source": bool(r.get("banglish")),
        "cluster": r["cluster"], "subtopic": en_sub if lang == "English" else bn_sub, "subtopic_en": en_sub,
        "hook_format": hook_en if lang == "English" else hook_bn, "visual_world": world_en,
        "intent": r.get("intent", "Informational"), "volume_tier": r.get("tier", "medium"),
        "opportunity": r.get("opp"), "draft_title": title, "hashtags": hashtags[:5], "tags": tags_for(r),
        "replacement_keyword": bool(r.get("replacement")),
    })

json.dump({"version": 1, "created": "2026-10-27", "slots_local": ["06:00", "15:00", "20:00"], "timezone": "+06:00",
           "shorts": plan}, open(f"{OUT}/plan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
c = collections.Counter(p["lang"] for p in plan)
print("plan:", len(plan), dict(c), "first", plan[0]["slot"], "last", plan[-1]["slot"])
print("replacements:", sum(p["replacement_keyword"] for p in plan))
for p in plan[:12]:
    print(p["id"], p["slot"][:16], p["lang"][:2], p["cluster"][:18], "|", p["draft_title"], "|", p["hook_format"])
