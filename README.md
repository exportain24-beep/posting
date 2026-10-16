# Exportain অটো রিল সিস্টেম

প্রতিদিন সকাল ৮টা আর সন্ধ্যা ৬টায় একটা করে বাংলা রিল **YouTube Shorts, Facebook Reels আর TikTok**-এ নিজে থেকে পোস্ট হয়।

```
Claude (প্রতি ২ দিন)        GitHub Actions (প্রতিদিন ০৬:১৭)                  প্ল্যাটফর্ম
 রিসার্চ + স্ক্রিপ্ট  ──►  content ব্রাঞ্চ ──► ElevenLabs ভয়েস ──► ভিডিও ──►  YouTube (নির্ধারিত সময়ে)
 (শুধু JSON ডেটা)                        ৯:১৬ রেন্ডার + থাম্বনেইল       Facebook (নির্ধারিত সময়ে)
                                                                         TikTok (Buffer, নির্ধারিত সময়ে)
```

- প্রতিদিন পরের ~৩ দিনের ফাঁকা স্লট (সর্বোচ্চ ৪টা) ভরে রাখে, তাই একদিন কিছু ব্যর্থ হলেও পোস্ট বন্ধ হয় না।
- কোনো রান ব্যর্থ হলে GitHub আপনাকে ইমেইল পাঠায়। রানের পাতায় বাংলায় সারাংশ থাকে।

## ব্রাঞ্চগুলো
| ব্রাঞ্চ | কী থাকে | কে লেখে |
|---|---|---|
| `main` | কোড আর ওয়ার্কফ্লো (লক করা) | শুধু আপনি |
| `content` | `queue/*.json` এপিসোড স্ক্রিপ্ট | Claude |
| `state` | কোন স্লটে কী পোস্ট হলো | ওয়ার্কফ্লো |
| `media` | আসন্ন পোস্টের ভিডিও (পুরনো নিজে মুছে যায়) | ওয়ার্কফ্লো |

---

## 🔒 নিরাপত্তা সেটআপ (একবারই, খুব জরুরি)

### ১. Secrets রাখবেন শুধু `production` Environment-এ
**Settings → Environments → New environment → `production`**
- **Deployment branches and tags → Selected branches → `main`** যোগ করুন। এতে অন্য কোনো ব্রাঞ্চের কোড Secrets পড়তে পারবে না।
- এই Environment-এর ভেতরে **Add environment secret** দিয়ে নিচের ৮টা Secret রাখুন।
- ⚠️ **Repository secrets-এ কিছু রাখবেন না।** ওগুলো যেকোনো ব্রাঞ্চ থেকে পড়া যায়।

| Secret | কোথা থেকে |
|---|---|
| `ELEVENLABS_API_KEY` | ElevenLabs → Developers → API keys। নতুন কী বানান: শুধু **Text to Speech** অনুমতি + মাসিক **character limit** দিন |
| `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` | Google Cloud + OAuth Playground (নিচে) |
| `FB_PAGE_ID`, `FB_PAGE_TOKEN`, `FB_APP_SECRET` | Meta Business System User টোকেন + অ্যাপের App Secret |
| `BUFFER_API_KEY` | Buffer → Settings → API |

### ২. `main` ব্রাঞ্চ লক করুন
**Settings → Rules → Rulesets → New branch ruleset**
- Target: `main`, Enforcement: **Active**
- টিক দিন: **Restrict updates**, **Restrict deletions**, **Block force pushes**, **Require a pull request before merging**
- **Bypass list**-এ শুধু নিজেকে (Repository admin) রাখুন।

ফলে Claude বা অন্য কেউ ওয়ার্কফ্লো কোড বদলাতে পারবে না, পারবে শুধু `content` ব্রাঞ্চে স্ক্রিপ্ট রাখতে।

### ৩. GitHub-এর সুরক্ষা চালু রাখুন
- **Settings → Code security → Secret Protection + Push protection: Enable** (কেউ ভুলে কী কমিট করলে আটকে দেয়)
- **Settings → Actions → General → Fork pull request workflows: Require approval for all external contributors**
- আপনার GitHub অ্যাকাউন্টে **Two-factor authentication** চালু করুন।
- Claude GitHub App-কে শুধু এই একটা রিপোর অ্যাক্সেস দিন (All repositories না)।

### ৪. একটা কী ফাঁস হলেও যেন পোস্ট করা না যায়
- **Facebook:** developers.facebook.com → আপনার অ্যাপ → **App settings → Advanced → Require app secret: ON**। এখন শুধু টোকেন দিয়ে কিছু করা যায় না, App Secret-ও লাগে (কোড দুটোই আলাদা Secret থেকে নেয়)।
- **YouTube:** Refresh token একা কাজ করে না, Client Secret-ও লাগে। আর অনুমতি শুধু **`youtube.upload`** নিন, এতে ভিডিও মোছা বা চ্যানেল বদলানো যায় না।
- **ElevenLabs:** শুধু TTS অনুমতি আর character limit, তাই কী ফাঁস হলেও শুধু ঐ লিমিট পর্যন্ত ক্রেডিট খরচ হতে পারে; কোথাও পোস্ট করা যায় না।
- **সন্দেহ হলে সাথে সাথে বাতিল করুন:** Google → myaccount.google.com/permissions · Facebook → System user টোকেন Revoke · Buffer → API key delete · ElevenLabs → key delete। তারপর নতুন কী Secret-এ বসান।

---

## প্ল্যাটফর্ম কানেকশন

### YouTube
1. console.cloud.google.com → নতুন প্রজেক্ট → **YouTube Data API v3** Enable
2. Google Auth Platform → Branding (নাম, ইমেইল) → Audience: **External** → **Publish app (In production)**
3. Clients → **Web application** → Redirect URI: `https://developers.google.com/oauthplayground`
4. developers.google.com/oauthplayground → ⚙️ **Use your own OAuth credentials** → শুধু `https://www.googleapis.com/auth/youtube.upload` সিলেক্ট → Authorize → **Exchange** → Refresh token
5. কাস্টম থাম্বনেইলের জন্য youtube.com/verify-এ চ্যানেল ভেরিফাই

### Facebook Page
1. developers.facebook.com → Create App → use case **"Manage everything on your Page"**
2. business.facebook.com → Settings → **System users** → Admin system user → Assign assets: Exportain Page
3. **Generate token** → অ্যাপ বেছে নিন → `pages_show_list`, `pages_read_engagement`, `pages_manage_posts` → Expiry: **Never**
4. App settings → Basic → **App secret** কপি করে `FB_APP_SECRET`-এ রাখুন

### TikTok (Buffer দিয়ে)
Buffer-এ TikTok (Business/Creator অ্যাকাউন্ট) কানেক্ট করুন। আলাদা কোনো সেটিং লাগবে না।

---

## চালানো ও পরীক্ষা
- **Actions → Produce and schedule reels → Run workflow → Dry run ✅**: শুধু ভিডিও বানায়, কিছু পোস্ট করে না। ভিডিওটা রানের নিচে `preview` হিসেবে ডাউনলোড করা যায়।
- Dry run ছাড়া চালালে আসল পোস্ট শিডিউল হয়।
- সেটিং বদলাতে `config.json` দেখুন (পোস্টের সময়, ভয়েস, মডেল ইত্যাদি)।

স্ক্রিপ্ট লেখার নিয়ম: [`CONTENT_GUIDE.md`](CONTENT_GUIDE.md)
