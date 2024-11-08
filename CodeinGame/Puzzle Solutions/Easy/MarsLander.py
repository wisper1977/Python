N = int(input())
for i in range(N):
    inputs = input().split()

while True:
    inputs = input().split()
    VS = int(inputs[3])

    if VS <= -40:
        print("0 4")
    else:
        print("0 0")
