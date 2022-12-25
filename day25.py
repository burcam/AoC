from dataclasses import dataclass
from enum import Enum
import functools
from math import ceil
from queue import Queue
import re
import time
from typing import Dict, List, Set, Tuple

with open("day25") as file:
    lines = file.readlines()
sum = 0
for line in lines:
    line = line.strip()
    for index, char in enumerate(reversed(line)):
        if "0" <= char <= "2":
            sum += int(char) * pow(5, index)
        elif char == "-":
            sum -= pow(5, index)
        else:
            sum -= 2*pow(5, index)
snafu = ""
print(sum)
max_pow = 1
while pow(5, max_pow) < sum:
    max_pow += 1
max_pow -= 1
base_5_rep = ""
while max_pow > -1:
    cur_pow = pow(5, max_pow)
    cur_val = sum//cur_pow
    base_5_rep += str(cur_val)
    sum -= cur_val*cur_pow
    max_pow -= 1
print(base_5_rep)

inc = False
for val in reversed(base_5_rep):
    if inc:
        val = str(int(val) + 1)
        if val == "5":
            val = "0"
            inc = True
        else:
            inc = False

    if "0" <= val <= "2":
        snafu = val + snafu
    elif val == "3":
        snafu = "=" + snafu
        inc = True
    elif val == "4":
        snafu = "-" + snafu
        inc = True

sum2 = 0
for index, char in enumerate(reversed(snafu)):
    if "0" <= char <= "2":
        sum2 += int(char) * pow(5, index)
    elif char == "-":
        sum2 -= pow(5, index)
    else:
        sum2 -= 2*pow(5, index)

print(snafu)
print(sum2)