#!/usr/bin/env python27
# -*- coding: utf-8 -*-

modesel = {
    "NONE": (False, False),
    "TEX":  (False, True),
    "DOCX": (True, False),
}


def include(file, basename="./", mode="none"):
    # regex filter to find out include statement
    _include = re.compile("`([^`]+)`\{.include}")
    # regex filter to find out rotate statement
    _rotimg = re.compile(
        "`([^`]+)`\{.rotate\s+(\.caption\s*=\s*[^`\.]+)\ +(\.angle\s*=\s*[^`\.]+)\}\{([^`]*)\}")
    # regex filter to find out listing statement
    listing = re.compile("`([^`]+)`\{.listingtable\ (\.[^`\.]+)}")
    # regex filter to remove markdown comment
    stripped = re.sub("<!--[\s\S]*?-->", "", open(file, "rb").read())

    _mode = modesel[mode.upper()]
    # print _mode

    output = []

    for line in stripped.split("\n"):
        if _include.search(line):
            print file + ": include",
            input_file = _include.search(line).groups()[0]
            print input_file
            # file_contents = open(input_file, "rb").read()
            line = _include.sub(line,
                                include(basename + input_file, mode=mode))
        if listing.search(line):
            print file + ": listingtable of",
            input_file = listing.search(line).groups()[0]
            filetype = listing.search(line).groups()[1]
            print filetype
            convert = f2l(input_file, filetype, _mode[0], _mode[1])
            line = listing.sub(line, convert)
        if _rotimg.search(line):
            print file + ": rotate image of",
            input_file = _rotimg.search(line).groups()[0]
            caption = _rotimg.search(line).groups()[1]
            angle = _rotimg.search(line).groups()[2]
            others = _rotimg.search(line).groups()[3]
            print input_file, angle
            rotatedcaption = rotatepic(input_file, caption, angle, others)
            # print rotatedcaption
            line = listing.sub(line, rotatedcaption)
        output.append(line)
    return "\n".join(output)

if __name__ == '__main__':
    import re
    import sys
    import argparse
    from file2listingtable import file2listingtable as f2l
    from rotateimg import rotatepic

    class MyParser(object):

        def __init__(self):
            self._parser = argparse.ArgumentParser(
                description="cat some.txt| python include.py --out out_f.md")
            self._parser.add_argument(  'infile',
                                        nargs='?',
                                        type=argparse.FileType('r'),
                                        default=sys.stdin)
            self._parser.add_argument(  '--out',
                                        '-O',
                                        help='output markdown file',
                                        default="table.md")
            self._parser.add_argument(  '--basedir',
                                        '-B',
                                        help='base directry of output',
                                        default="./")
            self._parser.add_argument(  '--mode',
                                        '-M',
                                        help='TeX or DOCX output',
                                        default="none")
            self.args = self._parser.parse_args(namespace=self)

    parser = MyParser()
    _file = parser.args.infile
    _output = parser.args.out
    _basedir = parser.args.basedir
    _mode = parser.args.mode
    __mode = modesel[_mode.upper()]
    # print _mode

    # regex filter to find out include statement
    _include = re.compile("`([^`]+)`\{.include}")

    # regex filter to find out listing statement
    listing = re.compile("`([^`]+)`\{.listingtable\ (\.[^`\.]+)}")

    # regex filter to find out rotate statement
    _rotimg = re.compile(
        "`([^`]+)`\{.rotate\ +(\.caption\ *=\ *[^`\.]+)\ +(\.angle\ *=\ *[^`\.]+)\}\{([^`]*)\}")

    # regex filter to remove markdown comment
    stripped = re.sub("<!--[\s\S]*?-->", "", _file.read())

    # regex filter to find out table caption
    tblcaption = re.compile(
        "(Table:)([\*_\ ]*)(.[^\{\}\*_]*)([\*_\ ]*).*\{\ *#(tbl:.[^\*\n]*[^\ ])\ *\}")
    output = open(_basedir + "/" + _output, 'wb')

    for line in stripped.split("\n"):
        if _include.search(line):
            print "main: include",
            input_file = _include.search(line).groups()[0]
            print input_file
            line = _include.sub(line, include(input_file, _basedir, _mode))
        if listing.search(line):
            print "main: listingtable of",
            input_file = listing.search(line).groups()[0]
            filetype = listing.search(line).groups()[1]
            print filetype
            convert = f2l(input_file, filetype, __mode[0], __mode[1])
            line = listing.sub(line, convert)
        if _rotimg.search(line):
            print "main: rotate image of",
            input_file = _rotimg.search(line).groups()[0]
            caption = _rotimg.search(line).groups()[1]
            angle = _rotimg.search(line).groups()[2]
            others = _rotimg.search(line).groups()[3]
            print input_file, angle
            rotatedcaption = rotatepic(input_file, caption, angle, others)
            # print rotatedcaption
            line = listing.sub(line, rotatedcaption)
        if tblcaption.search(line):
            if(__mode[0]):
                caption = tblcaption.search(line).groups()[2]
                link = tblcaption.search(line).groups()[4]
                line = "TC \"[@" + link + "] " + caption + "\" `\l` 5\n\n" + line
                print link
        output.write(line + "\n")
