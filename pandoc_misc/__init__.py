#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import subprocess as sp
import setuptools
import hashlib

separator = "/lib/"
docker = ""
if platform.system() == "Windows":
    separator = "/Lib/"
    docker = "docker run -v $PWD:/workdir k4zuki/pandocker-alpine:2.8"
install_base = setuptools.__path__[0].split(separator)[0]

COMMAND = "{} make init -f {}/var/pandoc_misc/user/Makefile"
command = COMMAND.format(docker, install_base)

pip_list = sp.run(["pip", "list"], stdout=sp.PIPE, stderr=sp.DEVNULL)


def pandocker_version():
    print(hashlib.sha1(pip_list.stdout).hexdigest()[:7])


def pip_base():
    print(install_base)


def main():
    sp.call(command, shell=True)


if __name__ == "__main__":
    main()
