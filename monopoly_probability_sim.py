import random

class BaseMonopolySim:
    """
        Base class for monopoly simulations. Plays a virtual game of monopoly, recording how many hits each board tile gets
        The virtual game is played by repeatedly calling newPosition(self, oldPosition: int, roll1: int, roll2: int) -> int,
        which calculates the new position to travel to after rolling the dice. The base class assumes that this method naively
        moves forward by adding up the dice, without any special effects from cards, tiles, or rolling doubles. Subclasses can
        override this method to implement jail and chance cards that change where the player goes after rolling.
    """
    TOTAL_SQUARES = 40
    DECIMAL_PRECISION = 4
    def __init__(self, seed=None):
        self.board = [0]*BaseMonopolySim.TOTAL_SQUARES
        self.position = 0
        self.totalMoves = 0
        self.rnd = None
        if seed == None:
            self.rnd = random.Random()
        else:
            self.rnd = random.Random(seed)

    def roll(self):
        self.position = self._safeNewPosition(self.position, self.rnd.randint(1,6), self.rnd.randint(1,6))
        self.landedOn(self.position)

    def landedOn(self, pos):
        """Records that the player landed on position pos. Call this if a card sends the player somewhere after landing
        on a card tile."""
        self.board[pos] += 1
        self.totalMoves += 1

    def play(self, n):
        [self.roll() for _ in range(n)]

    def getBoard(self):
        return [x for x in self.board]

    def getRnd(self):
        return self.rnd

    def averageOverNPlays(self, nPlays, playLength):
        """Plays a virtual game nPlays times. Assumes a single player, who rolls the dice and moves repeatedly.
        print(self) to see which tiles were landed on most"""
        for _ in range(nPlays):
            self.position = 0
            self.totalMoves = 0
            self.play(playLength)
        for i in range(BaseMonopolySim.TOTAL_SQUARES):
            self.board[i] /= nPlays

    def newPosition(self, oldPosition: int, roll1: int, roll2: int) -> int:
        """Override this method to implement Jail and special effects from Chance"""
        return (oldPosition + roll1 + roll2) % BaseMonopolySim.TOTAL_SQUARES

    def _safeNewPosition(self, oldPosition, roll1, roll2):
        result = self.newPosition(oldPosition, roll1, roll2)
        assert(result >= 0 and result < BaseMonopolySim.TOTAL_SQUARES)
        return result

    def percentageAt(self, pos):
        return self.board[pos]/self.totalMoves

    @staticmethod
    def monopolyFormatPercentage(frac: float):
        str_format = '{' + f':0{BaseMonopolySim.DECIMAL_PRECISION + 2}.{BaseMonopolySim.DECIMAL_PRECISION}f' + '}'
        return str_format.format(100*frac)+'%'

    def __str__(self):
        SIZE_OF_SQUARE = 2 + self.DECIMAL_PRECISION + 1
        legOfBoard = self.TOTAL_SQUARES//4 # number of tiles on one side, including one corner
        result = 'Go is on the top left\n|'
        for i in range(legOfBoard + 1):
            result += BaseMonopolySim.monopolyFormatPercentage(self.percentageAt(i))
            result += '|'
        result += '\n'
        for i in range(legOfBoard - 1):
            result += '|'
            result += BaseMonopolySim.monopolyFormatPercentage(self.percentageAt(self.TOTAL_SQUARES - 1 - i))
            result += '|'
            result += (' ' * (SIZE_OF_SQUARE * (legOfBoard - 1) + legOfBoard - 2))
            result += '|'
            result += BaseMonopolySim.monopolyFormatPercentage(self.percentageAt(legOfBoard + 1 + i))
            result += '|'
            result += '\n'
        result += '|'
        for i in range(3*legOfBoard, 2*legOfBoard - 1, -1):
            result += BaseMonopolySim.monopolyFormatPercentage(self.percentageAt(i))
            result += '|'

        return result



class JailsMonopolySim(BaseMonopolySim):
    """
        Simulates monopoly with the mechanism of sending the player to jail after three doubles in a row.
        When the player goes to jail, does not count the player as having landed on the spot they were aiming for,
        but instead counts them as having landed on the 'Go to jail' tile.
        On the next turn, they play as if they were starting on the 'Just visiting' tile, even though it does not
        count them as having landed on 'Just visiting'
        Does not take into account a player rolling to get out of jail. Going to jail is counted once.
        This is because rolling to get out (or paying $50) doesn't affect the frequency of landing on other tiles
    """
    VISITING_JAIL = 10
    GO_TO_JAIL = 30

    def __init__(self, seed=None):
        super().__init__(seed)
        self.doubles = 0

    def newPosition(self, oldPosition, roll1, roll2):
        if oldPosition == self.GO_TO_JAIL:
            oldPosition = self.VISITING_JAIL
        if (roll1 == roll2):
            self.doubles += 1
            if self.doubles == 3:
                self.doubles = 0
                return self.GO_TO_JAIL
        else:
            self.doubles = 0
        return super().newPosition(oldPosition, roll1, roll2)
    


class Deck:
    """Simple class for simulating a deck of cards"""
    def __init__(self, nCards: int, rnd: random.Random):
        self.nCards = nCards
        self.rnd = rnd
        self.cards = self.newRandomDeck()

    def newRandomDeck(self):
        deck = [i for i in range(self.nCards)]
        self.rnd.shuffle(deck)
        return deck

    def draw(self):
        card = self.cards.pop()
        if len(self.cards) == 0:
            self.cards = self.newRandomDeck()
        return card

class RealisticMonopolySim(JailsMonopolySim):
    """
        Simulates a realistic game of monopoly, computing the frequency of landing on each time. Takes into account
        the chance and community chest cards as well as the mechanism of going to jail after rolling three doubles
        in a row. Does not compute chances of winning, or anything involving money or value. Only computes
        frequency of landing on tiles. This can be useful for monopoly strategy.
    """
    CHANCES = {7, 22, 36}
    COMMUNITY_CHESTS = {2, 17, 33}
    CARDS_IN_DECK = 16
    GO = 0
    ILLINIOS_AVENUE = 24
    READING_RAILROAD = 5
    ST_CHARLES_PLACE = 11
    BOARDWALK = 39
    PENNSYLVANIA_RAILROAD = 15
    B_O_RAILROAD = 25
    WATER_WORKS = 28
    ELECTRIC_COMPANY = 12

    def __init__(self, seed=None):
        super().__init__(seed)
        self.chance = Deck(self.CARDS_IN_DECK, self.getRnd())
        self.communityChest = Deck(self.CARDS_IN_DECK, self.getRnd())

    def newPosition(self, oldPosition, roll1, roll2):
        superPosition = super().newPosition(oldPosition, roll1, roll2)
        onCommunityChest = superPosition in self.COMMUNITY_CHESTS
        onChance = superPosition in self.CHANCES
        if not onChance and not onCommunityChest:
            return superPosition # fallback on the default die roll if you didn't land on a card tile

        if onCommunityChest:
            # simulate community chest. Two of the cards send you to other places, affecting board positioning
            # the other cards (card > 1) affect your money, which we aren't incorporating into the sim
            card = self.communityChest.draw()
            if (card > 1):
                return superPosition

            self.landedOn(superPosition)
            if card == 0:
                return self.GO
            if card == 1:
                return self.GO_TO_JAIL
        
        card = self.chance.draw()
        # simulate chance deck. 9 of the cards send you to other places
        if card > 9:
            return superPosition

        self.landedOn(superPosition)
        if card == 0:
            return self.GO
        if card == 1:
            return self.GO_TO_JAIL
        if card == 2:
            return self.ST_CHARLES_PLACE
        if card == 3:
            return self.ILLINIOS_AVENUE
        if card == 4:
            return self.READING_RAILROAD
        if card == 5:
            return self.BOARDWALK
        if card == 6:
            return superPosition - 3
        # these last three are "go to next utility" and "go to next railroad"
        if card == 7:
            if superPosition == 22:
                return self.WATER_WORKS
            return self.ELECTRIC_COMPANY
        # else card == 8 or 9
        if superPosition == 7:
            return self.PENNSYLVANIA_RAILROAD
        if superPosition == 22:
            return self.B_O_RAILROAD
        return self.READING_RAILROAD
        
    def listPercentagesByMonopoly(self):
        """Call this method after running a simulation to see which monopolies are best to own.
        Prints out the total percentage of time player landed on each color group, as well as
        the average for that color group"""
        monopolyMap = {
            'brown':[1, 3],
            'light blue':[6, 8, 9],
            'pink':[11, 13, 14],
            'orange':[16, 18, 19],
            'red':[21, 23, 24],
            'yellow':[26, 27, 29],
            'green':[ 31, 32, 34],
            'dark blue':[37, 39],
            'railroads':[5, 15, 25, 35],
            'utilities':[12, 28]
        }
        for monopoly in monopolyMap:
            sum = 0
            for position in monopolyMap[monopoly]:
                sum += self.percentageAt(position)
            print(f'{monopoly}: {self.monopolyFormatPercentage(sum)}. Average: {self.monopolyFormatPercentage(sum/len(monopolyMap[monopoly]))}')

        

if __name__ == '__main__':
    game = RealisticMonopolySim(42) #instantiates with a seed to ensure reliable results
    game.averageOverNPlays(1000, 100000) #plays ten games, rolling the dice 10000 times each game
    print(game) # prints the percentages for each tile
    game.listPercentagesByMonopoly() # prints the percentages by monopoly (colors, railroads, and utilites)
    