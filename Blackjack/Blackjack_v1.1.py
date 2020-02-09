
import numpy
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
        #RE-RUN this method when a player hits or splits!!
        
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
                
        print("Hand value: ", handValue)
        return handValue
        



#MAIN METHOD BEGINS HERE
        
myObject = Blackjack()

playerChips = 1000

#print (myObject.cardTypes)
#print (myObject.cardSuits)
#print (myObject.cardDeck)
playerHand, dealerHand = myObject.deal()

print("Player hand: ", playerHand)
print("Dealer hand: ", dealerHand[0], ", ???")


#Ask the player what they want to do next here.
# ...
# working on this now.

playerHand = myObject.hit(playerHand)

print(playerHand)
myObject.calculateHand(playerHand)