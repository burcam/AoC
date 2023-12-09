from enum import Enum


class HandTypes(int, Enum):
    high=0
    pair=1
    twopair=2
    three=3
    full=4
    four=5
    five=6

def get_hand_val(hand: str):
    groups: dict[str, int] = {}
    dupes = set('J')
    for i in range(len(hand)-1):
        if hand[i] in dupes:
            continue
        for j in range(i+1, len(hand)):
            if hand[i] == hand[j]:
                a = groups.get(hand[i], 0)
                if a:
                    groups[hand[i]] = a+1
                else:
                    groups.setdefault(hand[i], 2)
                dupes.add(hand[i])
    return groups

def get_hand_type(groups: dict[str, int]):
    glen = len(groups)
    if not groups:
        return HandTypes.high
    
    if glen == 1:
        hlen = next( b for b in groups.values())
        if hlen == 5:
            return HandTypes.five
        if hlen == 4:
            return HandTypes.four
        if hlen == 3:
            return HandTypes.three
        return HandTypes.pair
    for b in groups.values():
        if b == 3:
            return HandTypes.full
    return HandTypes.twopair

def update_hand(type: HandTypes, hand: str):
    j = 0
    for h in hand:
        if h == "J":
            j+=1
    # 4-kind
    if type == HandTypes.four:
        return HandTypes.five
    
    # 3-kind
    if type == HandTypes.three:
        if j == 1:
            return HandTypes.four
        return HandTypes.five
    # pair
    if type == HandTypes.pair:
        if j == 1:
            return HandTypes.three
        if j == 2:
            return HandTypes.four
        return HandTypes.five
    #high
    if type == HandTypes.high:
        if j == 1:
            return HandTypes.pair
        if j == 2:
            return HandTypes.three
        if j == 3:
            return HandTypes.four
        return HandTypes.five
    #two pair
    return HandTypes.full

with open("./7") as file:
    lines = file.readlines()
    count = len(lines)
    hand_vals: list[tuple[list[int], int]] = []
    for line in lines:
        hand, bid = line.strip().split(" ")
        bid = int(bid)
        hand_group = get_hand_val(hand)
        hand_type = get_hand_type(hand_group)
        if 'J' in hand:
            hand_type = update_hand(hand_type, hand)
        hand_breaker = [hand_type]
        for h in hand:
            if h == 'T':
                hand_breaker.append(10)
                continue
            if h == 'Q':
                hand_breaker.append(12)
                continue
            if h == 'K':
                hand_breaker.append(13)
                continue
            if h == 'A':
                hand_breaker.append(14)
                continue
            if h == 'J':
                hand_breaker.append(1)
                continue
            hand_breaker.append(int(h))
        hand_vals.append((hand_breaker, bid))
    ordered = sorted(hand_vals, key=lambda x: x[0])
    t_win = 0
    rank = 1
    for o in ordered:
        t_win += rank*o[1]
        rank += 1
    print(t_win)