a = open('a.txt', 'r').readlines()
b = open('b.txt', 'r').readlines()
for i in range(len(a)):
    if a[i] == b[i]:
        print(i + 1)