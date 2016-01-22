#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv

from matplotlib.font_manager import FontProperties
fontP = FontProperties()
fontP.set_size('small')
fontP.set_family('Times New Roman')

import argparse
class MyParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description = "")
        self._parser.add_argument('--file', '-F', help = 'input csv file name', default = 'default.csv')

        self._parser.add_argument('--xmin', default = 0)
        self._parser.add_argument('--xmax', default = 1000)
        self._parser.add_argument('--xlabel', default = "I")
        self._parser.add_argument('--xsuffix', default = "in")
        self._parser.add_argument('--xunit', default = "mA")

        self._parser.add_argument('--ymin', default = 2.5)
        self._parser.add_argument('--ymax', default = 5.5)
        self._parser.add_argument('--ylabel', default = "V")
        self._parser.add_argument('--ysuffix', default = "out")
        self._parser.add_argument('--yunit', default = "V")

#        self._parser.add_argument('--input', '-I', help = 'input voltage', default = 3.6)
        self._parser.add_argument('--output', '-O', help = 'output file name', default = 'default.png')
#        self._parser.add_argument('--device', '-D', help = 'device number', default = 1)
#        self._parser.add_argument('--basename','-B', help = 'base directry of output',
#            default = "C:\\Users\\Public\\Documents\\")
        self.args = self._parser.parse_args(namespace=self)

parser = MyParser()
_file = parser.args.file
_output = parser.args.output

_xmin =     float(parser.args.xmin)
_xmax =     float(parser.args.xmax)
_xlabel =   parser.args.xlabel
_xsuffix =  parser.args.xsuffix
_xunit =    parser.args.xunit

_ymin =     float(parser.args.ymin)
_ymax =     float(parser.args.ymax)
_ylabel =   parser.args.ylabel
_ysuffix =  parser.args.ysuffix
_yunit =    parser.args.yunit

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
for i in range(len(x)):
    x[i] = float(x[i])
title.reverse()
plt.title(title.pop())
for y in data:
    for j in range(len(y)):
        y[j] = float(y[j])
#    print y
    plt.plot(x, y, 'o-', label = title.pop())
plt.legend( prop = fontP, loc = 'upper center', ncol=2)
#plt.xlabel("$I_{out}$[mA]")
plt.xlabel("$"+_xlabel+"_{"+_xsuffix+"}$["+_xunit+"]")
plt.xlim([_xmin,_xmax])
#plt.ylabel("$V_{in}$[V]")
plt.ylabel("$"+_ylabel+"_{"+_ysuffix+"}$["+_yunit+"]")
plt.ylim([_ymin, _ymax])
plt.grid()
plt.show()
plt.savefig(_output)
