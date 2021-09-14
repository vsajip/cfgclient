const config = require('cfg-lib');

var s = config.makeStream("key: 'Hello, world!'");
var cfg = new config.Config(s);
console.log(cfg.get('key'));
