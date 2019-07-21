#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess as sp
import site

install_base = site.getsitepackages()[0].split("/lib/")[0]

COMMAND = "docker run -v $PWD:/workdir k4zuki/pandocker make init -f {}/var/pandoc_misc/Makefile"
command = COMMAND.format(install_base)


def pip_base():
    print(install_base)


def main():
    sp.call(command, shell=True)


if __name__ == "__main__":
    main()
