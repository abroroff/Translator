import telebot
from telebot import types
from deep_translator import GoogleTranslator

# 1. BOTNI SOZLASH
TOKEN = 8656489669:AAEVMRvyP3A0O8vDbfSdD-PPjXk8RyUifZc
bot = telebot.TeleBot(TOKEN)

# 2. TILLAR RO'YXATI
LANGUAGES = {
    "O'zbekcha 🇺🇿": "uz",
    "English 🇬🇧": "en",
    "Russian 🇷🇺": "ru",
    "Turkish 🇹🇷": "tr",
    "German 🇩🇪": "de",
    "Arabic 🇸🇦": "ar",
    "Korean 🇰🇷": "ko",
    "French 🇫🇷": "fr"
}

# Foydalanuvchi tanlovini saqlash uchun
user_data = {}

# 3. START BUYRUG'I
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(lang) for lang in LANGUAGES.keys()]
    markup.add(*buttons)
    
    welcome_msg = (
        f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
        "Men **Professional Tarjimon** botman.\n"
        "Qaysi tilga tarjima qilishni tanlang va menga matn yuboring!"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup, parse_mode="Markdown")

# 4. TILNI TANLASHNI QABUL QILISH
@bot.message_handler(func=lambda m: m.text in LANGUAGES.keys())
def set_language(message):
    chat_id = message.chat.id
    user_data[chat_id] = LANGUAGES[message.text]
    bot.send_message(chat_id, f"✅ Sozlama saqlandi: **{message.text}**\nEndi istalgan tilda matn yuboring...", parse_mode="Markdown")

# 5. TARJIMA QILISH JARAYONI
@bot.message_handler(func=lambda m: True)
def translate_text(message):
    chat_id = message.chat.id
    # Agar til tanlanmagan bo'lsa, avtomat o'zbekcha qilamiz
    target_lang = user_data.get(chat_id, 'uz')
    
    # "Loading" animatsiyasi
    status = bot.reply_to(message, "⏳ Tarjima qilinmoqda...")
    
    try:
        # source='auto' har qanday tilni o'zi taniy oladi
        translated = GoogleTranslator(source='auto', target=target_lang).translate(message.text)
        
        # Natijani chiqarish
        result_text = f"🌐 **Tarjima ({target_lang}):**\n\n{translated}"
        bot.edit_message_text(result_text, chat_id, status.message_id, parse_mode="Markdown")
    
    except Exception as e:
        bot.edit_message_text("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.", chat_id, status.message_id)

# 6. BOTNI ISHLATISH
if __name__ == "__main__":
    print("Bot ishga tushdi...")
    bot.infinity_polling()
