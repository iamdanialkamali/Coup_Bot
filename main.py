import Game
import time


from telegram.ext import Updater
from telegram.ext import CommandHandler

players_queue = []
updater = Updater(token='747856178:AAG55_tg9z-7HK8nCkN5g1B1Eah9s0fmzuo', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to IUST Coup bot")

def play(update, context):
    players_queue.append(update.message.chat_id)
    
    context.bot.send_message(chat_id=update.message.chat_id, text="Wait for other players")
def match_maker(players_count):
    if(len(players_queue)>=players_count):
        game = Game([players_queue[0:players_count]])
        for i in range(players_count):
            del players_queue[0]



start_handler = CommandHandler('start', start)
play_handler = CommandHandler('play', play)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(play_handler)

updater.start_polling()

while True :
    match_maker(2)
    print(players_queue)
    time.sleep(3)    
