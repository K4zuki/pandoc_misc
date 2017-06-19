#!/usr/bin/env python27
# -*- coding: utf-8 -*-

import re
import docx
import datetime
import argparse
import yaml

monthname = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
}
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

file_contents = open(_infile, "r").read()
_yaml = re.compile("---[\s\S]*?\.\.\.")
_yaml = _yaml.findall(file_contents)[0]
data = yaml.load(_yaml)

import sys
# sysモジュールをリロードする
reload(sys)
# デフォルトの文字コードを変更する.
sys.setdefaultencoding('utf-8')
# デフォルトの文字コードを出力する.
print 'defaultencoding:', sys.getdefaultencoding()
print sys.stdout.encoding
# import pprint
# pprint.pprint(data)

docu = docx.Document(_outfile)

try:
    _comments = data['comments']
except:
    _comments = None

try:
    _keywords = data['keywords']
except:
    _keywords = None

try:
    _category = data['category']
except:
    _category = None

try:
    _subject = data['subject']
except:
    _subject = None

try:
    _content_status = data['content_status']
except:
    _content_status = None

try:
    _author = data['author']
except:
    _author = None

try:
    _title = data['title']
except:
    _title = None

try:
    _revision = data['revision']
except:
    _revision = None

try:
    _version = data['version']
except:
    _version = None

try:
    _created = data['created']
except:
    _created = None

try:
    _identifier = data['identifier']
except:
    _identifier = None

try:
    _language = data['language']
except:
    _language = None

try:
    _last_modified_by = data['last_modified_by']
except:
    _last_modified_by = None

# # YYYY = groups[2]
# # MM = monthname[ groups[3] ]
# # DD = groups[4]
# _last_printed        =   re.compile("last_printed:" + compiler["datetime"])
# _modified            =   re.compile("modified:" + compiler["datetime"])

# for line in _yaml:
if _comments:
    print unicode(_comments)
    docu.core_properties.comments = _comments
if _keywords:
    print (_keywords)
    docu.core_properties.keywords = _keywords
if _category:
    print _category
    docu.core_properties.category = _category
if _subject:
    print _subject
    docu.core_properties.subject = _subject
if _content_status:
    print _status
    docu.core_properties.content_status = _status
if _author:
    print _author
    docu.core_properties.author = _author
if _title:
    print _title
    docu.core_properties.title = _title
if _revision:
    print _revision
    docu.core_properties.revision = int(_revision)
if _version:
    print _version
    docu.core_properties.version = _version
if _created:
    print _created
    docu.core_properties.created = _created

docu.save(_outfile)
