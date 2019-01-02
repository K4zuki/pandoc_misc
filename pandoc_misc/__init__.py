#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess as sp

command = "docker run -v $PWD:/workdir k4zuki/pandocker make init -f /usr/local/var/pandoc_misc/Makefile"


def main():
    sp.call(command, shell=True)


if __name__ == "__main__":
    main()
