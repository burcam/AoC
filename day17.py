with open("day17") as file:
    input = file.readline().strip()
def infinite_iterator(iterable):
    while(True):
        for item in iterable:
            yield item
class Shape():
    