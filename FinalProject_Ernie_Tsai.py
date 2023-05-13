import os
import random
from itertools import combinations
import argparse
import sys
import math

class Card:  # Custom Card class record each card
    def __init__(self, suits, value):
        self.suits = suits
        self.value = value

    def __repr__(self):
        return "{}{}".format(self.suits,self.value)


class Deck:

    def __init__(self):
        self.deck = []  # Create list to store deck
        self.gen_deck()
        self.rand_draw()

    def gen_deck(self):  # Create a deck with 52 cards
        for i in ["S", "C", "H", "D"]:
            for v in range(1, 14):
                self.deck.append(str(Card(i, v)))
        return self.deck

    def rand_draw(self):  # Method that randomly draws a card and remove it from the deck
        rand = random.choice(self.deck)  # "S3"
        self.deck.remove(rand)
        return rand


class Player:  # Associate id with corresponding hand
    def __init__(self, player_id):  # {1:[c9,d7],2:[]}
        self.player_id = player_id
        self.player_money = 100
        self.player_card = []  # [c8,d7]
        self.player_dict = {}  # {1:[c9,d7],2:[]}
        self.player_bet = 0
        self.save_card()
        self.hand()

    def save_card(self):  # [[c8,d7],[H2,d2],[s2,d2]]
        for i in range(2):
            self.player_card.append(Deck().rand_draw())
        return self.player_card

    def hand(self):  # {1:[c9,d7],2:[c1,d4]}
        self.player_dict[self.player_id] = self.player_card
        return self.player_dict


def high_val(pCards):
    return max(save_values(pCards))  # Return the highest value in the sorted list


# Make hand to only numbers,eliminate letter
def save_values(pCards):
    suit_lst = []  # Create an empty list
    for card in range(len(pCards)):  # Loop list 5 times from index 2
        if len(str(pCards[card])) == 3:  # If length of card = 3 ("C18")
            suit_lst.append(int(str(pCards[card])[-2:]))  # Append to the empty list ("18")
        else:
            suit_lst.append(int(str(pCards[card])[1]))  # Append to the empty list ("1")
    return sorted(suit_lst)


# Full House
def full_House(pCards):
    if pairs(pCards) and three_of_kind(pCards):  # if pairs and three of kind are true
        return True
    return False


# Pairs
def pairs(pCards):
    for i in save_values(pCards):  # Loop through sorted hand
        if save_values(pCards).count(i) == 2:  # If a card appear twice return True
            return True
    return False


# Two Pair
def two_pairs(pCards):
    num_pairs = 0  # Set number of pairs to 0
    for i in save_values(pCards):  # Loop through sorted hand
        if save_values(pCards).count(i) == 2:  # If a card appear twice
            num_pairs += 1  # Number of pairs + 1
    if num_pairs == 4:  # Return true if number of pairs reaches 4
        return True
    return False


# Three of kind
def three_of_kind(pCards):
    for i in save_values(pCards):  # Loop through sorted hand
        kind = save_values(pCards).count(i)
        if kind == 3:  # If a card appear three times return true
            return True
        else:
            continue
    return False


# Four of a kind
def four_of_kind(pCards):
    x = save_values(pCards)
    tmp_value = max(set(x), key=x.count)  # Find the value that appear most time in sorted list
    count = 0
    for i in x:  # Loop throught the sorted hand
        if i == tmp_value:  # If the element = the most appeared element
            count += 1  # Count +1
    if count == 4:  # If count is 4 return true
        return True
    else:
        return False


# Flush
def flush(pCards):
    global suit
    for i in pCards:
        i = str(i)
        suit = i[0]

    count = 0
    for card in pCards:  # Check suit for Royal Flush
        for letter in str(card):
            if letter[0] == suit:  # If the card = suit
                count = count + 1  # Count+1
            if count == 5 and save_values(pCards) != [1, 10, 11, 12,
                                                      13]:  # If count is 5 and not equal value of royal flush
                return True
    return False


# Straight Flush
def straight_Flush(pCards):
    if flush(pCards) == True and (straight(pCards) == True) and (
            royal_Flush(pCards) == False):  # If flush and straight is True and Royal flush is false
        return True
    return False


# Straight
def straight(pCards):
    lst = [save_values(pCards)[i + 1] - save_values(pCards)[i] for i in
           range(len(save_values(pCards)) - 1)]  # Find the difference between elements and save in list
    for i in lst:  # Loop over the list
        if i != 1:  # if list isn't 1 return False
            return False
    if (int(save_values(pCards)[-1]) - int(save_values(pCards)[0]) == 4) and save_values(pCards)[
        0] != 1:  # If difference between first and element is 4 and first element isn't 1 return True
        return True


# Royal Flush
def royal_Flush(pCards):
    global suit
    for i in pCards:
        i = str(i)
        suit = i[0]
    count = 0
    for card in pCards:  # Check suit for Royal Flush
        for letter in str(card):
            if letter[0] == suit:  # If the card = suit
                count = count + 1  # Count+1
    if count == 5 and save_values(pCards) == [1, 10, 11, 12,
                                              13]:  # If count is 5 and equal value of royal flush return True
        return True
    return False


def most_common(lst):  # [2, 1, 3, 3, 9] returns int 3
    return max(set(lst), key=lst.count)


def determine_rank(lst):  # Determine rank of the hand
    rank = 0
    if royal_Flush(lst) == True:
        rank += 10
    elif straight_Flush(lst) == True:
        rank += 9
    elif four_of_kind(lst) == True:
        rank += 8
    elif full_House(lst) == True:
        rank += 7
    elif flush(lst) == True:
        rank += 6
    elif straight(lst) == True:
        rank += 5
    elif three_of_kind(lst) == True:
        rank += 4
    elif two_pairs(lst) == True:
        rank += 3
    elif pairs(lst) == True:
        rank += 2
    else:
        rank += 1
    return rank


# calculate the maximum most appeared value
def most_freq(lst):
    count = 0
    num = save_values(lst)[0]
    lst = save_values(lst)
    for i in lst:
        tmp = lst.count(i)
        if (tmp > count):
            count = tmp
            num = i
        elif tmp == count:
            if i > num:
                count = tmp
                num = i

    return num

def determine_prob(card):
    #Probability for each hand with deck of 52 cards
    # Number of possible card divide by number of all possible card combination
    prob_for_poss_hand = (math.factorial(52)/math.factorial(52-5))/math.factorial(5) #(2598960)
    prob_for_hand = 0
    if determine_rank(card) == 10: #Probability to get royal flush
        prob_for_hand = 4/prob_for_poss_hand
    elif determine_rank(card) == 9: #Probability to get straight flush
        prob_for_hand = 36/prob_for_poss_hand
    elif determine_rank(card) == 8: #Probability to get four of a kind
        prob_for_hand = 624/prob_for_poss_hand
    elif determine_rank(card) == 7: #Probability to get full house
        prob_for_hand = 3744/prob_for_poss_hand
    elif determine_rank(card) == 6: #Probability to get flush
        prob_for_hand = 5108/prob_for_poss_hand
    elif determine_rank(card) == 5: #Probability to get straight
        prob_for_hand = 10200/prob_for_poss_hand
    elif determine_rank(card) == 4: #Probability to get three of a kind
        prob_for_hand = 54912/prob_for_poss_hand
    elif determine_rank(card) == 3: #Probability to get two pair
        prob_for_hand = 123552/prob_for_poss_hand
    elif determine_rank(card) == 2: #Probability to get a pair
        prob_for_hand = 1098240/prob_for_poss_hand
    elif determine_rank(card) == 1: #Probability to get single high card
        prob_for_hand = 1302540/prob_for_poss_hand
    return prob_for_hand

def round_off_rating(number):
    return round(number * 2) / 2

# Run the Game
def player_game(num_player):
    if num_player <= 1:
        return print("Invalid Input")
    track_money = {}  # dictionary that keep tracks of money for each player
    for m in range(0, num_player):
        b = Player(m)
        track_money[m] = b.player_money

    play_decision = True
    player_dict = {}  # dictionary that keep tracks of hands for each player
    while play_decision:
        d = Deck()
        total_bet = 0
        first_bet = 0
        second_bet = 0
        third_bet = 0
        your_decision1 = ""

        # Initalize Game
        community_card1 = [d.rand_draw() for i in range(3)]  # Create 3 random community cards
        print("Initialization Game")
        for k in range(0, num_player):
            player_hand = Player(k)
            round1_lst = []
            hand = player_hand.player_card
            round1_lst.append(hand)
            round1_lst.append(community_card1)
            concat_list = [j for i in round1_lst for j in i]  # List of card containing 3 community cards and 2 hand card
            player_dict[k] = concat_list  # Dictionary that contain player id assosciate with concat_lst
        print("Player 0's card (You):", player_dict[1][0:2])  # Set Player 1 as you
        decision1 = True
        while decision1:
            your_decision1 = input("Enter your action(f:fold, b:bet,c:check):")  # Enter your decision for first round
            if your_decision1 == "f":  # If fold, bet 0 and
                del player_dict[0]
                decision1 = False
                f = True
            elif your_decision1 == "b":  # If bet, Enter valid amount
                while True:
                    first_bet = float(input("Enter the amount you want to bet:"))
                    if first_bet > track_money[0]:
                        print("You don't have enough money. Please enter again")
                    else:
                        break
                track_money[0] -= first_bet  # Subtract from your money
                total_bet += first_bet  # Add the amount of bet to the pot
                decision1 = False
            elif your_decision1 == "c":  # If check bet 0 , do nothing
                decision1 = False
            else:
                decision1 = True
                print("Invalid Input")

        print("Community Cards:", community_card1)  # 3 Community Cards are displayed
        print("Round:", 1)

        # Round 1 (Determine Bet)
        probability_dict = {} #Dictionary that store the player ID and the probability of the hand
        rank_dict = {} #Dictionary that store player ID and Rank of hand
        bet_dict = {}
        round_dict = {} #Dictionary that store player ID and the final decision bet of player
        for x, y in player_dict.items():
            rank_dict[x] = determine_rank(y)
            probability_dict[x] = determine_prob(y)
            bet_dict[x] = abs(math.log(determine_prob(y)))
            round_dict[x] = round_off_rating(abs(math.log(determine_prob(y))))
            #player_amount = Player(x)
            if x == 0:
                print("You bet: ${}".format(first_bet))
            elif x != 0:  # If not the first player (You), print the rest of player's bet and amount
                print("Bot player {}'s action: bet ${}".format(x, round_dict[x] ))
                track_money[x] -= round_dict[x]  # Subtract from player's moneyf
                total_bet += round_dict[x]  # Add the amount of bet to the pot

        decision2 = True
        fold = True
        while decision2 and your_decision1 != "f":  # Only ask for input if didn't fold in round 1
            your_decision2 = input("Enter your action(f:fold, b:bet):")  # Input Decision
            if your_decision2 == "f":
                del player_dict[0]
                decision2 = False
                fold = False
            elif your_decision2 == "b":
                while True:
                    second_bet = float(input("Enter the amount you want to bet:"))  # Input Amount
                    if second_bet > track_money[0]:
                        print("You don't have enough money. Please enter again")
                    else:
                        break
                track_money[0] -= second_bet
                total_bet += second_bet
                decision2 = False
            else:
                decision2 = True
                print("Invalid Input")
        # Round 2 :
        community_card2 = [d.rand_draw() for i in range(2)]  # Create 2 random community cards
        print("Community Cards:", community_card1 + community_card2)

        for k, v in player_dict.items():  # Add community card to associate player id
            player_dict[k] += community_card2  # Total of 7 cards for each player
        dic1 = {}  # Store player id and rank
        dic2 = {}  # Store player id and hand

        for key, value in player_dict.items():  # Compare the rank between each combination out of the 7 cards
            highest_rank = 0
            tmp_max = 0
            tmp = 0
            hands = ""  # Use for update default
            for cards in combinations(value, 5):
                r = determine_rank(list(cards))
                max_val = most_freq(list(cards))  # highest val and most appeared value in the list
                if r > highest_rank:  # if rank of hand is greater than previous hand
                    hands = cards  # update best hand
                    highest_rank = r  # update highest rank
                elif r == highest_rank:  # if rank of hand is equal to the previous hand
                    if r == 6:  # if players tie with Flush (rank 6)
                        if high_val(cards) > tmp_max:  # Compare the highest value of the hand and update
                            tmp_max = high_val(cards)  #
                            highest_rank = r
                            hands = cards

                    elif r == 5:  # if players tie with 5 Straight (rank 5)
                        if high_val(cards) > tmp_max:
                            tmp_max = high_val(cards)
                            highest_rank = r
                            hands = cards

                    elif r == 4:  # if players tie with Three of a kind (rank 4)
                        if max_val > tmp:
                            tmp = max_val
                            highest_rank = r
                            hands = cards

                    elif r == 3:  # if players tie with Two pairs(rank 3)
                        if max_val > tmp:
                            tmp = max_val
                            highest_rank = r
                            hands = cards
                    elif r == 2:  # if players tie with Pairs(rank 2)
                        if max_val > tmp:
                            tmp = max_val
                            highest_rank = r
                            hands = cards

                    elif r == 1:  # if players tie with Four of a Highcard(rank 1)
                        if high_val(cards) > tmp_max:
                            tmp_max = high_val(cards)
                            highest_rank = r
                            hands = cards

            dic1[key] = highest_rank  # Dictionary that saves id:rank
            dic2[key] = hands  # Dictionary that saves id:player hand

        tmp = 0
        tmp_r = list(dic1.values())[0]
        winner = ''
        tmp_max2 = 0
        highest_rank2 = 0
        tmp2 = 0
        for x, y in dic1.items():
            card = dic2[x]
            max_val2 = most_freq(list(card))
            if y > tmp_r:
                tmp_r = y
                winner = str(x)
            elif y == tmp_r:
                if y == 6:  # if players tie with Flush (rank 6)
                    if high_val(card) > tmp_max2:  # Compare the highest value of the hand and update
                        tmp_max2 = high_val(card)  #
                        highest_rank = y
                        winner = str(x)
                    elif high_val(card) == tmp_max2:
                        winner += str(x)

                elif y == 5:  # if players tie with 5 Straight (rank 5)
                    if high_val(card) > tmp_max2:
                        tmp_max2 = high_val(card)
                        highest_rank2 = y
                        winner = str(x)
                    elif high_val(card) == tmp_max2:
                        winner += str(x)

                elif y == 4:  # if players tie with Three of a kind (rank 4)
                    if max_val2 > tmp2:
                        tmp2 = max_val2
                        highest_rank2 = y
                        winner = str(x)
                    elif max_val2 == tmp2:
                        winner += str(x)

                elif y == 3:  # if players tie with Two pairs(rank 3)
                    if max_val2 > tmp:
                        tmp2 = max_val2
                        highest_rank2 = y
                        winner = str(x)
                    elif max_val2 == tmp2:
                        winner += str(x)

                elif y == 2:  # if players tie with Pairs(rank 2)
                    if max_val2 > tmp:
                        tmp2 = max_val2
                        highest_rank2 = y
                        winner = str(x)
                    elif max_val2 == tmp2:
                        winner += str(x)

                elif y == 1:  # if players tie with Four of a Highcard(rank 1)
                    if high_val(card) > tmp_max2:
                        tmp_max2 = high_val(card)
                        highest_rank2 = y
                        winner = str(x)
                    elif high_val(card) == tmp_max2:
                        winner += str(x)
                else:
                    winner += str(x)
        round_dict2 = {} #Dictioanry that store player ID and final deicision bet of player
        rank_dict2 = {} #Dictionary that store player ID and Rank of hand
        bet_dict2 = {}
        probability_dict2 = {}  #Dictionary that store player ID and probability of getting each hand
        for x,y in dic2.items():
            rank_dict2[x] = determine_rank(y)
            probability_dict2[x] = determine_prob(y)
            bet_dict2[x] = abs(math.log(determine_prob(y)))
            round_dict2[x] = round_off_rating(abs(math.log(determine_prob(y))))
            if x == 0:
                print("You bet: ${}".format(second_bet))
            if x != 0:
                if round_dict[x] >= 2 and 2 in round_dict.values():
                    print("Bot player {}'s action: bet ${}".format(x, 2*round_dict[x] + round_dict2[x]))
                    track_money[x] -= 2*round_dict[x] + round_dict2[x]# Subtract from player's money
                    total_bet += 2*round_dict[x] + round_dict2[x]
                else:
                    print("Bot player {}'s action: bet ${}".format(x, min(round_dict.values()) + round_dict2[x]))
                    track_money[x] -= min(round_dict.values()) +  round_dict2[x] # Subtract from player's money
                    total_bet += 2 * min(round_dict.values()) + round_dict2[x]

        decision3 = True
        while decision3 and your_decision1 != "f" and fold != False:  # Only ask for input if didn't fold in round 1 and 2
            your_decision3 = input("Enter your action(f:fold, b:bet):")  # Input Decision
            if your_decision3 == "f":
                del player_dict[0]
                decision3 = False
            elif your_decision3 == "b":
                while True:
                    third_bet = float(input("Enter the amount you want to bet:"))  # Input Amount
                    if third_bet > track_money[0]:
                        print("You don't have enough money. Please enter again")
                    else:
                        break
                track_money[0] -= third_bet  # Subtract from your money
                total_bet += third_bet  # Add the amount of bet to the pot
                decision3 = False
            else:
                decision3 = True
                print("Invalid Input")

        winner_lst = [winner[i:i + 1] for i in range(0, len(winner), 1)]  # Create a list for winners
        winner = ",".join(map(str, winner))  # Join the element in the list with comma
        for x, y in dic1.items():  # Add up/ split the total amount for the winners
            for w in winner_lst:
                w = int(w)
                if len(winner_lst) > 1:
                    if w == x:
                        track_money[w] += total_bet / len(winner_lst)
                elif len(winner_lst) == 1:
                    if w == x:
                        track_money[w] += total_bet

        print("Results")
        print("Winner:Player", winner)

        for player_id, final_amount in track_money.items():  # Check for final amount of money for each player
            print("Player", player_id, ":$", final_amount)

        for player_id, final_amount in track_money.items():  # Check for final amount of money for each player
            if player_id == 0 and final_amount <= 0:  # If player 0(you) doesn't have enough money, quit the game
                exit()
            elif final_amount == 0:  # If bot players doesnt have enought money remove them from the game
                del player_dict[player_id]

        play_again = input("Do you want to play again?(yes,no)")  # Ask if play again or not
        play_again = play_again.lower()  # Compare lower and upper case input
        if play_again == "yes":
            play_decision = True
        elif play_again == "no":
            play_decision = False
            break
        else:
            print("Invalid Input")
        print()


# Take in command line
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action='store_true')
    parser.add_argument('-p', type=int)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    mode = main()
    if mode.u is True and type(mode.p) == int:
        print("user mode")
        player_game(mode.p)
    else:
        print("Invalid Input")


