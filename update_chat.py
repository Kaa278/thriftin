import re

with open('lib/screens/chat_screen.dart', 'r') as f:
    content = f.read()

# 1. State vars
state_vars = """  bool _isLoading = true;
  bool _isSendingImage = false;
  File? _selectedImage;
  bool _isOtherUserOnline = false;
  bool _isOtherUserTyping = false;
  Timer? _typingDebounce;"""

content = re.sub(r'  bool _isLoading = true;[\s\S]*?bool _isOtherUserOnline = false;', state_vars, content)

# 2. Add typing signal and initState update
init_state_pattern = r'  @override\n  void initState\(\) {\n    super\.initState\(\);\n    _prepareRoom\(\);\n  }'
init_state_repl = """  @override
  void initState() {
    super.initState();
    _prepareRoom();
    _msgController.addListener(() {
      if (_msgController.text.isNotEmpty) {
        _sendTypingSignal();
      }
    });
  }

  void _sendTypingSignal() {
    final roomId = ChatScreen.activeRoomId;
    final currentUserId = UserService.currentUserId;
    if (roomId == null || currentUserId == null) return;
    _roomRealtimeChannel?.sendBroadcastMessage(
      event: 'typing',
      payload: {'user_id': currentUserId},
    );
  }"""
content = re.sub(init_state_pattern, init_state_repl, content)

# 3. Add typing listener in subscribe
subscribe_pattern = r'(\.onPostgresChanges\([\s\S]*?\n          \))\n          \.subscribe\('
subscribe_repl = r"""\1
          .onBroadcast(
            event: 'typing',
            callback: (payload) {
              final typingUserId = int.tryParse(payload['user_id']?.toString() ?? '');
              if (typingUserId != null && typingUserId != currentUserId) {
                if (!mounted) return;
                setState(() => _isOtherUserTyping = true);
                _typingDebounce?.cancel();
                _typingDebounce = Timer(const Duration(seconds: 3), () {
                  if (mounted) setState(() => _isOtherUserTyping = false);
                });
              }
            },
          )
          .subscribe("""
content = re.sub(subscribe_pattern, subscribe_repl, content)

# 4. Dispose
dispose_pattern = r'    _markReadDebounce\?\.cancel\(\);'
dispose_repl = """    _typingDebounce?.cancel();\n    _markReadDebounce?.cancel();"""
content = re.sub(dispose_pattern, dispose_repl, content)

# 5. ListView builder
listview_pattern = r'                      Widget messageWidget;\n                      if \(offerAmount != null\) {\n                        messageWidget = _buildOfferCard\(\n                          _formatPrice\(offerAmount\),\n                          _formatTime\(msg\[\'created_at\'\]\),\n                        \);\n                      } else {\n                        final messageText = msg\[\'message\'\]\?\.toString\(\) \?\? \'\'\;\n                        final imageUrl = ChatService\.imageUrlFromMessage\(\n                          messageText,\n                        \);\n                        if \(imageUrl != null\) {\n                          messageWidget = _buildImageBubble\(\n                            imageUrl,\n                            !isMine,\n                            _formatTime\(msg\[\'created_at\'\]\),\n                          \);\n                        } else {\n                          messageWidget = _buildBubble\(\n                            messageText,\n                            !isMine,\n                            _formatTime\(msg\[\'created_at\'\]\),\n                          \);\n                        }\n                      }'
listview_repl = """                      Widget messageWidget;
                      final isRead = msg['is_read'] == 1 || msg['is_read'] == true;
                      if (offerAmount != null) {
                        messageWidget = _buildOfferCard(
                          _formatPrice(offerAmount),
                          _formatTime(msg['created_at']),
                          isRead,
                          !isMine,
                        );
                      } else {
                        final messageText = msg['message']?.toString() ?? '';
                        final imageUrl = ChatService.imageUrlFromMessage(
                          messageText,
                        );
                        if (imageUrl != null) {
                          messageWidget = _buildImageBubble(
                            imageUrl,
                            !isMine,
                            _formatTime(msg['created_at']),
                            isRead,
                          );
                        } else {
                          messageWidget = _buildBubble(
                            messageText,
                            !isMine,
                            _formatTime(msg['created_at']),
                            isRead,
                          );
                        }
                      }"""
content = re.sub(listview_pattern, listview_repl, content)

# 6. UI: User is typing
typing_ui = """          if (_isOtherUserTyping)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 4),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'User sedang mengetik...',
                  style: TextStyle(
                    fontSize: 12,
                    fontStyle: FontStyle.italic,
                    color: AppColors.textHint,
                  ),
                ),
              ),
            ),
          // Input bar"""
content = content.replace('          // Input bar', typing_ui)


# 7. Modify `_buildBubble`, `_buildImageBubble`, `_buildOfferCard` signatures and return bodies.

# `_buildBubble`
def replace_bubble(m):
    time_block = m.group(1)
    new_time_block = """Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      time,
                      style: const TextStyle(
                        fontSize: 10,
                        color: AppColors.textHint,
                      ),
                    ),
                    if (!isSeller && isRead) ...[
                      const SizedBox(width: 4),
                      const Icon(Icons.done_all_rounded, size: 12, color: AppColors.primary),
                    ],
                  ],
                )"""
    return "Widget _buildBubble(String text, bool isSeller, String time, bool isRead) {\n" + time_block.replace("Text(\n                  time,\n                  style: const TextStyle(\n                    fontSize: 10,\n                    color: AppColors.textHint,\n                  ),\n                )", new_time_block)

content = re.sub(r'Widget _buildBubble\(String text, bool isSeller, String time\) {([\s\S]*?)(?=Widget _buildImageBubble)', replace_bubble, content)

# `_buildImageBubble`
def replace_image_bubble(m):
    time_block = m.group(1)
    new_time_block = """Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      time,
                      style: const TextStyle(
                        fontSize: 10,
                        color: AppColors.textHint,
                      ),
                    ),
                    if (!isSeller && isRead) ...[
                      const SizedBox(width: 4),
                      const Icon(Icons.done_all_rounded, size: 12, color: AppColors.primary),
                    ],
                  ],
                )"""
    return "Widget _buildImageBubble(String imageUrl, bool isSeller, String time, bool isRead) {\n" + time_block.replace("Text(\n                  time,\n                  style: const TextStyle(\n                    fontSize: 10,\n                    color: AppColors.textHint,\n                  ),\n                )", new_time_block)

content = re.sub(r'Widget _buildImageBubble\(String imageUrl, bool isSeller, String time\) {([\s\S]*?)(?=Widget _buildOfferCard)', replace_image_bubble, content)

# `_buildOfferCard`
# Wait, I need to know the exact signature and usage of `time` in _buildOfferCard.
# I passed `!isMine` as `isSeller` to `_buildOfferCard`. Let's check `_buildOfferCard`.
with open('lib/screens/chat_screen.dart', 'w') as f:
    f.write(content)
