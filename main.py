import Game


from telegram.ext import Updater
updater = Updater(token='747856178:AAG55_tg9z-7HK8nCkN5g1B1Eah9s0fmzuo', use_context=True)



dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a butt, please talk to me!")


from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()