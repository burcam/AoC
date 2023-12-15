

# Determine the ASCII code for the current character of the string.
from collections import OrderedDict


def toCode(char: str):
    return ord(char)

# Set the current value to itself multiplied by 17.
def mult(total: int):
    return total*17
# Set the current value to the remainder of dividing itself by 256.
def rem(total: int):
    return total % 256

def execute():
    with open ("./15") as file:
        line = file.readline()
    steps = line.split(",")
    total = 0
    for step in steps:
        step_tot = 0
        for char in step:
            step_tot += toCode(char)
            step_tot = rem(mult(step_tot))
        total += step_tot
    print(total)
execute()

def get_hash(label: str):
    step_tot = 0
    for char in label:
        step_tot += toCode(char)
        step_tot = rem(mult(step_tot))
    return step_tot


#If the operation character is a dash (-),
# go to the relevant box and remove the lens with the given label
# if it is present in the box. Then, move any remaining lenses as far
# forward in the box as they can go without changing their order, 
#filling any space made by removing the indicated lens. 
#(If no lens in that box has the given label, nothing happens.)
def dash_op(label: str, boxes: dict[int, list[str]]):
    label_hash = get_hash(label)
    try:
        box = boxes.get(label_hash)
        box.remove(label)
    except:
        ...

def eq_op(label: str, boxes: dict[int, list[str]]):
    label_hash = get_hash(label)
    box = boxes.get(label_hash)
    if label not in box:
        box.append(label)

def execute2():
    with open ("./15") as file:
        line = file.readline()
    steps = line.split(",")
    box_list: dict[int, list[str]] = OrderedDict()
    for i in range(256):
        box_list[i] = []
    lens_focal: dict[str, int] = {}
    for step in steps:
        if step[-1] == "-":
            dash_op(step[:-1], box_list)
        else:
            label, focal = step.split("=")
            eq_op(label, box_list)
            lens_focal[label] = int(focal)
    total = 0
    for box_idx, box in box_list.items():
        box_power = box_idx + 1
        box_total = 0
        lens_slot = 1
        for lens in box:
            box_total += box_power * lens_slot * lens_focal[lens]
            lens_slot+=1
        total += box_total
    print(total)

execute2()