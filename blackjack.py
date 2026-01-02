import random
from os import system
from time import sleep

def card_initialization():
    list_of_cards_available = [
        "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"
    ]


    list_flush = [
        "♥", "♦", "♣", "♠"
    ]

    list_cards = []
    for i in list_of_cards_available:
        for j in list_flush:
            list_cards.append(f"{i} {j}")
    
    return list_cards

def give_card(deck, nb):
    value = [0,0]
    set = []
    for i in range(nb):
        card = deck[random.randint(0,len(deck)-1)]
        deck.remove(card)

        set.append(card)

    value = compute_score(set, value)
    return set, value, deck

def add_card(set, deck, value):
    card = deck[random.randint(0,len(deck)-1)]
    set.append(card)
    deck.remove(card)
    value[0] += card_value[card.split(" ")[0]]
    value[1] += card_value[card.split(" ")[0]]
    return set, deck, value

def compute_score(set, value=[0,0]):
    for card in set:
        if card[0] == "A":
            value[0] += 11
            value[1] += 1
        else:
            value[0] += card_value[card.split(" ")[0]]
            value[1] += card_value[card.split(" ")[0]]

    return value

if __name__ == "__main__":
    system("clear||cls")
    card_value = {
        "2":2, "3":3, "4":4, "5":5,
        "6":6, "7":7, "8":8, "9":9, "10":10,
        "J":10, "Q":10, "K":10, "A":11
    }
    value_player, value_dealer = [0,0], [0,0]
    over = False
        
    deck = card_initialization()

    # Bet your money
    money_bet = int(input("How much money you want to bet? ($) : "))

    # Card distribution
    card_player, value_player, deck = give_card(deck, 2)
    card_dealer, value_dealer, deck = give_card(deck, 1)

    print("Here is the card of the dealer", card_dealer)
    print(
        f"Dealer's value : {value_dealer[0]} | {value_dealer[1]}" if value_dealer[0] != value_dealer[1] else
        f"Dealer's value : {value_dealer[0]}")
    
    print("=====================================")

    print("Here are your cards :", card_player)
    
    print(
        f"Your value : {value_player[0]} | {value_player[1]}" if value_player[0] != value_player[1] else
        f"Your value : {value_player[0]}")
    
    if value_player[0] == 21 or value_player[1] == 21:
        print(f"BLACKJACK ! +{3*money_bet}.")
        over = True


    check = False
    # Player turn
    while not check and not over:
        decision = input("Do you want to Hit (H) or Stand (S)?")
        system("clear||cls")
        if decision == "H":
            card_player, deck, value_player = add_card(card_player, deck, value_player)

            print("Here is the card of the dealer", card_dealer)

            print(
                f"Dealer's value : {value_dealer[0]} | {value_dealer[1]}" if value_dealer[0] != value_dealer[1] else
                f"Dealer's value : {value_dealer[0]}")
            
            print("=====================================")

            print("Here are your cards :", card_player)
            
            print(
                f"Your value : {value_player[0]} | {value_player[1]}" if value_player[0] != value_player[1] else
                f"Your value : {value_player[0]}")

            if value_player[0] > 21 or value_player[1] > 21:
                print(f"You lost. -{money_bet}$.")
                over = True
                break

        elif decision == "S":
            check = True
        else:
            continue
    
    # Dealer's turn
    while value_dealer[0] < 17 and value_dealer[1] < 17 and not over:
        system("clear||cls")
        print("The dealer hits...")

        card_dealer, deck, value_dealer = add_card(card_dealer, deck, value_dealer)
        print("Here is the dealer's cards : ", card_dealer)

        print(
            f"Dealer's value : {value_dealer[0]} | {value_dealer[1]}" if value_dealer[0] != value_dealer[1] else
            f"Dealer's value : {value_dealer[0]}")
        
        print("=====================================")

        print("Here are your cards :", card_player)
        
        print(
            f"Your value : {value_player[0]} | {value_player[1]}" if value_player[0] != value_player[1] else
            f"Your value : {value_player[0]}")
        
        if value_dealer[0] > 21 or value_dealer[1] > 21:
                print(f"Bust. +{money_bet*2}$")
                over = True
                break
        
        sleep(3)
    
    if not over:
        if value_player > value_dealer:
            print(f"You win ! +{2*money_bet}.")
        elif value_player < value_dealer:
            print(f"You lost. -{money_bet}$")
        else:
            print("Draw! +0$")