#!/usr/local/bin/python3
import sys
import os
import subprocess


def start(args):
    env = os.environ.copy()
    pwd = subprocess.check_output(['pwd'])
    dir = pwd.decode().rstrip() + '/passthrough.py'
    pid = subprocess.Popen([dir]+args).pid
    print(pid)

args = sys.argv[1:]
start(args)