from alicebot import Bot
from codeforces import CodeforcesHandler
from atcoder import AtcoderHandler
from Reminder import DailySubscribeRequestHandler,DailySubscribeSender
from common import InputChangeDispatcher,NewRequestHandler

bot = Bot()

if __name__ == "__main__":
    bot.load_plugins(CodeforcesHandler)
    bot.load_plugins(AtcoderHandler)

    bot.load_plugins(DailySubscribeRequestHandler)
    bot.load_plugins(DailySubscribeSender)

    bot.load_plugins(NewRequestHandler)
    bot.load_plugins(InputChangeDispatcher)
    bot.run()