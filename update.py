#!/usr/bin/python3.7

from os import path
from pathlib import Path
from subprocess import run
from subprocess import call
import os
import sys
import yaml
import getopt

def clone_tree(url,clone_dir,branch,revision):
    try:
        git_config = clone_dir + "/.git/config"
        if Path(git_config).is_file():
            print("### %s checkout is already present.Delete it." %clone_dir)
            run(["rm", "-rf", clone_dir], check=True)

        print("### Cloning or copy tree")
        Path(clone_dir).mkdir(exist_ok=True, parents=True)

        if not  url.startswith("https:") and not  url.startswith("git@"):
            print("### copy local tree")
            return copy_local_file(url+"/.",clone_dir)

        run(["git", "clone", "--recursive", url, clone_dir], check=True)
        print("### Clone done")

        if branch != "":
            print("### Checkout branch: %s"%branch)
            os.chdir(clone_dir)
            run(["git", "checkout", "origin/"+branch], check=True)
            print("### Checkout done")

        if revision != "":
            print("### Reset to Revision: %s"%revision)
            os.chdir(clone_dir)
            run(["git", "reset", "--hard", revision], check=True)
            print("### Reset done")

        os.chdir(clone_dir)
        run(["rm", "-rf", ".git/"], check=True)
        run(["rm", "-rf", ".github/"], check=True)
        return 0
    except:
        print("### Cloning the tree %s failed"%clone_dir)
        return 1

TOPDIR = Path.cwd().absolute()
CONFIG = "update.yml"

if not sys.version_info >= (3, 6):
    print("This script requires Python 3.6 or higher!")
    print("You are using Python {}.{} by default.".format(sys.version_info.major, sys.version_info.minor))
    print("The following versions of Python3 have been installed on your system.")
    print("You can use the command 'cd /usr/bin/ && ln -sf <python3_version> python3' to change it.")
    os.system("ls -l /usr/bin/python3*")
    sys.exit(1)

try:
    opts, args = getopt.getopt(sys.argv[1:], "c:", ["config="])
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

for o, a in opts:
    if o in ("-c", "--config"):
        CONFIG = a
    else:
        assert False, "unhandled option"

if not Path(CONFIG).is_file():
    print(f"Missing {CONFIG}")
    sys.exit(1)
CONFIG = yaml.safe_load(open(CONFIG))

source = CONFIG['feeds_url']
for n in source:
    if n.__contains__("name") and n.__contains__("url"):
        if n.__contains__("revision"):
            revision = n["revision"]
        else:
            revision = ""

        if n.__contains__("branch"):
            branch = n["branch"]
        else:
            branch = ""
       
        clone_tree(n["url"], n["name"], branch, revision)
        os.chdir(TOPDIR)
