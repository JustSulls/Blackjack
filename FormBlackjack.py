import CardGameBlackjack
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys


def declare_winner(hand1_score, hand2_score):
    """
            Determines who won
            :param hand1_score: player's hand
            :param hand2_score: dealer's hand
            :return: True if player won, False if dealer won.
            """
    # Dealer has 21. Return False.
    if hand2_score == 21:
        return False
    elif hand1_score == 21:
        return True
    elif hand2_score <= 21 < hand1_score:
        return False
    elif hand1_score <= 21 < hand2_score:
        return True
    elif hand1_score > 21 and hand2_score> 21:
        if hand1_score < hand2_score:
            return True
        else:
            return False
    elif hand1_score < 21 and hand2_score< 21:
        if hand1_score > hand2_score:
            return True
        else:
            return False


class FormBlackjack(QDialog):

    def __init__(self, parent=None):
        super(FormBlackjack, self).__init__(parent)

        # Creates deck, player's and dealer's hand
        self.game = CardGameBlackjack.CardGameBlackjack()

        # Declare layout
        self.layout = QVBoxLayout()

        # Text section
        self.txt_area = QLabel()

        # Hit button
        self.button_hit = QPushButton("Hit")

        # Stay button
        self.button_stay = QPushButton("Stay")

        # New game button
        self.button_new_game = QPushButton("New Game")

        self.timeline = QTimeLine()

        # Deal out cards
        self.setup()

        self.init_ui()

        self.setLayout(self.layout)

    def init_ui(self):
        # Text section
        # self.txt_area.setReadOnly(True)
        self.layout.addWidget(self.txt_area)

        # Hit button
        self.button_hit.setCheckable(True)
        self.button_hit.clicked.connect(self.hit_clicked)
        self.layout.addWidget(self.button_hit)

        # Stay button
        self.button_stay.setCheckable(True)
        self.button_stay.clicked.connect(self.stay_clicked)
        self.layout.addWidget(self.button_stay)

        # New game button
        self.button_new_game.clicked.connect(self.new_game_clicked)
        self.layout.addWidget(self.button_new_game)

    def new_game_clicked(self):
        self.game.dealer_hand.cards.clear()
        self.game.player_hand.cards.clear()
        self.setup()

    def stay_clicked(self):
        # Take dealer's turn
        dealer_score = self.game.dealer_turn(self.game.dealer_hand)

        # Determine winner
        if declare_winner(self.get_player_hand_score(), dealer_score):
            # Player won
            self.msg("Player won!\n")
        else:
            self.msg("Dealer won. \n")
        self.add_dialogue(self.game.player_hand.__str__(), '\n', str(self.get_player_hand_score()))
        self.add_dialogue(self.game.dealer_hand.__str__(), '\n', str(dealer_score))
        self.add_dialogue("\nEnding game...")

    def hit_clicked(self):
        self.game.player_hand.add(self.game.deck.top_deck())
        self.show_hand()

    def setup(self):
        # Deal cards
        self.game.deal_cards()
        self.txt_area.setText("Setup complete")

        self.show_hand()

    def player_turn(self, player):
        self.msg("Player's turn.")

        # Choose hit or stay
        self.add_dialogue("Choose hit or stay... ")
        self.button_hit.setEnabled(True)
        self.button_stay.setEnabled(True)

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

    def get_player_hand_score(self):
        hand = self.game.player_hand

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

    def show_hand(self):
        # self.txt_area.clear()
        self.txt_area.setText(self.game.player_hand.__str__())

    def msg(self, txt):
        self.txt_area.setText(txt)

    def add_dialogue(self, *args):
        full_txt = ''
        for txt in args:
            full_txt += txt
        self.txt_area.setText(self.txt_area.text() + "\n" + full_txt)