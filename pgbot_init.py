import pgbot
import config

bot = pgbot.AsyncPgBot()

if __name__ == '__main__':
    bot.run(config.bot_token)
