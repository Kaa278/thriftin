import 'dart:io';

void main() {
  var file = File('pubspec.yaml');
  var content = file.readAsStringSync();
  content = content.replaceFirst('version: 1.0.7+7', 'version: 1.0.8+8');
  file.writeAsStringSync(content);
}
