import main

balance = 1000
name = "demo"
pw = ""
domain = "bounty"
suffix = ":~$ "


def callAPI(str):
    # call API
    # bounty.gg/name/password/str
    main.log("synced: " + str)


def update():
    if name == "demo":
        return

    callAPI("setBalance=" + str(balance))


def verifyTransaction(amount):
    if balance - amount >= 0 and amount > 0:
        return True
    else:
        return False
