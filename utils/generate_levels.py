#!/usr/bin/env python27

def levels(count):
    x = 25
    inc = 25
    step = 25
    file = open('levels.dat', 'w')
    for i in range(count):
        file.write(str(x) + "\n")
        x = x + inc
        inc = inc + step
        if (i % 10) == 0:
            step = step * 2
    file.write("10000000\n")
    file.close()

levels(50)
