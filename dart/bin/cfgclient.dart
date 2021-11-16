import 'package:cfg_lib/cfg_lib.dart';

void main(List<String> arguments) {
  var src = "{key: 'Hello, world!'}";
  var cfg = Config.fromSource(src);
  print(cfg['key']);
}
