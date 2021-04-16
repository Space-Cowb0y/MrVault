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
        self.bot = bot
        self.deck = createDeck(4)
        self.player_hand = []
        self.dealer_hand = []

    def deal(self):
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

    @commands.command(aliases=['blackjack','bj'])
    async def startGame(self,ctx):
        dealer_cards = []
        player_cards = []

        dealer_cards.append(self.deal())
        player_cards.append(self.deal())
        dealer_cards.append(self.deal())
        player_cards.append(self.deal())

        dealer_value = self.calcValue(dealer_cards)
        player_value = self.calcValue(player_cards)

        dealer_hand_str = ''
        for card in dealer_cards:
            dealer_hand_str += '{0} '.format(card.suit + card.face)

        player_cards_str = ''
        for card in player_cards:
            player_cards_str += '{0} '.format(card.suit + card.face)

        message = 'Dealers\' Hand: {0}for a total of {1}'.format(dealer_hand_str,dealer_value)
        message += '\nPlayer\'s Hand: {0}for a total of {1}'.format(player_cards_str, player_value)
        await ctx.send('{0} {1}'.format(message, '\nRemaining Cards: ' + str(len(self.deck))))
