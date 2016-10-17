#!/usr/bin/env python27
# -*- coding: utf-8 -*-

import re
import docx
import datetime
import argparse

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
yaml = re.compile("---[\s\S]*?\.\.\.")
yaml = yaml.findall(file_contents)[0].split('\n')
docu = docx.Document(_outfile)

_comments = re.compile("comments:" + compiler["unicode"])
_keywords = re.compile("keywords:" + compiler["unicode"])
_category = re.compile("category:" + compiler["unicode"])
_subject = re.compile("subject:" + compiler["unicode"])
_content_status = re.compile("content_status:" + compiler["unicode"])

_author = re.compile("author:" + compiler["unicode"])
_title = re.compile("title:" + compiler["unicode"])
# _revision            =   re.compile("revision:" + compiler["int"])
# _version             =   re.compile("version:" + compiler["unicode"])
# _created             =   re.compile("created:" + compiler["datetime"])

# _identifier          =   re.compile("identifier:" + compiler["unicode"])
# _language            =   re.compile("language:" + compiler["unicode"])
# _last_modified_by    =   re.compile("last_modified_by:" + compiler["unicode"])
#
# # YYYY = groups[2]
# # MM = monthname[ groups[3] ]
# # DD = groups[4]
# _last_printed        =   re.compile("last_printed:" + compiler["datetime"])
# _modified            =   re.compile("modified:" + compiler["datetime"])


for line in yaml:
    if _comments.search(line):
        __comments = _comments.search(line).groups()[0]
        # print __comments
        docu.core_properties.comments = __comments
    if _keywords.search(line):
        __keywords = _keywords.search(line).groups()[0]
        # print __keywords
        docu.core_properties.keywords = __keywords
    elif _category.search(line):
        __category = _category.search(line).groups()[0]
        # print __category
        docu.core_properties.category = __category
    elif _subject.search(line):
        __subject = '-'.join(_subject.search(line).groups()[0].split(')')[0].split(' ')[5:])
        # print __subject
        docu.core_properties.subject = __subject
    elif _content_status.search(line):
        __status = "Revision " + _content_status.search(line).groups()[0].split(' ')[1]
        # print __status
        docu.core_properties.content_status = __status
    elif _author.search(line):
        __author = _author.search(line).groups()[0]
        # print __author
        docu.core_properties.author = __author
    elif _title.search(line):
        __title = _title.search(line).groups()[0]
        # print __title
        docu.core_properties.title = __title
    # elif _revision.search(line):
    #     __revision = _revision.search(line).groups()[0]
    #     # print __revision
    #     docu.core_properties.revision = int(__revision)
    # elif _version.search(line):
    #     __version = _version.search(line).groups()[0]
    #     # print __version
    #     docu.core_properties.version = __version
    # elif _created.search(line):
    #     __created = _created.search(line)
    #     YYYY = __created.groups()[1]
    #     MM = __created.groups()[2]
    #     # MMM = monthname[ __created.groups()[2] ]
    #     DD = __created.groups()[3]
    #     __created = datetime.datetime(int(YYYY), int(MM), int(DD))
    #     # print __created
    #     docu.core_properties.created = __created

docu.save(_outfile)
