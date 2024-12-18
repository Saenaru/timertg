import ptbot

TELEGRAM_TOKEN = '7218676290:AAE0Zl8bB2Kax0BxbzbHoe2E_u0EcTqc0kQ'  # подставьте свой ключ API
TG_CHAT_ID = '744120077'  # подставьте свой ID
bot = ptbot.Bot(TELEGRAM_TOKEN)
bot.send_message(TG_CHAT_ID, "Бот запущен")
