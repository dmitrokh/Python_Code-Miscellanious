
def wantsHit():
    choice = input("action? ('h' or 'H' - hit, otherwise - stay):   ")
    if choice == 'h' or choice == 'H':
        return True
    else:
        return False
    
def DealToPlayer():
    totalP = random.randint(1,11) + random.randint(1,11)
    print("Player got: ", totalP)
    while totalP <= 21:
        if wantsHit():
            totalP += random.randint(1,11)
            print("Player got: ", totalP)
        else:
            break
    return totalP
        
def DealToDealer(lim, totalPgiven):
    totalD = random.randint(1,11) + random.randint(1,11)
    print("Dealer got: ", totalD)
    while totalD < int(lim) and totalD < totalPgiven and totalD <= 21:
        totalD += random.randint(1,11)
        print("Dealer got: ", totalD)
    return totalD

import random
winsP = 0 
winsD = 0
flag = True
limitD = ''
while flag:
    while limitD.isdigit() != True:
        limitD = input("Enter Dealer's limit (An integer number): ")
    totalPlayer = DealToPlayer()
    if totalPlayer <= 21:
        totalDealer = DealToDealer(limitD, totalPlayer)
        if totalDealer > 21:
            winsP += 1
            print("Dealer busts, Player wins")
        elif totalDealer >= totalPlayer:
            winsD += 1
            print("Dealer won")
        else:
            winsP += 1
            print("Player won")
    else:
        winsD += 1
        print("Player busts, Dealer won")
    choice = input("Play again? ('y' or 'Y' - yes, otherwise - no) ")
    flag = choice == 'y' or choice == 'Y'
print("Player won: ", winsP, "Dealer won: ", winsD)

