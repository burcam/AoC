from typing import List

total_space = 70000000
required_space = 30000000
print("Start")
mlen = 14
class Dir:
    key: str
    size: int
    item_size: int
    children: List['Dir']
    prev: 'Dir'
    def __init__(self, key, size, item_size, children, prev):
        self.key = key
        self.size = size
        self.item_size = item_size
        self.children = children
        self.prev = prev
    def update_size(self):
        size = 0
        for child in self.children:
            child.update_size()
            size += child.size
        self.size = size + self.item_size
with open("day7") as file:
    root_dir = Dir(key="/", size=0, children=[], prev=None, item_size=0)
    lsd_dirs = []
    activeCommand = ""
    currentDirectory = root_dir
    item_count = 0
    for line in file:
        line = line.strip()
        if line[0] == "$":
            if activeCommand == "ls":
                lsdd = currentDirectory.key
                prev = currentDirectory.prev
                while(prev):
                    lsdd += prev.key
                    prev= prev.prev
                lsd_dirs.append(lsdd)
            if line[2] == "c":
                activeCommand = ""
                if line[5] == "/" and len(line) == 6:
                    currentDirectory = root_dir
                    continue
                if line[5] == "." and line[6] == ".":
                    currentDirectory = currentDirectory.prev
                    continue
                else:
                    for child in currentDirectory.children:
                        if child.key == line[5:]:
                            currentDirectory = child
                            break
                    else:
                        child = Dir(key=line[5:], size=0, children=[], prev=currentDirectory, item_size=0)
                        currentDirectory.children.append(child)
                        currentDirectory = child
                    continue
            if line[2] == "l":
                lsdd = currentDirectory.key
                prev = currentDirectory.prev
                while(prev):
                    lsdd += prev.key
                    prev = prev.prev
                if lsdd in lsd_dirs:
                    activeCommand = "skip"
                else:
                    activeCommand = "ls"
                continue
        if activeCommand == "ls":
            if line[0] == "d":
                new_dir = Dir(key=line[4:], size=0, children=[], prev=currentDirectory, item_size=0)
                for child in currentDirectory.children:
                    if child.key == line[5:]:
                        break
                else:
                    currentDirectory.children.append(new_dir)
                continue
            currentDirectory.item_size += int(line.split(" ")[0])
        else:
            print("?")
root_dir.update_size()
sizes = 0
min_dir_size = root_dir.size
space_left = total_space - root_dir.size
required_space = required_space - space_left
def tot_sizes(dir: Dir, min_size: int):

    if dir.size < min_size and dir.size >= required_space:
        min_size = dir.size
    for child in dir.children:
        min_size = tot_sizes(child, min_size)
    return min_size
print(tot_sizes(root_dir, min_dir_size))