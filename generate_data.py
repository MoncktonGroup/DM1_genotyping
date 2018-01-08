from __future__ import print_function
import math
import random
# that's our x data, i.e. reference
x = range(1, 101)

# generate a gaussian
def gaussian(x, amp, cen, wid):
    return amp * math.exp(-(x - cen) ** 2 / wid)

read1 = 18
read2 = 66

# that's our y data, i.e. reads
y = [int(round(gaussian(i, 20000, read1, 0.5) + gaussian(i, 20000, read2, 0.5) + random.gauss(200, 90))) for i in x]

# that's our data printed in pairs (x_i, y_i)
with open("input.txt", "w") as f:
    for pair in zip(x, y):
        for p in pair:
            print(p, end="\t", file=f)
        print(file=f)

# you have to set this manually to weed out all the noise. Every bit of noise should be below it.
