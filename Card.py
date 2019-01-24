class Card:
    SUITS = ('Clubs', 'Diamonds', 'Hearts', 'Spades')
    RANKS = ('Joker', 'Ace', '2', '3', '4', '5', '6', '7',
             '8', '9', '10', 'Jack', 'Queen', 'King')

    def __init__(self, suit=0, value=0):
        self._suit = suit
        self._value = value

    def __str__(self):
        """
          >>> print(Card(2, 11))
          Queen of Hearts
        """
        return '{0} of {1}'.format(Card.RANKS[self._value],
                                   Card.SUITS[self._suit])

    def __cmp__(self, other):
        # check the suits
        if self._suit > other.suit:
            return 1
        if self._suit < other.suit:
            return -1
        # suits are the same... check ranks
        if self._value > other.value:
            return 1
        if self._value < other.value:
            return -1
        # ranks are the same... it's a tie
        return 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, suit):
        self._suit = suit


class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))

    def __str__(self):
        s = ""
        for i in range(len(self.cards)):
            s += " " * i + str(self.cards[i]) + "\n"
        return s

    def shuffle(self):
        import random
        num_cards = len(self.cards)
        for i in range(num_cards):
            j = random.randrange(i, num_cards)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def trash(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False

    def top_deck(self):
        return self.cards.pop()

    def is_empty(self):
        return len(self.cards) == 0


class Hand(Deck):
    def __init__(self, name=""):
        self.cards = []
        self.name = name
        # super().__init__()

    def add(self, card):
        self.cards.append(card)

    def deal(self, hands, num_cards=999):
        num_hands = len(hands)
        for i in range(num_cards):
            if self.is_empty(): break  # break if out of cards
            card = self.pop()  # take the top card
            hand = hands[i % num_hands]  # whose turn is next?
            hand.add(card)  # add the card to the hand

    def __str__(self):
        s = self.name + "'s hand "
        if self.is_empty():
            s = s + "is empty.\n"
        else:
            s = s + "contains:\n"
        return s + Deck.__str__(self)

    @property
    def has_ace(self):
        """
        Returns true if hand has an ace.
        :return:
        """
        found = False
        for card in self.cards:
            if card.value == 1:
                found = True
        return found

    @property
    def blackjack_soft_ace_value(self):
        summed_hand = 0
        for card in self.cards:
            if card.value >= 10:
                summed_hand += 10
            else:
                summed_hand += card.value
        return summed_hand

    @property
    def blackjack_hard_ace_value(self):
        summed_hand = 0
        for card in self.cards:
            if card.value == 1:
                summed_hand += 11
            else:
                if card.value >= 10:
                    summed_hand += 10
                else:
                    summed_hand += card.value
        return summed_hand

    @property
    def blackjack_hand_value(self):
        summed_hand = 0
        for card in self.cards:
            if card.value >= 10:
                summed_hand += 10
            else:
                summed_hand += card.value
        return summed_hand


class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
