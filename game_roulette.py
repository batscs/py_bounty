import hashlib
import sys
import time

import bountyLib
import main
import random

import user

bcolors = bountyLib.bcolors

def getBetOutcomes():
    bet = {}

    bet["black"] = [[2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35], 1]
    bet["red"] = [[1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36], 1]
    bet["green"] = [[0, 37], 14]  # payout not taken into account, yet!

    bet["even"] = [[2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36], 1]
    bet["odd"] = [[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35], 1]

    bet["high"] = [[19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36], 1]
    bet["low"] = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 1]
    return bet


def hasWon(bet, result):
    bets = getBetOutcomes()
    # bets[bet][0] = möglichkeiten
    # bets[bet][1] = payout multiplier
    if result in bets[bet][0]:
        return True

    return False


def calcPayout(amount, bet, result):
    bets = getBetOutcomes()
    if hasWon(bet, result):
        return amount * bets[bet][1]
    else:
        return amount * -1


def getRouletteColor(number):
    black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    green = [0, 37]

    str_number = str(number)
    if 10 > number > 0:
        str_number = "0" + str_number
    elif number == 37:
        str_number = "00"
    str_number = " " + str_number + " "

    if number in black:
        return bcolors.roulette_black + str_number + bcolors.endc
    elif number in red:
        return bcolors.roulette_red + str_number + bcolors.endc
    else:
        return bcolors.roulette_green + str_number + bcolors.endc


def deckToString(deck, final):
    msgDeck = bcolors.endc + ""

    spacer = ""

    # draw deck
    for i in range(0, len(deck)):
        field = getRouletteColor(deck[i])
        if i == final:
            field = ">" + field + "<"
        msgDeck = msgDeck + field + spacer

    return msgDeck


def rollDeck(deck):
    deck.pop(0)
    deck.append(random.randint(0, 36))
    return deck


def play(amount, bet):
    # configuration
    hashed_random_seed = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()
    random.seed(hashed_random_seed)
    rollDuration = random.randint(80, 90)
    size = 23
    final = int(size / 2)
    deck = [None] * size
    result = -1

    # set deck starting position
    for i in range(0, size):
        deck[i] = random.randint(0, 36)

    # rolling animation of deck
    for x in range(0, rollDuration):
        deck = rollDeck(deck)
        msgDeck = deckToString(deck, final)
        sys.stdout.write('\r' + msgDeck)
        old_ms = (pow(x, 2.3) / rollDuration) * 0.001
        ms = (0.06 * (x*x)) * 0.001
        time.sleep(ms)
        result = deck[final]

    print("")

    cashback = calcPayout(amount, bet, result)
    user.balance += cashback
    if hasWon(bet, result):
        main.log("The ball landed on " + getRouletteColor(result) + " and you " + bcolors.lightgreen + "won " + str(
            cashback) + bcolors.endc + "!")
        main.log("Your new Balance is: " + bcolors.orange + str(user.balance))
    else:
        main.log("The ball landed on " + getRouletteColor(result) + " and you " + bcolors.red + "lost " + str(
            cashback) + bcolors.endc + "!")
        main.log("Your new Balance is: " + bcolors.orange + str(user.balance))


def query(cmd):
    cmd.pop(0)  # Removes first Element because first element is "roulette"
    if len(cmd) == 0:
        main.log(
            bcolors.red + "Usage: roulette <command>                   " + bcolors.endc + " | type 'help' for help")
        return
    if cmd[0] == "bet":
        if len(cmd) != 3:  # bet <amount> <bet>
            main.log(bcolors.red + "Usage: bet (amount) (bet)")
        else:
            amount = int(cmd[1])
            bet = cmd[2]

            if not user.verifyTransaction(amount):
                main.log(bcolors.red + "You don't have enough Balance to make this bet!")
                return

            play(amount, bet)
