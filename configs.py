# (c) @AbirHasan2005

# Don't Forget That I Made This!
# So Give Credits!


import os


class Config(object):
	BOT_TOKEN = os.environ.get("BOT_TOKEN")
	API_ID = int(os.environ.get("API_ID", 12345))
	API_HASH = os.environ.get("API_HASH")
	STREAMTAPE_API_PASS = os.environ.get("STREAMTAPE_API_PASS", "NoNeed")
	STREAMTAPE_API_USERNAME = os.environ.get("STREAMTAPE_API_USERNAME", "NoNeed")
	LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))
	UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", None)
	DOWN_PATH = os.environ.get("DOWN_PATH", "./downloads")
	PRESET = os.environ.get("PRESET", "ultrafast")
	OWNER_ID = int(os.environ.get("OWNER_ID", 1445283714))
	CAPTION = "By @AHToolsBot"
	BOT_USERNAME = os.environ.get("BOT_USERNAME", "VideoWatermark_Bot")
	DATABASE_URL = os.environ.get("DATABASE_URL")
	BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", False))
	ALLOW_UPLOAD_TO_STREAMTAPE = bool(os.environ.get("ALLOW_UPLOAD_TO_STREAMTAPE", True))
	USAGE_WATERMARK_ADDER = """
🖐با سلام  عزیز.

❤️به ربات واترمارک  خوش آمدید.

➖➖➖➖➖➖➖➖

⁉️ دوست داری روی فیلم هات واتر مارک کنی تا دیگه کسی از اون ها سو استفاده نکنه؟

✅ من یک ربات کاربردی هستم ک میتونی عکس مورد نظرت رو روی فیلمت بزاری تا حجم ۲ گیگابایت

☑️ کافیه عکس مورد نظرت رو با فرمت (jpg یا Png ) برام ارسال کنی تا بزارم روی فیلمت 

⚙️ از دستور /settings  برای ست کردن تنظیمات استفاده کن

دقت کن استفاده از من رایگانه و محدودیت حجمی ای وجود نداره 💎

👇🏻 فایل مورد نظرت رو بفرست برام

➖➖➖➖➖➖➖➖

📣 @hector_tm
"""
	PROGRESS = """
Percentage : {0}%
Done ✅: {1}
Total 🌀: {2}
Speed 🚀: {3}/s
ETA 🕰: {4}
"""
