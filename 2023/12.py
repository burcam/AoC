from dataclasses import dataclass
from enum import Enum
from functools import lru_cache

class Condition(str, Enum):
    Unk = "?"
    Op = "."
    Dam = "#"

@dataclass
class Record:
    conditions: list[Condition] # actually a str
    dam_spring_groups: list[int]
    def __hash__(self) -> int:
        return hash((self.conditions, tuple(self.dam_spring_groups)))


def can_start_dam_group(conditions: list[Condition], idx: int, length:int):
    #print(conditions, idx, length)
    if conditions[idx] == Condition.Op:
        #print("No", conditions, idx, length)
        return False
    if idx != 0 and conditions[idx - 1] == Condition.Dam:
        #print("Nope", conditions, idx, length)
        return False
    if len(conditions) - idx < length:
        #print("Nada", conditions, idx, length)
        return False
    for i in range(idx, idx+length):
        if conditions[i] == Condition.Op:
            #print("Nuuh", conditions, idx, length)
            return False
    if len(conditions) > idx + length and conditions[idx+length] == Condition.Dam:
        return False
    
    return True

@lru_cache
def record_count(rec: Record):
    if not rec.conditions:
        if not rec.dam_spring_groups:
            return 1
        return 0
    if not rec.dam_spring_groups:
        for c in rec.conditions:
            if c == Condition.Dam:
                return 0
        return 1
    
    length = rec.dam_spring_groups[0]
    starters: list[int] = []
    for idx in range(len(rec.conditions)):
        if can_start_dam_group(rec.conditions, idx, length):
            starters.append(idx)
        if rec.conditions[idx] == Condition.Dam:
            break
    sums = 0
    for starter in starters:
        next_rec = Record(rec.conditions[starter+length+1:], rec.dam_spring_groups[1:])
        sums += record_count(next_rec)
    return sums
    

def execute():
    records: list[Record] = []
    with open("./12") as f:
        lines = [l.strip() for l in f.readlines()]
        for line in lines:
            conditions, dam_grps = line.strip().split(" ")
            rec = Record(conditions, [int(g) for g in dam_grps.split(",")])
            records.append(rec)
    sums = 0
    for rec in records:
        rec_sum = record_count(rec)
        sums += rec_sum
    print(sums)

execute()

def execute2():
    records: list[Record] = []
    with open("./12") as f:
        lines = [l.strip() for l in f.readlines()]
        for line in lines:
            conditions, dam_grps = line.strip().split(" ")
            conditions = conditions + "?" + conditions + "?" +conditions + "?" +conditions + "?" + conditions
            dam_grps = dam_grps + "," + dam_grps+ "," + dam_grps+ "," + dam_grps+ "," + dam_grps
            rec = Record(conditions, [int(g) for g in dam_grps.split(",")])
            records.append(rec)
    sums = 0
    for rec in records:
        rec_sum = record_count(rec)
        sums += rec_sum
    print(sums)

execute2()