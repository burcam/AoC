
from typing import List


class Monkey:
    def __init__(self, id: int):
        self.id = id
    items: List[int] = []
    item_cnt = 0
    #received_items: List[int] = []
    operation_op: str
    operation_2nd: str
    test_div = 0
    true_throw: 'Monkey' = None
    false_throw: 'Monkey' = None
    def inspect_items(self):
        pass
    def test_items(self):
        item_cnt = len(self.items)
        for item in self.items:
            if item%self.test_div==0:
                self.true_throw.items.append(item)
            else:
                self.false_throw.items.append(item)
        self.items = []
        self.item_cnt += item_cnt
    def print(self):
        print(f"Monkey {self.id}:")
        print(f"    Starting items: {self.items}")
        print(f"    Operation: new = old {self.operation_op} {self.operation_2nd}")
        print(f"    Test: divisible by {self.test_div}")
        print(f"        If true: throw to monkey {self.true_throw.id}")
        print(f"        If false: throw to monkey {self.false_throw.id}")
        
k = 22192890720
def inspect_items1(monkey: Monkey):
    for item in monkey.items:
        n = item + item
        if n % monkey.test_div == 0:
            monkey.true_throw.items.append(n%k)
        else:
            monkey.false_throw.items.append(n%k)
    monkey.item_cnt += len(monkey.items)
    monkey.items = []
def inspect_items2(val: int):
    def temp(monkey: Monkey): 
        for item in monkey.items:
            n = item + val
            if n % monkey.test_div == 0:
                monkey.true_throw.items.append(n%k)
            else:
                monkey.false_throw.items.append(n%k)
        monkey.item_cnt += len(monkey.items)
        monkey.items = []
    return temp
def inspect_items3(monkey: Monkey):
    for item in monkey.items:
        n = item * item
        if n % monkey.test_div == 0:
            monkey.true_throw.items.append(n%k)
        else:
            monkey.false_throw.items.append(n%k)
    monkey.item_cnt += len(monkey.items)
    monkey.items = []
def inspect_items4(val: int):
    def temp(monkey: Monkey): 
        for item in monkey.items:
            n = item * val
            if n % monkey.test_div == 0:
                monkey.true_throw.items.append(n%k)
            else:
                monkey.false_throw.items.append(n%k)
        monkey.item_cnt += len(monkey.items)
        monkey.items = []
    return temp
with open("day11") as file:
    lines = file.readlines()
    monkeys: List[Monkey] = [Monkey(i) for i in range(8)]
    i = -1
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if line[0] == "M":
            i += 1
            continue
        if line[0] == "S":
            monkeys[i].items = [int(val) for val in line.split(": ")[1].split(", ")]
            continue
        if line[0] == "O":
            monkeys[i].operation_op = line[21]
            monkeys[i].operation_2nd = line[23:]
            continue
        if line[0] == "T":
            monkeys[i].test_div = int(line.split(" ")[-1])
            continue
        if not monkeys[i].true_throw:
            monkeys[i].true_throw = monkeys[int(line.split(" ")[-1])]
            continue
        monkeys[i].false_throw = monkeys[int(line.split(" ")[-1])]
for monkey in monkeys:
    if monkey.operation_op == "+":
        if monkey.operation_2nd == "old":
            monkey.inspect_items = inspect_items1
        else:
            monkey.inspect_items = inspect_items2(int(monkey.operation_2nd))
    else:
        if monkey.operation_2nd == "old":
            monkey.inspect_items = inspect_items3

        else:
            monkey.inspect_items = inspect_items4(int(monkey.operation_2nd))
for i in range(10000):
    for monkey in monkeys:
        monkey.inspect_items(monkey)
    if i%1000 == 0:
        print("1k passed")

monkeys.sort(key=lambda m: m.item_cnt, reverse=True)
print(monkeys[0].item_cnt*monkeys[1].item_cnt)