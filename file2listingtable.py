#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# os.path.basename(path)


def file2listingtable(file="Makefile",
                      type=".makefile",
                      docx=False,
                      tex=False):
    _file = file
    _basename = os.path.basename(_file)
    _type = type
    isDocx = docx
    isTex = tex

    _label = _basename.lower().replace(".", "_")
    _label = _label.replace("/", "_")
    anchor = "" if not isDocx else 'TC "[@lst:%s] %s" `\l` 6\n\n' % (_label, _basename)
    # print (anchor)
    # print (_basename)

    _file_title = _basename if not isTex else _basename.replace("_", "\\\\\\_")
    # print ("_file_title", _file_title)

    _list = ["Listing: %s %s" % (_file_title, anchor),
             "```{#lst:%s %s}" % (_label, _type),
             "```"]
    # _list = _list.split("\n")
    # print (_list)

    widthlist = [80]
    widthlist.extend([len(value) for value in _list])
    # print (widthlist)

    result = []
    try:
        with open(_file, "r") as read:
            _read = list(read)
        # print (_read)

        height = len(_read)  # number of lines in list
        # print (height)

        for content in _read:
            swap = content.strip("\n").replace("\t", "    ")
            width = len(swap)
            widthlist.append(width)

        _maxwidth = max(widthlist)
        # print (_maxwidth)

        hline = "+" + "".ljust(_maxwidth, "-") + "+"
        # print (hline)

        headers = []
        for statement in _list:
            # print (statement)
            header = "|" + statement.ljust(_maxwidth) + "|"
            headers.append(header)

        if isTex:
            _dummyhead = '```{%s .numberLines numbers="left"}' % (_type)
            _dummytail = "```"
        else:
            _dummyhead = "```{%s}" % (_type)
            _dummyhead = "|" + _dummyhead.ljust(_maxwidth) + "|"
            _dummytail = "|" + "```".ljust(_maxwidth) + "|"

        lines = []
        for i in range(height):
            swap = _read[i].rstrip('\n').replace("\t", "    ")
            width = len(swap)
            if(isTex):
                lines.append(swap)
            else:
                line = "|" + swap.ljust(_maxwidth) + "|"
                lines.append(line)

        # print lines

        result.append(hline)
        result.extend(headers)
        result.append(hline)
        if(isTex):
            result.append("")
        result.append(_dummyhead)
        result.extend(lines)
        result.append(_dummytail)
        if not isTex:
            result.append(hline)
        # print "\n".join(result)
    except:
        result.append("failed to open file %s" % (_file))

    return "\n".join(result)


if __name__ == '__main__':
    import argparse

    class MyParser(object):

        def __init__(self):
            self._parser = argparse.ArgumentParser(
                description="convert from a file to markdown grid table")
            self._parser.add_argument('--file',
                                      '-F',
                                      help='input file',
                                      default="Makefile")
            self._parser.add_argument('--out',
                                      '-O',
                                      help='output markdown file',
                                      default="Makefile_t.md")
            self._parser.add_argument('--type',
                                      '-T',
                                      help='input file type',
                                      default=".makefile")
            self.args = self._parser.parse_args(namespace=self)

    parser = MyParser()
    _file = parser.args.file
    _output = parser.args.out
    _type = parser.args.type

    hoge = file2listingtable(_file, _type, docx=False, tex=False)
    with open(_output, "w") as output:
        output.write(hoge)
