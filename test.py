import time
import unittest

from card import Card, Deck, Hand, PokerSession


class TestCard(unittest.TestCase):
    def setUp(self):
        self.card1 = Card(14, 0)
        self.card2 = Card(12, 0)

    def tearDown(self):
        pass

    def test_card_constructed(self):
        self.assertIsInstance(self.card1, Card)
        self.assertIsInstance(self.card1, Card)

    def test_card_greater_than(self):
        self.assertTrue(self.card1 > self.card2)
        self.assertFalse(self.card2 > self.card1)

    def test_card_less_than(self):
        self.assertFalse(self.card1 < self.card2)
        self.assertTrue(self.card2 < self.card1)

    def test_card_string(self):
        card_strings = ('A\u2660', 'Q\u2660')
        self.assertEqual(card_strings[0], self.card1.card_string())
        self.assertEqual(card_strings[1], self.card2.card_string())


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_is_constructed(self):
        self.assertIsInstance(self.deck, Deck)
        self.assertTrue(len(self.deck.cards), 52)

    def test_card_draw(self):
        self.assertIsInstance(self.deck.draw(), Card)

    def test_discard(self):
        card = self.deck.draw()
        self.deck.discard(card)
        self.assertTrue(len(self.deck.discard_pile), 1)

    def test_deck_reshuffled_if_all_cards_drawn(self):
        # draw and discard all cards
        for i in range(52):
            card = self.deck.draw()
            self.deck.discard(card)

        # draw initiates reshuffle
        card = self.deck.draw()
        self.deck.discard(card)
        self.assertEqual(len(self.deck.cards), 51)
        self.assertEqual(len(self.deck.discard_pile), 1)


class TestHand(unittest.TestCase):
    def setUp(self):
        # get a deck with no cards to test scoring
        self.score_deck = Deck()
        self.score_deck.cards = []

        # get a regular deck
        self.deck = Deck()

        # get a Hand
        self.hand = Hand(self.deck)

    def score_hand(self, score_string):
        """Test helper for scoring hands."""
        self.hand.cards = self.score_deck.cards
        score_dict = self.hand.score(self.score_deck)

        # test if score_strings are equivalent
        self.assertEqual(score_dict["score_string"], score_string)
        # make sure the copied hand has 5 cards
        self.assertEqual(len(score_dict["cards"]), 5)

    def test_items_are_constructed(self):
        self.assertIsInstance(self.deck, Deck)
        self.assertIsInstance(self.score_deck, Deck)
        self.assertIsInstance(self.hand, Hand)

        # make sure score deck has no cards
        self.assertEqual(len(self.score_deck.cards), 0)

        # make sure regular deck has all cards. Deck should be short from hand draw
        self.assertEqual(len(self.deck.cards), 52 - 5)

    def test_one_card_dicard_success(self):
        card = self.hand.cards[1]
        self.hand.discard([1], self.deck)

        # make sure card has been disarded and the new card is in the hand.
        self.assertEqual(card, self.deck.discard_pile[0])
        self.assertNotEqual(card, self.hand.cards[1])

    def test_two_card_dicard_success(self):
        indices = [0, 1]
        cards = self.hand.cards[:2]
        self.hand.discard(indices, self.deck)


        # make sure cards have been disarded and the new cards are in the hand.
        for card in cards:
            self.assertTrue(card in self.deck.discard_pile)
            self.assertFalse(card in self.hand.cards)

    def test_two_card_dicard_success(self):
        indices = [0, 1, 2, 3]
        cards = self.hand.cards[:4]
        self.hand.discard(indices, self.deck)

        # make sure cards have been disarded and the new cards are in the hand.
        for card in cards:
            self.assertTrue(card in self.deck.discard_pile)
            self.assertFalse(card in self.hand.cards)

    def test_no_card_dicard_success(self):
        indices = []
        cards = self.hand.cards[:5]
        self.hand.discard(indices, self.deck)

        # make sure cards have been disarded and the new cards are in the hand.
        for card in cards:
            self.assertFalse(card in self.deck.discard_pile)
            self.assertTrue(card in self.hand.cards)

    def test_five_card_discard_fail(self):
        indices = [0,1,2,3,4]
        self.assertEqual(self.hand.discard(indices, self.deck), "Invalid Index")

    def test_bad_index_discard_fail(self):
        indices = [7]
        self.assertEqual(self.hand.discard(indices, self.deck), "Invalid Index")

    def test_negative_index_discard_fail(self):
        indices = [-2]
        self.assertEqual(self.hand.discard(indices, self.deck), "Invalid Index")

    def test_historgram_exists(self):
        self.assertTrue(self.hand.get_histogram())

    def test_flush(self):
        self.score_deck.cards = [Card(6, 0), Card(2, 0), Card(12, 0), Card(13, 0), Card(1,0)]
        self.hand.cards = self.score_deck.cards
        self.assertTrue(self.hand.is_flush())

    def test_hand_pair(self):
        self.score_deck.cards = [Card(14, 0), Card(14, 1), Card(12, 1), Card(13, 1), Card(1,2)]
        self.hand.cards = self.score_deck.cards
        self.score_hand("One Pair")

    def test_hand_two_pair(self):
        self.score_deck.cards = [Card(14, 0), Card(14, 1), Card(12, 1), Card(12, 2), Card(1,2)]
        self.score_hand("Two Pair")

    def test_three_of_a_kind(self):
        self.score_deck.cards = [Card(14, 0), Card(14, 1), Card(14, 2), Card(12, 2), Card(1,2)]
        self.score_hand("Three of a Kind")

    def test_four_of_a_kind(self):
        self.score_deck.cards = [Card(14, 0), Card(14, 1), Card(14, 2), Card(14, 3), Card(1,2)]
        self.score_hand("Four of a Kind")

    def test_full_house(self):
        self.score_deck.cards = [Card(14, 0), Card(14, 1), Card(14, 2), Card(12, 3), Card(12,2)]
        self.score_hand("Full House")

    def test_royal_flush(self):
        self.score_deck.cards = [Card(10, 0), Card(11, 0), Card(12, 0), Card(13, 0), Card(14,0)]
        self.score_hand("Royal Flush")

    def test_straight(self):
        self.score_deck.cards = [Card(1, 0), Card(2, 1), Card(3, 2), Card(4, 3), Card(5,2)]
        self.score_hand("Straight")

    def test_straight_five_at_bottom(self):
        self.score_deck.cards = [Card(2, 0), Card(3, 1), Card(4, 2), Card(5, 3), Card(14,2)]
        self.score_hand("Straight")

    def test_straight_flush(self):
        self.score_deck.cards = [Card(1, 0), Card(2, 0), Card(3, 0), Card(4, 0), Card(5,0)]
        self.score_hand("Straight Flush")

    def test_ace_high(self):
        self.score_deck.cards = [Card(14, 1), Card(12, 2), Card(5, 4), Card(7, 0), Card(10,0)]
        self.score_hand("Ace High")

    def test_high_card(self):
        self.score_deck.cards = [Card(11, 1), Card(12, 2), Card(5, 3), Card(7, 0), Card(10,0)]
        self.score_hand(f"High Card:Q\u2666")


class PokerSessionTest(unittest.TestCase):
    def setUp(self):
        self.session = PokerSession()
        self.game_session = self.session.new_session()

    def test_pokersession_constructed(self):
        self.assertIsInstance(self.session, PokerSession)

    def test_get_session(self):
        session_id = self.session.new_session()
        self.assertIsNotNone(session_id)

    def test_sessions_have_different_ids(self):
        session_1 = self.session.new_session()
        session_2 = self.session.new_session()

        self.assertNotEqual(session_1, session_2)

    def test_sessions_stored(self):
        session_id = self.session.new_session()
        session_dict = self.session.sessions[session_id]

        self.assertIn(session_id, self.session.sessions)

    def test_assert_data_in_session(self):
        session_id = self.session.new_session()

        session_dict = self.session.sessions[session_id]

        print(session_dict)

        # test for data
        self.assertIsNotNone(session_dict['timestamp'])
        self.assertIsInstance(session_dict['deck'], Deck)
        self.assertIsNone(session_dict['hand'], Hand)

    def test_get_hand(self):
        hand = self.session.get_hand(self.game_session)

        self.assertIsInstance(hand, Hand)
        self.assertEqual(hand, self.session.sessions[self.game_session]['hand'])

    def test_get_score_discard_none(self):
        hand = self.session.get_hand(self.game_session)
        score_dict = self.session.get_score(self.game_session, [])

        self.assertTrue(len(score_dict['score_string']) > 0)
        self.assertTrue(len(score_dict['cards']) == 5)

    def test_get_score_discard_2(self):
        hand = self.session.get_hand(self.game_session)
        score_dict = self.session.get_score(self.game_session, [1, 2])

        self.assertTrue(len(score_dict['score_string']) > 0)
        self.assertTrue(len(score_dict['cards']) == 5)


if __name__ == '__main__':
    unittest.main()
