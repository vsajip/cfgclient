package.cpath = package.cpath .. ';/home/vinay/.local/lib/lua/5.5/?.so'
config = require('config')
src = "{key: 'Hello, world!'}"
cfg = config.Config:from_source(src)
print(cfg.key)
