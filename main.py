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
    # … добавь остальные вопросы здесь …
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

user_data = {}

# Старт теста
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_data[message.from_user.id] = {
        "scores": defaultdict(int),
        "q": 0,
        "msg_id": None
    }
    await message.answer("🥞 Добро пожаловать в тест «Какой ты масленичный блин?»")
    await send_question(message.from_user.id, message.chat.id)

# Отправка вопроса
async def send_question(user_id, chat_id):
    data = user_data.get(user_id)
    if data is None:
        return

    q_index = data["q"]
    if q_index >= len(questions):
        await show_result(user_id, chat_id)
        return

    question, answers = questions[q_index]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for text, typ in answers:
        keyboard.insert(types.InlineKeyboardButton(text=text, callback_data=f"ans:{typ}"))

    if data["msg_id"] is None:
        msg = await bot.send_message(chat_id, question, reply_markup=keyboard)
        data["msg_id"] = msg.message_id
    else:
        await bot.edit_message_text(
            question,
            chat_id=chat_id,
            message_id=data["msg_id"],
            reply_markup=keyboard
        )

# Обработка ответов
@dp.callback_query_handler(lambda c: c.data.startswith("ans:") or c.data == "restart")
async def handle_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    data = user_data.get(user_id)

    await callback.answer()

    if callback.data == "restart":
        user_data[user_id] = {"scores": defaultdict(int), "q": 0, "msg_id": None}
        await send_question(user_id, chat_id)
        return

    if data is None:
        user_data[user_id] = {"scores": defaultdict(int), "q": 0, "msg_id": None}
        data = user_data[user_id]

    # Записываем результат
    answer_type = callback.data.split(":")[1]
    data["scores"][answer_type] += 1
    data["q"] += 1

    # Отправляем следующий вопрос
    await send_question(user_id, chat_id)

# Показ результата
async def show_result(user_id, chat_id):
    data = user_data[user_id]
    scores = data["scores"]

    await bot.send_message(chat_id, "🥞 Считаем твой результат...")
    await asyncio.sleep(1.5)

    result_type = max(scores, key=scores.get)
    image_path, description = results[result_type]

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🔁 Пройти заново", callback_data="restart"))

    with open(image_path, "rb") as photo:
        await bot.send_photo(chat_id, photo, caption=description, reply_markup=keyboard)

    # Сброс данных для нового прохождения
    data["msg_id"] = None
    data["q"] = 0
    data["scores"] = defaultdict(int)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
