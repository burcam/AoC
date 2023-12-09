from math import ceil, floor, sqrt


with open("./6") as f:
    times = [int(l) for l in f.readline().split(":")[1].strip().split(" ") if l]
    distances = [int(l) for l in f.readline().split(":")[1].strip().split(" ") if l]
    races = 1
    for i in range(len(times)):
        half = times[i]/2.0
        partner = half
        if half != int(half):
            half = ceil(half)
            partner = half - 1
            c = 0
        else:
            c = 0
        while half*partner > distances[i]:
            c += 1
            half += 1
            partner -= 1
        if times[i] % 2:
            c = 2*c
        else:
            c = 2*c - 1
        races *= c
    print(races)

with open("./6") as f:
    times = [l for l in f.readline().split(":")[1].strip().split(" ") if l]
    distances = [l for l in f.readline().split(":")[1].strip().split(" ") if l]
    time = ""
    for t in times:
        time += t
    time = int(time)
    distance = ""
    for t in distances:
        distance += t
    distance = int(distance)
    half = time/2.0
    partner = half
    if half != int(half):
        half = ceil(half)
        partner = half - 1
    c = 0
    while half*partner > distance:
        c += 1
        half += 1
        partner -= 1
    if time % 2:
        c = 2*c
    else:
        c = 2*c - 1
    print(c)