import ar from "./locales/ar";
import de from "./locales/de";
import fr from "./locales/fr";
import tr from "./locales/tr";

export type Lang = "en" | "fa" | "tr" | "ar" | "de" | "fr";

export const LANGS: { code: Lang; label: string; name: string; dir: "ltr" | "rtl" }[] = [
  { code: "en", label: "EN", name: "English", dir: "ltr" },
  { code: "fa", label: "فا", name: "فارسی", dir: "rtl" },
  { code: "ar", label: "ع", name: "العربية", dir: "rtl" },
  { code: "tr", label: "TR", name: "Türkçe", dir: "ltr" },
  { code: "de", label: "DE", name: "Deutsch", dir: "ltr" },
  { code: "fr", label: "FR", name: "Français", dir: "ltr" },
];

export const RTL_LANGS: Lang[] = ["fa", "ar"];

export function dirFor(lang: Lang): "ltr" | "rtl" {
  return RTL_LANGS.includes(lang) ? "rtl" : "ltr";
}

type Dict = Record<string, string>;

const en: Dict = {
  "brand.name": "Trade AI",
  "brand.tagline": "AI-assisted proprietary trading",

  "nav.challenges": "Challenges",
  "nav.how": "How It Works",
  "nav.platform": "Platform",
  "nav.payouts": "Payouts",
  "nav.faq": "FAQ",
  "nav.about": "About",
  "nav.contact": "Contact",
  "nav.dashboard": "Dashboard",
  "nav.login": "Log in",
  "nav.register": "Get Funded",
  "nav.logout": "Log out",

  "hero.badge": "Live AI engine · 4 markets streaming",
  "hero.title": "Trade our capital.",
  "hero.titleAccent": "Keep up to 90%.",
  "hero.sub":
    "Pass a transparent evaluation, get funded up to $200,000, and let our AI risk engine watch every position alongside you.",
  "hero.cta": "Start a challenge",
  "hero.cta2": "See how it works",
  "hero.note": "No hidden rules. No time limit. Payouts every 14 days.",

  "stats.traders": "Funded traders",
  "stats.paid": "Paid out",
  "stats.countries": "Countries",
  "stats.uptime": "Engine uptime",

  "models.title": "Choose your evaluation",
  "models.sub": "Three routes to funding. Same profit split, different pace.",
  "models.evaluation": "Evaluation",
  "models.express": "Express",
  "models.instant": "Instant",
  "models.evaluationDesc": "Two phases. Lowest fee. The classic route.",
  "models.expressDesc": "One phase. Faster to funded, tighter targets.",
  "models.instantDesc": "No evaluation. Trade live capital from day one.",
  "models.accountSize": "Account size",
  "models.fee": "One-time fee",
  "models.profitTarget": "Profit target",
  "models.dailyLoss": "Max daily loss",
  "models.maxLoss": "Max overall loss",
  "models.split": "Profit split",
  "models.timeLimit": "Time limit",
  "models.unlimited": "Unlimited",
  "models.phase1": "Phase 1",
  "models.phase2": "Phase 2",
  "models.select": "Start with",
  "models.popular": "Most popular",
  "models.refund": "Fee refunded with your first payout",

  "how.title": "From sign-up to payout",
  "how.sub": "Four steps. Everything measured against rules published up front.",
  "how.s1.t": "Pick a challenge",
  "how.s1.d": "Choose an account size and model. Pay the one-time fee — refunded on your first payout.",
  "how.s2.t": "Hit the target",
  "how.s2.d": "Trade your own strategy on MT5. Stay inside the daily and overall loss limits.",
  "how.s3.t": "Get funded",
  "how.s3.d": "Credentials for your funded account land within 24 hours of verification.",
  "how.s4.t": "Withdraw",
  "how.s4.d": "Request a payout every 14 days. You keep 80% — up to 90% with scaling.",

  "platform.title": "The engine behind the account",
  "platform.sub":
    "Trade AI is not just a funding desk. The same stack that clears your trades also watches them.",
  "platform.f1.t": "AI risk governor",
  "platform.f1.d":
    "Position-level exposure, drawdown and correlation checks run continuously — you get warned before a rule breach, not after.",
  "platform.f2.t": "Live market intelligence",
  "platform.f2.d":
    "Streaming ticks on EURUSD, GBPUSD, XAUUSD and BTCUSD feed a smart-money and liquidity model you can read in the dashboard.",
  "platform.f3.t": "Trade journal that writes itself",
  "platform.f3.d":
    "Every fill, close and reason is recorded and scored. The feedback loop turns it into a per-symbol performance profile.",
  "platform.f4.t": "Backtest before you risk",
  "platform.f4.d":
    "Run any strategy against historical candles from inside your account and compare it to your live results.",
  "platform.f5.t": "MT5 native",
  "platform.f5.d":
    "Connect the terminal you already use. Our bridge mirrors positions in real time — no copy-trade lag.",
  "platform.f6.t": "Guardian supervision",
  "platform.f6.d":
    "An always-on supervisor process monitors execution health and closes orphaned positions automatically.",

  "payout.title": "Payouts, in plain terms",
  "payout.sub": "The part most firms bury in a PDF.",
  "payout.p1.t": "Every 14 days",
  "payout.p1.d": "Your first request unlocks 14 days after the first funded trade. After that, every cycle.",
  "payout.p2.t": "80% → 90%",
  "payout.p2.d": "Base split is 80%. Scaling adds 5% at each profit milestone, capped at 90%.",
  "payout.p3.t": "Paid in 24h",
  "payout.p3.d": "Bank transfer, USDT or Wise. Processed within one business day of approval.",
  "payout.p4.t": "Fee back",
  "payout.p4.d": "The challenge fee is added to your first payout in full.",

  "rules.title": "The rules, all of them",
  "rules.sub": "If it is not on this page, it is not a rule.",
  "rules.allowed": "Allowed",
  "rules.forbidden": "Not allowed",
  "rules.a1": "News trading",
  "rules.a2": "Holding over the weekend",
  "rules.a3": "Expert Advisors and algos",
  "rules.a4": "Hedging inside one account",
  "rules.f1": "Latency and arbitrage abuse",
  "rules.f2": "Copy trading between funded accounts",
  "rules.f3": "Group / coordinated order flow",
  "rules.f4": "Tick scalping under 15 seconds",

  "testi.title": "Traders on the desk",
  "testi.sub": "Payout-verified accounts.",

  "faq.title": "Questions worth answering",
  "faq.q1": "Is there a time limit on the evaluation?",
  "faq.a1":
    "No. Both phases run without a deadline. The only requirement is that you place at least one trade every 30 days so the account is not treated as dormant.",
  "faq.q2": "How is the daily loss calculated?",
  "faq.a2":
    "Against the higher of your starting balance or your equity at the last daily reset (00:00 server time), including floating PnL. The dashboard shows the exact remaining buffer in real time.",
  "faq.q3": "Can I use an Expert Advisor?",
  "faq.a3":
    "Yes, on both evaluation and funded accounts. What is not allowed is an EA whose edge comes from exploiting feed latency or from coordinating orders across several accounts.",
  "faq.q4": "What happens if I break a rule?",
  "faq.a4":
    "The account is closed and you keep any payout already approved. You can restart with a discounted fee. The risk engine warns you at 80% of every limit before that point.",
  "faq.q5": "Which platforms can I trade on?",
  "faq.a5":
    "MetaTrader 5 today, through our own bridge. Positions and history are mirrored into the Trade AI dashboard live.",
  "faq.q6": "Do you take a cut of losses?",
  "faq.a6": "No. Losses sit with the firm. Your downside is the one-time challenge fee.",

  "cta.title": "The capital is ready.",
  "cta.sub": "Start the evaluation today and trade a funded account this month.",
  "cta.button": "Get funded",

  "footer.product": "Product",
  "footer.company": "Company",
  "footer.legal": "Legal",
  "footer.terms": "Terms of service",
  "footer.privacy": "Privacy policy",
  "footer.risk": "Risk disclosure",
  "footer.refund": "Refund policy",
  "footer.careers": "Careers",
  "footer.blog": "Blog",
  "footer.affiliate": "Affiliate program",
  "footer.support": "Support",
  "footer.rights": "All rights reserved.",
  "footer.disclaimer":
    "Trade AI provides simulated trading accounts for evaluation purposes. Nothing on this site is investment advice. Trading carries substantial risk of loss and is not suitable for every investor.",

  "auth.loginTitle": "Welcome back",
  "auth.loginSub": "Log in to your Trade AI account.",
  "auth.registerTitle": "Create your account",
  "auth.registerSub": "One account for challenges, payouts and the dashboard.",
  "auth.username": "Username",
  "auth.email": "Email",
  "auth.password": "Password",
  "auth.deviceName": "Device name (optional)",
  "auth.submitLogin": "Log in",
  "auth.submitRegister": "Create account",
  "auth.noAccount": "No account yet?",
  "auth.haveAccount": "Already registered?",
  "auth.forgot": "Forgot password?",
  "auth.forgotTitle": "Reset your password",
  "auth.forgotSub": "We will email you a reset link.",
  "auth.sendReset": "Send reset link",
  "auth.resetSent": "If that email exists, a reset link is on its way.",
  "auth.registered": "Account created. You can log in now.",
  "auth.passwordHint": "At least 8 characters.",

  "dash.title": "Live desk",
  "dash.sub": "Everything below is read straight from the Trade AI backend.",
  "dash.system": "System",
  "dash.market": "Market",
  "dash.guardian": "Guardian",
  "dash.positions": "Open positions",
  "dash.history": "Trade history",
  "dash.journal": "AI journal",
  "dash.sessions": "Active sessions",
  "dash.performance": "AI performance",
  "dash.stream": "Live tick stream",
  "dash.refresh": "Refresh",
  "dash.close": "Close",
  "dash.empty": "Nothing to show yet.",
  "dash.loginRequired": "Log in to see your desk.",
  "dash.journalCount": "Journal entries",
  "dash.backtest": "Backtest",
  "dash.runBacktest": "Run backtest",
  "dash.symbol": "Symbol",
  "dash.timeframe": "Timeframe",
  "dash.runSignal": "Generate signal",
  "dash.runMarket": "Run market cycle",
  "dash.tools": "Engine tools",

  "state.loading": "Loading…",
  "state.error": "Could not reach the backend",
  "state.offline": "Offline",
  "state.online": "Online",
  "state.connecting": "Connecting",

  "about.title": "Why we built a prop firm",
  "about.sub": "We were the traders getting the vague rejection emails.",
  "about.body1":
    "Trade AI started as an execution and risk engine, not a funding desk. We ran it on our own capital for two years: streaming market data, an AI risk governor sitting over every position, and a journal that scored each decision after the fact.",
  "about.body2":
    "The reason we opened it to outside traders is simple. The infrastructure scales, discretionary talent does not — and most funding programmes fail traders on rules that were never written down clearly. Ours are all on one page, and the same engine that enforces them shows you the numbers live.",
  "about.body3":
    "We make money when funded traders make money. That is the whole model. There is no incentive for us to fail you on a technicality.",
  "about.v1.t": "Rules in public",
  "about.v1.d": "Every limit is on the site and in your dashboard, calculated the same way.",
  "about.v2.t": "Warnings before breaches",
  "about.v2.d": "The risk engine flags at 80% of a limit. Silent failure is a design bug.",
  "about.v3.t": "Payouts on schedule",
  "about.v3.d": "Fixed 14-day cycles, processed within one business day.",

  "contact.title": "Talk to a human",
  "contact.sub": "Support answers in under 4 hours, every day.",
  "contact.name": "Your name",
  "contact.message": "Message",
  "contact.send": "Send message",
  "contact.sent": "Thanks — we will reply by email.",
  "contact.channels": "Other channels",

  "common.perMonth": "/ challenge",
  "common.mostChosen": "Most chosen",
  "common.viewAll": "View all",
  "common.back": "Back",
  "common.retry": "Retry",
};

const fa: Dict = {
  "brand.name": "تریدAI",
  "brand.tagline": "پراپ‌تریدینگ با موتور هوش مصنوعی",

  "nav.challenges": "چالش‌ها",
  "nav.how": "چطور کار می‌کند",
  "nav.platform": "پلتفرم",
  "nav.payouts": "تسویه",
  "nav.faq": "سؤالات",
  "nav.about": "درباره ما",
  "nav.contact": "تماس",
  "nav.dashboard": "داشبورد",
  "nav.login": "ورود",
  "nav.register": "شروع فاند",
  "nav.logout": "خروج",

  "hero.badge": "موتور هوش مصنوعی فعال · ۴ بازار زنده",
  "hero.title": "با سرمایه‌ی ما ترید کن.",
  "hero.titleAccent": "تا ۹۰٪ سود مال توست.",
  "hero.sub":
    "یک ارزیابی شفاف را پشت سر بگذار، تا ۲۰۰٬۰۰۰ دلار سرمایه بگیر، و بگذار موتور ریسک هوش مصنوعی ما کنار تو مراقب هر پوزیشن باشد.",
  "hero.cta": "شروع چالش",
  "hero.cta2": "چطور کار می‌کند؟",
  "hero.note": "بدون قانون پنهان. بدون محدودیت زمانی. تسویه هر ۱۴ روز.",

  "stats.traders": "تریدر فاندشده",
  "stats.paid": "پرداخت‌شده",
  "stats.countries": "کشور",
  "stats.uptime": "پایداری موتور",

  "models.title": "ارزیابی خودت را انتخاب کن",
  "models.sub": "سه مسیر تا فاند شدن. تقسیم سود یکسان، سرعت متفاوت.",
  "models.evaluation": "ارزیابی",
  "models.express": "اکسپرس",
  "models.instant": "آنی",
  "models.evaluationDesc": "دو مرحله. کمترین هزینه. مسیر کلاسیک.",
  "models.expressDesc": "تک‌مرحله. سریع‌تر تا فاند، با هدف سخت‌گیرانه‌تر.",
  "models.instantDesc": "بدون ارزیابی. از روز اول با سرمایه‌ی واقعی.",
  "models.accountSize": "حجم حساب",
  "models.fee": "هزینه‌ی یک‌بار",
  "models.profitTarget": "هدف سود",
  "models.dailyLoss": "حداکثر ضرر روزانه",
  "models.maxLoss": "حداکثر ضرر کل",
  "models.split": "سهم سود",
  "models.timeLimit": "محدودیت زمانی",
  "models.unlimited": "نامحدود",
  "models.phase1": "مرحله ۱",
  "models.phase2": "مرحله ۲",
  "models.select": "شروع با",
  "models.popular": "پرطرفدارترین",
  "models.refund": "هزینه با اولین تسویه برمی‌گردد",

  "how.title": "از ثبت‌نام تا تسویه",
  "how.sub": "چهار قدم. همه چیز بر اساس قوانینی که از اول منتشر شده‌اند.",
  "how.s1.t": "چالش را انتخاب کن",
  "how.s1.d": "حجم حساب و مدل را انتخاب کن. هزینه‌ی یک‌بار را بپرداز — با اولین تسویه برمی‌گردد.",
  "how.s2.t": "به هدف برس",
  "how.s2.d": "با استراتژی خودت روی MT5 ترید کن و داخل سقف ضرر روزانه و کل بمان.",
  "how.s3.t": "فاند شو",
  "how.s3.d": "اطلاعات حساب فاندشده حداکثر ۲۴ ساعت بعد از تأیید برایت ارسال می‌شود.",
  "how.s4.t": "برداشت کن",
  "how.s4.d": "هر ۱۴ روز درخواست تسویه بده. ۸۰٪ سهم توست — با اسکیلینگ تا ۹۰٪.",

  "platform.title": "موتوری که پشت حساب است",
  "platform.sub":
    "تریدAI فقط یک میز فاندینگ نیست. همان زیرساختی که معاملات را اجرا می‌کند، مراقبشان هم هست.",
  "platform.f1.t": "ناظر ریسک هوشمند",
  "platform.f1.d":
    "بررسی مداوم اکسپوژر، دراودان و همبستگی در سطح هر پوزیشن — قبل از نقض قانون هشدار می‌گیری، نه بعد از آن.",
  "platform.f2.t": "هوش بازار زنده",
  "platform.f2.d":
    "جریان تیک زنده روی EURUSD، GBPUSD، XAUUSD و BTCUSD که مدل اسمارت‌مانی و نقدینگی را تغذیه می‌کند و در داشبورد قابل مشاهده است.",
  "platform.f3.t": "ژورنالی که خودش را می‌نویسد",
  "platform.f3.d":
    "هر ورود، خروج و دلیلش ثبت و امتیازدهی می‌شود. حلقه‌ی بازخورد آن را به پروفایل عملکرد هر نماد تبدیل می‌کند.",
  "platform.f4.t": "بک‌تست قبل از ریسک",
  "platform.f4.d":
    "هر استراتژی را روی کندل‌های تاریخی از داخل حسابت اجرا کن و با نتایج زنده‌ات مقایسه کن.",
  "platform.f5.t": "بومیِ MT5",
  "platform.f5.d":
    "همان ترمینالی که استفاده می‌کنی را وصل کن. پل ما پوزیشن‌ها را بلادرنگ آینه می‌کند — بدون تأخیر کپی‌تریدینگ.",
  "platform.f6.t": "نظارت Guardian",
  "platform.f6.d":
    "یک پروسه‌ی ناظر همیشه‌فعال سلامت اجرا را پایش می‌کند و پوزیشن‌های بی‌صاحب را خودکار می‌بندد.",

  "payout.title": "تسویه، بدون حاشیه",
  "payout.sub": "همان بخشی که اکثر شرکت‌ها ته یک PDF پنهانش می‌کنند.",
  "payout.p1.t": "هر ۱۴ روز",
  "payout.p1.d": "اولین درخواست ۱۴ روز بعد از اولین معامله‌ی فاندشده باز می‌شود. بعد از آن، هر دوره.",
  "payout.p2.t": "۸۰٪ تا ۹۰٪",
  "payout.p2.d": "سهم پایه ۸۰٪ است. اسکیلینگ در هر پله‌ی سود ۵٪ اضافه می‌کند، تا سقف ۹۰٪.",
  "payout.p3.t": "پرداخت در ۲۴ ساعت",
  "payout.p3.d": "حواله‌ی بانکی، USDT یا Wise. حداکثر یک روز کاری بعد از تأیید.",
  "payout.p4.t": "بازگشت هزینه",
  "payout.p4.d": "هزینه‌ی چالش به‌طور کامل به اولین تسویه‌ات اضافه می‌شود.",

  "rules.title": "قوانین، همه‌شان",
  "rules.sub": "اگر در این صفحه نیست، قانون نیست.",
  "rules.allowed": "مجاز",
  "rules.forbidden": "غیرمجاز",
  "rules.a1": "معامله در زمان اخبار",
  "rules.a2": "نگه‌داشتن پوزیشن در آخر هفته",
  "rules.a3": "اکسپرت ادوایزر و الگوریتم",
  "rules.a4": "هج داخل یک حساب",
  "rules.f1": "سوءاستفاده از تأخیر و آربیتراژ",
  "rules.f2": "کپی‌تریدینگ بین حساب‌های فاندشده",
  "rules.f3": "سفارش‌گذاری گروهی و هماهنگ",
  "rules.f4": "اسکالپ تیکی زیر ۱۵ ثانیه",

  "testi.title": "تریدرهای میز ما",
  "testi.sub": "حساب‌هایی با تسویه‌ی تأییدشده.",

  "faq.title": "سؤال‌هایی که جواب می‌خواهند",
  "faq.q1": "ارزیابی محدودیت زمانی دارد؟",
  "faq.a1":
    "نه. هر دو مرحله بدون مهلت اجرا می‌شوند. تنها شرط این است که هر ۳۰ روز حداقل یک معامله بگذاری تا حساب راکد حساب نشود.",
  "faq.q2": "ضرر روزانه چطور محاسبه می‌شود؟",
  "faq.a2":
    "نسبت به بیشترینِ موجودی اولیه یا اکوییتی در آخرین ریست روزانه (۰۰:۰۰ به وقت سرور)، شامل سود و زیان شناور. داشبورد دقیقاً نشان می‌دهد چقدر فضا باقی مانده است.",
  "faq.q3": "می‌توانم از اکسپرت استفاده کنم؟",
  "faq.a3":
    "بله، هم در ارزیابی و هم در حساب فاندشده. چیزی که مجاز نیست، اکسپرتی است که سودش از سوءاستفاده از تأخیر فید یا هماهنگی سفارش بین چند حساب می‌آید.",
  "faq.q4": "اگر قانونی را نقض کنم چه می‌شود؟",
  "faq.a4":
    "حساب بسته می‌شود و هر تسویه‌ی تأییدشده‌ای که داشته‌ای مال خودت می‌ماند. می‌توانی با هزینه‌ی تخفیف‌دار دوباره شروع کنی. موتور ریسک در ۸۰٪ هر سقف به تو هشدار می‌دهد.",
  "faq.q5": "روی چه پلتفرم‌هایی می‌شود ترید کرد؟",
  "faq.a5":
    "فعلاً متاتریدر ۵، از طریق پل اختصاصی ما. پوزیشن‌ها و تاریخچه به‌صورت زنده در داشبورد تریدAI آینه می‌شوند.",
  "faq.q6": "از ضرر هم سهم برمی‌دارید؟",
  "faq.a6": "نه. ضرر با شرکت است. تنها ریسک تو همان هزینه‌ی یک‌بارِ چالش است.",

  "cta.title": "سرمایه آماده است.",
  "cta.sub": "همین امروز ارزیابی را شروع کن و همین ماه با حساب فاندشده ترید کن.",
  "cta.button": "فاند شو",

  "footer.product": "محصول",
  "footer.company": "شرکت",
  "footer.legal": "حقوقی",
  "footer.terms": "شرایط استفاده",
  "footer.privacy": "حریم خصوصی",
  "footer.risk": "افشای ریسک",
  "footer.refund": "سیاست بازگشت وجه",
  "footer.careers": "فرصت‌های شغلی",
  "footer.blog": "بلاگ",
  "footer.affiliate": "همکاری در فروش",
  "footer.support": "پشتیبانی",
  "footer.rights": "تمام حقوق محفوظ است.",
  "footer.disclaimer":
    "تریدAI حساب‌های معاملاتی شبیه‌سازی‌شده برای اهداف ارزیابی ارائه می‌دهد. هیچ بخشی از این سایت توصیه‌ی سرمایه‌گذاری نیست. معامله ریسک قابل‌توجه زیان دارد و برای همه مناسب نیست.",

  "auth.loginTitle": "خوش برگشتی",
  "auth.loginSub": "به حساب تریدAI خود وارد شوید.",
  "auth.registerTitle": "ساخت حساب",
  "auth.registerSub": "یک حساب برای چالش‌ها، تسویه‌ها و داشبورد.",
  "auth.username": "نام کاربری",
  "auth.email": "ایمیل",
  "auth.password": "رمز عبور",
  "auth.deviceName": "نام دستگاه (اختیاری)",
  "auth.submitLogin": "ورود",
  "auth.submitRegister": "ساخت حساب",
  "auth.noAccount": "هنوز حساب نداری؟",
  "auth.haveAccount": "قبلاً ثبت‌نام کرده‌ای؟",
  "auth.forgot": "رمز را فراموش کرده‌ای؟",
  "auth.forgotTitle": "بازیابی رمز عبور",
  "auth.forgotSub": "لینک بازیابی برایت ایمیل می‌شود.",
  "auth.sendReset": "ارسال لینک بازیابی",
  "auth.resetSent": "اگر این ایمیل ثبت شده باشد، لینک بازیابی ارسال شد.",
  "auth.registered": "حساب ساخته شد. حالا می‌توانی وارد شوی.",
  "auth.passwordHint": "حداقل ۸ کاراکتر.",

  "dash.title": "میز زنده",
  "dash.sub": "همه‌ی داده‌های زیر مستقیم از بک‌اند تریدAI خوانده می‌شوند.",
  "dash.system": "سیستم",
  "dash.market": "بازار",
  "dash.guardian": "Guardian",
  "dash.positions": "پوزیشن‌های باز",
  "dash.history": "تاریخچه معاملات",
  "dash.journal": "ژورنال هوش مصنوعی",
  "dash.sessions": "نشست‌های فعال",
  "dash.performance": "عملکرد هوش مصنوعی",
  "dash.stream": "جریان زنده‌ی تیک",
  "dash.refresh": "بروزرسانی",
  "dash.close": "بستن",
  "dash.empty": "فعلاً چیزی برای نمایش نیست.",
  "dash.loginRequired": "برای دیدن میز خود وارد شوید.",
  "dash.journalCount": "تعداد رکورد ژورنال",
  "dash.backtest": "بک‌تست",
  "dash.runBacktest": "اجرای بک‌تست",
  "dash.symbol": "نماد",
  "dash.timeframe": "تایم‌فریم",
  "dash.runSignal": "تولید سیگنال",
  "dash.runMarket": "اجرای چرخه‌ی بازار",
  "dash.tools": "ابزارهای موتور",

  "state.loading": "در حال بارگذاری…",
  "state.error": "دسترسی به بک‌اند ممکن نشد",
  "state.offline": "آفلاین",
  "state.online": "آنلاین",
  "state.connecting": "در حال اتصال",

  "about.title": "چرا یک پراپ‌فرم ساختیم",
  "about.sub": "خودمان همان تریدرهایی بودیم که ایمیل ردِ مبهم می‌گرفتند.",
  "about.body1":
    "تریدAI به‌عنوان یک موتور اجرا و ریسک شروع شد، نه یک میز فاندینگ. دو سال آن را روی سرمایه‌ی خودمان اجرا کردیم: داده‌ی زنده‌ی بازار، یک ناظر ریسک هوشمند روی هر پوزیشن، و ژورنالی که هر تصمیم را بعد از وقوع امتیاز می‌داد.",
  "about.body2":
    "دلیل بازکردنش به روی تریدرهای بیرونی ساده است. زیرساخت مقیاس می‌گیرد، استعداد شخصی نه — و بیشتر برنامه‌های فاندینگ تریدرها را با قوانینی رد می‌کنند که هیچ‌وقت شفاف نوشته نشده‌اند. قوانین ما همه در یک صفحه است، و همان موتوری که اجراشان می‌کند اعداد را زنده نشانت می‌دهد.",
  "about.body3":
    "ما وقتی پول درمی‌آوریم که تریدرهای فاندشده پول دربیاورند. کل مدل همین است. هیچ انگیزه‌ای نداریم که با یک بهانه‌ی فنی ردت کنیم.",
  "about.v1.t": "قوانین علنی",
  "about.v1.d": "هر سقفی روی سایت و در داشبورد هست، با همان فرمول محاسبه.",
  "about.v2.t": "هشدار قبل از نقض",
  "about.v2.d": "موتور ریسک در ۸۰٪ هر سقف هشدار می‌دهد. شکست بی‌صدا یک باگ طراحی است.",
  "about.v3.t": "تسویه‌ی سر وقت",
  "about.v3.d": "دوره‌های ثابت ۱۴ روزه، پردازش در یک روز کاری.",

  "contact.title": "با یک آدم واقعی حرف بزن",
  "contact.sub": "پشتیبانی هر روز، زیر ۴ ساعت پاسخ می‌دهد.",
  "contact.name": "نام شما",
  "contact.message": "پیام",
  "contact.send": "ارسال پیام",
  "contact.sent": "ممنون — با ایمیل پاسخ می‌دهیم.",
  "contact.channels": "کانال‌های دیگر",

  "common.perMonth": "/ چالش",
  "common.mostChosen": "پرانتخاب‌ترین",
  "common.viewAll": "دیدن همه",
  "common.back": "بازگشت",
  "common.retry": "تلاش دوباره",
};

const dicts: Record<Lang, Dict> = { en, fa, tr, ar, de, fr };

export function translate(lang: Lang, key: string): string {
  return dicts[lang]?.[key] ?? dicts.en[key] ?? key;
}

const FA_DIGITS = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];
const AR_DIGITS = ["٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"];

/** Renders Latin digits in the script the current language actually uses. */
export function localizeDigits(value: string, lang: Lang): string {
  const set = lang === "fa" ? FA_DIGITS : lang === "ar" ? AR_DIGITS : null;
  if (!set) return value;
  return value.replace(/[0-9]/g, (d) => set[Number(d)]);
}
