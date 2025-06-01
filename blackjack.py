### Abner Herrera
### BLACKJACK SIMULATOR
### The aim is to build a program around a blackjack strategy and see the odds of the player of having a positive win/lose ratio.

import time
from colorama import Fore, Back, Style
from classes import *

def main():
    my_player, dealer = start_game()
    
    deck = Deck()
    card = Card()

    while my_player.money > 0:
        round(my_player, dealer)

        if not continue_playing(my_player):
            resumen(my_player)
            cerrar()
    
    if my_player.money == 0:
        print(f"{my_player}'s has ran out of coins D:")
        resumen(my_player)
        cerrar()


def start_game():
    print(Fore.CYAN + Back.LIGHTBLACK_EX + Style.BRIGHT + "Bienvenido al juego Blackjack." + Style.RESET_ALL + "\n")
    time.sleep(0.75)
    name = input("What is your name?\n" + Fore.BLUE)
    initial_money = int(input(Fore.RESET + "How much in coins you want to play:\n" + Fore.BLUE))
    print(Fore.RESET + "\n")

    player = Player(name, initial_money)
    house = House()

    return player, house


def check_blackjack(player, house):
    if player.calculate_score() == 21:
            if player.blackjack() and not house.blackjack():
                house.show_hand()
                player.wins()
            elif house.blackjack() and player.blackjack():
                house.show_hand()
                player.push()
            return True


def round(player, house):
    print(Fore.CYAN + "Empieza la ronda." + Fore.RESET)
    time.sleep(0.75)
    player.place_bet()

    player.initial_hand()
    house.initial_hand()

    player.show_hand()
    house.show_first_hand()

    while player.calculate_score() <= 21:
        if check_blackjack(player, house):
            if not player.check_multiple_hands():
                break

        action_control = True

        while action_control:
            action_control = player.action()

        #print(f"el valor de action_control es {action_control}")
        print(f"El jugador tiene {len(player.hands)} manos.")
        time.sleep(0.75)

        #if (action_control == False) and (len(player.hands) >= 1) and (hand_number < len(player.hands)):
        if (action_control == False):
            if player.calculate_score() > 21:
                player.loses()
                house.show_hand()
                #print(f"El jugador tiene {len(player.hands)} manos.")
                if player.check_multiple_hands():
                    action_control == True
                    player.show_hand()

            else:
                house.play()
                if house.calculate_score() > 21 or house.calculate_score() < player.calculate_score():
                    player.wins()
                    #print(f"El jugador tiene {len(player.hands)} manos.")
                    if player.check_multiple_hands():
                        action_control == True
                        player.show_hand()
                    else:
                        break
                    #break
                elif house.calculate_score() > player.calculate_score():
                    player.loses()
                    #print(f"El jugador tiene {len(player.hands)} manos.")
                    if player.check_multiple_hands():
                        action_control == True
                        player.show_hand()
                    else:
                        break
                    #break
                elif house.calculate_score() == player.calculate_score():
                    player.push()
                    #print(f"El jugador tiene {len(player.hands)} manos.")
                    if player.check_multiple_hands():
                        action_control == True
                        player.show_hand()
                    else:
                        break
                    #break
        print(f"Control 2. La mano actual es: {player.hand}.")

def continue_playing(player):
    response = input("""
          Do you want to play another round?
          1. Yes.
          2. No.
          """ + Fore.BLUE)
    print(Fore.RESET)
    
    if response == "1":
        print("You have " + Back.BLACK + Fore.GREEN + f"{player.money} coins" + Style.RESET_ALL + ". Your current balance is: " +
              Back.BLACK + Fore.LIGHTBLUE_EX + f"{player.money - player.initial_money} coins" + Style.RESET_ALL + ".\n\n")
        time.sleep(0.75)

        return True
    
    elif response == "2":
        if player.initial_money > player.money:
            print("You've lost " + Back.BLACK + Fore.RED + f"{player.money - player.initial_money} coins" + Style.RESET_ALL + ".\n\n")
            time.sleep(0.75)
        else:
            print("You've won " + Back.BLACK + Fore.GREEN + f"{player.money - player.initial_money} coins" + Style.RESET_ALL + ".\n\n")
            time.sleep(0.75)

        return False
    
    else:
        print("Invalid option.\n")
        continue_playing(player)


def resumen(player):
    print("Your initial amount of money was " + Back.BLACK + Fore.LIGHTYELLOW_EX + f"{player.initial_money} coins" + Style.RESET_ALL +
          ".\nYour balance: " + Back.BLACK + Fore.LIGHTYELLOW_EX + f"{player.money - player.initial_money} coins" + Style.RESET_ALL +
          ".\nRounds played: " + Back.BLACK + Fore.LIGHTBLUE_EX + f"{player.rounds_won + player.rounds_lost + player.rounds_pushed} rounds" + Style.RESET_ALL +
          "\nRounds won: " + Back.BLACK + Fore.LIGHTBLUE_EX + f"{player.rounds_won} rounds" + Style.RESET_ALL +
          "\nRounds pushed: " + Back.BLACK + Fore.LIGHTBLUE_EX + f"{player.rounds_pushed} rounds" + Style.RESET_ALL +
          "\n\n" + Back.WHITE + Fore.BLACK + Style.BRIGHT + f"See ya {player.name}!!!" + Style.RESET_ALL + "\n")

def cerrar():
    print("Closing...")
    time.sleep(2)
    quit()


while True:
    main()