import random
done = False
playerWins = 0
dealerWins = 0
while not done:
    card1 = random.randint(1,11)
    card2 = random.randint(1,11)
    totalP = card1 + card2
    print("\nHand = ", card1, " ", card2, "  (", totalP, ")", sep = ' ', end = '  ')
    while totalP <= 21:
        choice = input("action? (h=hit, s=stay):   ")
        if choice == 'h':
            card = random.randint(1,11)
            totalP = totalP + card
            print("    new card = ", card, "  (", totalP, ")", sep = ' ', end = '  ')
        else:
            if choice == 's':
                break
    if totalP > 21:
        print("\nDealer won!")
        dealerWins += 1
    else:    
        card1 = random.randint(1,11)
        card2 = random.randint(1,11)
        totalD = card1 + card2
        print("Dealer got  ", card1, card2, "  (", totalD, ")")
        while totalD < 17 and totalD < totalP:
            card = random.randint(1,11)
            totalD = totalD + card
            print("    new card: ", card, " Dealers total (", totalD, ")")
        print("\nPlayer's total (", totalP, ")   vs   Dealer's total (", totalD, ")")
        if totalD > 21:
            print("Player won!")
            playerWins += 1
        elif totalD >= totalP:
            print("Dealer won!")
            dealerWins += 1
        else:
            print("Player won!")
            playerWins += 1
    ans = input("Wanna try your luck again? 'n' or 'N' for 'No' or everything else for 'Yes'   ")
    done = ans == 'n' or ans == 'N'
print ("\nplayer won", playerWins, "hands, dealer won", dealerWins, "hands")

