"""
=======================================
plot line and dash
=======================================

"""
import numpy as np
import matplotlib.pyplot as plt
import os
import sys, getopt

#x = np.linspace(0, 10, 500)

y1 = []
z1 = []
k1 = []
nline=0
print "Tzzzzzzzz\n"
with open(sys.argv[1], 'r') as fig:
    for line in fig:
        data = line.split()
        if nline == 0:
            y1 = data[1:]
        elif nline == 1:
            z1 = data[1:]
        elif nline == 2:
            k1 = data[1:]
        nline=nline+1

x = np.linspace(1, len(y1)-1, len(y1)-1)
print "TTTTTTTTTT", y1

## read file2
y2 = []
z2 = []
k2 = []
nline=0
with open(sys.argv[2], 'r') as fig:
    for line in fig:
        data = line.split()
        if nline == 0:
            y2 = data[1:]
        elif nline == 1:
            z2 = data[1:]
        elif nline == 2:
            k2 = data[1:]
        nline=nline+1


print y2
print len(x), len(y1), len(y2)
fig, ax = plt.subplots()
line1, = ax.plot(x, y1, '--', linewidth=2, label='Dashesset retroactively')
dashes = [10, 5, 100, 5]
line1.set_dashes(dashes)   #   dash line

line2, = ax.plot(x, y2, dashes=[30, 5, 10, 5], label='Dashes set proactively')

#  several dash line example
#line3, = ax.plot(x, y3, ':', label='..style')
#line4, = ax.plot(x,-np.sin(x)/2, '-.', label='-.style')
#line5, = ax.plot(x,np.sin(x)/4, '--', label='--style')
#line6, = ax.plot(x,-np.sin(x)/4, '^', label='--style')

ax.legend(loc='lowerright')   #   legend , loc is the legend location
plt.savefig(sys.argv[3])
plt.show()
