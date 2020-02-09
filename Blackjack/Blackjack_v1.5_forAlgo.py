
import random

class Blackjack:
    
    def __init__(self):
        self.cardTypes = ["A","K","Q","J",10,9,8,7,6,5,4,3,2]
        self.cardSuits = ["Spade","Heart","Diamond","Club"]
        self.cardDeck = []
        
        for z in range(0,5):
            for x in range(0,13):
                for y in range(0,4):
                    self.cardDeck.append([self.cardTypes[x],self.cardSuits[y]])
                    
        random.shuffle(self.cardDeck)
    
    def reshuffle(self):
        #This method exists because we might want to re-shuffle after depleting too many cards.
        #The criteria for when to shuffle will be deployed in the main code.
        # ( <40 cards remain or something)
        
        #We just completely re-create a fresh 5-deck deck (260 cards) and shuffle it.
        
        for z in range(0,5):
            for x in range(0,13):
                for y in range(0,4):
                    self.cardDeck.append([self.cardTypes[x],self.cardSuits[y]])
                    
        random.shuffle(self.cardDeck)
    
    
    def deal(self):
        #Deals a card to the player, then then dealer, then the player, then the dealer again, from the top of the deck.
        
        playerHand = [self.cardDeck.pop(0)]
        dealerHand = [self.cardDeck.pop(0)]
        
        playerHand.append(self.cardDeck.pop(0))
        dealerHand.append(self.cardDeck.pop(0))
        
        return playerHand, dealerHand
    
    def hit(self, hand):
        #This method adds a card to the hand, then returns the new hand.
        
        hand.append(self.cardDeck.pop(0))
        return hand
    
    def stand(self, hand): #Lol, pretty silly method. But I want it anyway because it will make the main method more readable.
        return hand
    
    def split(self, hand): #You are allowed to split if your first two cards are the same (a pair). 
        #If this method is called, and you do have two identical first cards, first it seperates the cards, and
        #draws a new pair for both of them.
        #They can then be played seperately, as normal.
        #Currently not used in the game.
        
        if (hand[0][0] != hand[1][0]):
            print ("I'm sorry, you are not allowed to split this hand!")
            return hand
        else:
            hand1 = hand[0]
            hand1.append(self.cardDeck.pop(0))
            hand2 = hand[1]
            hand2.append(self.cardDeck.pop(0))
            return hand1, hand2
            
        
    def calculateHand(self, hand):
        #Provided the current player or dealer's hand, calculate its value
        
        handValue = 0
        
        # len(hand) gives the current number of cards in the hand.
        
        #We deal with all non-Aces FIRST.
        for x in range (0, len(hand)):
            if (hand[x][0] != "A"): #If the first card isn't an Ace, we want to calculate it.
                if (hand[x][0] == "K" or hand[x][0] == "Q" or hand[x][0] == "J"): #If its a King, Queen, or Jack, we need to add 10 to value.
                    handValue = handValue + 10
                else: #If it's not a A, K, Q, or J, it is a number. We simply add the number to the value.
                    handValue = handValue + hand[x][0]
                
        #We deal with the Aces LAST.
        for x in range (0, len(hand)):
            if (hand[x][0] == "A" and handValue > 10): #The 10 here is to avoid busting. Basically, if a hand value is 11, and you add 11, you get 22. We don't want that.
                handValue = handValue + 1
            elif (hand[x][0] == "A" and handValue <= 10):
                handValue = handValue + 11
                
        #print("Hand value: ", handValue)
        return handValue
    
    def resolve(self, playerHand, dealerHand): #This method returns 0 if you Lose, 1 if you Win, 2 if you Push

        
        #do this in one loop, no print statements.
        resolved = False
        
        while(resolved == False):
            #3 options
            #if dealer busts
            #if dealer stands
            #if dealer hits
            
            #Option 1, dealer busts.
            if(self.calculateHand(dealerHand) > 21):
                resolved = True
                return 1
            
            #Option 2, dealer stands
            if(self.calculateHand(dealerHand) >= 17 and self.calculateHand(dealerHand) <= 21):
                #check if player or dealer won
                if (self.calculateHand(playerHand) > self.calculateHand(dealerHand)):
                    resolved = True
                    return 1
                elif (self.calculateHand(playerHand) == self.calculateHand(dealerHand)):
                    resolved = True
                    return 2
                elif (self.calculateHand(playerHand) < self.calculateHand(dealerHand)):
                    resolved = True
                    return 0
            
            #Option 3, dealer hits.
            else:
                self.hit(dealerHand)
                




###################################################################################
    def playBlackjack(self, inputDecisionArray):
        
        loopNum = 1000
        leftCasino = False
        handComplete = False
        winPercent = 100.00
        numGames = 0
        numWins = 0
        
        while leftCasino == False:
            if (loopNum == 0):
                leftCasino = True
                return winPercent
            
            if(len(self.cardDeck) < 40):
                self.reshuffle()
            
            handComplete = False
            playerHand, dealerHand = self.deal()
            initialHand = [playerHand[0], playerHand[1]] #Adding this variable as a convienient reference, to check if you got a natural blackjack.
                
            while handComplete == False:
                if (self.calculateHand(playerHand) == 21):
                    if (self.calculateHand(initialHand) == 21): #Player got a blackjack
                        if(self.resolve(playerHand, dealerHand) == 1): #Player wins
                            numWins = numWins + 1
                            numGames = numGames + 1
                            winPercent = numWins / numGames
                            loopNum = loopNum - 1
                            break
                    
                    elif(self.calculateHand(dealerHand) == 21): #Dealer also got a blackjack. Push. Don't increase numGames (neutral outcome)
                        loopNum = loopNum - 1
                        break
                else:
                    if(self.resolve(playerHand, dealerHand) == 1): #Player got a 21 and dealer did not. Player wins.
                        numWins = numWins + 1
                        numGames = numGames + 1
                        winPercent = numWins / numGames
                        loopNum = loopNum - 1
                        break
                    else: #Both got 21. Push. No change to W/L or numGames
                        loopNum = loopNum - 1
                        break
            
                #The decision. We choose based on the given inputDecisionArray.
                #Decision options are Hit, Stand, Double.
                
                #This depends on the checkTable method written by Ethan! Don't have it in this file yet.
            
                player_choice = input(self.checkTable(self.calculateHand(playerHand), dealerHand[0][0], inputDecisionArray))
                
                # 0 is stand, 1 hit, 2 double. double is worth 2 wins (but only 1 game)
                
                if (player_choice == 1): # decision 1 is HIT
                    playerHand = self.hit(playerHand)
                    if (self.calculateHand(playerHand) <= 21): #Make another decision. Game is not over.
                        continue
                    else: #You bust, you lose this game.
                        numGames = numGames + 1
                        winPercent = numWins / numGames
                        handComplete = True
                
                if (player_choice == 0): # decision 0 is STAND
                    playerHand = self.stand(playerHand)
        
                # myGame.resolve(playerHand, dealerHand) --> returns 0, 1, or 2. 0 means you lose, 1 means you win, 2 means push.
                    if(self.resolve(playerHand, dealerHand) == 0): #You lost.
                        numGames = numGames + 1
                        winPercent = numWins / numGames
                        handComplete = True
            
                    elif(myGame.resolve(playerHand, dealerHand) == 1): #You won
                        numWins = numWins + 1
                        numGames = numGames + 1
                        winPercent = numWins / numGames
                        handComplete = True
                    else: #You push, no change to games or winLoss
                        handComplete = True
                    
                if (player_choice == 2): #Decision is DOUBLE. GAME WORTH 2x IF YOU WIN!
                    playerHand = self.hit(playerHand)
                    
                    if(self.calculateHand(playerHand) > 21): #You lost, bust.
                        numGames = numGames + 1
                        winPercent = numWins / numGames
                        handComplete = True
                    
                    else:
                
                        if(myGame.resolve(playerHand, dealerHand) == 0): #You lost. Dealer beats you.
                            numGames = numGames + 1
                            winPercent = numWins / numGames
                            handComplete = True
                            
                        elif(myGame.resolve(playerHand, dealerHand) == 1): #You win DOUBLE!
                            numWins = numWins + 2
                            numGames = numGames + 1
                            winPercent = numWins / numGames
                            handComplete = True
                            
                        else: #Push, no change. 
                            handComplete = True
                    
            
            loopNum = loopNum - 1
            
###################################################################################



#MAIN METHOD BEGINS HERE
            # Known bugs:
            # Game will crash if played too many times. Need to implement reshuffle.
            # When you use the split option, it causes too many cards to be drawn
            
#OK, the main changes we need to make are we need to accept 0,1,or 2 as automated input.
#Also, playBlackjack(inputDecisionArray) needs to be a method.
#Ethan is working on the createInitialArray() method.
            
            

print("Welcome to the AI version of the Hacklahoma 2020 Blackjack table!")
myGame = Blackjack()
