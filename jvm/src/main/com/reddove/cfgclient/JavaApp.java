package com.reddove.cfgclient;

import java.io.*;

import com.reddove.config.*;

public class JavaApp {
    public static void main(String[] args) {
        String s = "{key: 'Hello, Java world!'}";
        StringReader r = new StringReader(s);
        Config cfg = new Config();
        cfg.load(r);
        //System.out.println((String) cfg.asDict().get("key"));
        System.out.println((String) cfg.get("key"));
    }
}
