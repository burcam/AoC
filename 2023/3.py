import re


with open("./3") as f:
    num_matches = []
    sym_matches = []
    line_num = 0
    for line in f.readlines():
        line = line.strip()
        nums = re.finditer("[0-9]+", line)
        for num in nums:
            num_matches.append((line_num, num.start(), num.end()-1, num.group()))
        syms = re.finditer("[^0-9.]", line)
        for sym in syms:
            sym_matches.append((line_num, sym.start()))
        line_num += 1
    total = 0
    for num in num_matches:
        found = False
        for y in range(num[0]-1,num[0]+2):
            for x in range(num[1]-1,num[2]+2):
                if (y, x) in sym_matches:
                    total += int(num[3])
                    found = True
                    break
            if found:
                break
    print(total)

with open("./3") as f:
    num_matches = {}
    sym_matches = []
    line_num = 0
    for line in f.readlines():
        line = line.strip()
        nums = re.finditer("[0-9]+", line)
        for num in nums:
            for x in range(num.start(), num.end()):
                num_matches.setdefault((line_num, x), num.group())
        syms = re.finditer("[*]", line)
        for sym in syms:
            sym_matches.append((line_num, sym.start()))
        line_num += 1
    total = 0
    print(num_matches)
    print(sym_matches)
    for sym in sym_matches:
        links = []
        for y in range(sym[0]-1, sym[0]+2):
            if len(links) > 2:
                links = []
                break
            x = sym[1]-1
            while x < sym[1]+2:
                if (y, x) in num_matches:
                    links.append(int(num_matches[(y,x)]))
                    if (y, x+1) in num_matches:
                        x += 1
                        if (y, x+1) in num_matches:
                            x += 1
                x+=1
        if len(links)==2:
            total += links[0]*links[1]
            
    print(total)