#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Red Dove Consultants Limited
#
import argparse
import os
import subprocess
import sys

if sys.version_info[:2] < (3, 6):
    print('This program must be run under Python 3.6 or later.')
    sys.exit(1)

DEBUGGING = 'PY_DEBUG' in os.environ

def test_dlang(basedir):
    wd = os.path.join(basedir, 'dlang')
    cmd = 'dub run'.split()
    out = subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    lines = out.splitlines()
    if lines[-1] != 'Hello, world!':
        raise ValueError('Unexpected result for D: %s' % out)

def test_dotnet(basedir):
    wd = os.path.join(basedir, 'dotnet')
    cmd = 'dotnet run'.split()
    out = subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    lines = out.splitlines()
    if lines[-1] != 'Hello, world!':
        raise ValueError('Unexpected result for C#: %s' % out)

def test_go(basedir):
    wd = os.path.join(basedir, 'go')
    cmd = 'go mod download github.com/vsajip/go-cfg-lib/config'.split()
    out = subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    lines = out.splitlines()
    cmd = 'go run main.go'.split()
    out = subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    lines = out.splitlines()
    if lines[-1] != 'Hello, world!':
        raise ValueError('Unexpected result for Go: %s' % out)

def test_js(basedir):
    wd = os.path.join(basedir, 'js')
    cmd = 'npm i cfg-lib'.split()
    out = subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    lines = out.splitlines()
    cmd = 'node app.js'.split()
    out = subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    lines = out.splitlines()
    if lines[-1] != 'Hello, world!':
        raise ValueError('Unexpected result for JavaScript/Node: %s' % out)

def test_jvm(basedir):
    wd = os.path.join(basedir, 'jvm')
    cmd = 'gradle run'.split()
    out = subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    if os.name == 'nt':
        expected = '> Task :run\r\nHello, world!\r\nHello, world!\r\n'
    else:
        expected = '> Task :run\nHello, world!\nHello, world!\n'
    if expected not in out:
        raise ValueError('Unexpected result for JVM: %s' % out)

def test_python(basedir):
    wd = os.path.join(basedir, 'python')
    cmd = 'python3 app.py'.split()
    out = subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    lines = out.splitlines()
    if not lines[-1].startswith('Hello, world! ('):
        raise ValueError('Unexpected result for Python: %s' % out)

def test_ruby(basedir):
    wd = os.path.join(basedir, 'ruby')
    cmd = 'bundle install'.split()
    out = subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    lines = out.splitlines()
    cmd = 'ruby cfgclient.rb'.split()
    out = subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    lines = out.splitlines()
    if not lines[-1].startswith('Hello, world! ('):
        raise ValueError('Unexpected result for Ruby: %s' % out)

def test_rust(basedir):
    wd = os.path.join(basedir, 'rust')
    cmd = 'cargo run'.split()
    out = subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    lines = out.splitlines()
    if lines[-1] != 'Hello, world!':
        raise ValueError('Unexpected result for Rust: %s' % out)

def main():
    adhf = argparse.ArgumentDefaultsHelpFormatter
    ap = argparse.ArgumentParser(formatter_class=adhf)
    aa = ap.add_argument
    # aa('--example', help='Example argument')
    options = ap.parse_args()
    basedir = os.getcwd()
    test_dlang(basedir)
    test_dotnet(basedir)
    test_go(basedir)
    test_js(basedir)
    test_jvm(basedir)
    test_python(basedir)
    test_ruby(basedir)
    test_rust(basedir)

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
