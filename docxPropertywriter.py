#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import docx
import datetime
import argparse
import yaml
import importlib

monthname = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun",
             "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec", }

compiler = {
    "unicode": " *([^`\n]+)",
    "datetime": " *([\s\S]*)(000[1-9]|[1-9]\d\d\d)-(0[1-9]|\
    1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])",
    "int": " *([^`\n]\d*)"
}


class MyParser(object):

    def __init__(self):
        self._parser = argparse.ArgumentParser(description="")
        self._parser.add_argument('--infile', '-I', help='markdown input',
                                  default="document.md")
        self._parser.add_argument('--outfile', '-O', help='docx output',
                                  default="document.docx")
        self.args = self._parser.parse_args(namespace=self)


parser = MyParser()
_infile = parser.infile
_outfile = parser.outfile

file_contents = open(_infile, "r",  encoding="utf8").read()
_yaml = re.compile("---[\s\S]*?\.\.\.")
_yaml = _yaml.findall(file_contents)[0]
data = yaml.load(_yaml)

docu = docx.Document(_outfile)
keys = ['reporter', 'dnumber', 'project', 'rep_date', 'revision', 'author',
        'title', 'version', 'created']
# , 'identifier', 'language', 'last_modified_by']
properties = [docu.core_properties.comments,  # reporter
              docu.core_properties.keywords,  # dnumber
              docu.core_properties.category,  # project
              docu.core_properties.subject,  # rep_date
              docu.core_properties.content_status,  # revision
              docu.core_properties.author,
              docu.core_properties.title,
              docu.core_properties.version,
              docu.core_properties.created,
              ]
# docu.core_properties.revision
# 'revision' is exception
for p, k in zip(properties, keys):
    p = str(data[k]) if k in data else None
    print(k, p)
docu.core_properties.revision = int(data['revision']) if 'revision' in data else 1
properties.append(docu.core_properties.revision)

docu.save(_outfile)
