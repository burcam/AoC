#aame 1: 7 blue, 4 red, 11 green; 2 red, 2 blue, 7 green; 2 red, 13 blue, 8 green; 18 blue, 7 green, 5 red
r=12
g=13
b=14
with open("2.txt") as f:
    game=1
    sum=0
    for line in f.readlines():
        line=line.strip()
        _, sets = line. split(":")
        subgames = sets. split(";")
        a=True
        for sub in subgames :
            values = sub.split(",")
            blue,red, green=-1,-1,-1
            for value in values:
                value=value. strip()
                target=int(value. split(" ")[0])
                if "blu" in value:
                    if target>b:
                        break
                    blue=target
                elif "re" in value:
                    if target>r:
                        break
                    red=target
                else:
                    if target>g:
                        break
                    green=target
            if red==-1 or green==-1 or blue==-1:
                a=False
                break
        if a:
            sum+=game
        game +=1
print(sum)

