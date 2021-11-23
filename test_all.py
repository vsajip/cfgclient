#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Vinay Sajip
#
import argparse
import os
import subprocess
import sys
import time

if sys.version_info[:2] < (3, 6):
    print('This program must be run under Python 3.6 or later.')
    sys.exit(1)

DEBUGGING = 'PY_DEBUG' in os.environ

def get_exe(s):
    if os.name == 'posix':
        return s
    ext = '.exe'
    if s in ('npm', 'bundle', 'bundler', 'racc', 'rake', 'rdoc', 'ri', 'ridk',
             'erb', 'irb', 'gem'):
        ext = '.cmd'
    elif s in ('mix',):
        ext = '.bat'
    return '%s%s' % (s, ext)

def find_base(base, drive):
    start = '%s:/' % drive
    prefix = base.lower()
    for root, dirs, files in os.walk(start):
        for fn in files:
            n, e = os.path.splitext(fn)
            if n.lower() == prefix:
                p = os.path.join(root, fn)
                print(p.replace(os.sep, '/'))

def run_command(cmd, wd):
    print("Running '%s'" % cmd)
    if not isinstance(cmd, list):
        cmd = cmd.split()
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=wd)
        stdout, stderr = p.communicate()
        if p.returncode == 0:
            return stdout.decode('utf-8')
        else:
            print('Command failed with return code %d' % p.returncode)
            print('stdout was:')
            if stdout: print(stdout.decode('utf-8'))
            print('stderr was:')
            if stderr: print(stderr.decode('utf-8'))
            print('Raising an exception')
            raise subprocess.CalledProcessError(p.returncode, p.args,
                                                output=stdout, stderr=stderr)
        # return subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    except FileNotFoundError as e:
        # temporary kludge to find where things are
        if os.name == 'nt':
            exe = cmd[0]
            if os.path.isabs(exe):
                if os.path.exists(exe):
                    print('Path exists, some other problem: %s' % exe)
                else:
                    print('Not looking, because absolute: %s' % exe)
            else:
                base = os.path.splitext(exe)[0]
                print('Looking for %s' % base)
                find_base(base, 'c')
        raise


# TODO extend this to make everything more data-driven

LANGS = {
    'dlang': {
        'name': 'D',
        'commands': ['dub run'],
    },
    'dotnet': {
        'name': 'C#/.NET',
        'commands': ['dotnet run'],
    },
    'go': {
        'name': 'Go',
        'commands': [
            'go mod download github.com/vsajip/go-cfg-lib/config',
            'go run main.go'
        ],
    },
    'javascript': {
        'name': 'JavaScript/Node',
        'subdir': 'js'
    },
    'jvm': {
        'name': 'Kotlin/Java',
    },
    'python': {
        'name': 'Python',
    },
    'ruby': {
        'name': 'Ruby',
    },
    'rust': {
        'name': 'Rust',
        'commands': ['cargo run']
    },
    'elixir': {
        'name': 'Elixir',
    },
    'nim': {
        'name': 'Nim',
        'commands': ['nimble run -y']
    },
    'dart': {
        'name': 'Dart',
        'commands': [
            'dart pub get',
            'dart run'
        ]
    }
}

def lang(s):
    if s not in LANGS:
        raise ValueError('Invalid lang: %s' % s)
    return s


def test_generic(lang, basedir):
    info = LANGS[lang]
    print('Testing for %(name)s ...' % info)
    wd = os.path.join(basedir, info.get('subdir', lang))
    commands = info['commands']
    n = len(commands)
    if n > 1:
        for i in range(n - 1):
            run_command(commands[i], wd)
    out = run_command(commands[-1], wd)
    lines = out.splitlines()
    match = info.get('match', 'Hello, world!')
    if lines[-1] != match:
        raise ValueError('Unexpected result for %s: %s' % (lang, out))

# def test_dlang(basedir):
    # print('Testing for D ...')
    # wd = os.path.join(basedir, 'dlang')
    # out = run_command('dub run', wd)
    # lines = out.splitlines()
    # if lines[-1] != 'Hello, world!':
        # raise ValueError('Unexpected result for D: %s' % out)
    # test_generic('dlang', basedir)

# def test_dotnet(basedir):
    # print('Testing for C#/.NET ...')
    # wd = os.path.join(basedir, 'dotnet')
    # out = run_command('dotnet run', wd)
    # lines = out.splitlines()
    # if lines[-1] != 'Hello, world!':
        # raise ValueError('Unexpected result for C#: %s' % out)
    # test_generic('dotnet', basedir)

# def test_go(basedir):
    # print('Testing for Go ...')
    # wd = os.path.join(basedir, 'go')
    # run_command('go mod download github.com/vsajip/go-cfg-lib/config', wd)
    # out = run_command('go run main.go', wd)
    # lines = out.splitlines()
    # if lines[-1] != 'Hello, world!':
        # raise ValueError('Unexpected result for Go: %s' % out)
    # test_generic('go', basedir)

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
    start = time.time()
    out = run_command('%s run --no-daemon' % get_exe('gradle'), wd)
    if os.name == 'nt':
        expected1 = 'Hello, Kotlin world!\r\n'
        expected2 = 'Hello, Java world!\r\n'
    else:
        expected1 = 'Hello, Kotlin world!\n'
        expected2 = 'Hello, Java world!\n'
    if expected1 not in out or expected2 not in out:
        raise ValueError('Unexpected result for JVM: %s' % out)
    # elapsed = time.time() - start
    # print('Run completed in %.2f secs' % elapsed)
    # print(out)

def test_python(basedir):
    print('Testing for Python ...')
    wd = os.path.join(basedir, 'python')
    out = run_command(['python', 'app.py'], wd)
    if 'Hello, world! (' not in out:
        p = os.path.join(wd, 'app.log')
        with open(p, encoding='utf-8') as f:
            data = f.read()
        print(data)
        raise ValueError('Unexpected result for Python: %s' % out)

def test_ruby(basedir):
    print('Testing for Ruby ...')
    wd = os.path.join(basedir, 'ruby')
    run_command('%s install' % get_exe('bundle'), wd)
    out = run_command('%s cfgclient.rb' % get_exe('ruby'), wd)
    lines = out.splitlines()
    if not lines[-1].startswith('Hello, world! ('):
        raise ValueError('Unexpected result for Ruby: %s' % out)

# def test_rust(basedir):
    # print('Testing for Rust ...')
    # wd = os.path.join(basedir, 'rust')
    # out = run_command('cargo%s run' % EXE_EXT, wd)
    # lines = out.splitlines()
    # if lines[-1] != 'Hello, world!':
        # raise ValueError('Unexpected result for Rust: %s' % out)
    # test_generic('rust', basedir)

def test_elixir(basedir):
    print('Testing for Elixir ...')
    wd = os.path.join(basedir, 'elixir')
    run_command('%s deps.get' % get_exe('mix'), wd)
    run_command('%s compile' % get_exe('mix'), wd)
    out = run_command('%s run cfgclient.exs' % get_exe('mix'), wd)
    lines = out.splitlines()
    if lines[-1] != 'Hello, world!':
        raise ValueError('Unexpected result for Elixir: %s' % out)

# def test_nim(basedir):
    # print('Testing for Nim ...')
    # wd = os.path.join(basedir, 'nim')
    # out = run_command('%s run -y' % get_exe('nimble'), wd)
    # lines = out.splitlines()
    # if lines[-1] != 'Hello, world!':
        # raise ValueError('Unexpected result for Nim: %s' % out)
    # test_generic('nim', basedir)

# def test_dart(basedir):
    # print('Testing for Dart ...')
    # wd = os.path.join(basedir, 'dart')
    # run_command('%s pub get' % get_exe('dart'), wd)
    # out = run_command('%s run' % get_exe('dart'), wd)
    # lines = out.splitlines()
    # if lines[-1] != 'Hello, world!':
        # raise ValueError('Unexpected result for Dart: %s' % out)
    # test_generic('dart', basedir)

def main():
    print('Running on Python %s: %s' % (sys.version_info[:2], sys.executable))
    adhf = argparse.ArgumentDefaultsHelpFormatter
    ap = argparse.ArgumentParser(formatter_class=adhf)
    aa = ap.add_argument
    aa('langs', metavar='LANG', nargs='*', type=lang,
       help='Language to run test for')
    options = ap.parse_args()
    options.all = not bool(options.langs)
    basedir = os.getcwd()

    for language, info in LANGS.items():
        if not options.all and language not in options.langs:
            continue
        if 'commands' in info:
            test_generic(language, basedir)
        else:
            if language == 'javascript':
                test_js(basedir)
            elif language == 'ruby':
                test_ruby(basedir)
            elif language == 'python':
                test_python(basedir)
            elif language =='elixir':
                test_elixir(basedir)
            elif language == 'jvm':
                test_jvm(basedir)

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
