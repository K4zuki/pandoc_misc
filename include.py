#-*- coding: utf-8 -*-
#!/usr/bin/env python27

modesel = {
    "NONE": (False,False),
    "TEX":  (False,True),
    "DOCX": (True,False),
}

def include(file, basename = "./", mode = "none"):
    _include = re.compile("`([^`]+)`\{.include}") # regex filter to find out include statement
    listing = re.compile("`([^`]+)`\{.listingtable\ (\.[^`\.]+)}") # regex filter to find out listing statement
    stripped = re.sub("<!--[\s\S]*?-->", "", open(file, "rb").read()) # regex filter to remove markdown comment

    _mode = modesel[mode.upper()]
    print _mode

    output = []

    for line in stripped.split("\n"):
        if _include.search(line):
            print file+": include",
            input_file = _include.search(line).groups()[0]
            print input_file
            # file_contents = open(input_file, "rb").read()
            line = _include.sub(line, include(basename+input_file, mode = mode))
        if listing.search(line):
            print file+": listingtable of",
            input_file = listing.search(line).groups()[0]
            filetype = listing.search(line).groups()[1]
            print filetype
            convert = f2l(input_file, filetype, _mode[0], _mode[1])
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
            self._parser.add_argument('--mode','-M', help = 'TeX or DOCX output', default = "none")
            self.args = self._parser.parse_args(namespace=self)

    parser = MyParser()
    _file = parser.args.infile
    _output = parser.args.out
    _basedir = parser.args.basedir
    _mode = parser.args.mode
    __mode = modesel[_mode.upper()]
    print _mode

    _include = re.compile("`([^`]+)`\{.include}") # regex filter to find out include statement
    listing = re.compile("`([^`]+)`\{.listingtable\ (\.[^`\.]+)}") # regex filter to find out listing statement
    stripped = re.sub("<!--[\s\S]*?-->", "", _file.read()) # regex filter to remove markdown comment
    tblcaption = re.compile("(Table:)([\*_\ ]*)(.[^\{\}\*_]*)([\*_\ ]*).*\{\ *#(tbl:.[^\*\n]*[^\ ])\ *\}") # regex filter to find out table caption
    # figcaption = re.compile("(Figure:)([\*_\ ]*)(.[^\{\}\*_]*)([\*_\ ]*).*\{\ *#(fig:.[^\*\n]*[^\ ])\ *\}") # regex filter to find out figure caption
    # lstcaption = re.compile("(List:)([\*_\ ]*)(.[^\{\}\*_]*)([\*_\ ]*).*\{\ *#(lst:.[^\*\n]*[^\ ])\ *\}") # regex filter to find out listing caption
    output = open(_basedir + "/" + _output,'wb')

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
        if tblcaption.search(line):
            if(__mode[0]):
                caption =   tblcaption.search(line).groups()[2]
                link =      tblcaption.search(line).groups()[4]
                line = "TC \"[@"+link+"] "+caption+"\" `\l` 5\n\n"+line
                print link
        # if figcaption.search(line):
        #     caption =   figcaption.search(line).groups()[2]
        #     link =      figcaption.search(line).groups()[4]
        #     print "TC \"[@"+link+"] "+caption+"\" `\l` 6\n"+line
        # if lstcaption.search(line):
        #     caption =   lstcaption.search(line).groups()[2]
        #     link =      lstcaption.search(line).groups()[4]
        #     # line = listing.sub(line, convert)
        #     print "TC \"[@"+link+"] "+caption+"\" `\l` 7\n"+line
        output.write(line+"\n")
