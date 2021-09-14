namespace app
{
    using System;
    using System.IO;

    using RedDove.Config;

    class App
    {
        static void Main(string[] args)
        {
            var s = "{key: 'Hello, world!'}";
            var reader = new StringReader(s);
            var cfg = new Config(reader);
            Console.WriteLine(cfg["key"]);
        }
    }
}
