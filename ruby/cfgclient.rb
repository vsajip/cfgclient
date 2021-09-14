# frozen_string_literal: true
require 'stringio'
require 'CFG/config'
require 'CFG/version'

include CFG

src = "{key: 'Hello, world!'}"
stream = StringIO.new src, 'r:utf-8'
cfg = Config.new stream
printf "%s (%s)\n", cfg['key'], CFG::VERSION
