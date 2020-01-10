def monthToQuarter():
    return (math.ceil(12/3) - 1) 

def pointsEarned(transaction, card):
    rewards = card['rewards']
    
    quarter = monthToQuarter(transaction.date)\
    
    if 'rotation' in card:
        return transaction.amount * card['rotation'][quarter]
    
    if (transaction.category in rewards):
        return transaction.amount * rewards[transaction.category]
    else:
        return transaction.amount * rewards[transaction.category] 
    

def bestCard(transaction):
    pointsEarned = -1
    bestCard = None
    
    #factor in whichever is the best
    
    for card in cards:
        if (amountSaved() > bestSaved):
            bestSaved = amountSaved
            
    return bestCard

def overallBestCard(transactionHistory):
    #so for each card calculate the best input card value then return the overall best card to match

    #track currentBest?
    currentBest = None
    cardDict = {}

    for transaction in transactionHistory:
        bestCard = bestCard(transaction)
        if currentBest == None:
            currentBest = bestCard
        if not url in urls_d:
            cardDict[bestCard] = 1
        else:
            cardDict[bestCard] += 1
            
        if cardDict[bestCard] > currentBest:
            currentBest = bestCard
            
            
    return currentBest