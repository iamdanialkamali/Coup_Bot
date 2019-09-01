from Game import Game
import time,datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from telegram.ext import Updater
from telegram.ext import CommandHandler

players_queue = []
games = []
updater = Updater(token='747856178:AAG55_tg9z-7HK8nCkN5g1B1Eah9s0fmzuo', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to IUST Coup bot")

def play(update, context):
    players_queue.append(update)
    
    context.bot.send_message(chat_id=update.message.chat_id, text="Wait for other players")
def match_maker(players_count):
    if(len(players_queue)>=players_count):
        game = Game( players_queue[0:players_count] , 0 )
        print(time.time())
        games.append(game)
        for i in range(players_count):
            del players_queue[0]
    
def game_handler():
    for game_index in range(len(games)):
        if(games[game_index].get_state() == "Starting"):
            for player in games[game_index].players:
                keyboard = [[InlineKeyboardButton("Start Play", callback_data="{} | {}".format(games[game_index].get_id(),player.get_id().message.chat_id ))]] 
                reply_markup = InlineKeyboardMarkup(keyboard)
                player.get_id().message.reply_text('Game Is Ready!', reply_markup=reply_markup)
            games[game_index].set_state("Waiting")

        if(games[game_index].get_state() == "Waiting"):
            players_states = [player.get_state() for player in  games[game_index].get_players()]
            next_state = "Ready"
            
            for state in players_states:
                if(state != "Ready"):
                    next_state = "Waiting"
            if(next_state=="Ready"):
                print("SAY GOODBYE MOONMEN")
            games[game_index].set_state(next_state)

                
def button_handler(update, context):
    query = update.callback_query
    game_id , chat_id  = list(map(int,query.data.split("|")))
    query.edit_message_text(text="Selected option: {}".format(query.data))
    for game_index in range(len(games)):
        if(games[game_index].get_id() == game_id ):
            for player in games[game_index].get_players():
                if(player.id.message.chat_id == chat_id):
                    player.set_state("Ready")



updater.dispatcher.add_handler(CallbackQueryHandler(button_handler))

start_handler = CommandHandler('start', start)
play_handler = CommandHandler('play', play)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(play_handler)

updater.start_polling()

while True :
    match_maker(2)
    game_handler()
    print(players_queue)
    time.sleep(3)    
