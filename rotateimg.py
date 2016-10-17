#!/usr/bin/env python27
# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image


def rotatepic(filename, caption="", angle=0):

    # print "rotatepic"
    try:
        img = Image.open(filename)
        path, ext = os.path.splitext(filename)
        print path, ext
        angle = angle.split("=")[-1]
        angle = angle.strip()
        angle = int(angle)
        caption = caption.split("=")[-1]
        caption = caption.strip(' "" ')
        # print caption, angle

        if(angle == 0):
            pass
        elif(angle == 90):
            tmp = img.transpose(Image.ROTATE_90)
            filename = "%s_r+090%s" % (path, ext)
        elif(angle == 180 or angle == -180):
            tmp = img.transpose(Image.ROTATE_180)
            filename = "%s_r180%s" % (path, ext)
        elif(angle == 270 or angle == -90):
            tmp = img.transpose(Image.ROTATE_270)
            filename = "%s_r-090%s" % (path, ext)
        else:
            angle = angle % 360
            if(angle < 0):
                angle = 360 - abs(angle)
            # print angle
            tmp = img.rotate(angle)
            filename = "%s_r%+03d%s" % (path, angle, ext)
        if not os.path.exists(filename):
            tmp.save(filename)
    except:
        print sys.exc_info()
    finally:
        return "![%s](%s)" % (caption, filename)

if __name__ == '__main__':
    import argparse

    class MyParser(object):

        def __init__(self):
            self._parser = argparse.ArgumentParser(
                description="convert from a file to markdown grid table")
            self._parser.add_argument(  '--file',
                                        '-F',
                                        help='input file',
                                        default="picture.png")
            self._parser.add_argument(  '--rotate',
                                        '-R',
                                        help='rotate angle',
                                        default=0)
            self.args = self._parser.parse_args(namespace=self)

    parser = MyParser()
    _file = parser.args.file
    _rotate = parser.args.rotate

    hoge = rotatepic(_file, int(_rotate))
