import Card


class CardGameBlackjack(Card.CardGame):

    def __init__(self):
        super().__init__()
        self.player_hand = Card.Hand("Player")
        self.dealer_hand = Card.Hand("Dealer")

    def play_game(self):
        """
        Plays one round of blackjack
        :return: Nothing
        """
        # deal the cards
        self.deal_cards()
        print("---------- Cards have been dealt")

        # Player's turn
        player_score = self.take_turn(self.player_hand)

        # Dealer's turn
        dealer_score = self.dealer_turn(self.dealer_hand)

        # Determine winner
        if self.declare_winner(player_score, dealer_score):
            # Player won
            print('Player won!\n')
        else:
            print('Dealer won.\n')
        print(self.player_hand, '\n', player_score)
        print(self.dealer_hand, '\n', dealer_score)

        print('\nEnding game...')

    def deal_cards(self):
        """
        Deal's cards out to player and dealer
        :return: Nothing
        """
        self.player_hand.add(self.deck.top_deck())
        self.player_hand.add(self.deck.top_deck())
        self.dealer_hand.add(self.deck.top_deck())
        self.dealer_hand.add(self.deck.top_deck())

    def take_turn(self, hand):
        """
        Does player's turn
        :param hand: Player's hand originally dealt
        :return: Score of player's hand
        """
        print("Player's turn.")
        print(hand)
        while hand.blackjack_soft_ace_value < 21 and self.choose_hit_stay():
            # Choose hit or stay
            hand.add(self.deck.top_deck())
            print(hand)

        # If hand hard ace = 21
        if hand.blackjack_hard_ace_value == 21:
            return hand.blackjack_hard_ace_value
        # If hand hard ace > 21
        elif hand.blackjack_hard_ace_value > 21:
            return hand.blackjack_soft_ace_value
        # If hand hard ace < 21
        else:
            if hand.blackjack_hard_ace_value > hand.blackjack_soft_ace_value:
                return hand.blackjack_hard_ace_value
            else:
                return hand.blackjack_soft_ace_value

    def dealer_turn(self, hand):
        """
        Does dealer's turn
        :param hand: Dealer's hand originally dealt
        :return: Score of dealer's hand
        """
        def logic_hand_with_ace(aced_hand):
            """
            Draw until has good hand
            :param aced_hand: hand with ace
            :return: score of hand after drawing
            """
            # Hit until you're at 17 or over 21
            while aced_hand.blackjack_hard_ace_value <= 17:
                aced_hand.add(self.deck.top_deck())
            # If over 21 hard ace
            if aced_hand.blackjack_hard_ace_value > 21:
                # Hit until <= 17 using soft ace
                while aced_hand.blackjack_soft_ace_value <= 17:
                    aced_hand.add(self.deck.top_deck())
                return aced_hand.blackjack_soft_ace_value
            # If at 21 hard ace
            elif aced_hand.blackjack_hard_ace_value == 21:
                return aced_hand.blackjack_hard_ace_value
            else:  # under 21 soft ace
                # Hit until at 17 soft ace
                while aced_hand.blackjack_soft_ace_value <= 17:
                    aced_hand.add(self.deck.top_deck())
                return aced_hand.blackjack_soft_ace_value

        def logic_hand_without_ace(no_ace_hand):
            """
            Draw until has good hand
            :param no_ace_hand: hand
            :return:
            """
            # Hit until 17 or over
            while no_ace_hand.blackjack_hand_value < 17:
                no_ace_hand.add(self.deck.top_deck())
                if no_ace_hand.has_ace:
                    hand_with_ace = no_ace_hand
                    return logic_hand_with_ace(hand_with_ace)
            return no_ace_hand.blackjack_hand_value

        if hand.has_ace:
            return logic_hand_with_ace(hand)
        else:
            return logic_hand_without_ace(hand)

    @staticmethod
    def get_choice():
        """
        Get user input for choice 1 or 2.
        :return: Any user input (1 for hit 2 for stay)
        """
        choice = input("Choose hit or stay... \n")
        if choice == 'hit' or choice == 'stay':
            return choice
        else:
            print
            "You must enter 'hit' or 'stay'... "
            CardGameBlackjack.get_choice()

    @staticmethod
    def choose_hit_stay():
        """
        Get user input hit or stay
        :return: True for hit; False for Stay
        """
        choice = CardGameBlackjack.get_choice()
        if choice == 'hit':
            return True
        else:
            return False

    @staticmethod
    def declare_winner(hand1, hand2):
        """
        Determines who won
        :param hand1: player's hand
        :param hand2: dealer's hand
        :return: True if player won, False if dealer won.
        """
        # Dealer has 21. Return False.
        if hand2 == 21:
            return False
        elif hand1 == 21:
            return True
        elif hand2 <= 21 < hand1:
            return False
        elif hand1 <= 21 < hand2:
            return True
        elif hand1 > 21 and hand2 > 21:
            if hand1 < hand2:
                return True
            else:
                return False
        elif hand1 < 21 and hand2 < 21:
            if hand1 > hand2:
                return True
            else:
                return False
