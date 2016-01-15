#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv

from matplotlib.font_manager import FontProperties
fontP = FontProperties()
fontP.set_size('small')

import argparse
class MyParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description = """take screenshot from Tek MSO/DPO/MDO4000 Oscilloscope,
        will *Not* control instuments other than Oscillo
        """)
        self._parser.add_argument('--file', '-F', help = 'inputcsv file name', default = 'default.csv')
#        self._parser.add_argument('--input', '-I', help = 'input voltage', default = 3.6)
        self._parser.add_argument('--output', '-O', help = 'output file name', default = 'default.png')
#        self._parser.add_argument('--device', '-D', help = 'device number', default = 1)
#        self._parser.add_argument('--basename','-B', help = 'base directry of output',
#            default = "C:\\Users\\Public\\Documents\\")
        self.args = self._parser.parse_args(namespace=self)

parser = MyParser()
_file = parser.args.file
_output = parser.args.output

read = csv.reader(open(_file,'r'), delimiter=',',quotechar='"')
title = []
data = []

for row in read:
    row.reverse()
    title.append(row.pop())
    row.reverse()
    data.append(row)
data.reverse()
x = data.pop()
data.reverse()
for hoge in range(len(x)):
    x[hoge] = float(x[hoge])
title.reverse()
plt.title(title.pop())
for y in data:
    for hoge in range(len(y)):
        y[hoge] = float(y[hoge])
#    print y
    plt.plot(x, y, 'o-', label = title.pop())

plt.legend( prop = fontP, loc = 'upper center', ncol=2)
plt.xlabel("$I_{out}$[mA]")
plt.ylabel("$V_{in}$[V]")
plt.xlim([0,1000])
plt.ylim([2.5, 5.5])
plt.grid()
plt.show()
plt.savefig(_output)
