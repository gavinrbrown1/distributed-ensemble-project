with open('foo.txt', 'w') as f:
    for i in range(100000):
        f.write('I must not tell lies.\n')
        if i % 1000 == 0:
            print(i)
