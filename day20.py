from dataclasses import dataclass
from enum import Enum
import functools
from math import ceil
import re
import time
from typing import Dict, List, Set, Tuple

@dataclass
class Link():
    previous: 'Link'
    next: 'Link'
    value: int
    shift_val: int
    def __repr__(self) -> str:
        return f"{self.value}_{self.previous.value}_{self.next.value}"
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Link) and self.value == __o.value
def print_links(link: Link):
    line = f"{link.value}"
    next_link = link.next
    while(next_link != link):
        line += f", {next_link.value}"
        next_link = next_link.next
    return line

with open("day20") as file:
    lines = file.readlines()
initial: List[Link] = []

length = len(lines)
for line in lines:
    line = line.strip()
    value = int(line)*811589153
    shift_val = value%length + value//length
    while shift_val > length or shift_val < 0:
        shift_val = shift_val%length + shift_val//length
    initial.append(Link(None, None, value, shift_val))

for index, link in enumerate(initial):
    link.previous = initial[index-1]
    link.next = initial[(index+1)%length]
    if link.value == 0:
        print("Zero found!")
        zero_link = link

for i in range(10):
    for link in initial:
        shift = link.shift_val
        if shift > 0:
            working = link
            link.previous.next = link.next
            link.next.previous = link.previous
            for i in range(shift):
                working = working.next
            link.previous = working
            link.next = working.next
            
            link.next.previous = link
            link.previous.next = link
        if shift < 0:
            working = link
            link.previous.next = link.next
            link.next.previous = link.previous
            for i in range(-shift):
                working = working.previous    
            link.next = working
            link.previous = working.previous
            
            link.next.previous = link
            link.previous.next = link

root = zero_link
t_vals = []
for i in range(3001):
    if i == 1000 or i == 2000 or i == 3000:
        print(i, root.value)
        t_vals.append(root.value)
    root = root.next

print(sum(t_vals))
#8764
#-12418125630053