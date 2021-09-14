from io import StringIO
import config

sio = StringIO("key: 'Hello, world!'")
cfg = config.Config(sio)
print('%s (%s)' % (cfg['key'], config.__version__))