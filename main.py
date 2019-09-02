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

def make_actions_keyborad(game_id):
    actions_keyboard = [
    [InlineKeyboardButton("Coup", callback_data= "COMMAND|COUP|{}".format(game_id))],
    [InlineKeyboardButton("Income", callback_data= "COMMAND|INCOME|{}".format(game_id)),InlineKeyboardButton("Foreign Aid ", callback_data= "COMMAND|FOREIGN_AID|{}".format(game_id))],
    [InlineKeyboardButton("Tax", callback_data= "COMMAND|TAX|{}".format(game_id)),InlineKeyboardButton("Steal", callback_data= "COMMAND|STEAL|{}".format(game_id))],
    [InlineKeyboardButton("Assasinate", callback_data= "COMMAND|ASSASINATE|{}".format(game_id)),InlineKeyboardButton("Exchange", callback_data= "COMMAND|EXCHANGE|{}".format(game_id))]
    ]

    return actions_keyboard

def make_challenge_keyboard(game,player_index):
    
    keyboard = [[InlineKeyboardButton("CHALLENGE", callback_data="CHALLENGE|{}|{}".format(game.get_id(), game.get_players()[player_index].get_id().message.chat_id))]] 
    if(game.get_players()[player_index] == game.target_player):
        if(game.get_action() == "ASSASINATE"):
            keyboard.append([InlineKeyboardButton("Contessa", callback_data="REACTION|BLOCK_ASSASIANTE|{}|{}".format(game.get_id(), game.get_players()[player_index].get_id().message.chat_id))])
        if(game.get_action() == "STEAL"):
            keyboard.append([InlineKeyboardButton("Ambassador", callback_data="REACTION|Ambassador|{}|{}".format(game.get_id(), game.get_players()[player_index].get_id().message.chat_id))])
            keyboard.append([InlineKeyboardButton("Capitan", callback_data="REACTION|Capitan|{}|{}".format(game.get_id(), game.get_players()[player_index].get_id().message.chat_id))])
            
    return keyboard
def make_players_keyborad(game):
    keyboard = []
   
    for player_index in range(len(game.get_players())):
        if(player_index != game.get_turn() and  game.get_players()[player_index].get_state() != "DEAD" ):
            keyboard.append([InlineKeyboardButton(game.get_players()[player_index].get_name(), callback_data="PLAYER|{}|{}".format(game.get_id(), player_index))])

    return keyboard
     
                    
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
            for player in games[game_index].get_players():
                keyboard = [[InlineKeyboardButton("Start Play", callback_data="READY|{}|{}".format(games[game_index].get_id(),player.get_id().message.chat_id))]] 
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
            games[game_index].start() ## next state = Acting

        if(games[game_index].get_state() == "Acting"):
            for player_index in range(len(games[game_index].get_players())):
                if(player_index == games[game_index].get_turn()):

                    reply_markup = InlineKeyboardMarkup(make_actions_keyborad(games[game_index].get_id()))

                    games[game_index].get_players()[player_index].get_id().message.reply_text('You Better Be Careful !!!!', reply_markup=reply_markup)
                else:
                    games[game_index].get_players()[player_index].get_id().message.reply_text('Wait FOR IT  !!!!  '+ str( games[game_index].get_players()[games[game_index].get_turn()].get_id().message.chat_id ) )
        

            games[game_index].set_state("Wait_For_Action_Btn")
        if(games[game_index].get_state() == "Sending_Challenge_Btn"):
            for player_index in range(len(games[game_index].get_players())):
                if(player_index != games[game_index].get_turn()):
                
                    keyboard = make_challenge_keyboard(games[game_index],player_index ) 
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    games[game_index].get_players()[player_index].get_id().message.reply_text('Wait FOR IT  !!!!  '+ str( games[game_index].get_players()[games[game_index].get_turn()].get_id().message.chat_id) + "IS DOING "+ str(games[game_index].get_action()  ) )
                    games[game_index].get_players()[player_index].get_id().message.reply_text('READY TO CHALLENGE', reply_markup=reply_markup)
            games[game_index].set_last_action_time(time.time())
                 
            games[game_index].set_state("Wait_For_Challenge_Btn")
        if(games[game_index].get_state() == "Wait_For_Challenge_Btn"):
            a = time.time()
            b = games[game_index].last_action_time
            if( a - b  > 10 ):
                games[game_index].set_state("Performig")
        
        if(games[game_index].get_state() == "Sending_Players_Btn"):
            for player_index in range(len(games[game_index].get_players())):
                if(player_index == games[game_index].get_turn()):
                    keyboard = make_players_keyborad(games[game_index])
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    games[game_index].get_players()[player_index].get_id().message.reply_text('Wait FOR IT  !!!!  '+ str( games[game_index].get_players()[games[game_index].get_turn()].get_id().message.chat_id) + "IS CHOOSING FOR "+ str(games[game_index].get_action()  ) )
                    games[game_index].get_players()[player_index].get_id().message.reply_text('READY TO CHALLENGE', reply_markup=reply_markup)
            games[game_index].set_state("Waiting_For_PLayers_Btn")

        if(games[game_index].get_state() == "Performing"):
            games[game_index].perform()
            games[game_index].set_state("Acting")


def button_handler(update, context):
    query = update.callback_query
    state , game_id , chat_id  = query.data.split("|")
    query.edit_message_text(text="Selected option: {}".format(query.data))
    for game_index in range(len(games)):
        if(games[game_index].get_id() == int(game_id) ):
            for player in games[game_index].get_players():
                if(player.id.message.chat_id == int(chat_id) ):
                    player.set_state("Ready")


def action_button_handler(update, context):
    query = update.callback_query

    state , action , game_id =  query.data.split("|")
    query.edit_message_text(text="Selected option: {}".format(query.data))
    
    for game_index in range(len(games)):
            if(games[game_index].get_id() == int(game_id) ):
                game = games[game_index]

    game.set_action(action)
    is_target_player_needed = game.check_target_player_need()
    if(is_target_player_needed):
        game.set_state("Sending_Players_Btn")
        return
    
    game.set_state("Performing")


def target_player_handler(update, context):
    query = update.callback_query

    state , game_id , target_player_chat_id =  query.data.split("|")
    query.edit_message_text(text="Selected option: {}".format(query.data))
    
    for game_index in range(len(games)):
            if(games[game_index].get_id() == int(game_id) ):
                game = games[game_index]
    
    game.set_target_player(target_player_chat_id)
    
    is_challenge_possible = game.check_challenge_possibility() #TODO : CHECK NEEDED
    
    if(is_challenge_possible):
            game.set_state("Sending_Challenge_Btn")
            return
    game.set_state("Performing")


def challenge_button_handler(update, context):
    query = update.callback_query

    state , game_id , target_player_chat_id =  query.data.split("|")
    query.edit_message_text(text="Selected option: {}".format(query.data))
    
    for game_index in range(len(games)):
            if(games[game_index].get_id() == int(game_id) ):
                game = games[game_index]
    
    

    game.set_state("Performing")




updater.dispatcher.add_handler(CallbackQueryHandler(button_handler,pattern=r'READY'))
updater.dispatcher.add_handler(CallbackQueryHandler(target_player_handler,pattern=r'PLAYER'))
updater.dispatcher.add_handler(CallbackQueryHandler(action_button_handler,pattern=r'COMMAND'))
updater.dispatcher.add_handler(CallbackQueryHandler(challenge_button_handler,pattern=r'CHALLENGE'))


start_handler = CommandHandler('start', start)
play_handler = CommandHandler('play', play)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(play_handler)

updater.start_polling()

while True :
    match_maker(2)
    game_handler()
    print(players_queue)
    time.sleep(1)    
