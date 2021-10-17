alias CFG.Config
src = "{key: 'Hello, world!'}"
{:ok, cfg} = Config.from_source(src)
{:ok, v} = Config.get(cfg, "key")
IO.puts(v)
