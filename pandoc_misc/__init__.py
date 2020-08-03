#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import subprocess as sp
import hashlib
import yaml

COMMAND = "{} make init -f {}/var/pandoc_misc/user/Makefile"
SEPARATOR = "/lib/"
DOCKER = ""

if platform.system() == "Windows":
    SEPARATOR = "/Lib/"
    DOCKER = "docker run -v $PWD:/workdir k4zuki/pandocker-alpine:2.8"


def build_command():
    install_base = pip_base()
    command = COMMAND.format(DOCKER, install_base)

    return command


def pandocker_version():
    pip_list = sp.run(["pip3", "list"], stdout=sp.PIPE, stderr=sp.DEVNULL)
    print(hashlib.sha1(pip_list.stdout).hexdigest()[:7])


def pip_base():
    pip_info = sp.run(["pip3", "show", "pandoc-misc"], stdout=sp.PIPE, stderr=sp.DEVNULL)
    pip_inst_dir = yaml.load(pip_info.stdout, Loader=yaml.SafeLoader)["Location"]
    install_base = pip_inst_dir.split(SEPARATOR)[0]

    print(install_base)


def main():
    command = build_command()
    sp.call(command, shell=True)


if __name__ == "__main__":
    main()
