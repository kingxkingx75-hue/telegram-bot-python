import os
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

users = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    if user_id not in users:
        users[user_id] = {"balance": 0, "referrals": 0}
    
    args = message.text.split()
    
    if len(args) > 1:
        referrer_id = int(args[1])
        if referrer_id != user_id and referrer_id in users:
            users[referrer_id]["balance"] += 10
            users[referrer_id]["referrals"] += 1
    
    bot.reply_to(message, 
        f"👋 Welcome {message.from_user.first_name}!\n\n"
        f"💰 Your Balance: {users[user_id]['balance']} coins\n"
        f"👥 Your Referrals: {users[user_id]['referrals']}\n\n"
        f"🔗 Your Referral Link:\n"
        f"https://t.me/{bot.get_me().username}?start={user_id}"
    )

@bot.message_handler(commands=['balance'])
def balance(message):
    user_id = message.from_user.id
    if user_id in users:
        bot.reply_to(message,
            f"💰 Balance: {users[user_id]['balance']} coins\n"
            f"👥 Referrals: {users[user_id]['referrals']}"
        )
    else:
        bot.reply_to(message, "❌ Please start the bot first using /start")

print("Bot is running...")
bot.infinity_polling()
