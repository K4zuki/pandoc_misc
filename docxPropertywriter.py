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
        self._parser.add_argument("--infile", "-I", help="markdown input",
                                  default="document.md")
        self._parser.add_argument("--outfile", "-O", help="docx output",
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
"""this does not work
keys = ["reporter",
        "dnumber",
        "project",
        "rep_date",
        "revision",
        "author",
        "title",
        "version",
        "created"]

properties = [docu.core_properties.comments,  # reporter
              docu.core_properties.keywords,  # dnumber
              docu.core_properties.category,  # project
              docu.core_properties.subject,  # rep_date
              docu.core_properties.content_status,  # revision
              docu.core_properties.author,
              docu.core_properties.title,
              docu.core_properties.version,
              docu.core_properties.created
              ]
for prop, key in zip(properties, keys):
    if key in data:
        prop = data[key]
        print(key)
docu.core_properties.revision = int(data["revision"]) if "revision" in data else 1
"""
"""this work"""
if "reporter" in data:
    docu.core_properties.comments = data["reporter"]
if "dnumber" in data:
    docu.core_properties.keywords = data["dnumber"]
if "project" in data:
    docu.core_properties.category = data["project"]
if "rep_date" in data:
    docu.core_properties.subject = data["rep_date"]
if "revision" in data:
    docu.core_properties.content_status = data["revision"]
if "author" in data:
    docu.core_properties.author = data["author"]
if "title" in data:
    docu.core_properties.title = data["title"]
if "version" in data:
    docu.core_properties.version = data["version"]
if "created" in data:
    docu.core_properties.created = data["created"]

docu.save(_outfile)
