import std.algorithm.iteration;
import std.stdio;
import std.range;
import std.string;

import config;

void main()
{
	auto s = "{key: 'Hello, world!'}";
	auto r = inputRangeObject(s.representation.map!(b => ubyte(b)));
	auto cfg = new Config(r);
	writeln(cfg["key"]);
}
