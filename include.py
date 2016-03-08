#-*- coding: utf-8 -*-
#!/usr/bin/env python27

import re
import sys
import argparse
class MyParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description = "cat some.txt| python include.py --out out_f.md")
        self._parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
        self._parser.add_argument('--out', '-O', help = 'output markdown file', default = "table.md")
        self._parser.add_argument('--basedir','-B', help = 'base directry of output', default = "./")
        self.args = self._parser.parse_args(namespace=self)


parser = MyParser()
_file = parser.args.infile
_output = parser.args.out
_basedir = parser.args.basedir

include = re.compile("`([^`]+)`\{.include}")
stripped = re.sub("<!--[\s\S]*?-->", "", _file.read())
output = open(_basedir+"/"+_output,'wb')

for line in stripped.split("\n"):
    if include.search(line):
        input_file = include.search(line).groups()[0]
        file_contents = open(_basedir+"/"+input_file, "rb").read()
        line = include.sub(line, file_contents)
    output.write(line+"\n")
