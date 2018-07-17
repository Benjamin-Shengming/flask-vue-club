#! /usr/bin/python3
import os
from invoke import run

def gen_mo_files():
    files = os.listdir(".")
    print(files)
    for file in files:
        if "po" in file or "pot" in file:
            mo_file = os.path.splitext(file)[0] + ".mo"
            print(mo_file)
            cmd = "msgfmt -o {} {}".format(mo_file, file)
            print("execmd: {}".format(cmd) )
            run(cmd, hide=False, warn=True)
        else:
            pass

if __name__ == "__main__":

    gen_mo_files()
