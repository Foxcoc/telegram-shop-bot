import telebot
from telebot import types

bot = telebot.TeleBot("8008957438:AAHWmkjKzxJXbiopw_pPGnHOb0uun1PLj6Y")

# Товары
products = {
    "premium": {
        "title": "🎫 Telegram Premium",
        "price": "1500₸",
        "desc": "Официальная подписка на 1 месяц"
    },
    "vpn": {
        "title": "🛡 VPN-доступ",
        "price": "800₸",
        "desc": "Быстрый и надёжный VPN на 1 месяц"
    }
}

# /start
@bot.message_handler(commands=['start'])
def start(message):
    text = "👋 Добро пожаловать!\n\nЭтот бот — магазин Telegram Premium, VPN и цифровых товаров.\n\nВыберите действие ниже 👇"
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🛍 Магазин", callback_data="menu_shop"),
        types.InlineKeyboardButton("📞 Связаться с автором", callback_data="menu_contact")
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)

# Обработка inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "menu_shop":
        markup = types.InlineKeyboardMarkup()
        for key, item in products.items():
            markup.add(types.InlineKeyboardButton(item["title"], callback_data=f"product_{key}"))
        markup.add(types.InlineKeyboardButton("⬅ Назад", callback_data="back_main"))
        text = "🛍 Наш магазин:\nВыберите товар 👇"
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    elif call.data == "menu_contact":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅ Назад", callback_data="back_main"))
        text = "📞 Связь с продавцом:\nНапишите сюда: @ТВОЙ_ЮЗЕР"
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    elif call.data.startswith("product_"):
        key = call.data.split("_")[1]
        item = products[key]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 Купить", callback_data=f"buy_{key}"))
        markup.add(types.InlineKeyboardButton("⬅ Назад", callback_data="menu_shop"))
        text = f"{item['title']}\nЦена: {item['price']}\n\n{item['desc']}"
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    elif call.data.startswith("buy_"):
        key = call.data.split("_")[1]
        item = products[key]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅ Назад", callback_data="menu_shop"))
        text = f"✅ Заказ оформлен: {item['title']}\n\nСвяжитесь с продавцом: @ТВОЙ_ЮЗЕР"
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    elif call.data == "back_main":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🛍 Магазин", callback_data="menu_shop"),
            types.InlineKeyboardButton("📞 Связаться с автором", callback_data="menu_contact")
        )
        text = "👋 Добро пожаловать!\n\nЭтот бот — магазин Telegram Premium, VPN и цифровых товаров.\n\nВыберите действие ниже 👇"
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

# Запуск
print("Бот работает.")
bot.polling()
