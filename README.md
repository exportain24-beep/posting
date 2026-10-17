# Exportain অটো রিল সিস্টেম

প্রতিদিন দুপুর ১২টা আর সন্ধ্যা ৬টায় একটা বাংলা রিল **YouTube Shorts, Facebook Reels আর TikTok**-এ যায়। কেউ হাত দেয় না।

```
Claude (প্রতিদিনের শিডিউলড টাস্ক)                      GitHub Actions (Claude চালু করে)
 ১. পরের নম্বরের স্ক্রিপ্ট নেয় (content/scripts/007.txt)
 ২. যাচাই করে ভয়েস-স্ক্রিপ্ট বানায়  ──────────────►  voice.yml: ElevenLabs v4 Turbo (Debashish) → audio ব্রাঞ্চ
 ৩. অডিও নিয়ে স্কিল দিয়ে ভিডিও বানায়  ◄─────────────┘
 ৪. কভার, টাইটেল, ডেসক্রিপশন, ট্যাগ  ──────────────►  publish.yml: YouTube API (থাম্বনেইল সহ)
                                                         Facebook API (title, description, থাম্বনেইল)
                                                         Buffer → TikTok
```
🔒 **লক করা:** ভয়েস শুধু Debashish (`3XjJ1C8taYP9CHnHKmK5`), মডেল শুধু `eleven_v4_turbo`, ভাষা শুধু বাংলা। এগুলো `scripts/voice.py`-তে কোডে বাঁধা; অন্য কিছু দিলে ওয়ার্কফ্লো ভয়েস বানাতে অস্বীকার করে।

Claude কখনো কোনো কী দেখে না। কী শুধু GitHub-এর `production` Environment-এ থাকে, আর শুধু `main` ব্রাঞ্চের ওয়ার্কফ্লো সেটা পড়তে পারে।

## ব্রাঞ্চ
| ব্রাঞ্চ | কী থাকে | কে লেখে |
|---|---|---|
| `main` | কোড আর ওয়ার্কফ্লো (লক করা) | শুধু আপনি |
| `content` | `scripts/001.txt…` আপনার স্ক্রিপ্ট, `voice/<এপিসোড>/narration.json` | আপনি + Claude |
| `audio` | ElevenLabs-এর অডিও (৭ দিন পর মুছে যায়) | voice.yml |
| `media` | তৈরি ভিডিও, কভার, টেক্সট (GitHub Pages থেকে Buffer-এ যায়) | Claude |
| `state` | কোন ভিডিও কোথায় পোস্ট হলো | publish.yml |

## স্ক্রিপ্ট দেওয়া
`content` ব্রাঞ্চে `scripts` ফোল্ডারে `001.txt`, `002.txt` … নামে বাংলায় স্ক্রিপ্ট রাখুন (GitHub-এ **Add file → Create new file**, ব্রাঞ্চ `content`)। অথবা Claude-কে চ্যাটে দিন, সে রেখে দেবে। প্রতিটা প্রায় ৯০০ অক্ষরের মধ্যে (৯০ সেকেন্ড)। Claude নম্বর অনুযায়ী একটা একটা করে নেয়।

---

## 🔒 একবারের সেটআপ (ক্রম অনুযায়ী)

### ১. `production` Environment আর Secrets
**Settings → Environments → `production`** (না থাকলে New environment)
- **Deployment branches and tags → Selected branches and tags → Add rule → `main`**
- এখানে **Add environment secret** দিয়ে রাখুন:

| Secret | কোথা থেকে |
|---|---|
| `ELEVENLABS_API_KEY` | ElevenLabs → Developers → API keys → নতুন কী: শুধু **Text to Speech** অনুমতি + মাসিক **credit limit** |
| `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` | নিচের YouTube ধাপ |
| `FB_PAGE_ID`, `FB_PAGE_TOKEN`, `FB_APP_SECRET` | নিচের Facebook ধাপ |
| `BUFFER_API_KEY` | Buffer → Settings → API |

⚠️ **Repository secrets-এ কিছু রাখবেন না।** ওগুলো যেকোনো ব্রাঞ্চ পড়তে পারে।

### ২. GitHub Pages (Buffer ভিডিও এখান থেকে নেয়)
**Settings → Pages → Build and deployment → Source: Deploy from a branch → `media` / `(root)` → Save**

### ৩. Actions-এর ডিফল্ট অনুমতি কমান
**Settings → Actions → General**
- **Workflow permissions: Read repository contents and packages permissions**
- **Fork pull request workflows: Require approval for all external contributors**

### ৪. `main` লক করুন (সবশেষে, Claude-এর সেটআপ শেষ হলে)
**Settings → Rules → Rulesets → New branch ruleset**: Target `main` · Enforcement **Active** ·
**Restrict updates**, **Restrict deletions**, **Block force pushes**, **Require a pull request before merging (1 approval)** ·
**Bypass list খালি রাখুন।** এরপর কেউ (Claude-ও) ওয়ার্কফ্লো কোড বদলাতে পারবে না; নিজে বদলাতে চাইলে Ruleset সাময়িক বন্ধ করবেন।

### ৫. অ্যাকাউন্ট সুরক্ষা
- GitHub, Google, Facebook, Buffer, ElevenLabs — সবগুলোতে **Two-factor authentication**।
- **Settings → Code security → Secret Protection + Push protection: Enable**।
- Claude GitHub App-কে শুধু `posting` রিপোর অ্যাক্সেস দিন।

---

## প্ল্যাটফর্ম কী নেওয়া

### YouTube (শুধু আপলোডের অনুমতি)
1. console.cloud.google.com → নতুন প্রজেক্ট → **YouTube Data API v3** Enable
2. Google Auth Platform → Branding → Audience: **External** → **Publish app (In production)** (Testing-এ রাখলে ৭ দিনে কানেকশন বাতিল)
3. Clients → **Web application** → Redirect URI `https://developers.google.com/oauthplayground`
4. developers.google.com/oauthplayground → ⚙️ **Use your own OAuth credentials** → **শুধু** `https://www.googleapis.com/auth/youtube.upload` → Authorize → Exchange → **Refresh token**
5. থাম্বনেইলের জন্য youtube.com/verify-এ চ্যানেল ভেরিফাই

### Facebook Page
1. developers.facebook.com → Create App → **Manage everything on your Page**
2. **App settings → Advanced → Require app secret: ON** (টোকেন ফাঁস হলেও App Secret ছাড়া কাজ করবে না)
3. business.facebook.com → Settings → **System users** → Admin → Assign assets: আপনার Page
4. **Generate token** → Expiry **Never** → অনুমতি: `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`, আর থাম্বনেইলের জন্য `pages_read_user_content`, `pages_manage_engagement`
5. App settings → Basic → **App secret** → `FB_APP_SECRET`

### TikTok
Buffer-এ TikTok (Business/Creator) কানেক্ট করুন। Buffer-এ কাস্টম থাম্বনেইল হয় না, তাই ভিডিওর প্রথম ফ্রেমটাই কভার।

---

## কী ফাঁস হলে কী হয়, কী করবেন
| কী | একা ফাঁস হলে | বাতিল করুন |
|---|---|---|
| ElevenLabs | শুধু আপনার দেওয়া credit limit পর্যন্ত TTS; কোথাও পোস্ট করা যায় না | ElevenLabs → API keys → Delete |
| YouTube refresh token | Client Secret ছাড়া অকেজো; থাকলেও শুধু আপলোড, মোছা যায় না | myaccount.google.com/permissions |
| Facebook page token | App Secret ছাড়া অকেজো (Require app secret ON) | System user → Revoke tokens |
| Buffer | Buffer-এ পোস্ট করা যায় | Buffer → API → Delete key |

নতুন কী বানিয়ে একই নামে Secret আপডেট করলেই সিস্টেম আবার চলবে।

## পরীক্ষা (Claude চালায়)
- `publish.yml` **check**: শুধু লগইনগুলো আর ভিডিও ফাইল যাচাই, কিছু পোস্ট হয় না
- `publish.yml` **private**: YouTube private + Facebook draft (প্রথম আসল পরীক্ষা)
- `voice.yml` **test_tone**: ElevenLabs ছাড়া পুরো পথ পরীক্ষা, ক্রেডিট খরচ নেই

Claude-এর প্রতিদিনের কাজের নিয়ম: [`DAILY_TASK.md`](DAILY_TASK.md)
