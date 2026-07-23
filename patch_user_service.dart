import 'dart:io';
void main() {
  var file = File('lib/services/user_service.dart');
  var content = file.readAsStringSync();
  
  // Add localPhotoOverride
  content = content.replaceFirst(
    'static Map<String, dynamic>? currentUser;',
    'static Map<String, dynamic>? currentUser;\n  static String? localPhotoOverride;'
  );
  
  // Update updateBioAndPhoto
  var oldUpdate = '''
    if (photoPath != null) {
      data['photo_path'] = photoPath.startsWith('http')
          ? photoPath
          : await uploadProfilePhoto(
              userId: userId,
              imageFile: File(photoPath),
            );
    }
''';
  var newUpdate = '''
    if (photoPath != null) {
      if (!photoPath.startsWith('http')) {
        localPhotoOverride = photoPath;
        data['photo_path'] = await uploadProfilePhoto(
          userId: userId,
          imageFile: File(photoPath),
        );
      } else {
        data['photo_path'] = photoPath;
      }
    }
''';
  content = content.replaceFirst(oldUpdate, newUpdate);
  
  // Clear on logout
  content = content.replaceFirst(
    'currentUser = null;\n    _userCache.clear();',
    'currentUser = null;\n    localPhotoOverride = null;\n    _userCache.clear();'
  );
  
  file.writeAsStringSync(content);
}
