import os
from pytimeparse import parse
from dotenv import load_dotenv
import ptbot

load_dotenv("tok.env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

message_id_dict = {}


def wait(chat_id, question):
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
        message_id=message_id
    )
    bot.create_timer(time_seconds, choose, author_id=chat_id)


def choose(author_id):
    bot.send_message(author_id, "Время вышло!")


def notify_progress(secs_left, chat_id, message_id):
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
    global bot
    bot = ptbot.Bot(TELEGRAM_TOKEN)
    bot.reply_on_message(wait)
    bot.run_bot()


if __name__ == '__main__':
    main()