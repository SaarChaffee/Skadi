import config
import Skadi

bot = Skadi.init(config)
app = bot.asgi

if __name__ == '__main__':
    bot.run(use_reloader=False)
