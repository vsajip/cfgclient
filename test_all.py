#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Vinay Sajip
#
import argparse
import os
import subprocess
import sys

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
            if stdout:
                print(stdout.decode('utf-8'))
            print('stderr was:')
            if stderr:
                print(stderr.decode('utf-8'))
            print('Raising an exception')
            raise subprocess.CalledProcessError(p.returncode, p.args,
                                                output=stdout, stderr=stderr)
        # return subprocess.check_output(cmd, cwd=wd).decode('utf-8')
    except FileNotFoundError:
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
        'subdir': 'js',
        'commands': [
            '%s i cfg-lib' % get_exe('npm'),
            '%s app.js' % get_exe('node')
        ]
    },
    'jvm': {
        'name': 'Kotlin/Java',
        'commands': [
            '%s run --no-daemon' % get_exe('gradle')
        ],
        'match': [
            ('in', 'Hello, Kotlin world!\r\n' if os.name == 'nt' else 'Hello, Kotlin world!\n'),
            ('in', 'Hello, Java world!\r\n' if os.name == 'nt' else 'Hello, Java world!\n'),
        ]
    },
    'python': {
        'name': 'Python',
        'commands': ['python app.py'],
        'match': [
            ('startswith', 'Hello, world! (')
        ]
    },
    'ruby': {
        'name': 'Ruby',
        'commands': [
            '%s install' % get_exe('bundle'),
            '%s cfgclient.rb' % get_exe('ruby')
        ],
        'match': [
            ('startswith', 'Hello, world! (')
        ]
    },
    'rust': {
        'name': 'Rust',
        'commands': ['cargo run']
    },
    'elixir': {
        'name': 'Elixir',
        'commands': [
            '%s deps.get' % get_exe('mix'),
            '%s compile' % get_exe('mix'),
            '%s run cfgclient.exs' % get_exe('mix')
        ]
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
    },
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
    match = info.get('match', 'Hello, world!')
    if isinstance(match, str):
        lines = out.splitlines()
        if lines[-1] != match:
            raise ValueError('Unexpected result for %s: %s' % (lang, out))
    else:
        assert isinstance(match, (list, tuple))
        for kind, value in match:
            assert kind in ('startswith', 'in')
            if kind == 'startswith':
                lines = out.splitlines()
                if not lines[-1].startswith(value):
                    raise ValueError('Unexpected result for %s: %s' % (lang, out))
            else:
                if value not in out:
                    raise ValueError('Unexpected result for %s: %s' % (lang, out))


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

    def sortkey(t):
        return t[0] if t[0] != 'jvm' else 'zzz'  # sort JVM last, as it takes forever
    for language, info in sorted(LANGS.items(), key=sortkey):
        if not options.all and language not in options.langs:
            continue
        assert 'commands' in info
        test_generic(language, basedir)


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
        if DEBUGGING:
            import traceback
            traceback.print_exc()
        rc = 1
    sys.exit(rc)
