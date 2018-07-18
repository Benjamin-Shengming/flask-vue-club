#!/usr/bin/python3

import sh
import os

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)

current_folder = os.path.dirname(__file__)
app_foder = os.path.join(current_folder, "apps")
libs_folder = os.path.join(current_folder, "libs")
locale_folder = os.path.join(current_folder, "locale/zh_CN/LC_MESSAGES")


def extract_pot_file(full_p, file):
    logger.debug("extract file " + full_p)
    tmp_pot = "tmp.pot"
    merge_pot = "merge.pot"
    sh.pygettext3("-o",tmp_pot, full_p)
    old_pot = os.path.join(locale_folder, os.path.splitext(file)[0] + ".pot")
    if os.path.exists(old_pot):
        logger.debug("merge pots{} {}".format(old_pot, tmp_pot))
        sh.msgmerge("-o", merge_pot, old_pot,  tmp_pot)
    # copy new pot to local folder
    else:
        merge_pot = tmp_pot
    logger.debug("copy pot file")
    sh.cp(merge_pot, old_pot)


def extract_pots():
    for (dirpath, dirnames, filenames) in os.walk("."):
        for file in filenames:
            if os.path.splitext(file)[1] != '.py':
                continue
            full_path = os.path.join(dirpath, file)
            extract_pot_file(full_path, file)

def generate_mo():
    with sh.pushd(locale_folder):
        cmd = sh.Command("./regenerate.py")
        cmd()

if __name__ == "__main__":
    extract_pots()
    generate_mo()

