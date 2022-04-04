import hashlib
import random
import sys
import time

import bountyLib
import main
import user

bcolors = bountyLib.bcolors

faces = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "X", "J", "Q", "K"]
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def generateRandomCard():
    color = random.randint(0, 4)
    value = random.randint(0, 12)
    # 1 = Ass (1 oder 11)
    # 2 = 2
    # ...
    # 10 = 10
    # 11 = Joker
    # 12 = Queen
    # 13 = King
    card = {"value": value, "color": color}
    return card


def getDeckSum(deck, hideLast=False):
    sumval = 0
    hiding = -99
    if hideLast:
        hiding = len(deck) - 1

    for x in range(0, len(deck)):

        val = values[deck[x]["value"]]

        if x == hiding:
            val = 0

        sumval += val

    return sumval


def getBlackjackColor(card):
    code = card["color"]
    if code % 2 == 0:
        return bcolors.blackjack_red
    else:
        return bcolors.blackjack_black


def drawDeck(deck, hideLast=False):
    out = ""

    prefix = " "
    suffix = " "

    hiding = -99

    if hideLast:
        hiding = len(deck) - 1

    for x in range(0, len(deck)):
        value = faces[deck[x]["value"]]
        color = getBlackjackColor(deck[x])

        if x == hiding:
            value = "?"
        out += color + prefix + value + suffix + bcolors.endc + " "

    return out


def play(amount):
    print("")
    print("")
    print("")

    hashed_random_seed = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()
    random.seed(hashed_random_seed)

    running = True
    first = True
    stand = False
    finished = False
    line_remove_multiplier = 3

    player = []
    dealer = []

    dealer.append(generateRandomCard())
    dealer.append(generateRandomCard())

    player.append(generateRandomCard())

    while running:

        if finished:
            running = False
            result = "You: " + str(getDeckSum(player)) + " vs Dealer: " + str(getDeckSum(dealer))

            player_sum = getDeckSum(player)
            dealer_sum = getDeckSum(dealer)

            game = {}
            game["payout"] = 0
            game["result"] = bcolors.orange + "tied" + bcolors.endc
            game["return"] = bcolors.lightgreen + "+" + str(game["payout"] * amount) + bcolors.endc

            if player_sum > 21 and dealer_sum > 21:  # both busted
                game["payout"] = 0
                game["result"] = bcolors.orange + "tied on 21" + bcolors.endc
                game["return"] = bcolors.orange + "+" + str(game["payout"] * amount) + bcolors.endc
            elif player_sum > 21:  # only player busted
                game["payout"] = -1
                game["result"] = bcolors.red + "lost by bust!" + bcolors.endc
                game["return"] = bcolors.red + "" + str(game["payout"] * amount) + bcolors.endc
            elif dealer_sum > 21:  # only dealer busted
                game["payout"] = 1
                game["result"] = bcolors.lightgreen + "win by bust!" + bcolors.endc
                game["return"] = bcolors.lightgreen + "+" + str(game["payout"] * amount) + bcolors.endc
            elif player_sum == dealer_sum:  # both tied
                game["payout"] = 0
                game["result"] = bcolors.orange + "tied!" + bcolors.endc
                game["return"] = bcolors.orange + "+" + str(game["payout"] * amount) + bcolors.endc
            elif player_sum > dealer_sum:  # player wins by better hand
                game["payout"] = 1
                game["result"] = bcolors.lightgreen + "win by a better hand!" + bcolors.endc
                game["return"] = bcolors.lightgreen + "+" + str(game["payout"] * amount) + bcolors.endc
            elif dealer_sum > player_sum:  # player loses by worse hand
                game["payout"] = -1
                game["result"] = bcolors.red + "lose by a worse hand!" + bcolors.endc
                game["return"] = bcolors.red + "" + str(game["payout"] * amount) + bcolors.endc

            user.balance += amount * game["payout"]

            # **** clearing the last 2 lines
            n_lines = 2
            if len(dealer) == 2:
                n_lines += 1

            sys.stdout.write(("\033[F" + "\r" + " " * 90 + "\r") * n_lines)

            d = "Dealer (" + str(getDeckSum(dealer)) + "): " + drawDeck(dealer)
            p = "Player (" + str(getDeckSum(player)) + "): " + drawDeck(player)

            print(d)
            print(p)

            main.log("You " + game["result"] + " Outcome: " + game["return"] + " " * 30)
            main.log("Your new Balance is: " + bcolors.orange + str(user.balance) + " " * 30)


        else:
            if getDeckSum(dealer) <= 16 and stand:
                dealer.append(generateRandomCard())

            if not stand:
                player.append(generateRandomCard())

            d = "Dealer (" + str(getDeckSum(dealer, first)) + "): " + drawDeck(dealer, first)
            p = "Player (" + str(getDeckSum(player)) + "): " + drawDeck(player)

            sys.stdout.write("\033[F" * line_remove_multiplier + d + "\n" + p + "\n")

            # check for instant bust
            if getDeckSum(dealer) > 21 or getDeckSum(player) > 21:
                finished = True
            else:
                if not stand:
                    uInput = input("\033[K" + "Draw another Card? [hit/stand]: ")
                else:
                    time.sleep(0.3)
                    line_remove_multiplier = 2

                if uInput.lower() == "stand":
                    stand = True
                    first = False

                if stand and getDeckSum(dealer) > 16 and not first:
                    finished = True


def query(cmd):
    cmd.pop(0)  # Removes first Element because first element is "blackjack"
    if len(cmd) == 0:
        main.log(
            bcolors.red + "Usage: blackjack (command)                   " + bcolors.endc + " | type 'help' for help")
        return

    if cmd[0] == "bet":
        if len(cmd) == 2:
            amount = int(cmd[1])
            if user.verifyTransaction(amount):
                play(amount)
            else:
                main.log(bcolors.red + "Invalid betting amount (negativ or insufficient balance).")
        else:
            main.log(bcolors.red + "Usage: blackjack bet (amount)")
