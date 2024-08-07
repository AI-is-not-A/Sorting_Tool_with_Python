data = []
while True:
    try:
        for number in input().split():
            if number != "":
                data.append(int(number))
    except EOFError:
        break

data.sort()
X = len(data)
Y = data[-1]
Z = data.count(data[-1])

print(f"Total numbers: {X}.\nThe greatest number: {Y} ({Z} time(s)).")