#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Red Dove Consultants Limited
#
import argparse
import os
import shutil
import subprocess
import sys

if sys.version_info[:2] < (3, 6):
    print('This program must be run under Python 3.6 or later.')
    sys.exit(1)

import venv

DEBUGGING = 'PY_DEBUG' in os.environ

def main():
    adhf = argparse.ArgumentDefaultsHelpFormatter
    ap = argparse.ArgumentParser(formatter_class=adhf)
    aa = ap.add_argument
    # aa('--example', help='Example argument')
    options = ap.parse_args()
    if os.path.isdir('env'):
        shutil.rmtree('env')
    try:
        envpath = os.path.abspath('env')
        venv.create(envpath, with_pip=True)
        if os.name == 'posix':
            pyexec = os.path.join(envpath, 'bin', 'python')
        else:
            pyexec = os.path.join(envpath, 'Scripts', 'python.exe')
        if not os.path.exists(pyexec):
            d = os.path.dirname(pyexec)
            print('Executable %s not found, dir has: %s' % (pyexec, os.listdir(d)))
        cmd = [pyexec, '-m', 'pip', 'install', 'config']
        out = subprocess.check_output(cmd).decode('utf-8')
        cmd = [pyexec, 'prog.py']
        subprocess.check_call(cmd)
    except Exception as e:
        print('Failed for %s: %s' % (cmd, e.__class__))

if __name__ == '__main__':
    try:
        rc = main()
    except KeyboardInterrupt:
        rc = 2
    except Exception as e:
        if DEBUGGING:
            s = ' %s:' % type(e).__name__
        else:
            s = ''
        sys.stderr.write('Failed:%s %s\n' % (s, e))
        if DEBUGGING: import traceback; traceback.print_exc()
        rc = 1
    sys.exit(rc)
