import logging
import time
from Game import Game

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler,CallbackQueryHandler)

# Enable logging


##################################################################################################
START , PHOTO = range(2)


players_queue = []
games = []

actions_keyboard = [[InlineKeyboardButton("Coup", callback_data= "COUP")]
,[InlineKeyboardButton("Income", callback_data= "INCOME"),InlineKeyboardButton("Foreign Aid ", callback_data= "FOREIGN_AID")]
,[InlineKeyboardButton("Tax", callback_data= "TAX"),InlineKeyboardButton("Steal", callback_data= "STEAL")]
,[InlineKeyboardButton("Assasinate", callback_data= "ASSASINATE"),InlineKeyboardButton("Exchange", callback_data= "EXCHANGE")]]

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to IUST Coup bot")
    
    return START
def play(update, context):
    players_queue.append(update)
    
    context.bot.send_message(chat_id=update.message.chat_id, text="Wait for other players")
    return START
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
            for player in games[game_index].get_players():
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
        
        if(games[game_index].get_state() == "Ready"):
            games[game_index].start()
        
        if(games[game_index].get_state() == "Acting"):
            for player_index in range(len(games[game_index].get_players())):
                if(player_index == games[game_index].get_turn()):

                    reply_markup = InlineKeyboardMarkup(actions_keyboard)
                    games[game_index].get_players()[player_index].get_id().message.reply_text('You Better Be Careful !!!!', reply_markup=reply_markup)
                else:
                    games[game_index].get_players()[player_index].get_id().message.reply_text('Wait FOR IT  !!!!  '+ str( games[game_index].get_players()[games[game_index].get_turn()].get_id().message.chat_id ) )
            
            games[game_index].set_state("Acting2")


def button_handler(update, context):
    query = update.callback_query
    game_id , chat_id  = list(map(int,query.data.split("|")))
    query.edit_message_text(text="Selected option: {}".format(query.data))
    for game_index in range(len(games)):
        if(games[game_index].get_id() == game_id ):
            for player in games[game_index].get_players():
                if(player.id.message.chat_id == chat_id):
                    player.set_state("Ready")

    return START

def button_handler1(update, context):
    query = update.callback_query
    game_id , chat_id  = list(map(int,query.data.split("|")))
    query.edit_message_text(text="Selected option: {}".format(query.data))
    for game_index in range(len(games)):
        if(games[game_index].get_id() == game_id ):
            for player in games[game_index].get_players():
                if(player.id.message.chat_id == chat_id):
                    player.set_state("Ready")


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END



def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token='747856178:AAG55_tg9z-7HK8nCkN5g1B1Eah9s0fmzuo', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            START: [CommandHandler('start', start),
                    CommandHandler('play', play),
                    CallbackQueryHandler(button_handler)],

            PHOTO: [
                    CallbackQueryHandler(button_handler1)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors

    # Start the Bot
    updater.start_polling()
    
    while True :
        match_maker(2)
        game_handler()
        print(players_queue)
        time.sleep(3)    


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.


main()