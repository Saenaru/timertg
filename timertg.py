import os
from pytimeparse import parse
from dotenv import load_dotenv
import ptbot

def wait(bot, message_id_dict, chat_id, question):
    time_seconds = parse(question)
    message_id = bot.send_message(
        chat_id, 
        "Обратный отсчёт начался: осталось {} секунд.".format(time_seconds)
    )
    message_id_dict[message_id] = time_seconds
    bot.create_countdown(
        time_seconds,
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        bot=bot,
        message_id_dict=message_id_dict
    )
    bot.create_timer(time_seconds, choose, bot=bot, author_id=chat_id)

def choose(bot, author_id):
    bot.send_message(author_id, "Время вышло!")

def notify_progress(secs_left, message_id_dict, chat_id, message_id, bot):
    total_time = message_id_dict[message_id]
    progressbar = render_progressbar(total_time, total_time - secs_left)
    message_content = "Осталось {} секунд.\n{}".format(secs_left, progressbar)
    bot.update_message(chat_id, message_id, message_content)

def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return "{0} |{1}| {2}% {3}".format(prefix, pbar, percent, suffix)

def main():
    load_dotenv("token.env")
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    tg_chat_id = os.getenv("TG_CHAT_ID")
    message_id_dict = {}
    bot = ptbot.Bot(telegram_token)
    
    bot.reply_on_message(lambda chat_id, text: wait(bot, message_id_dict, chat_id, text))
    bot.run_bot()

if __name__ == '__main__':
    main()