from random import shuffle


class Card:
    suits = ('\u2660', '\u2665', '\u2666', '\u2663')

    values = (None, None, "2", "3",
        "4", "5", "6", "7", "8", "9", "10",
        "J", "Q", "K", "A")

    def __init__(self, v, s):
        self.value = v
        self.suit = s

    def __lt__(self, c2):
        if self.value < c2.value:
            return True
        if self.value == c2.value:
            if self.suit < c2.suit:
                return True
        else:
            return False

    def __gt__(self, c2):
        if self.value > c2.value:
            return True
        if self.value == c2.value:
            if self.suit > c2.suit:
                return True
            else:
                return False
        return False

    def card_string(self):
        v = self.values[self.value] +self.suits[self.suit]
        return v

    def __str__(self):
        return self.card_string()

    def __repr__(self):
        return self.card_string()


class Deck:
    def __init__(self):
        self.cards = []
        self.discard_pile = []

        # populate the deck
        for i in range(2, 15):
            for j in range(4):
                self.cards.append(Card(i, j))

        # shuffle the deck
        shuffle(self.cards)

    def draw(self):
        """Draw one card from cards pile."""
        if len(self.cards) == 0 and len(self.discard_pile) > 0:
                # set the draw pile to the discard_pile
                self.cards = self.discard_pile
                self.discard_pile = []
                shuffle(self.cards)

        # There should always be a card to pop
        return self.cards.pop()

    def discard(self, card):
        """Return card to deck. Discarded card always goes to the discard pile."""
        self.discard_pile.append(card)


class Hand:
    def __init__(self, deck):
        self.scored = False
        self.cards = []

        # get cards
        for _ in range(5):
            card = deck.draw()
            self.cards.append(card)

    def discard(self, indices, deck):
        """indices must be a list of integers 0-5, and cannot
        exceed a length of 4. Length of list can be 0."""
        try:
            n = len(indices)
            if n > 4:
                raise ValueError

            if n == 0:
                return

            for index in indices:
                if index > 5 or index < 0:
                    raise ValueError
                else:
                    # discard cards at index
                    deck.discard(self.cards[index])
                    # replace items at index with another card
                    self.cards[index] = deck.draw()

            self.scored = True

        except ValueError:
            return "Invalid Index"

    def score(self, deck):
        """Score the hand and replace the cards to the discard pile."""
        # get histogram
        histogram = self.get_histogram()
        # sort the list of histogram keys by rank, in ascending order
        keys = sorted(histogram.items(),key=lambda x: x[1], reverse=True)
        number_indices = len(keys)
        score_string = ""

        # start scoring
        if number_indices == 2:
            if keys[0][1] == 4 and keys[1][1] == 1:
                score_string = "Four of a Kind"
            else:
                score_string = "Full House"
        if number_indices == 3:
            if keys[0][1] == 3:
                score_string = "Three of a Kind"
            else:
                score_string = "Two Pair"
        if number_indices == 4:
            score_string = "One Pair"
        if number_indices == 5:
            # check for flush
            flush = self.is_flush()
            straight = False
            # get a sorted list of cards
            straight_cards = sorted(self.cards)

            # if a 5 is in the bottom and and Ace is high, the Ace turns to a
            #   1, making the hand a straight
            if straight_cards[4].value == 14 and straight_cards[3].value == 5:
                straight = True
            # If the difference between the high and low card is 4, it is a
            #   straight
            elif straight_cards[4].value - straight_cards[0].value == 4:
                straight = True
            else:
                straight = False

            # Determine the score string of the straight cards
            if straight and flush and straight_cards[0].value == 10:
                score_string = "Royal Flush"
            elif straight and flush:
                score_string = "Straight Flush"
            elif straight:
                score_string = "Straight"
            elif not straight and straight_cards[4].value == 14:
                straight = False
                score_string = "Ace High"
            else:
                score_string = "High Card:" + str(straight_cards[4])

        # copy cards
        display_cards = self.cards[:]
        # replace the cards to the discard pile
        for card in self.cards:
            deck.discard(card)

        # return score string
        return {"cards": display_cards, "score_string": score_string}

    def is_flush(self):
        first_card = self.cards[0]
        for card in self.cards[1:]:
            if first_card.suit != card.suit:
                return False

        return True

    def get_histogram(self):
        """Get a histogram of the cards."""
        histogram = {}

        for card in self.cards:
            if card.value in histogram:
                histogram[card.value] += 1
            else:
                histogram[card.value] = 1

        return histogram


    def __str__(self):
        """String representing a hand. Displays cards separated by pipe."""
        v = "Hand: "

        for card in self.cards:
            v += "|" + str(card)

        v += "|"

        return v


if __name__ == '__main__':
    deck = Deck()

    while True:
        # deal cards and display them
        hand = Hand(deck)
        print(hand)
        # get a list of integer from the standard input. out_cards is the list
        # of strings to be processed for input (in_cards) to the hand object.
        cards = input("Input which cards you would like to discard (1-5) separated by space,\
            return if none:")
        if cards == "":
            # If player does not wish to discard anything, return out_cards as empty list
            out_cards = []
        else:
            try:
                # out_cards holds card indices to be discarded.
                out_cards = []
                # in_cards holds an array of strings to convert to ints
                in_cards = cards.split(" ")
                for card in in_cards:
                    card = int(card)
                    if card < 0 or card > 5:
                        raise ValueError
                    else:
                        out_cards.append(int(card) - 1)
            except ValueError:
                print("INPUT: Card must be an number between 1 and 5")
        hand.discard(out_cards, deck)
        score_dict = hand.score(deck)
        
        # print hand
        
        for card in score_dict["cards"]:
            print('|', end='')
            print(card, end='')
        print('|')
        
        # print score string
        print(score_dict["score_string"])

        # input for play again
        again = input("Would you like to play again? y/n: ")
        if again == 'n':
            break
