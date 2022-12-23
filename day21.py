from dataclasses import dataclass
from enum import Enum
import functools
from math import ceil
import re
import time
from typing import Dict, List, Set, Tuple

with open("day21") as file:
    lines = file.readlines()
@dataclass
class Monkey():
    name: str
    def get_value(self) -> int:
        pass
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Monkey) and self.name == __o.name
    def print(self):
        pass
@dataclass
class FixedMonkey(Monkey):
    value: int
    def get_value(self) -> int:
        return self.value
    def print(self):
        print(self.name, self.value)
@dataclass
class EquationMonkey(Monkey):
    left: Monkey|str
    right: Monkey|str
    operation: str
    _value: int
    def get_value(self) -> int:
        if self._value is not None:
            return self._value
        if self.operation == "+":
            self._value = self.left.get_value() + self.right.get_value()
        if self.operation == "-":
            self._value = self.left.get_value() - self.right.get_value()
        if self.operation == "*":
            self._value = self.left.get_value() * self.right.get_value()
        if self.operation == "/":
            self._value = self.left.get_value() / self.right.get_value()
        return self._value
    def print(self):
        if self._value is not None:
            print(self.name, f"{self.left.name} {self.operation} {self.right.name} = {self._value}")
        else:
            print(self.name, f"{self.left.name} {self.operation} {self.right.name}")
monkeys: Dict[str, Monkey] = {}
eq_monkeys: List[EquationMonkey] = []
for line in lines:
    m1: Tuple[str] = re.match("^(.*): (.*)$", line.strip()).groups()
    if m1[1].isnumeric():
        monkeys.setdefault(m1[0], FixedMonkey(m1[0], int(m1[1])))
    else:
        m2: Tuple[str] = re.match("^(.*) (.) (.*)$", m1[1]).groups()
        monkeys.setdefault(m1[0], EquationMonkey(m1[0], m2[0], m2[2], m2[1], None))
        eq_monkeys.append(monkeys[m1[0]])
for monkey in monkeys.values():
    if isinstance(monkey, EquationMonkey):
        monkey.left = monkeys[monkey.left]
        monkey.right = monkeys[monkey.right]

print(monkeys["root"].get_value())

for monkey in eq_monkeys:
    monkey._value = None
human: FixedMonkey = monkeys["humn"]

min_value = 1000000000000
max_value = 10000000000000
average = (max_value + min_value)//2
human.value = (max_value + min_value)//2
root_value = monkeys["root"].get_value()

while(root_value != 0):

    for monkey in eq_monkeys:
        monkey._value = None
    root_value = monkeys["root"].get_value()
    print(human.value, root_value)
    if root_value > 0:
        min_value = human.value+1
    elif root_value < 0:
        max_value = human.value-1
    else:
        break
    ohv = human.value
    human.value = (max_value + min_value)//2
    if human.value == ohv:
        human.value += 1
    
print(monkeys["humn"].get_value())