import 'dart:io';
void main() {
  var file = File('lib/screens/profile_screen.dart');
  var content = file.readAsStringSync();
  
  content = content.replaceFirst(
    "photoPath: UserService.currentUser?['photo_path']?.toString(),",
    "photoPath: UserService.localPhotoOverride ?? UserService.currentUser?['photo_path']?.toString(),"
  );
  
  file.writeAsStringSync(content);
}
