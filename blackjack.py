import discord
from discord.ext import commands
import random

SUITS = ['\u2664', '\u2661', '\u2667','\u2662']
FACES = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
BLACKJACK_VALUES = {'A': 1, 'J' : 10, 'Q' : 10, 'K' : 10}

class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

def createDeck(numDecks):
        deck = []
        for i in range(0,numDecks):
            deck += [Card(suit,face) for suit in SUITS for face in FACES]
        random.shuffle(deck)
        return deck


class BlackjackCog(commands.Cog):
    def __init__(self, bot):
        self.gameStarted = False
        self.bot = bot
        self.deck = createDeck(4)
        self.player_hand = []
        self.dealer_hand = []

    def deal(self):
        if not self.deck:
            self.deck = createDeck(4)
        return self.deck.pop(0)

    def calcValue(self,hand):
        value = 0
        for card in hand:
            if card.face in BLACKJACK_VALUES:
                value += BLACKJACK_VALUES[card.face]
            else:
                value += int(card.face)
        if(value < 12 and any([card.face == 'A' for card in hand])):
            value += 10
        return value

    def toStrHand(self,hand):
        hand_str = ''
        for card in hand:
            hand_str += '{0} '.format(card.suit + card.face)
        return hand_str

    def checkWin(self,stand=False):
        dealer_value = self.calcValue(self.dealer_hand)
        player_value = self.calcValue(self.player_hand)


        if dealer_value == 21:
            return 2
        elif player_value == 21:
            return 1
        elif player_value > dealer_value and dealer_value > 17 and stand:
            return 0

    @commands.command(aliases=['blackjack','bj'])
    async def startGame(self,ctx):
        self.dealer_hand = []
        self.player_hand = []

        dealer_cards.append(self.deal())
        player_cards.append(self.deal())
        dealer_cards.append(self.deal())
        player_cards.append(self.deal())

        dealer_value = self.calcValue(dealer_cards)
        player_value = self.calcValue(player_cards)

        message += 'Dealers\' Hand: {0}for a total of {1}'.format(toStrHand(dealer_cards),dealer_value)
        message += '\nPlayer\'s Hand: {0}for a total of {1}'.format(toStrHand(player_cards), player_value)

        await ctx.send('{0} {1}'.format(message, '\nRemaining Cards: ' + str(len(self.deck))))

    @commands.command
    async def hit(self,ctx):

