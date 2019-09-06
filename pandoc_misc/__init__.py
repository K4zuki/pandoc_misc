#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess as sp
import site
import pip
import hashlib

install_base = site.getsitepackages()[0].split("lib")[0][:-1]

COMMAND = "docker run -v $PWD:/workdir k4zuki/pandocker make init -f {}/var/pandoc_misc/Makefile"
command = COMMAND.format(install_base)
env_hash = hashlib.sha1("\n".join(str(d) for d in pip.get_installed_distributions()).encode("utf-8")).hexdigest()[:7]


def env_version():
    print(env_hash)


def pip_base():
    print(install_base)


def main():
    sp.call(command, shell=True)


if __name__ == "__main__":
    main()
