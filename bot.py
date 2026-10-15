import telebot
import qrcode
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==================== CONFIGURATION ====================
BOT_TOKEN = "8855553129:AAGbCJEtQZ9dDOvOEzNl8S-2fpPFqiUIGjM"
CHANNEL_USERNAME = "@villainpremium"
UPI_ID = "rishabhx07@fam"
ADMIN_ID = 8551378606
ADMIN_USERNAME = "iwontheracebaby"
VOUCHES_LINK = "https://t.me/villainpremium"
# =======================================================

bot = telebot.TeleBot(BOT_TOKEN)

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

# Exact amount ka dynamic QR generate karne ka function
def generate_upi_qr(upi_id, amount, filename="dynamic_qr.png"):
    # UPI standard payment URI format
    upi_url = f"upi://pay?pa={upi_id}&am={amount}&cu=INR&pn=V-Premium"
    
    # QR code generate karna
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    return filename

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
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

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    
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
        # Plans ke sath unka exact amount set kar diya hai
        plan_details = {
            "buy_netflix": ("Netflix (1 Month) - ₹99", 99),
            "buy_spotify": ("Spotify (3 Months) - ₹60", 60),
            "buy_youtube": ("YouTube Premium (1 Month) - ₹25", 25),
            "buy_hotstar": ("JioHotstar (1 Month) - ₹50", 50),
            "buy_crunchyroll": ("Crunchyroll (1 Month) - ₹50", 50),
            "buy_prime_1": ("Amazon Prime (1 Month) - ₹70", 70),
            "buy_prime_6": ("Amazon Prime (6 Months) - ₹299", 299)
        }
        
        selected_plan, amount = plan_details.get(call.data, ("Plan", 0))
        
        caption_text = f"Aapne select kiya hai: **{selected_plan}**\n\n"
        caption_text += f"Is QR Code ko scan karke exact **₹{amount}** pay karein:\nUPI ID: `{UPI_ID}`\n\n"
        caption_text += "Payment karne ke baad payment ka **Screenshot** yahan bhej dein."
        
        try:
            # Dynamic QR Code generate karke bhejna
            qr_path = generate_upi_qr(UPI_ID, amount)
            with open(qr_path, 'rb') as photo:
                sent_msg = bot.send_photo(chat_id, photo, caption=caption_text, parse_mode="Markdown")
                bot.register_next_step_handler(sent_msg, process_screenshot, selected_plan)
        except Exception as e:
            sent_msg = bot.send_message(chat_id, caption_text + "\n\n(⚠️ QR generation error, please pay directly via UPI ID)", parse_mode="Markdown")
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
        "Aapka payment screenshot receive ho gaya hai! ✅ Admin verification kar raha hai, thoda intezaar karein.",
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

print("V-Premium Bot is running with Dynamic QR...")
bot.infinity_polling()
        
