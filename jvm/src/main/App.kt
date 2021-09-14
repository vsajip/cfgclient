package com.reddove.cfgclient

import java.io.*

import com.reddove.config.*

class App {
    val greeting: String
        get() {
            val s = "{key: 'Hello, world!'}"
            val r = StringReader(s)
            val cfg = Config()
            cfg.load(r)
            return cfg.get("key") as String
        }
}

fun main() {
    println(App().greeting)
}
