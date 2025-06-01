### List of clases: Deck, Card, Players, Player and House.

from colorama import Fore, Back, Style
import random, time

### Deck class ###

class Deck:
    def __init__(self):
        self.cards = self.build_deck()
    
    def __repr__(self):
        return f"Deck.cards{self.cards}"
    
    def __len__(self):
        return len(self.cards)

    def __getitem__(self, index):
        return self.cards[index]  # Makes deck[n] and random.choice work

    def build_deck(self):
        cards = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["J", "Q", "K", "A"]

        for i in range(10, 1, -1):
            ranks.insert(0, str(i))

        for suit in suits:
            for rank in ranks:
                cards.append(rank + "_" + suit)

        return cards * 6
    
    def draw_card(self):
        cut = random.randint(60,75)
        remaining_deck = len(self.cards)

        if remaining_deck > cut:
            pos = random.randint(0, remaining_deck - 1)
            return self.cards.pop(pos)
        else:
            self.cards = self.build_deck()
            print("\nSHUFFLING DECK.\n")
            time.sleep(0.75)
            self.draw_card()
    

### Card class ###

class Card:
    def __init__(self):
        pass

    def get_rank(self, card):
        dict = {
            "J" : 10,
            "Q" : 10,
            "K" : 10,
            "A" : [1, 11]
        }

        try:
            rank = int(card.split('_')[0])
        except ValueError:
            rank = dict[card.split('_')[0]]
            
        return rank
    

### Players class ###

class Players:
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.hand = []
        self.deck = Deck()
        self.card = Card()
        self.score = 0

    def __repr__(self):
        return f"Players.name{self.name}"
    
    def __int__(self):
        return self.score

    def initial_hand(self):
        self.hand = []

        card1 = self.deck.draw_card()
        card2 = self.deck.draw_card()

        rank_card1 = self.card.get_rank(card1)
        rank_card2 = self.card.get_rank(card2)

        self.hand = [card1, rank_card1, card2, rank_card2]

        return self.hand
    
    def draw(self):
        next_card = self.deck.draw_card()
        self.hand.append(next_card)

        rank_card = self.card.get_rank(next_card)
        self.hand.append(rank_card)

        return self.hand
    
    def show_hand(self):
        print(Back.BLACK + Fore.BLUE + f"{self.name}'s" + Style.RESET_ALL + f" hand is:\n" + Back.BLACK + Fore.MAGENTA + f"{self.hand[::2]}" + Style.RESET_ALL +
              ". It's score is " + Back.BLACK + Fore.MAGENTA + f"{self.calculate_score()}" + Style.RESET_ALL + ".")
        time.sleep(0.75)

    def blackjack(self):
        if ((len(self.hand) == 4) and (10 in self.hand) and ([1, 11] in self.hand)):
            return True
        else:
            return False

    def calculate_score(self):
        self.score = 0
        ranks = self.hand[1::2]

        # Sorting ranks: First numbers and last the Ace, which has two values in a list: [1, 11]
        ranks = sorted(ranks, key=lambda x: (0, x) if isinstance(x, int) else (1, x))

        for rank in ranks:
            if isinstance(rank, list):
                score1 = self.score + rank[0]
                score2 = self.score + rank[1]

                if score1 <= 21 and score2 <= 21:
                    self.score = max(score1, score2)
                else:
                    self.score = min(score1, score2)

            else:
                self.score +=  rank

        return self.score


### House class ###

class House(Players):
    def __init__(self):
        super().__init__("House")

    def show_first_hand(self):
        print(Back.BLACK + Fore.YELLOW + f"{self.name}'s" + Style.RESET_ALL + " hand is:\n" + Back.BLACK + Fore.LIGHTMAGENTA_EX + f"{self.hand[0]} and **hidden card**" + Style.RESET_ALL + ".\n")
        time.sleep(0.75)

    def show_hand(self):
        print(Back.BLACK + Fore.YELLOW + f"{self.name}'s" + Style.RESET_ALL + f" hand is:\n" + Back.BLACK + Fore.MAGENTA + f"{self.hand[::2]}" + Style.RESET_ALL +
              ". It's score is " + Back.BLACK + Fore.MAGENTA + f"{self.calculate_score()}" + Style.RESET_ALL + ".")
        time.sleep(0.75)

    def play(self):
        if self.calculate_score() > 17:
            self.show_hand()

        while self.calculate_score() < 17:
            self.draw()
            self.show_hand()


### Player class ###

class Player(Players):
    def __init__(self, name, money):
        super().__init__(name)
        self.initial_money = money
        self.money = money
        self.rounds_won = 0
        self.rounds_lost = 0
        self.rounds_pushed = 0
        self.bet = 0
        self.hands = []

    def __int__(self):
        return self.money

    def place_bet(self):
        self.bet = int(input("How much money you want to bet?\n" + Fore.CYAN))
        
        if self.money >= self.bet:
            self.money -= self.bet
            print(Fore.RESET + "Remaining coins: " + Back.BLACK + Fore.GREEN + f"{self.money}" + Style.RESET_ALL)
            time.sleep(0.75)
            #return self.bet
        else:
            print(Fore.RED + "Insuficient coins.\n" + Fore.RESET)
            time.sleep(0.75)
            self.bet(self.money)

    def reset_hand(self):
        self.hands = []

    def hit(self, hand):
        self.hand = hand
        self.draw()
        self.show_hand()
    
    def double(self, hand):
        self.hand = hand
        self.money -= self.bet
        self.bet += self.bet
        print("You've doubled your bet: " + Fore.BLUE + f"{self.bet}" + Fore.RESET + ". Remaining coins: " + Fore.GREEN + f"{self.money}" + Fore.RESET)
        time.sleep(0.75)
        self.draw()
        
        return False

    def split(self):
        self.money -= self.bet
        hands_to_split = []
        new_hands = []
        
        # First identify all splittable hands
        for hand in self.hands:
            if len(hand) >= 4 and hand[1] == hand[3]:  # Check if splittable
                hands_to_split.append(hand)
            else:
                new_hands.append(hand)  # Keep non-splittable hands
        
        # Split the identified hands
        for hand in hands_to_split:
            new_hands.append([hand[0], hand[1]])  # First card as new hand
            new_hands.append([hand[2], hand[3]])  # Second card as new hand
        
        # Update the hands
        self.hands = new_hands
        if self.hands:  # Ensure we have hands
            self.hand = self.hands[0]  # Focus on first hand
        
        print("The hand has been split. Total of hands: " + Fore.BLUE + f"{len(self.hands)}" + Fore.RESET)
        time.sleep(0.75)

    def action(self):
        if len(self.hands) == 0:
            self.hands.append(self.hand)

        option1 = "1. Hit"
        option2 = "2. Stand"
        option3 = "3. Double"
        option4 = "4. Split"

        for hand in self.hands:
            #print(len(hand))
            if len(hand) == 2:
                self.hit(hand)

            if len(hand) == 4 and (hand[1] == hand[3]):
                selection = input("What would you like to do?\n" + Style.BRIGHT +
                                  f"{option1}\n" + 
                                  f"{option2}\n" + 
                                  f"{option3}\n" + 
                                  f"{option4}\n" + Style.RESET_ALL + Fore.BLUE)
                print(Style.RESET_ALL)
            
            elif len(hand) == 4 and (hand[1] != hand[3]):
                selection = input("What would you like to do?\n" + Style.BRIGHT +
                                  f"{option1}\n" + 
                                  f"{option2}\n" + 
                                  f"{option3}\n" + Style.RESET_ALL + Fore.BLUE)
                print(Style.RESET_ALL)

            else:
                selection = input("What would you like to do?\n" + Style.BRIGHT +
                                  f"{option1}\n" + 
                                  f"{option2}\n" + Style.RESET_ALL + Fore.BLUE)
                print(Style.RESET_ALL)
                
            if selection == "1":
                self.hit(hand)
                if self.calculate_score() >= 21:
                    return False
                else:
                    return True
            elif selection == "2":
                return False
            elif selection == "3":
                self.double(hand)
                self.show_hand()
                return False
            elif selection == "4":
                self.split()
                self.show_hand()
                return True
            
    def check_multiple_hands(self):
        if len(self.hands) > 1:
            hand_index = self.hands.index(self.hand)
            try:
                self.hand = self.hands[hand_index + 1]
                self.hands.pop(hand_index)
                return True
            except IndexError:
                return False
        else:
            return False

    def wins(self):
        self.money += self.bet * 2
        self.rounds_won += 1
        
        if len(self.hands) == 1:
            self.reset_hand()
        
        print(f"\nCongrats {self.name}! You've won " + Back.BLACK + Fore.GREEN + f"{self.bet} coins" + Style.RESET_ALL +
              ". You have " + Back.BLACK + Fore.GREEN + f"{self.money} coins" + Style.RESET_ALL + ".")
        time.sleep(0.75)

    def loses(self):
        self.rounds_lost += 1
        
        if len(self.hands) == 1:
            self.reset_hand()
        
        print(f"\nBad luck {self.name}. You've lost " + Back.BLACK + Fore.RED + f"{self.bet} coins" + Style.RESET_ALL +
              ". You have " + Back.BLACK + Fore.GREEN + f"{self.money} coins" + Style.RESET_ALL + ".")
        time.sleep(0.75)

    def push(self):
        self.money += self.bet
        self.rounds_pushed += 1
        
        if len(self.hands) == 1:
            self.reset_hand()
        
        print(f"\nWow {self.name}! This is a tie. You've recovered " + Back.BLACK + Fore.GREEN + f"{self.bet} coins" + Style.RESET_ALL +
              ". You have " + Back.BLACK + Fore.GREEN + f"{self.money} coins" + Style.RESET_ALL + ".")
        time.sleep(0.75)