#aame 1: 7 blue, 4 red, 11 green; 2 red, 2 blue, 7 green; 2 red, 13 blue, 8 green; 18 blue, 7 green, 5 red
r=12
g=13
b=14
with open("./2.txt") as f:
    game=1
    tot=0
    for line in f.readlines():
        line=line.strip()
        
        _, sets = line. split(":")
        subgames = sets. split(";")
        a=True
        
        for sub in subgames :
            values = sub.split(",")
            for value in values:
                values=value. strip().split(" ")
                target=int(values[0])
                if values[1]=="blue":
                    if target>b:
                        a = False
                        break
                elif values[1]=="red":
                    if target>r:
                        a = False
                        break
                else:
                    if target>g:
                        a = False
                        break
            if not a:
                break
        if a:
            tot+=game
        game +=1
print(tot)


with open("./2.txt") as f:
    tot=0
    for line in f.readlines():
        line=line.strip()
        
        _, sets = line. split(":")
        subgames = sets. split(";")
        rm = 0
        gm = 0
        bm = 0
        for sub in subgames :
            values = sub.split(",")
            for value in values:
                vals=value. strip().split(" ")
                target=int(vals[0])
                if vals[1]=="blue":
                    if bm<target:
                        bm=target
                elif vals[1]=="red":
                    if target>rm:
                        rm = target
                else:
                    if target>gm:
                        gm = target
        tot += rm*gm*bm
print(tot)