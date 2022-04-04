# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import platform
import sys
import os
import time

import bountyLib
import game_blackjack
import game_roulette
import user

import hashlib
from datetime import datetime
import getpass

# https://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=hallo Font: ANSI Shadow

running = True
bcolors = bountyLib.bcolors

prog_name = "bounty"
prog_version = "0.2.0"

def init():
    title = prog_name + " v" + prog_version
    # print(platform.system())
    if platform.system() == "Windows":
        os.system('color 0F')
    if platform.system() == "Linux":
        os.system('color 0F')
    if platform.system() == "Darwin":
        os.system('color 0F')

    os.system("title " + title)


def getPrefix():
    prefix = bcolors.lightgreen + user.name + "@" + user.domain + bcolors.endc + ":" + bcolors.lightcyan + "~" + bcolors.endc + "$"
    prefix = prefix + bcolors.lightgrey + " "
    return prefix


def printIntro():
    print(bcolors.purple)
    print("  ██████╗  ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗ ")
    print("  ██╔══██╗██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝ ")
    print("  ██████╔╝██║   ██║██║   ██║██╔██╗ ██║   ██║    ╚████╔╝  ")
    print("  ██╔══██╗██║   ██║██║   ██║██║╚██╗██║   ██║     ╚██╔╝   ")
    print("  ██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║   ██║      ██║  ")
    print("  ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝      ╚═╝  v" + prog_version)
    print(bcolors.endc)


def log(msg):
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    print(bcolors.green + "[" + current_time + "] " + bcolors.endc + msg)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def printWelcome():
    cls()
    printIntro()
    time.sleep(0.1)
    log(bcolors.endc + "Welcome back " + bcolors.orange + user.name + bcolors.endc + "!")
    time.sleep(0.1)
    log(bcolors.endc + "Your Balance is " + bcolors.lightgreen + str(user.balance) + bcolors.endc + "")
    time.sleep(0.1)

    if user.name == "demo":
        log("This is a demo account, no stats will be saved! To register type '" + bcolors.lightblue + "register" + bcolors.endc + "'.")
        time.sleep(0.1)


def requestLogin():
    log("Please " + bcolors.lightgreen + "Login" + bcolors.endc + " or use the '" + bcolors.cyan + "demo" + bcolors.endc + "' account.")
    username = input(bcolors.endc + "Enter Username: " + bcolors.orange)

    if username == "demo":
        user.balance = 1000
        user.name = "demo"
        printWelcome()
    else:
        password = getpass.getpass(bcolors.endc + "Enter Password: ")
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # TODO: Call API
        if username == "root" and password == "3d03d69c231712f3851250fac88c2b8c13aee04863c1558c97c8992ed24b49fd":
            user.balance = 2000
            user.name = "root"
            printWelcome()
        else:
            log(bcolors.red + "Failed to log in as: " + bcolors.orange + username)
            requestLogin(False)


def start():
    requestLogin()

    while running:
        game()


def game():
    prefix = getPrefix()
    msg = input(prefix)

    cmd = msg.lower().split(" ")
    if cmd[0] == "roulette":
        game_roulette.query(cmd)
    elif cmd[0] == "blackjack":
        game_blackjack.query(cmd)
    elif cmd[0] == "stop":
        sys.exit()
    else:
        log(bcolors.lightblue + "you entered: " + bcolors.lightgrey + msg)


if __name__ == '__main__':
    init()
    printIntro()
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
