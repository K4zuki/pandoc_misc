#-*- coding: utf-8 -*-
#!/usr/bin/env python27

import os
# os.path.basename(path)
def file2listingtable(file = "Makefile", type = ".makefile", docx = False, tex = False):
    _file = file
    _basename = os.path.basename(_file)
    _type = type
    _docx = docx
    _tex = tex

    _label = _basename.lower().replace(".","_")
    _label = _label.replace("/","_")
    _link = ""
    if(_docx):
        _link = "TC \"[@lst:"+_label+"] "+_basename+"\" `\l` 6\n\n"

    # print _link
    if (_tex):
        _file_title = _basename.replace("_","\\\\\\_")
    else:
        _file_title = _basename

    _list = """Listing: %s %s
```{#lst:%s %s}
```"""%(_file_title, _link, _label, _type)
    _list = _list.split("\n")
    # print _list

    widthlist = []
    for i in range(len(_list)):
        # print _list[i]
        width = len(_list[i])
        widthlist.append( width )

    result = []
    try:
        with open(_file, "r") as read:
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
        for statement in _list:
            # print statement
            header = "|" + statement.ljust(_maxwidth) + "|"
            headers.append(header)
        # for i in range(len(_list)):
        #     # print _list[i]
        #     header = "|" + _list[i].ljust(_maxwidth) + "|"
        #     headers.append(header)

        if _tex:
            _dummyhead = '```{%s .numberLines numbers="left"}'%(_type)
            _dummytail = "```"
        else:
            _dummyhead = "```{%s}"%(_type)
            _dummyhead = "|" + _dummyhead.ljust(_maxwidth) + "|"
            _dummytail = "|" + "```".ljust(_maxwidth) + "|"

        lines = []
        for i in range(height):
            swap = _read[i].rstrip('\n').replace("\t","    ")
            width = len(swap)
            if(_tex):
                lines.append(swap)
            else:
                line = "|" + swap.ljust(_maxwidth) + "|"
                lines.append(line)

        # print lines

        result.append(hline)
        result.extend(headers)
        result.append(hline)
        if(_tex):
            result.append("")
        result.append(_dummyhead)
        result.extend(lines)
        result.append(_dummytail)
        if not _tex:
            result.append(hline)
        # print "\n".join(result)
    except:
        result.append("failed to open file %s" %(_file))

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

    hoge = file2listingtable(_file, _type, docx = False, tex = False)
    output = open(_output,"wb")
    output.write(hoge)
    output.close()
