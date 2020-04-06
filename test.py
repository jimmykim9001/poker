from poker import *

import time
for i in range(10):
    deck = np.arange(52)
    np.random.seed(i)
    cards = np.random.choice(deck, 9, replace = False)
    hole_card1 = [Card.from_num(x) for x in cards[:2]]
    hole_card2 = [Card.from_num(x) for x in cards[2:4]]
    public_cards = [Card.from_num(x) for x in cards[4:]]

    print("======= start round {} ======".format(str(i)))
    print('hand 1 {}, hand 2 {}, public {}'.format(str([str(x) for x in hole_card1]), \
            str([str(x) for x in hole_card2]), str([str(x) for x in public_cards])))

    hand1 = Hand(hole_card1, public_cards)
    hand2 = Hand(hole_card2, public_cards)
    print('hand 1 kicker: {}'.format(str(hand1.value.ordered_list)))
    print('hand 2 kicker: {}'.format(str(hand2.value.ordered_list)))
    print('hand 1 ({}) hand 2 ({})'.format(str(hand1), str(hand2)))

    if (hand1 > hand2):
        print('hand 1 wins')
    elif (hand1 == hand2):
        print('tie')
    else:
        print('hand 2 wins')
    print("======= end round {} ======\n".format(str(i)))
