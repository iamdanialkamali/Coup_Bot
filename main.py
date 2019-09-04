from Game import Game
import time,datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from telegram.ext import Updater
from telegram.ext import CommandHandler

players_queue = []
# playing_players = []
games = []
updater = Updater(token='747856178:AAG55_tg9z-7HK8nCkN5g1B1Eah9s0fmzuo', use_context=True)
dispatcher = updater.dispatcher


def broadcast_to_players(game, message):
    for player in game.get_players():
        player.get_id().message.reply_text(message)

        

def make_exchange_keyborad(game):
    
    cards =  game.get_exchanging_cards()
    cards_keyboard = []
    for card_index in range(len(cards)):
        cards_keyboard.append(
            [InlineKeyboardButton(cards[card_index].get_name(), callback_data= "EXCHANGE|{}|{}".format(game.get_id(),card_index))]
        ) 
    

    return cards_keyboard


def make_actions_keyborad(game,player_index):
    actions_keyboard = []
    if(game.get_players()[player_index].get_coins() >= 7):
        actions_keyboard.append([InlineKeyboardButton("Coup", callback_data= "COMMAND|COUP|{}".format(game.get_id()))])
    actions_keyboard = actions_keyboard + [
    [InlineKeyboardButton("Income", callback_data= "COMMAND|INCOME|{}".format(game.get_id())),InlineKeyboardButton("Foreign Aid ", callback_data= "COMMAND|FOREIGN_AID|{}".format(game.get_id()))],
    [InlineKeyboardButton("Tax", callback_data= "COMMAND|TAX|{}".format(game.get_id())),InlineKeyboardButton("Steal", callback_data= "COMMAND|STEAL|{}".format(game.get_id()))],
    ]
    last_row = [InlineKeyboardButton("Exchange", callback_data= "COMMAND|EXCHANGE|{}".format(game.get_id()))]
   
    if(game.get_players()[player_index].get_coins() >= 3):
        last_row.append(InlineKeyboardButton("Assasinate", callback_data= "COMMAND|ASSASINATE|{}".format(game.get_id())))
    
    actions_keyboard = actions_keyboard + [last_row]
    
    return actions_keyboard


def make_challenge_keyboard(game,player_index):
    
    keyboard = [[InlineKeyboardButton("CHALLENGE", callback_data="CHALLENGE|{}|{}|{}".format(game.get_id(), game.get_players()[player_index].get_id().message.chat_id,game.get_turn_counter()))]] 
    if(game.get_players()[player_index] == game.target_player):
        if(game.get_action() == "ASSASINATE"):
            keyboard.append([InlineKeyboardButton("Contessa", callback_data="REACTION|Contessa|{}|{}".format(game.get_id(), game.get_players()[player_index].get_id().message.chat_id))])
        if(game.get_action() == "STEAL"):
            keyboard.append([InlineKeyboardButton("Ambassador", callback_data="REACTION|Ambassador|{}|{}".format(game.get_id(), game.get_players()[player_index].get_id().message.chat_id))])
            keyboard.append([InlineKeyboardButton("Captain", callback_data="REACTION|Captain|{}|{}".format(game.get_id(), game.get_players()[player_index].get_id().message.chat_id))])
    if(game.get_action() == "FOREIGN_AID"):
        keyboard.append([InlineKeyboardButton("Duke", callback_data="REACTION|Duke|{}|{}".format(game.get_id(), game.get_players()[player_index].get_id().message.chat_id))])
            
    return keyboard


def make_react_challenge_keyboard(game,player_index):
    
    keyboard = [[InlineKeyboardButton("REACT CHALLENGE", callback_data="REACT_CHALLENGE|{}|{}|{}".format(game.get_id(), game.get_players()[player_index].get_id().message.chat_id,game.get_turn_counter()))]]         
    return keyboard


def make_players_keyborad(game):
    keyboard = []
   
    for player_index in range(len(game.get_players())):
        if(player_index != game.get_turn() and  game.get_players()[player_index].get_state() != "DEAD" ):
            keyboard.append([InlineKeyboardButton(game.get_players()[player_index].get_name(), callback_data="PLAYER|{}|{}".format(game.get_id(), game.get_players()[player_index].get_id().message.chat_id))])

    return keyboard


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to IUST Coup bot")


def play(update, context):
    players_queue.append(update)
    
    context.bot.send_message(chat_id=update.message.chat_id, text="Wait for other players")

def check_winning(game):
    c = game.get_living_players()
    if( len(c) == 1):
        broadcast_to_players(game , " {} Is Winner ".format(game.get_players()[0].get_name()))
        return True
    return False

def match_maker(players_count):
    if(len(players_queue)>=players_count):
        game = Game( players_queue[0:players_count] , 0 )
        print(time.time())
        games.append(game)
        for i in range(players_count):
            del players_queue[0]
    
def send_cards_and_coins(game):
    for player in game.get_living_players():
        
        cards = []
        for card in player.get_cards():
            if(card.get_state() == "active" ):
                cards.append(card.get_name())
        player.get_id().message.reply_text( "CARDS : " + " | ".join(cards) )
        player.get_id().message.reply_text( "Coins : " + str(player.get_coins()) )

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
            send_cards_and_coins(games[game_index])
            for player_index in range(len(games[game_index].get_players())):
                if(player_index == games[game_index].get_turn()):
                    keyboard = make_actions_keyborad(games[game_index],player_index)
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    players = games[game_index].get_players()
                    player = players[player_index]
                    id = player.get_id()
                    message = id.message
                    send = message.reply_text('Please choose your actions', reply_markup=reply_markup)
                else:
                    games[game_index].get_players()[player_index].get_id().message.reply_text('Wait '+ str( games[game_index].get_players()[games[game_index].get_turn()].get_id().effective_user.first_name ) + " is choosing " )
                    # games[game_index].get_players()[player_index].get_id().message.reply_text(str( games[game_index].get_players()[games[game_index].get_turn()].get_id().message.chat_id ) )
        

            games[game_index].set_state("Wait_For_Action_Btn")
        if(games[game_index].get_state() == "Sending_Challenge_Btn"):
            for player_index in range(len(games[game_index].get_players())):
                if(player_index != games[game_index].get_turn()):
                
                    keyboard = make_challenge_keyboard(games[game_index],player_index ) 
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    games[game_index].get_players()[player_index].get_id().message.reply_text(str( games[game_index].get_players()[games[game_index].get_turn()].get_id().effective_user.first_name )+ " is doing "+ str(games[game_index].get_action()  ) )
                    games[game_index].get_players()[player_index].get_id().message.reply_text('CHALLENGE ? ', reply_markup=reply_markup)
            games[game_index].set_last_action_time(time.time())
                 
            games[game_index].set_state("Wait_For_Challenge_Btn")
        if(games[game_index].get_state() == "Wait_For_Challenge_Btn"):
            a = time.time()
            b = games[game_index].last_action_time
            if( a - b  > 6 ):
                is_exchange = games[game_index].check_action_is_exchange()
                if(is_exchange):
                    games[game_index].get_cards_for_exchange()
                    games[game_index].set_state("Sending_Exchange_Btn")
                    return
                games[game_index].set_state("Performing")
        
        if(games[game_index].get_state() == "Sending_Players_Btn"):
            for player_index in range(len(games[game_index].get_players())):
                if(player_index == games[game_index].get_turn()):
                    keyboard = make_players_keyborad(games[game_index])
                    reply_markup = InlineKeyboardMarkup(keyboard)

                    # games[game_index].get_players()[player_index].get_id().message.reply_text(str( games[game_index].get_players()[games[game_index].get_turn()].get_id().message.chat_id) + "IS CHOOSING FOR "+ str(games[game_index].get_action()  ) )
                    games[game_index].get_players()[player_index].get_id().message.reply_text('Choose your targer', reply_markup=reply_markup)

            games[game_index].set_last_action_time(time.time())
            games[game_index].set_state("Waiting_For_PLayers_Btn")

        if(games[game_index].get_state() == "Performing"):
            card , is_dead = games[game_index].perform()
            broadcast_to_players(games[game_index],"{} Is Doing {}".format(games[game_index].get_players()[games[game_index].get_turn()].get_name(), games[game_index].get_action()))

            if(card != None and is_dead):
                broadcast_to_players(games[game_index] ,"{} is Dead".format(games[game_handler].get_target_player()))
                if(check_winning(games[game_index])):
                    games[game_index].set_state("FINISHED")
                    return

            games[game_index].next_turn()
            games[game_index].set_state("Acting")
            

        if(games[game_index].get_state() == "Sending_React_Challenge_Btn"):
            for player_index in range(len(games[game_index].get_players())):
                if(games[game_index].get_players()[player_index] != games[game_index].get_target_player() ):
                    
                    keyboard = make_react_challenge_keyboard(games[game_index],player_index ) 
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    games[game_index].get_players()[player_index].get_id().message.reply_text( str( games[game_index].get_target_player().get_name()) + " is doing "+ str(games[game_index].get_reaction_card()  ) )
                    games[game_index].get_players()[player_index].get_id().message.reply_text('REACT OR CHALLENGE ?', reply_markup=reply_markup)
            games[game_index].set_last_action_time(time.time())   
            games[game_index].set_state("Wait_For_React_Challenge_Btn")

        if(games[game_index].get_state() == "Wait_For_React_Challenge_Btn"):
            a = time.time()
            b = games[game_index].last_action_time
            if( a - b  > 6):
                games[game_index].next_turn()
                games[game_index].set_state("Acting")
        
        if(games[game_index].get_state() == "Sending_Exchange_Btn"):
            for player_index in range(len(games[game_index].get_players())):
                if(player_index == games[game_index].get_turn() ):

                    
                    keyboard = make_exchange_keyborad(games[game_index] ) 
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    # games[game_index].get_players()[player_index].get_id().message.reply_text('Wait str( games[game_index].get_players()[games[game_index].get_turn()].get_id().message.chat_id) + " is doing "+ str(games[game_index].get_action()  ) )
                    games[game_index].get_players()[player_index].get_id().message.reply_text('Choose Wisely !', reply_markup=reply_markup)
        
            games[game_index].set_last_action_time(time.time())
                 
            games[game_index].set_state("Waiting_For_Exchange_Btn")

        if(games[game_index].get_state() == "FINISHED"):
            del games[game_index]
            break
def button_handler(update, context):
    query = update.callback_query
    state , game_id , chat_id  = query.data.split("|")
    # query.edit_message_text(text="Selected option: {}".format(query.data))
    query.edit_message_text(text="Game Started")

    for game_index in range(len(games)):
        if(games[game_index].get_id() == int(game_id) ):
            for player in games[game_index].get_players():
                if(player.id.message.chat_id == int(chat_id) ):
                    player.set_state("Ready")


def action_button_handler(update, context):

    query = update.callback_query

    state , action , game_id =  query.data.split("|")
    # query.edit_message_text(text="Selected option: {}".format(query.data))
    query.edit_message_text(text = action)
    for game_index in range(len(games)):
            if(games[game_index].get_id() == int(game_id) ):
                game = games[game_index]
    game.set_action(action)


    is_target_player_needed = game.check_target_player_need()
    if(is_target_player_needed):
        game.set_state("Sending_Players_Btn")
        return
    
    is_challenge_possible = game.check_challenge_possibility() #TODO : CHECK NEEDED
    if(is_challenge_possible):
            game.set_state("Sending_Challenge_Btn")
            return
    
    is_exchange = game.check_action_is_exchange()
    if(is_exchange):
        game.get_cards_for_exchange()
        game.set_state("Sending_Exchange_Btn")
        return
    
    game.set_state("Performing")


def target_player_handler(update, context):
    query = update.callback_query

    state , game_id , target_player_chat_id =  query.data.split("|")
    # query.edit_message_text(text="Selected option: {}".format(query.data))
    for game_index in range(len(games)):
            if(games[game_index].get_id() == int(game_id) ):
                game = games[game_index]
    game.set_target_player(int(target_player_chat_id))
    
    query.edit_message_text(text=game.get_target_player().get_id().effective_user.first_name)
    
    is_challenge_possible = game.check_challenge_possibility() #TODO : CHECK NEEDED
    
    if(is_challenge_possible):
            game.set_state("Sending_Challenge_Btn")
            return
    
    is_exchange = game.check_action_is_exchange()
    if(is_exchange):
        game.get_cards_for_exchange()
        game.set_state("Sending_Exchange_Btn")
        return
    
    game.set_state("Performing")


def challenge_button_handler(update, context):
    query = update.callback_query

    state , game_id , target_player_chat_id , turn_counter =  query.data.split("|")
    # query.edit_message_text(text="Selected option: {}".format(query.data))
    query.edit_message_text(text="Challenging !")
    for game_index in range(len(games)):
            if(games[game_index].get_id() == int(game_id) ):
                game = games[game_index]
    
    if(game.get_state() != "Wait_For_Challenge_Btn"):
        return
    is_bluffing , deactivated_card , is_dead = game.check_challenge(int(target_player_chat_id))
    
    
    if(is_bluffing):
        broadcast_to_players(game,"{} was bluffing".format(game.get_players()[game.get_turn()].get_name())  )  
        broadcast_to_players(game ,"{}'s {} card is killed ".format(game.get_players()[game.get_turn()].get_name() , deactivated_card.get_name() ))
        if(is_dead):
            broadcast_to_players(games[game_index] ,"{} is Dead".format(game.get_players()[game.get_turn()].get_name() ))
            if(check_winning(games[game_index])):
                game.set_state("FINISHED")
                return


        game.next_turn()
        game.set_state("Acting")
        return
    
    broadcast_to_players(game,"{} was not bluffing".format(game.get_players()[game.get_turn()].get_name())  )  
    broadcast_to_players(game ,"{}'s {} card is killed ".format(game.get_challenging_player().get_name() , deactivated_card.get_name() ))
    if(is_dead):
            broadcast_to_players(games[game_index] ,"{} is Dead".format(game.get_players()[game.get_turn()].get_name() ))
            if(check_winning(games[game_index])):
                game.set_state("FINISHED")
                return

    is_exchange = game.check_action_is_exchange()
    if(is_exchange):
        game.get_cards_for_exchange()
        game.set_state("Sending_Exchange_Btn")
        return
    
    game.set_state("Performing")
    
   
def react_button_handler(update,context):
    "REACTION|BLOCK_ASSASIANTE|{}|{}"
    query = update.callback_query

    
  
    state , card ,game_id , target_player_chat_id  =  query.data.split("|")
    # query.edit_message_text(text="Selected option: {}".format(query.data))
    query.edit_message_text(text=card)
    for game_index in range(len(games)):
            if(games[game_index].get_id() == int(game_id) ):
                game = games[game_index]

    if(game.get_state() != "Wait_For_Challenge_Btn"):
        return
    if(card == "Duke"):
        game.set_target_player(int(target_player_chat_id))

    game.set_reaction_card(card)
    
    game.set_state("Sending_React_Challenge_Btn")


def react_challenge_button_handler(update,context):
    "REACT_CHALLENGE|{}|{}|{}"
    query = update.callback_query

    state ,game_id , target_player_chat_id , turn_count  =  query.data.split("|")
    # query.edit_message_text(text="Selected option: {}".format(query.data))
    query.edit_message_text(text="React Challenge !")
    
    for game_index in range(len(games)):
            if(games[game_index].get_id() == int(game_id) ):
                game = games[game_index]
    if(game.get_state() != "Wait_For_React_Challenge_Btn"):
        return
    is_bluffing ,deactivated_card , is_dead = game.check_react_challenge()
    
    # if( is_dead):
    #     broadcast_to_players(games[int(game_index)] ,"{} is Dead".format(games[int(game_index)].get_target_player()))


    if(is_bluffing):
        broadcast_to_players(game,"{} was bluffing".format(game.get_target_player().get_name())  )  
        broadcast_to_players(game ,"{}'s {} card is killed ".format(game.get_target_player().get_name() , deactivated_card.get_name() ))
        if( is_dead):
            broadcast_to_players(games[game_index] ,"{} is Dead".format(games[game_handler].get_target_player()))
            if(check_winning(games[game_index])):
                game.set_state("FINISHED")
                return

        game.set_state("Performing")
        return
    
    broadcast_to_players(game,"{} was not bluffing".format(game.get_players()[game.get_turn()].get_name())  )  
    if(is_dead):
            broadcast_to_players(games[game_index] ,"{} is Dead".format(games[game_handler].get_players()[game.get_turn()].get_name()))
            if(check_winning(games[game_index])):
                game.set_state("FINISHED")
                return



    is_exchange = game.check_action_is_exchange()
    if(is_exchange):
        game.get_cards_for_exchange()
        game.set_state("Sending_Exchange_Btn")
        return

    game.set_state("Acting")

        
    # game.set_state("Sending_React_Challenge_Btn")


def exchange_button_handler(update,context):
    "EXCHANGE|{}|{}.format(game.get_id(),card_index)"
    query = update.callback_query

    state ,game_id ,card_index =  query.data.split("|")
    # query.edit_message_text(text="Selected option: {}".format(query.data))
    for game_index in range(len(games)):
            if(games[game_index].get_id() == int(game_id) ):
                game = games[game_index]
    query.edit_message_text(text="Chosen cards is {}".format(game.get_exchanging_cards()[int(card_index)].get_name()))
    
    player = game.get_players()[game.get_turn()]
    cards = game.get_exchanging_cards() 
    
    if(len(cards) > 2 ):
        player.add_card(cards[int(card_index)])
        del cards[int(card_index)]
        # list(cards).remove()


        if(len(cards) <= 2):
            game.next_turn()
            game.set_state("Acting")
            # query.edit_message_text(text="Selected option: {}".format(query.data))
            # query.edit_message_text(text="")
            # query.edit_message_text(text="Chosen cards is {}".format(game.get_exchanging_cards()[int(card_index)].get_name()))

        else:
            game.set_state("Sending_Exchange_Btn")
            # query.edit_message_text(text="Selected option: {}".format(query.data))
            # query.edit_message_text(text="")
            # query.edit_message_text(text="Chosen cards is {}".format(game.get_exchanging_cards()[int(card_index)].get_name()))

    # game.set_state("Sending_React_Challenge_Btn")


updater.dispatcher.add_handler(CallbackQueryHandler(button_handler,pattern=r'READY'))
updater.dispatcher.add_handler(CallbackQueryHandler(target_player_handler,pattern=r'PLAYER'))
updater.dispatcher.add_handler(CallbackQueryHandler(action_button_handler,pattern=r'COMMAND'))
updater.dispatcher.add_handler(CallbackQueryHandler(challenge_button_handler,pattern=r'CHALLENGE'))
updater.dispatcher.add_handler(CallbackQueryHandler(react_challenge_button_handler,pattern=r'REACT_CHALLENGE'))
updater.dispatcher.add_handler(CallbackQueryHandler(react_button_handler,pattern=r'REACT'))
updater.dispatcher.add_handler(CallbackQueryHandler(exchange_button_handler,pattern=r'EXCHANGE'))


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
