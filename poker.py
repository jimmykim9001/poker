import numpy as np
class PokerHand:
    def __gt__(self, other):
        if self.hand_type > other.hand_type:
            return True
        elif self.hand_type == other.hand_type:
            return PokerHand.compare_lists(self.ordered_list, other.ordered_list) > 0
        else:
            return False
    def __lt__(self, other):
        if self.hand_type > other.hand_type:
            return False
        elif self.hand_type == other.hand_type:
            return PokerHand.compare_lists(self.ordered_list, other.ordered_list) < 0
        else:
            return True
    def __eq__(self, other):
        return self.hand_type == other.hand_type and \
                PokerHand.compare_lists(self.ordered_list, other.ordered_list) == 0

    def get_suits(deck):
        return np.sum(deck, axis = 1)
    def get_nums(deck):
        return np.sum(deck, axis = 0)
    def true_num(idx):
        if isinstance(idx, list) or isinstance(idx, np.ndarray):
            return [PokerHand.true_num(x) for x in idx]
        idx += 1
        if idx == 1:
            return 14
        else:
            return idx
    def get_idx(num):
        if num == 14:
            return 0
        return num - 1
    def get_kickers(nums, special_cards, n = 2):
        nonzero_nums = nums.nonzero()[0]
        nonzero_nums = [PokerHand.true_num(x) for x in nonzero_nums]
        nonzero_nums = sorted(nonzero_nums, reverse = True)
        others = []
        for elem in nonzero_nums:
            idx_elem = PokerHand.get_idx(elem)
            if idx_elem not in special_cards:
                for i in range(int(nums[idx_elem])):
                    others.append(elem)
        return others[:n]
    def compare_lists(list1, list2):
        assert(len(list1) == len(list2))
        eq_ct = 0
        for i in range(len(list1)):
            if list1[i] < list2[i]:
                return -1
            elif list1[i] == list2[i]:
                eq_ct += 1
        if eq_ct == len(list1):
            return 0
        return 1
    def convert_num_to_card(num):
        if isinstance(num, list):
            return [PokerHand.convert_num_to_card(x) for x in num]
        face = 'JQKA'
        if num > 10:
            return face[num - 11]
        else:
            return str(num)
class StraightFlush(PokerHand):
    def __init__(self, high_card):
        self.ordered_list = [high_card]
        self.hand_type = 8
    def is_instance(deck):
        sf_ct = []
        for i in range(9):
            sf_ct.append(np.sum(deck[:, i:i + 5], axis = 1).reshape((4, 1)))

        # royal flush exception
        royal_flush = np.hstack((deck[:, 0:1],deck[:, -4:]))
        sf_ct.append(np.sum(royal_flush, axis = 1).reshape((4, 1)))

        sf_ct = np.hstack(sf_ct)
        suit_idx, num_idx = np.greater(sf_ct, 4).nonzero()

        if suit_idx.shape[0] == 0:
            return False, None
        else:
            return True, StraightFlush(np.max(num_idx) + 5)
    def __str__(self):
        lst = [self.ordered_list[0] - 4, self.ordered_list[0]]
        return 'straight flush ({} to {})'.format(*PokerHand.convert_num_to_card(lst))
class Quads(PokerHand):
    def __init__(self, quad, kicker):
        self.ordered_list = [quad] + kicker
        self.hand_type = 7

    def is_instance(deck):
        num = PokerHand.get_nums(deck)
        quad_idx = (num == 4).nonzero()[0]
        if len(quad_idx) == 0:
            return False, None
        else:
            return True, Quads(PokerHand.true_num(quad_idx[0]), PokerHand.get_kickers(num, quad_idx, n = 1) )
    def __str__(self):
        return 'quads ({})'.format(PokerHand.convert_num_to_card(self.ordered_list[0]))

class FullHouse(PokerHand):
    def __init__(self, trips, pair):
        self.ordered_list = [trips, pair]
        self.hand_type = 6
    def is_instance(deck):
        num = PokerHand.get_nums(deck)
        trips_idx = (num == 3).nonzero()[0]
        pairs_idx = (num == 2).nonzero()[0]

        if len(trips_idx) == 0 or len(pairs_idx) == 0:
            return False, None
        else:
            return True, FullHouse(PokerHand.true_num(np.max(trips_idx)),
                                    PokerHand.true_num(np.max(pairs_idx)))
    def __str__(self):
        return 'full house ({} over {})'.format(*PokerHand.convert_num_to_card(self.ordered_list))
class Flush(PokerHand):
    def __init__(self, cards):
        assert(len(cards) == 5)
        self.ordered_list = sorted(cards, reverse = True)
        self.hand_type = 5
        
    def is_instance(deck):
        suits = PokerHand.get_suits(deck)
        suit_idx = np.greater(suits, 4).nonzero()[0]
        if len(suit_idx) == 0:
            return False, None
        else:
            nums = PokerHand.true_num(deck[suit_idx].nonzero()[1])
            nums = sorted(nums, reverse = True)
            return True, Flush(nums[:5])
    def __str__(self):
        return 'flush ({} high)'.format(PokerHand.convert_num_to_card(self.ordered_list[0]))

class Straight(PokerHand):
    def __init__(self, top_card):
        self.ordered_list = [top_card]
        self.hand_type = 4
    def is_instance(deck):
        num = PokerHand.get_nums(deck)
        num[num > 0] = 1
        straight_ct = []
        for i in range(9):
            straight_ct.append(np.sum(num[i:i + 5]))
        broad_straight = np.hstack((num[0:1], num[-4:]))
        straight_ct.append(np.sum(broad_straight))

        num_idx = np.greater(straight_ct, 4).nonzero()[0]
        if num_idx.shape[0] == 0:
            return False, None
        else:
            return True, Straight(PokerHand.true_num(np.max(num_idx) + 4))
    def __str__(self):
        lst = [self.ordered_list[0] - 4, self.ordered_list[0]]
        if lst[0] == 1:
            lst[0] = 14
        return 'straight ({} to {})'.format(*PokerHand.convert_num_to_card(lst))
class Triple(PokerHand):
    def __init__(self, trip, kickers):
        self.ordered_list = [trip] + sorted(kickers, reverse = True)
        self.hand_type = 3
    def is_instance(deck):
        num = PokerHand.get_nums(deck)
        triple_idx = (num == 3).nonzero()[0]
        if triple_idx.shape[0] == 0:
            return False, None
        else:
            triple_idx = [np.max(triple_idx)]
            kickers= PokerHand.get_kickers(num, triple_idx, n = 2)
            return True, Triple(PokerHand.true_num(triple_idx[0]), kickers)
    def __str__(self):
        return 'triple ({})'.format(PokerHand.convert_num_to_card(self.ordered_list[0]))
class TwoPair(PokerHand):
    def __init__(self, pairs, kickers):
        self.ordered_list = sorted(pairs, reverse = True) + sorted(kickers, reverse = True)
        self.hand_type = 2
    def is_instance(deck):
        nums = PokerHand.get_nums(deck)
        pairs_idx = (nums == 2).nonzero()[0]
        if pairs_idx.shape[0] < 2:
            return False, None
        kickers = PokerHand.get_kickers(nums, pairs_idx, n = 1)
        return True, TwoPair(PokerHand.true_num(pairs_idx[:2]), kickers)
    def __str__(self):
        return 'two pair ({}, {})'.format(*PokerHand.convert_num_to_card(self.ordered_list[:2]))
class Pair(PokerHand):
    def __init__(self, pair_num, kickers):
        self.ordered_list = [pair_num] + sorted(kickers, reverse = True)
        self.hand_type = 1
    def is_instance(deck):
        nums = PokerHand.get_nums(deck)
        pairs_idx = (nums == 2).nonzero()[0]
        if pairs_idx.shape[0] == 0:
            return False, None
        kickers = PokerHand.get_kickers(nums, pairs_idx, n = 3)
        return True, Pair(PokerHand.true_num(pairs_idx[0]), kickers)
    def __str__(self):
        return 'pair ({})'.format(PokerHand.convert_num_to_card(self.ordered_list[0]))
    
class HighCard(PokerHand):
    def __init__(self, kickers):
        self.ordered_list = sorted(kickers, reverse = True)
        self.hand_type = 0
    def is_instance(deck):
        nums = PokerHand.get_nums(deck)
        return True, HighCard(PokerHand.get_kickers(nums, [], n = 5))
    def __str__(self):
        return 'high card ({})'.format(PokerHand.convert_num_to_card(self.ordered_list[0]))


class Card:
    suits = ['diamonds', 'clubs', 'hearts', 'spades']
    def __init__(self, suit, num):
        assert(suit in Card.suits)
        self.suit = suit
        self.suit_idx = Card.suits.index(suit)
        self.num = num
        self.num_idx = num - 1

    def from_num(num):
        return Card(Card.suits[num // 13], (num % 13) + 1)
    def __str__(self):
        return PokerHand.convert_num_to_card(PokerHand.true_num(self.num_idx)) +\
                Card.suits[self.suit_idx][0]

class Hand:
    order = [HighCard, Pair, TwoPair, Triple, Straight, Flush, FullHouse, Quads, StraightFlush]
    def __init__(self, hole_cards, public_cards):
        self.deck = np.zeros((4, 13))
        self.cards = hole_cards + public_cards
        assert(len(self.cards) == 7)
        self._setup_deck()
    def _setup_deck(self):
        for card in self.cards:
            self.deck[card.suit_idx, card.num_idx] = 1
        self.value = None
        for card_type in Hand.order[::-1]:
            is_instance, res = card_type.is_instance(self.deck)
            if is_instance:
                self.value = res
                break
    def __lt__(self, other):
        return self.value < other.value
    def __eq__(self, other):
        return self.value == other.value
    def __gt__(self, other):
        return self.value > other.value
    def __str__(self):
        return str(self.value)

# 1 <= num1, num2 <= 13
def test(num1, num2, suited = True, n = 1000, num_players = 2):
    num1, num2 = num1 - 1, num2 - 1
    if num1 == num2:
        assert(not suited)
    if not suited:
        num2 += 13
    all_others = [x for x in range(52) if x != num1 and x != num2]
    ct = 0
    for test_idx in range(n):
        deck = np.array(all_others)
        hole_cards1 = [Card.from_num(num1), Card.from_num(num2)]

        np.random.seed(test_idx)
        cards = np.random.choice(deck, 7, replace = False)
        # all_holecards = [[Card.from_num(y) for y in cards[2*x:2*(x+1)] ] for x in range(num_players - 1)]
        hole_cards2 = [Card.from_num(x) for x in cards[:2]]
        public_cards = [Card.from_num(x) for x in cards[2:]]

        hand1 = Hand(hole_cards1, public_cards)
        hand2 = Hand(hole_cards2, public_cards)

        if (hand1 > hand2):
            ct += 1

    return ct / n

import itertools
from itertools import product
res = np.zeros((13, 13))
from tqdm import tqdm
for i, j in tqdm(itertools.product(list(range(13)), list(range(13)))):
    res[i, j] = test(i + 1, j + 1, suited = i < j, n = 5000)
np.save('pockets_two_people.npy', res)
print(res)



# # test pocket aces
# non_aces = [x for x in range(52) if x != 0 and x != 13]
# ct = 0
# for test_idx in range(1000):
#     deck = np.array(non_aces)
#     hole_cards1 = [Card.from_num(0), Card.from_num(13)]
#
#     np.random.seed(test_idx)
#     cards = np.random.choice(deck, 7, replace = False)
#     hole_cards2 = [Card.from_num(x) for x in cards[:2]]
#     public_cards = [Card.from_num(x) for x in cards[2:]]
#
#     hand1 = Hand(hole_cards1, public_cards)
#     hand2 = Hand(hole_cards2, public_cards)
#
#     if (hand1 > hand2):
#         ct += 1
# print(ct / 1000)

