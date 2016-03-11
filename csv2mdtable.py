#-*- coding: utf-8 -*-
#!/usr/bin/env python27

import csv

import argparse
class MyParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description = "convert from csv file to markdown grid table")
        self._parser.add_argument('--file', '-F', help = 'input csv file', default = "csv.csv")
        self._parser.add_argument('--out', '-O', help = 'output markdown file', default = "csv_t.md")
        self._parser.add_argument('--delimiter', '-D', help = 'device number', default = ',')
#        self._parser.add_argument('--basedir','-B', help = 'base directry of output',
#            default = "C:\\Users\\Public\\Documents\\")
        self.args = self._parser.parse_args(namespace=self)

parser = MyParser()
_file = parser.args.file
_output = parser.args.out
_delimiter = parser.args.delimiter

_read = csv.reader(open(_file, 'r'), delimiter=_delimiter, quotechar='\"')
_outfile = open( _output,'w' )

lst = list(_read)
width = len(lst[0]) #number of member in list
height = len(lst)

widthlist = []
maxwidthlist = []
for i in range(width): #x
    widthlist.append([])
    for j in range(height): #y
        widthlist[i].append(len(lst[j][i])) #list up width of (x=i, y=0~(j-1))
#        print lst[j][i]
    maxwidthlist.append(max(widthlist[i])) #get longest length of each x
#    print max(widthlist[i])

#print widthlist
#print maxwidthlist
hbar="+"
hline="+"
for i in maxwidthlist:
    for j in range(i+1):
        hbar+=u"="
        hline+=u"-"
    hbar+=u"+"
    hline+=u"+"
#print hbar
#print hline

str=""
for i in range(width): #x
    for j in range(height): #y
#        print "%d" %(maxwidthlist[i] - len(lst[j][i])),
        str=""
        for s in range(maxwidthlist[i] - len(lst[j][i]) +1):
            str+=" "
        lst[j][i] = lst[j][i]+str
#        print lst[j][i],
#    print "|"

_outfile.write( hline+"\n")
_outfile.write( "|%s|\n" %"|".join(lst[0]))
_outfile.write( hbar+"\n")
for j in range(height-1): #y
    _outfile.write( "|%s|\n" %"|".join(lst[j+1]))
    _outfile.write( hline+"\n")

_outfile.close()
