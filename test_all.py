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
EXE_EXT = '.exe' if os.name == 'nt' else ''

def get_exe(s):
    if os.name == 'posix':
        return s
    ext = '.exe'
    if s in ('npm', 'bundle', 'bundler', 'racc', 'rake', 'rdoc', 'ri', 'ridk',
             'erb', 'irb', 'gem'):
        ext = '.cmd'
    elif s == 'gradle':
        ext = '.bat'
    return '%s%s' % (s, ext)

def run_command(cmd, wd):
    print("Running '%s'" % cmd)
    if not isinstance(cmd, list):
        cmd = cmd.split()
    return subprocess.check_output(cmd, cwd=wd).decode('utf-8')

def test_dlang(basedir):
    print('Testing for D ...')
    wd = os.path.join(basedir, 'dlang')
    out = run_command('dub run', wd)
    lines = out.splitlines()
    if lines[-1] != 'Hello, world!':
        raise ValueError('Unexpected result for D: %s' % out)

def test_dotnet(basedir):
    print('Testing for C#/.NET ...')
    wd = os.path.join(basedir, 'dotnet')
    out = run_command('dotnet run', wd)
    lines = out.splitlines()
    if lines[-1] != 'Hello, world!':
        raise ValueError('Unexpected result for C#: %s' % out)

def test_go(basedir):
    print('Testing for Go ...')
    wd = os.path.join(basedir, 'go')
    run_command('go mod download github.com/vsajip/go-cfg-lib/config', wd)
    out = run_command('go run main.go', wd)
    lines = out.splitlines()
    if lines[-1] != 'Hello, world!':
        raise ValueError('Unexpected result for Go: %s' % out)

def test_js(basedir):
    print('Testing for JavaScript ...')
    wd = os.path.join(basedir, 'js')
    run_command('%s i cfg-lib' % get_exe('npm'), wd)
    out = run_command('%s app.js' % get_exe('node'), wd)
    lines = out.splitlines()
    if lines[-1] != 'Hello, world!':
        raise ValueError('Unexpected result for JavaScript/Node: %s' % out)

def test_jvm(basedir):
    print('Testing for Kotlin/Java ...')
    wd = os.path.join(basedir, 'jvm')
    out = run_command('%s run' % get_exe('gradle'), wd)
    if os.name == 'nt':
        expected = '> Task :run\r\nHello, world!\r\nHello, world!\r\n'
    else:
        expected = '> Task :run\nHello, world!\nHello, world!\n'
    if expected not in out:
        raise ValueError('Unexpected result for JVM: %s' % out)

def test_python(basedir):
    print('Testing for Python ...')
    wd = os.path.join(basedir, 'python')
    out = run_command([sys.executable, 'app.py'], wd)
    lines = out.splitlines()
    if not lines[-1].startswith('Hello, world! ('):
        raise ValueError('Unexpected result for Python: %s' % out)

def test_ruby(basedir):
    print('Testing for Ruby ...')
    wd = os.path.join(basedir, 'ruby')
    run_command('%s install' % get_exe('bundle'), wd)
    out = run_command('%s cfgclient.rb' % get_exe('ruby'), wd)
    lines = out.splitlines()
    if not lines[-1].startswith('Hello, world! ('):
        raise ValueError('Unexpected result for Ruby: %s' % out)

def test_rust(basedir):
    print('Testing for Rust ...')
    wd = os.path.join(basedir, 'rust')
    out = run_command('cargo%s run' % EXE_EXT, wd)
    lines = out.splitlines()
    if lines[-1] != 'Hello, world!':
        raise ValueError('Unexpected result for Rust: %s' % out)

LANGS = set(('dlang', 'dotnet', 'go', 'javascript', 'jvm', 'python', 'ruby', 'rust'))

def lang(s):
    if s not in LANGS:
        raise ValueError('Invalid lang: %s' % s)
    return s

def main():
    adhf = argparse.ArgumentDefaultsHelpFormatter
    ap = argparse.ArgumentParser(formatter_class=adhf)
    aa = ap.add_argument
    aa('langs', metavar='LANG', nargs='*', type=lang,
       help='Language to run test for')
    options = ap.parse_args()
    options.all = not bool(options.langs)
    basedir = os.getcwd()
    if options.all or 'dlang' in options.langs:
        test_dlang(basedir)
    if options.all or 'dotnet' in options.langs:
        test_dotnet(basedir)
    if options.all or 'go' in options.langs:
        test_go(basedir)
    if options.all or 'javascript' in options.langs:
        test_js(basedir)
    if options.all or 'jvm' in options.langs:
        test_jvm(basedir)
    if options.all or 'python' in options.langs:
        test_python(basedir)
    if options.all or 'ruby' in options.langs:
        test_ruby(basedir)
    if options.all or 'rust' in options.langs:
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
