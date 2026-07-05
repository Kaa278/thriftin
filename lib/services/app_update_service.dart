import 'supabase_config.dart';

class AppUpdateInfo {
  final String latestVersion;
  final String playStoreUrl;
  final bool isRequired;

  AppUpdateInfo({
    required this.latestVersion,
    required this.playStoreUrl,
    required this.isRequired,
  });
}

class AppUpdateService {
  static const String currentAppVersion = '1.0.2';

  Future<AppUpdateInfo?> checkForUpdate() async {
    try {
      // Query app_config table from Supabase
      final results = await SupabaseConfig.client
          .from('app_config')
          .select()
          .limit(10);

      if (results.isEmpty) return null;

      String? latestVersion;
      String? playStoreUrl;
      bool isRequired = false;

      for (var row in results) {
        final key = row['key']?.toString();
        final value = row['value']?.toString();

        if (key == 'latest_version') {
          latestVersion = value;
        } else if (key == 'play_store_url') {
          playStoreUrl = value;
        } else if (key == 'update_required') {
          isRequired = value == 'true' || value == '1';
        }
      }

      if (latestVersion != null && playStoreUrl != null) {
        if (_isVersionOlder(currentAppVersion, latestVersion)) {
          return AppUpdateInfo(
            latestVersion: latestVersion,
            playStoreUrl: playStoreUrl,
            isRequired: isRequired,
          );
        }
      }
    } catch (_) {
      // Graceful error handling if table or columns don't exist yet
    }
    return null;
  }

  bool _isVersionOlder(String current, String latest) {
    try {
      final currentParts = current.split('+')[0].split('.').map(int.parse).toList();
      final latestParts = latest.split('+')[0].split('.').map(int.parse).toList();

      for (var i = 0; i < 3; i++) {
        final currentPart = currentParts.length > i ? currentParts[i] : 0;
        final latestPart = latestParts.length > i ? latestParts[i] : 0;

        if (latestPart > currentPart) return true;
        if (currentPart > latestPart) return false;
      }
    } catch (_) {}
    return false;
  }
}
