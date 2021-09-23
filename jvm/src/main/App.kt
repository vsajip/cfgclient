package com.reddove.cfgclient

import java.io.*

import com.reddove.config.*

class App {
    val greeting: String
        get() {
            val s = "{key: 'Hello, Kotlin world!'}"
            val r = StringReader(s)
            val cfg = Config()
            cfg.load(r)
            return cfg["key"] as String
        }
}

fun main() {
    JavaApp.main(arrayOf(""))
    println(App().greeting)
}
