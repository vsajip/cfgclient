# Package

version       = "0.1.0"
author        = "Vinay Sajip"
description   = "A test client program for the CFG library."
license       = "BSD-3-Clause"
srcDir        = "src"
bin           = @["cfgclient"]


# Dependencies

requires "nim >= 1.4.4"
# requires "config >= 0.1.0"
requires "https://github.com/vsajip/nim-cfg-lib" # temporary
