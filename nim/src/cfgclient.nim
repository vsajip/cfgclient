import config
when isMainModule:
  var src = "{key: 'Hello, world!'}"
  var cfg = fromSource(src)
  echo cfg["key"].stringValue

