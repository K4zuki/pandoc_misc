#-*- coding: utf-8 -*-
#!/usr/bin/env python27

def include(file, basename = "./"):
    _include = re.compile("`([^`]+)`\{.include}")
    listing = re.compile("`([^`]+)`\{.listingtable\ (\.[^`\.]+)}")
    stripped = re.sub("<!--[\s\S]*?-->", "", open(file, "rb").read())
    output = []

    for line in stripped.split("\n"):
        if _include.search(line):
            print file+" include",
            input_file = _include.search(line).groups()[0]
            print input_file
            # file_contents = open(input_file, "rb").read()
            line = _include.sub(line, include(basename+input_file))
        if listing.search(line):
            print file+" lisingtable",
            input_file = listing.search(line).groups()[0]
            filetype = listing.search(line).groups()[1]
            print filetype
            convert = f2l(input_file, filetype)
            line = listing.sub(line, convert)
        output.append(line)
    return "\n".join(output)

if __name__ == '__main__':
    import re
    import sys
    import argparse
    from file2listingtable import file2listingtable as f2l

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

    _include = re.compile("`([^`]+)`\{.include}")
    listing = re.compile("`([^`]+)`\{.listingtable\ (\.[^`\.]+)}")
    stripped = re.sub("<!--[\s\S]*?-->", "", _file.read())
    output = open(_basedir+"/"+_output,'wb')

    for line in stripped.split("\n"):
        if _include.search(line):
            print "main include",
            input_file = _include.search(line).groups()[0]
            print input_file
            line = _include.sub(line, include(input_file, _basedir))
        if listing.search(line):
            print "main lisingtable",
            input_file = listing.search(line).groups()[0]
            filetype = listing.search(line).groups()[1]
            print filetype
            convert = f2l(input_file, filetype)
            line = listing.sub(line, convert)
        output.write(line+"\n")
