import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from collections import defaultdict

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

TOTAL_QUESTIONS = 10

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

# Словарь для хранения данных пользователей
user_data = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_data[message.from_user.id] = {
        "scores": defaultdict(int),
        "q": 0
    }

    await message.answer("🥞 Добро пожаловать в тест «Какой ты масленичный блин?»")
    await send_question(message)

async def send_question(message):
    data = user_data.get(message.from_user.id)
    if data is None:
        await message.answer("Произошла ошибка. Попробуй /start")
        return

    q_index = data["q"]

    if q_index >= TOTAL_QUESTIONS:
        await show_result(message)
        return

    question, answers = questions[q_index]
    keyboard = types.InlineKeyboardMarkup()

    for text, typ in answers:
        keyboard.add(types.InlineKeyboardButton(text=text, callback_data=typ))

    await message.answer(question, reply_markup=keyboard)

@dp.callback_query_handler()
async def handle_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()

    # Если пользователь не найден, создаём заново
    if user_id not in user_data:
        user_data[user_id] = {
            "scores": defaultdict(int),
            "q": 0
        }

    # Обработка перезапуска
    if callback.data == "restart":
        user_data[user_id] = {
            "scores": defaultdict(int),
            "q": 0
        }

        # Создаём "виртуальное" сообщение для send_question
        class DummyMessage:
            def __init__(self, chat_id, from_user):
                self.chat = types.Chat(id=chat_id, type="private")
                self.from_user = from_user

        dummy_msg = DummyMessage(callback.message.chat.id, callback.from_user)
        await send_question(dummy_msg)
        return

    # Добавляем очки и переходим к следующему вопросу
    data = user_data[user_id]
    data["scores"][callback.data] += 1
    data["q"] += 1

    # Удаляем старое сообщение с кнопками
    await callback.message.delete()

    # Отправляем следующий вопрос
    await send_question(callback.message)

async def show_result(message):
    data = user_data[message.from_user.id]
    scores = data["scores"]

    await message.answer("🥞 Считаем твой результат...")
    await asyncio.sleep(2)

    # Определяем результат
    result_type = max(scores, key=scores.get)
    image_path, description = results[result_type]

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🔁 Пройти заново", callback_data="restart"))

    # Отправляем фото с результатом
    with open(image_path, "rb") as photo:
        await bot.send_photo(message.chat.id, photo, caption=description, reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
