import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# ==================== CONFIGURATION ====================
BOT_TOKEN = "8855553129:AAGbCJEtQZ9dDOvOEzNl8S-2fpPFqiUIGjM"
CHANNEL_USERNAME = "@villainpremium"
UPI_ID = "rishabhx07@fam"
ADMIN_ID = 8551378606
QR_IMAGE_PATH = "qr.jpg"
ADMIN_USERNAME = "iwontheracebaby"
VOUCHES_LINK = "https://t.me/villainpremium"
USERS_FILE = "users.txt"
# =======================================================

bot = telebot.TeleBot(BOT_TOKEN)

def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            f.write("")
    
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
        
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")

def check_sub(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if status in ['member', 'creator', 'administrator']:
            return True
        return False
    except Exception as e:
        return False

def main_home_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛍️ Products", callback_data="open_products"),
        InlineKeyboardButton("💬 Support / Help", url=f"https://t.me/{ADMIN_USERNAME}"),
        InlineKeyboardButton("⭐ Vouches / Proofs", url=VOUCHES_LINK)
    )
    return markup

def products_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🎬 Netflix - ₹99", callback_data="buy_netflix"),
        InlineKeyboardButton("📦 Amazon Prime", callback_data="menu_prime")
    )
    markup.add(
        InlineKeyboardButton("🎵 Spotify (3M) - ₹60", callback_data="buy_spotify"),
        InlineKeyboardButton("▶️ YouTube Pro - ₹25", callback_data="buy_youtube")
    )
    markup.add(
        InlineKeyboardButton("🌐 JioHotstar - ₹50", callback_data="buy_hotstar"),
        InlineKeyboardButton("🍥 Crunchyroll - ₹50", callback_data="buy_crunchyroll")
    )
    markup.add(
        InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    save_user(user_id)
    
    if check_sub(user_id):
        bot.send_message(
            message.chat.id, 
            "Welcome to V-Premium! 🎉 Sabse saste aur reliable premium accounts.\nNiche diye gaye options mein se select karein:", 
            reply_markup=main_home_menu()
        )
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
        markup.add(InlineKeyboardButton("✅ Check / Verify", callback_data="verify_sub"))
        
        bot.send_message(
            message.chat.id, 
            "⚠️ **Bhai, aage badhne ke liye pehle hamara official channel join karna zaroori hai!**\n\nNiche diye gaye button par click karke channel join karein aur phir 'Check / Verify' dabayein:", 
            reply_markup=markup,
            parse_mode="Markdown"
        )

# ==================== BROADCAST COMMAND ====================
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Aap yeh command use nahi kar sakte!")
        return
        
    msg = bot.send_message(message.chat.id, "📢 Sabhi users ko bhejne ke liye message ya photo type karein:")
    bot.register_next_step_handler(msg, send_broadcast_to_all)

def send_broadcast_to_all(message):
    if not os.path.exists(USERS_FILE):
        bot.send_message(message.chat.id, "❌ Koi user nahi mila!")
        return
        
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
        
    success = 0
    failed = 0
    
    bot.send_message(message.chat.id, f"🚀 Broadcast shuru ho gaya hai... Total users: {len(users)}")
    
    for user_id in users:
        try:
            if message.photo:
                file_id = message.photo[-1].file_id
                caption = message.caption if message.caption else ""
                bot.send_photo(user_id, file_id, caption=caption)
            else:
                bot.send_message(user_id, message.text)
            success += 1
        except Exception as e:
            failed += 1
            
    bot.send_message(message.chat.id, f"✅ Broadcast Complete!\n\nSuccessful: {success}\nFailed (Blocked bot): {failed}")
# ==========================================================

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    save_user(user_id)
    
    if call.data == "verify_sub":
        if check_sub(user_id):
            bot.delete_message(chat_id, call.message.message_id)
            bot.send_message(chat_id, "Verification Successful! 🎉\nNiche diye gaye options mein se select karein:", reply_markup=main_home_menu())
        else:
            bot.answer_callback_query(call.id, "❌ Aapne abhi tak channel join nahi kiya hai! Pehle join karein.", show_alert=True)
            
    elif call.data == "open_products":
        bot.edit_message_text(
            "🛍️ **V-Premium Store:**\nApna pasandida OTT plan select karein:", 
            chat_id, 
            call.message.message_id, 
            reply_markup=products_menu(),
            parse_mode="Markdown"
        )
        
    elif call.data == "menu_prime":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("1 Month - ₹70", callback_data="buy_prime_1"))
        markup.add(InlineKeyboardButton("6 Month - ₹299", callback_data="buy_prime_6"))
        markup.add(InlineKeyboardButton("🔙 Back to Products", callback_data="open_products"))
        bot.edit_message_text("Amazon Prime ka plan select karein:", chat_id, call.message.message_id, reply_markup=markup)
        
    elif call.data == "back_main":
        bot.edit_message_text(
            "Welcome to V-Premium! 🎉 Sabse saste aur reliable premium accounts.\nNiche diye gaye options mein se select karein:", 
            chat_id, 
            call.message.message_id, 
            reply_markup=main_home_menu()
        )
        
    elif call.data.startswith("buy_"):
        plan_details = {
            "buy_netflix": "Netflix (1 Month) - ₹99",
            "buy_spotify": "Spotify (3 Months) - ₹60",
            "buy_youtube": "YouTube Premium (1 Month) - ₹25",
            "buy_hotstar": "JioHotstar (1 Month) - ₹50",
            "buy_crunchyroll": "Crunchyroll (1 Month) - ₹50",
            "buy_prime_1": "Amazon Prime (1 Month) - ₹70",
            "buy_prime_6": "Amazon Prime (6 Months) - ₹299"
        }
        
        selected_plan = plan_details.get(call.data, "Plan")
        
        caption_text = f"Aapne select kiya hai: **{selected_plan}**\n\n"
        caption_text += f"Is QR Code ko scan karke payment karein:\nUPI ID: `{UPI_ID}`\n\n"
        caption_text += "Payment karne ke baad payment ka **Screenshot** yahan bhej dein."
        
        try:
            with open(QR_IMAGE_PATH, 'rb') as photo:
                sent_msg = bot.send_photo(chat_id, photo, caption=caption_text, parse_mode="Markdown")
                bot.register_next_step_handler(sent_msg, process_screenshot, selected_plan)
        except Exception as e:
            sent_msg = bot.send_message(chat_id, caption_text + "\n\n(⚠️ QR image not found in folder, please use UPI ID directly)", parse_mode="Markdown")
            bot.register_next_step_handler(sent_msg, process_screenshot, selected_plan)

    elif call.data.startswith("reply_"):
        parts = call.data.split("_")
        target_user_id = parts[1]
        plan_code = parts[2] if len(parts) > 2 else "other"
        
        if plan_code == "youtube":
            msg = bot.send_message(chat_id, "Aapne YouTube select kiya hai. Ab user se Gmail mangne ke liye koi bhi message type karo (jaise 'OK'):")
            bot.register_next_step_handler(msg, ask_for_gmail, target_user_id)
        else:
            msg = bot.send_message(chat_id, "Ab is user ke liye ID / Password (message) type karke bhejo:")
            bot.register_next_step_handler(msg, send_id_to_user, target_user_id)
        
    elif call.data.startswith("reject_"):
        target_user_id = call.data.split("_")[1]
        try:
            bot.send_message(target_user_id, "❌ Aapka payment screenshot verify nahi ho paya. Kripya sahi screenshot dobara bhejein.")
            bot.send_message(chat_id, "❌ Order reject kar diya gaya hai.")
        except:
            bot.send_message(chat_id, "❌ User tak message nahi gaya.")

def process_screenshot(message, selected_plan):
    user_id = message.from_user.id
    username = message.from_user.username
    
    if not message.photo:
        sent_msg = bot.send_message(message.chat.id, "⚠️ Bhai text mat bhejo, payment ka **Screenshot (Photo)** upload karo!")
        bot.register_next_step_handler(sent_msg, process_screenshot, selected_plan)
        return
        
    file_id = message.photo[-1].file_id
    
    bot.send_message(
        message.chat.id, 
        "Aapka payment screenshot receive ho gaya hai! ✅ Admin verification kar raha hai, thoda intezaار karein.",
    )
    
    is_youtube = "youtube" in selected_plan.lower()
    plan_tag = "youtube" if is_youtube else "other"
    
    admin_caption = f"🔔 **New Payment Screenshot!**\n\n"
    admin_caption += f"📦 Plan: **{selected_plan}**\n"
    admin_caption += f"👤 User: @{username if username else 'No Username'} (ID: `{user_id}`)\n\n"
    admin_caption += f"Screenshot check karke niche click karein:"
    
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ Reply & Send ID", callback_data=f"reply_{user_id}_{plan_tag}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")
    )
    
    bot.send_photo(ADMIN_ID, file_id, caption=admin_caption, reply_markup=markup, parse_mode="Markdown")

def ask_for_gmail(message, target_user_id):
    try:
        sent_msg = bot.send_message(
            target_user_id, 
            "🎉 **Aapka Payment Verify Ho Gaya Hai!**\n\n**SEND YOUR MAIL 💌**", 
            parse_mode="Markdown"
        )
        bot.register_next_step_handler(sent_msg, receive_user_gmail)
        bot.send_message(message.chat.id, "✅ User ke paas Gmail mangne ka message bhej diya gaya hai!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: User tak message nahi gaya. Shayad usne bot block kar rakha hai.")

def receive_user_gmail(message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_gmail = message.text
    
    bot.send_message(
        ADMIN_ID, 
        f"📩 **Received Gmail from User!**\n\n👤 User: @{username if username else 'No Username'} (ID: `{user_id}`)\n📧 Gmail: `{user_gmail}`\n\nAb aap is Gmail par YouTube invite bhej sakte hain!",
        parse_mode="Markdown"
    )
    bot.send_message(chat_id=user_id, text="✅ Aapki Gmail receive ho gayi hai! Jaldi hi aapko YouTube Premium activate karke de diya jayega. Thank you! 🙏")

def send_id_to_user(message, target_user_id):
    account_details = message.text
    
    try:
        bot.send_message(
            target_user_id, 
            f"🎉 **Aapka Payment Verify Ho Gaya Hai!**\n\nAapka Account Details:\n\n{account_details}\n\nThank you for buying from V-Premium! 🙏",
            parse_mode="Markdown"
        )
        bot.send_message(message.chat.id, "✅ ID/Password successfully user ko bhej diya gaya hai!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: User tak message nahi gaya. Shayad usne bot block kar rakha hai.")

# Conflict error fix karne ke liye remove_webhook aur skip_pending add kiya hai
bot.remove_webhook()
print("V-Premium Bot is running...")
bot.infinity_polling(skip_pending=True)
    
