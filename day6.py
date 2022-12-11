print("Start")
mlen = 14
with open("day6_") as file:
    for line in file:
        i = 0
        while i < len(line):
            no_match = True
            for j in range(mlen):
                for k in range(1, mlen - j):
                    if line[i + j] == line[i + j + k]:
                        no_match = False
                        break
                if not no_match:
                    break
            if (
                no_match
            ):
                print(i + mlen)
                break
            i += 1
        break