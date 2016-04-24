#-*- coding: utf-8 -*-
#!/usr/bin/env python27


def file2listingtable(file = "Makefile", type = ".makefile"):
    _file = file
    _type = type

    _list = """Listing: %s
```{#lst:%s %s}
```"""%(_file, _file.lower().replace(".","_"), _type)
    _list = _list.split("\n")
    # print _list

    widthlist = []
    for i in range(len(_list)):
        # print _list[i]
        width = len(_list[i])
        widthlist.append( width )

    read = open(_file,"r")
    _read = list(read)
    # print _read

    height = len(_read) #number of lines in list
    # print height

    for i in range(height):
        swap = _read[i].rstrip('\n').replace("\t","    ")
        width = len(swap )
        widthlist.append( width )
    _maxwidth = max(widthlist)
    # print _maxwidth

    hline = "+" + "".ljust(_maxwidth,"-") + "+"
    # print hline

    headers = []
    for i in range(len(_list)):
        # print _list[i]
        width = len(_list[i])
        header = "|" + _list[i].ljust(_maxwidth) + "|"
        headers.append(header)

    _dummyhead = "```{%s}"%(_type)
    _dummyhead = "|" + _dummyhead.ljust(_maxwidth) + "|"

    _dummytail = "|" + "```".ljust(_maxwidth) + "|"
    lines = []
    for i in range(height):
        swap = _read[i].rstrip('\n').replace("\t","    ")
        width = len(swap)
        line = "|" + swap.ljust(_maxwidth) + "|"
        lines.append(line)

    # print lines

    result = [hline]
    result.extend(headers)
    result.append(hline)
    result.append(_dummyhead)
    result.extend(lines)
    result.append(_dummytail)
    result.append(hline)
    # print "\n".join(result)

    return "\n".join(result)

if __name__ == '__main__':
    import argparse
    class MyParser(object):
        def __init__(self):
            self._parser = argparse.ArgumentParser(description = "convert from a file to markdown grid table")
            self._parser.add_argument('--file', '-F', help = 'input file', default = "Makefile")
            self._parser.add_argument('--out', '-O', help = 'output markdown file', default = "Makefile_t.md")
            self._parser.add_argument('--type', '-T', help = 'input file type', default = ".makefile")
            self.args = self._parser.parse_args(namespace=self)

    parser = MyParser()
    _file = parser.args.file
    _output = parser.args.out
    _type = parser.args.type

    hoge = file2listingtable(_file, _type)
    output = open(out,"wb")
    output.write(hoge)
    output.close()
