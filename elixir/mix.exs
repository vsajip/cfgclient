defmodule CFGClient.MixProject do
  use Mix.Project

  def project do
    [
      app: :cfg_client,
      version: "0.1.0",
      elixir: "~> 1.12",
      start_permanent: Mix.env() == :prod,
      escript: [main_module: CFGClient],
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger]
    ]
  end

  defp deps do
    [
      {:cfg_lib, "~> 0.0"}
    ]
  end
end
