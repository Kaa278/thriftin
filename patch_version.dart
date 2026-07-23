import 'dart:io';

void main() {
  var file = File('pubspec.yaml');
  var content = file.readAsStringSync();
  content = content.replaceFirst('version: 1.0.6+6', 'version: 1.0.7+7');
  file.writeAsStringSync(content);
}
