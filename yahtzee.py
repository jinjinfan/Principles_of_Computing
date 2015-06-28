"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(150)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: sorted tuple representing a full Yahtzee hand

    Returns an integer score
    """
    max_score = 0
    score_result = 0
    hand_item = 0
    for hand_idx in range(len(hand)):
        if hand_item != hand[hand_idx]:
            hand_item = hand[hand_idx]
            score_result = hand_item
        else:
            score_result += hand[hand_idx]
        if score_result > max_score:
            max_score = score_result
    return max_score

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: a sorted tuple representing dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    score_total = 0
    free_roll_orders = gen_all_sequences(range(1,num_die_sides+1), num_free_dice)
    # for every possible free roll combination
    for free_roll in free_roll_orders:
        dice_order = list(held_dice + free_roll)
        dice_order.sort()
        dice_sorted = tuple(dice_order)
        score_total += score(dice_sorted)
    return float(score_total) /float(len(free_roll_orders))

def verify_if_sublist(list_, sub_list):
    """
    Verify whether a list is a sublist of another list

    list_ : the main list

    sub_list: the list needed to be verified

    Returns True if is a sublist
    """
    for item in sub_list:
        if sub_list.count(item) > list_.count(item):
            return False
    return True

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: sorted tuple representing a full Yahtzee hand

    Returns a set of sorted tuples, where each tuple is dice to hold
    """
    answer_set = set([()])
    answer_result = set([()])
    for dummy_idx in range(len(hand)-1):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in hand:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                new_sequence.sort()
                if verify_if_sublist(list(hand),new_sequence):
                    temp_set.add(tuple(new_sequence))
        answer_set = temp_set
        for sequence in answer_set:
            answer_result.add(sequence)
    answer_result.add(hand)
    return answer_result

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: sorted tuple representing a full Yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    possible_holds = gen_all_holds(hand)
    possible_holds_sorted = [tuple(sorted(sequence)) for sequence in possible_holds]
    print possible_holds_sorted
    hand_len = len(hand)
    dict_result = {}
    max_value = 0
    for possible_hold in possible_holds:
        hold_len = len(possible_hold)
        expectvalue = expected_value(possible_hold, num_die_sides, hand_len-hold_len)
        if expectvalue > max_value:
            max_value = expectvalue
        dict_result[expectvalue] = possible_hold
    return (max_value, dict_result[max_value])

#def run_example():
#    num_die_sides = 6
#    hand = (1,)
    #hand_score, hold = strategy(hand, num_die_sides)
    #print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score

#run_example()
