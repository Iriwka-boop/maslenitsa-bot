import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from collections import defaultdict

API_TOKEN = os.getenv("BOT_TOKEN")  # Установите свой токен бота в переменной окружения

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

TOTAL_QUESTIONS = 10

# Вопросы и варианты
questions = [
    ("1️⃣ В новой рабочей задаче ты…",
     [("Берёшь ответственность", "ikra"),
      ("Сначала анализируешь", "salmon"),
      ("Вдохновляешь других", "chocolate"),
      ("Поддерживаешь команду", "smetana")]),

    ("2️⃣ Тебя чаще хвалят за…",
     [("Результат", "ikra"),
      ("Надёжность", "ham"),
      ("Атмосферу", "jam"),
      ("Креатив", "chocolate")]),

    ("3️⃣ Если в команде стресс…",
     [("Беру управление", "ikra"),
      ("Сглаживаю углы", "honey"),
      ("Шучу", "jam"),
      ("Молча делаю своё", "mushrooms")]),

    ("4️⃣ Твой идеальный проект…",
     [("Амбициозный", "ikra"),
      ("Структурный", "ham"),
      ("Творческий", "chocolate"),
      ("Глубокий", "mushrooms")]),

    ("5️⃣ Ты больше…",
     [("Рациональный", "ham"),
      ("Эмоциональный", "chocolate"),
      ("Интуитивный", "salmon"),
      ("Практичный", "smetana")]),

    ("6️⃣ Вне работы ты…",
     [("Активный", "jam"),
      ("Домосед", "smetana"),
      ("Любишь тусовки", "chocolate"),
      ("Книги и подкасты", "mushrooms")]),

    ("7️⃣ Тебя злит сильнее всего…",
     [("Несправедливость", "ikra"),
      ("Хаос", "ham"),
      ("Холодность", "smetana"),
      ("Поверхностность", "mushrooms")]),

    ("8️⃣ Коллеги идут к тебе за…",
     [("Решением", "salmon"),
      ("Поддержкой", "smetana"),
      ("Настроением", "jam"),
      ("Советом", "honey")]),

    ("9️⃣ В конфликте ты…",
     [("Прямой", "ikra"),
      ("Дипломат", "honey"),
      ("Избегаешь", "jam"),
      ("Разбираешься глубоко", "mushrooms")]),

    ("🔟 Твоя роль в команде…",
     [("Лидер", "ikra"),
      ("Стабилизатор", "ham"),
      ("Генератор идей", "chocolate"),
      ("Аналитик", "salmon")]),
]

# Результаты
results = {
    "ikra": ("ikra.jpg", "🥞 Блин с икрой\nТы лидер и драйвер команды."),
    "smetana": ("smetana.jpg", "🥞 Блин со сметаной\nТы создаёшь атмосферу поддержки."),
    "ham": ("ham.jpg", "🥞 Блин с ветчиной и сыром\nТы системный и устойчивый."),
    "chocolate": ("chocolate.jpg", "🍫 Блин с шоколадом и клубникой\nТы креатив и вдохновение."),
    "honey": ("honey.jpg", "🍯 Блин с мёдом\nТы дипломат и миротворец."),
    "salmon": ("salmon.jpg", "🐟 Блин с красной рыбой\nТы стратег и аналитик."),
    "mushrooms": ("mushrooms.jpg", "🍄 Блин с грибами\nТы глубокий эксперт."),
    "jam": ("jam.jpg", "🍓 Блин с вареньем\nТы душа команды.")
}

# Данные пользователей
user_data = {}

# Старт теста
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {
        "scores": defaultdict(int),
        "q": 0
    }
    await message.answer("🥞 Добро пожаловать в тест «Какой ты масленичный блин?»")
    await send_question(user_id, message.chat.id)

# Отправка вопроса
async def send_question(user_id, chat_id):
    data = user_data.get(user_id)
    if not data:
        return

    q_index = data["q"]
    if q_index >= TOTAL_QUESTIONS:
        await show_result(user_id, chat_id)
        return

    question_text, answers = questions[q_index]
    keyboard = types.InlineKeyboardMarkup(row_width=1)  # кнопки в столбик
    for text, typ in answers:
        keyboard.add(types.InlineKeyboardButton(text=text, callback_data=f"answer:{typ}"))

    await bot.send_message(chat_id, question_text, reply_markup=keyboard)

# Обработка ответа
@dp.callback_query_handler(lambda c: c.data and c.data.startswith("answer:"))
async def handle_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    data = user_data.get(user_id)
    if not data:
        await callback.answer("Произошла ошибка, начни заново /start", show_alert=True)
        return

    answer_type = callback.data.split(":")[1]
    data["scores"][answer_type] += 1
    data["q"] += 1

    await callback.answer()  # убирает "часики"
    await send_question(user_id, callback.message.chat.id)

# Показ результата
async def show_result(user_id, chat_id):
    data = user_data.get(user_id)
    if not data:
        return

    scores = data["scores"]
    result_type = max(scores, key=scores.get)
    image_path, description = results[result_type]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton("🔁 Пройти заново", callback_data="restart"))

    with open(image_path, "rb") as photo:
        await bot.send_photo(chat_id, photo, caption=description, reply_markup=keyboard)

# Пройти заново
@dp.callback_query_handler(lambda c: c.data == "restart")
async def restart(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_data[user_id] = {
        "scores": defaultdict(int),
        "q": 0
    }
    await callback.answer()
    await send_question(user_id, callback.message.chat.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
