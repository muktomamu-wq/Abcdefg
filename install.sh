#!/bin/bash

echo "🚀 DRX INSTALLER STARTING..."

# 1. सभी फाइलों को परमिशन देना
chmod +x *

# 2. ज़रूरी लाइब्रेरीज़ इंस्टॉल करना
pip install pyTelegramBotAPI flask requests

# 3. बाइनरी फाइल कंपाइल करना (attack.c से bgmi बनाना)
gcc -pthread attack.c -o bgmi

# 4. बोट को चालू करना
echo "✅ SETUP COMPLETE! STARTING DRX BOT..."
python3 drx.py
