#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Red Dove Consultants Limited
#
import argparse
import logging
import os
import shutil
import subprocess
import sys

if sys.version_info[:2] < (3, 6):
    print('This program must be run under Python 3.6 or later.')
    sys.exit(1)

import venv

DEBUGGING = 'PY_DEBUG' in os.environ

logger = logging.getLogger(__name__)

def dump_dirs(start):
    for root, dirs, files in os.walk(start):
        for fn in files:
            p = os.path.join(root, fn)
            print(p)

def main():
    logging.basicConfig(level=logging.DEBUG,
                        filename='app.log', filemode='w',
                        format='%(levelname)-8s %(name)s %(message)s')
    adhf = argparse.ArgumentDefaultsHelpFormatter
    ap = argparse.ArgumentParser(formatter_class=adhf)
    aa = ap.add_argument
    # aa('--example', help='Example argument')
    options = ap.parse_args()
    if os.path.isdir('env'):
        shutil.rmtree('env')
    try:
        envpath = os.path.abspath('env')
        logger.debug('Creating venv at %s', envpath)
        venv.create(envpath, with_pip=True)
        logger.debug('Created venv at %s', envpath)
        if os.name == 'posix':
            pyexec = os.path.join(envpath, 'bin', 'python')
        else:
            # dump_dirs(envpath)
            d = os.path.join(envpath, 'Scripts')
            if not os.path.exists(d):
                d = os.path.join(envpath, 'bin')
            pyexec = os.path.join(d, 'python.exe')
        if not os.path.exists(pyexec):
            d = os.path.dirname(pyexec)
            logger.debug('Executable %s not found, dir has: %s', (pyexec, os.listdir(d)))
        cmd = [pyexec, '-m', 'pip', 'install', 'config']
        logger.debug('About to run: \'%s\'' % ' '.join(cmd))
        out = subprocess.check_output(cmd).decode('utf-8')
        cmd = [pyexec, 'prog.py']
        logger.debug('About to run: \'%s\'' % ' '.join(cmd))
        subprocess.check_call(cmd)
    except Exception as e:
        logger.exception('Failed: %s: %s' % (e.__class__, e))

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
