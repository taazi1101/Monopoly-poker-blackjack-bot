import time, os

fileName = "data/bjLogs.txt"


def most_common(lst):
    return max(set(lst), key=lst.count)

with open(fileName,"r") as f:
    data = f.read()

hands = data.count("Hand:")
handZeroError = data.count("Hand:0")
dealerHandZeroError = data.count("Dealers hand:0")
agressivePlays = data.count("Agressive")
antiBustPlays = data.count("Anti bust")
win = data.count("WIN")
lose = data.count("LOSE")
push = data.count("PUSH")
hit = data.count("Play:0")
stand = data.count("Play:1")
double = data.count("Play:2")

totalCompleteRounds = win + lose + push

data = data.replace(" WON","").replace(" LOSE","").replace(" PUSH","")

lines = data.split("\n")
deleteUsedLogs = True

x = 0
for line in lines:
    if "Program run..." in line:
        lines.pop(x)
    x += 1
x = 0
for line in lines:
    if "Started." in line:
        lines.pop(x)
    if "Stopped." in line:
        lines.pop(x)
    x += 1
lines.pop(0)
lines.pop()

allHands = []
overReadHandError = 0
for line in lines:
    handSplit = line.split("|")[0]
    number = int(handSplit.split(":")[1])
    allHands.append(number)
    if number > 30:
        overReadHandError += 1
    if number != 0:
        allHands.append(number)
commonHand = most_common(allHands)

allDealerHands = []
overReadHandDealerError = 0
for line in lines:
    handSplit = line.split("|")[1]
    number = int(handSplit.split(":")[1])
    if number > 30:
        overReadHandDealerError += 1
    if number != 0:
        allDealerHands.append(number)
commonDealer = most_common(allDealerHands)

print(f"Hands: {hands}\nTotal complete rounds: {totalCompleteRounds}\nHand zero error: {handZeroError}\nDealer zero error: {dealerHandZeroError}\nAgressive plays: {agressivePlays}\nAnti bust plays: {antiBustPlays}\nHand over read error: {overReadHandError}\nDealer over read error: {overReadHandDealerError}\nMost common hand: {commonHand}\nDealer common hand: {commonDealer}")

print(f"Hits: {hit} |Stands: {stand} |Doubles: {double}")
print(f"Hit rate: {round((hit/hands)*100)} |Stand rate: {round((stand/hands)*100)} |Double rate: {round((double/hands)*100)}")

print(f"Hand zero errors: {round((handZeroError/hands)*100)}% |Dealer hand zero errors: {round((dealerHandZeroError/hands)*100)}%\nHand over errors: {round((overReadHandError/hands)*100)}% |Dealer hand over errors: {round((overReadHandDealerError/hands)*100)}%")

print(f"Total wins:{win} |Total loses: {lose} |Total pushes: {push}\nWin rate: {round((win/totalCompleteRounds)*100)}% |Lose rate: {round((lose/totalCompleteRounds)*100)}% |Push rate: {round((push/totalCompleteRounds)*100)}%")

if os.path.exists("debugging") == False:
    os.mkdir("debugging")

with open(f"debugging/formatterResults{time.monotonic()}.txt","w") as f:
    f.write(f"Hands {hands}\nHand zero error {handZeroError}\nDealer zero error {dealerHandZeroError}\nAgressive plays {agressivePlays}\nAnti bust plays {antiBustPlays}\nHand over read error {overReadHandError}\nDealer over read error {overReadHandDealerError}\nMost common hand {commonHand}\nDealer common hand {commonDealer}\n")
    f.write(f"Hits: {hit} |Stands: {stand} |Doubles: {double}\n")
    f.write(f"Hit rate: {round((hit/hands)*100)}% |Stand rate: {round((stand/hands)*100)}% |Double rate: {round((double/hands)*100)}%\n")
    f.write(f"Hand zero errors: {round((handZeroError/hands)*100)}% |Dealer hand zero errors: {round((dealerHandZeroError/hands)*100)}%\nHand over errors: {round((overReadHandError/hands)*100)}% |Dealer hand over errors: {round((overReadHandDealerError/hands)*100)}%\n")
    f.write(f"Total wins: {win} |Total loses: {lose} |Total pushes: {push}\nWin rate: {round((win/totalCompleteRounds)*100)}% |Lose rate: {round((lose/totalCompleteRounds)*100)}% |Push rate: {round((push/totalCompleteRounds)*100)}%")

if deleteUsedLogs:
    os.remove(fileName)