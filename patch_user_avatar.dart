import 'dart:io';
void main() {
  var file = File('lib/widgets/user_avatar.dart');
  var content = file.readAsStringSync();
  
  var oldCode = '''
    final file = File(path);
    if (file.existsSync()) {
      return CircleAvatar(
        radius: radius,
        backgroundColor: const Color(0xFFE8EEF4),
        backgroundImage: FileImage(file),
      );
    }
''';
  var newCode = '''
    final file = File(path);
    if (file.existsSync()) {
      final fileImage = FileImage(file);
      fileImage.evict(); // Force Flutter to read from disk again
      return CircleAvatar(
        radius: radius,
        backgroundColor: const Color(0xFFE8EEF4),
        backgroundImage: fileImage,
      );
    }
''';
  content = content.replaceFirst(oldCode, newCode);
  file.writeAsStringSync(content);
}
