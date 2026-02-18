{\rtf1\ansi\ansicpg1251\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 AppleColorEmoji;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww19080\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import logging\
import os\
import asyncio\
from aiogram import Bot, Dispatcher, executor, types\
from collections import defaultdict\
\
API_TOKEN = os.getenv("BOT_TOKEN")\
\
logging.basicConfig(level=logging.INFO)\
\
bot = Bot(token=API_TOKEN)\
dp = Dispatcher(bot)\
\
TOTAL_QUESTIONS = 10\
\
questions = [\
    ("
\f1 1\uc0\u65039 \u8419 
\f0  \uc0\u1042  \u1085 \u1086 \u1074 \u1086 \u1081  \u1088 \u1072 \u1073 \u1086 \u1095 \u1077 \u1081  \u1079 \u1072 \u1076 \u1072 \u1095 \u1077  \u1090 \u1099 \'85",\
     [("\uc0\u1041 \u1077 \u1088 \u1105 \u1096 \u1100  \u1086 \u1090 \u1074 \u1077 \u1090 \u1089 \u1090 \u1074 \u1077 \u1085 \u1085 \u1086 \u1089 \u1090 \u1100 ", "ikra"),\
      ("\uc0\u1057 \u1085 \u1072 \u1095 \u1072 \u1083 \u1072  \u1072 \u1085 \u1072 \u1083 \u1080 \u1079 \u1080 \u1088 \u1091 \u1077 \u1096 \u1100 ", "salmon"),\
      ("\uc0\u1042 \u1076 \u1086 \u1093 \u1085 \u1086 \u1074 \u1083 \u1103 \u1077 \u1096 \u1100  \u1076 \u1088 \u1091 \u1075 \u1080 \u1093 ", "chocolate"),\
      ("\uc0\u1055 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1080 \u1074 \u1072 \u1077 \u1096 \u1100  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1091 ", "smetana")]),\
\
    ("
\f1 2\uc0\u65039 \u8419 
\f0  \uc0\u1058 \u1077 \u1073 \u1103  \u1095 \u1072 \u1097 \u1077  \u1093 \u1074 \u1072 \u1083 \u1103 \u1090  \u1079 \u1072 \'85",\
     [("\uc0\u1056 \u1077 \u1079 \u1091 \u1083 \u1100 \u1090 \u1072 \u1090 ", "ikra"),\
      ("\uc0\u1053 \u1072 \u1076 \u1105 \u1078 \u1085 \u1086 \u1089 \u1090 \u1100 ", "ham"),\
      ("\uc0\u1040 \u1090 \u1084 \u1086 \u1089 \u1092 \u1077 \u1088 \u1091 ", "jam"),\
      ("\uc0\u1050 \u1088 \u1077 \u1072 \u1090 \u1080 \u1074 ", "chocolate")]),\
\
    ("
\f1 3\uc0\u65039 \u8419 
\f0  \uc0\u1045 \u1089 \u1083 \u1080  \u1074  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1077  \u1089 \u1090 \u1088 \u1077 \u1089 \u1089 \'85",\
     [("\uc0\u1041 \u1077 \u1088 \u1091  \u1091 \u1087 \u1088 \u1072 \u1074 \u1083 \u1077 \u1085 \u1080 \u1077 ", "ikra"),\
      ("\uc0\u1057 \u1075 \u1083 \u1072 \u1078 \u1080 \u1074 \u1072 \u1102  \u1091 \u1075 \u1083 \u1099 ", "honey"),\
      ("\uc0\u1064 \u1091 \u1095 \u1091 ", "jam"),\
      ("\uc0\u1052 \u1086 \u1083 \u1095 \u1072  \u1076 \u1077 \u1083 \u1072 \u1102  \u1089 \u1074 \u1086 \u1105 ", "mushrooms")]),\
\
    ("
\f1 4\uc0\u65039 \u8419 
\f0  \uc0\u1058 \u1074 \u1086 \u1081  \u1080 \u1076 \u1077 \u1072 \u1083 \u1100 \u1085 \u1099 \u1081  \u1087 \u1088 \u1086 \u1077 \u1082 \u1090 \'85",\
     [("\uc0\u1040 \u1084 \u1073 \u1080 \u1094 \u1080 \u1086 \u1079 \u1085 \u1099 \u1081 ", "ikra"),\
      ("\uc0\u1057 \u1090 \u1088 \u1091 \u1082 \u1090 \u1091 \u1088 \u1085 \u1099 \u1081 ", "ham"),\
      ("\uc0\u1058 \u1074 \u1086 \u1088 \u1095 \u1077 \u1089 \u1082 \u1080 \u1081 ", "chocolate"),\
      ("\uc0\u1043 \u1083 \u1091 \u1073 \u1086 \u1082 \u1080 \u1081 ", "mushrooms")]),\
\
    ("
\f1 5\uc0\u65039 \u8419 
\f0  \uc0\u1058 \u1099  \u1073 \u1086 \u1083 \u1100 \u1096 \u1077 \'85",\
     [("\uc0\u1056 \u1072 \u1094 \u1080 \u1086 \u1085 \u1072 \u1083 \u1100 \u1085 \u1099 \u1081 ", "ham"),\
      ("\uc0\u1069 \u1084 \u1086 \u1094 \u1080 \u1086 \u1085 \u1072 \u1083 \u1100 \u1085 \u1099 \u1081 ", "chocolate"),\
      ("\uc0\u1048 \u1085 \u1090 \u1091 \u1080 \u1090 \u1080 \u1074 \u1085 \u1099 \u1081 ", "salmon"),\
      ("\uc0\u1055 \u1088 \u1072 \u1082 \u1090 \u1080 \u1095 \u1085 \u1099 \u1081 ", "smetana")]),\
\
    ("
\f1 6\uc0\u65039 \u8419 
\f0  \uc0\u1042 \u1085 \u1077  \u1088 \u1072 \u1073 \u1086 \u1090 \u1099  \u1090 \u1099 \'85",\
     [("\uc0\u1051 \u1102 \u1073 \u1080 \u1096 \u1100  \u1072 \u1082 \u1090 \u1080 \u1074 ", "jam"),\
      ("\uc0\u1051 \u1102 \u1073 \u1080 \u1096 \u1100  \u1091 \u1102 \u1090 ", "smetana"),\
      ("\uc0\u1051 \u1102 \u1073 \u1080 \u1096 \u1100  \u1090 \u1091 \u1089 \u1086 \u1074 \u1082 \u1080 ", "chocolate"),\
      ("\uc0\u1051 \u1102 \u1073 \u1080 \u1096 \u1100  \u1082 \u1085 \u1080 \u1075 \u1080 /\u1087 \u1086 \u1076 \u1082 \u1072 \u1089 \u1090 \u1099 ", "mushrooms")]),\
\
    ("
\f1 7\uc0\u65039 \u8419 
\f0  \uc0\u1063 \u1090 \u1086  \u1090 \u1077 \u1073 \u1103  \u1079 \u1083 \u1080 \u1090  \u1089 \u1080 \u1083 \u1100 \u1085 \u1077 \u1077 ?",\
     [("\uc0\u1053 \u1077 \u1089 \u1087 \u1088 \u1072 \u1074 \u1077 \u1076 \u1083 \u1080 \u1074 \u1086 \u1089 \u1090 \u1100 ", "ikra"),\
      ("\uc0\u1061 \u1072 \u1086 \u1089 ", "ham"),\
      ("\uc0\u1061 \u1086 \u1083 \u1086 \u1076 \u1085 \u1086 \u1089 \u1090 \u1100 ", "smetana"),\
      ("\uc0\u1055 \u1086 \u1074 \u1077 \u1088 \u1093 \u1085 \u1086 \u1089 \u1090 \u1085 \u1086 \u1089 \u1090 \u1100 ", "mushrooms")]),\
\
    ("
\f1 8\uc0\u65039 \u8419 
\f0  \uc0\u1050 \u1086 \u1083 \u1083 \u1077 \u1075 \u1080  \u1080 \u1076 \u1091 \u1090  \u1082  \u1090 \u1077 \u1073 \u1077  \u1079 \u1072 \'85",\
     [("\uc0\u1056 \u1077 \u1096 \u1077 \u1085 \u1080 \u1077 \u1084 ", "salmon"),\
      ("\uc0\u1055 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1082 \u1086 \u1081 ", "smetana"),\
      ("\uc0\u1053 \u1072 \u1089 \u1090 \u1088 \u1086 \u1077 \u1085 \u1080 \u1077 \u1084 ", "jam"),\
      ("\uc0\u1057 \u1086 \u1074 \u1077 \u1090 \u1086 \u1084 ", "honey")]),\
\
    ("
\f1 9\uc0\u65039 \u8419 
\f0  \uc0\u1042  \u1082 \u1086 \u1085 \u1092 \u1083 \u1080 \u1082 \u1090 \u1077  \u1090 \u1099 \'85",\
     [("\uc0\u1055 \u1088 \u1103 \u1084 \u1086 \u1081 ", "ikra"),\
      ("\uc0\u1044 \u1080 \u1087 \u1083 \u1086 \u1084 \u1072 \u1090 ", "honey"),\
      ("\uc0\u1048 \u1079 \u1073 \u1077 \u1075 \u1072 \u1077 \u1096 \u1100 ", "jam"),\
      ("\uc0\u1056 \u1072 \u1079 \u1073 \u1080 \u1088 \u1072 \u1077 \u1096 \u1100 \u1089 \u1103  \u1075 \u1083 \u1091 \u1073 \u1086 \u1082 \u1086 ", "mushrooms")]),\
\
    ("
\f1 \uc0\u55357 \u56607 
\f0  \uc0\u1058 \u1074 \u1086 \u1103  \u1088 \u1086 \u1083 \u1100  \u1074  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1077 ?",\
     [("\uc0\u1051 \u1080 \u1076 \u1077 \u1088 ", "ikra"),\
      ("\uc0\u1057 \u1090 \u1072 \u1073 \u1080 \u1083 \u1080 \u1079 \u1072 \u1090 \u1086 \u1088 ", "ham"),\
      ("\uc0\u1043 \u1077 \u1085 \u1077 \u1088 \u1072 \u1090 \u1086 \u1088  \u1080 \u1076 \u1077 \u1081 ", "chocolate"),\
      ("\uc0\u1040 \u1085 \u1072 \u1083 \u1080 \u1090 \u1080 \u1082 ", "salmon")]),\
]\
\
results = \{\
    "ikra": ("ikra.jpg", "
\f1 \uc0\u55358 \u56670 
\f0  \uc0\u1041 \u1083 \u1080 \u1085  \u1089  \u1080 \u1082 \u1088 \u1086 \u1081 \\n\u1058 \u1099  \u1083 \u1080 \u1076 \u1077 \u1088  \u1080  \u1076 \u1088 \u1072 \u1081 \u1074 \u1077 \u1088  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1099 ."),\
    "smetana": ("smetana.jpg", "
\f1 \uc0\u55358 \u56670 
\f0  \uc0\u1041 \u1083 \u1080 \u1085  \u1089 \u1086  \u1089 \u1084 \u1077 \u1090 \u1072 \u1085 \u1086 \u1081 \\n\u1058 \u1099  \u1089 \u1086 \u1079 \u1076 \u1072 \u1105 \u1096 \u1100  \u1072 \u1090 \u1084 \u1086 \u1089 \u1092 \u1077 \u1088 \u1091  \u1087 \u1086 \u1076 \u1076 \u1077 \u1088 \u1078 \u1082 \u1080 ."),\
    "ham": ("ham.jpg", "
\f1 \uc0\u55358 \u56670 
\f0  \uc0\u1041 \u1083 \u1080 \u1085  \u1089  \u1074 \u1077 \u1090 \u1095 \u1080 \u1085 \u1086 \u1081  \u1080  \u1089 \u1099 \u1088 \u1086 \u1084 \\n\u1058 \u1099  \u1089 \u1080 \u1089 \u1090 \u1077 \u1084 \u1085 \u1099 \u1081  \u1080  \u1091 \u1089 \u1090 \u1086 \u1081 \u1095 \u1080 \u1074 \u1099 \u1081 ."),\
    "chocolate": ("chocolate.jpg", "
\f1 \uc0\u55356 \u57195 
\f0  \uc0\u1041 \u1083 \u1080 \u1085  \u1089  \u1096 \u1086 \u1082 \u1086 \u1083 \u1072 \u1076 \u1086 \u1084  \u1080  \u1082 \u1083 \u1091 \u1073 \u1085 \u1080 \u1082 \u1086 \u1081 \\n\u1058 \u1099  \u1082 \u1088 \u1077 \u1072 \u1090 \u1080 \u1074  \u1080  \u1074 \u1076 \u1086 \u1093 \u1085 \u1086 \u1074 \u1077 \u1085 \u1080 \u1077 ."),\
    "honey": ("honey.jpg", "
\f1 \uc0\u55356 \u57199 
\f0  \uc0\u1041 \u1083 \u1080 \u1085  \u1089  \u1084 \u1105 \u1076 \u1086 \u1084 \\n\u1058 \u1099  \u1076 \u1080 \u1087 \u1083 \u1086 \u1084 \u1072 \u1090  \u1080  \u1084 \u1080 \u1088 \u1086 \u1090 \u1074 \u1086 \u1088 \u1077 \u1094 ."),\
    "salmon": ("salmon.jpg", "
\f1 \uc0\u55357 \u56351 
\f0  \uc0\u1041 \u1083 \u1080 \u1085  \u1089  \u1082 \u1088 \u1072 \u1089 \u1085 \u1086 \u1081  \u1088 \u1099 \u1073 \u1086 \u1081 \\n\u1058 \u1099  \u1089 \u1090 \u1088 \u1072 \u1090 \u1077 \u1075  \u1080  \u1072 \u1085 \u1072 \u1083 \u1080 \u1090 \u1080 \u1082 ."),\
    "mushrooms": ("mushrooms.jpg", "
\f1 \uc0\u55356 \u57156 
\f0  \uc0\u1041 \u1083 \u1080 \u1085  \u1089  \u1075 \u1088 \u1080 \u1073 \u1072 \u1084 \u1080 \\n\u1058 \u1099  \u1075 \u1083 \u1091 \u1073 \u1086 \u1082 \u1080 \u1081  \u1101 \u1082 \u1089 \u1087 \u1077 \u1088 \u1090 ."),\
    "jam": ("jam.jpg", "
\f1 \uc0\u55356 \u57171 
\f0  \uc0\u1041 \u1083 \u1080 \u1085  \u1089  \u1074 \u1072 \u1088 \u1077 \u1085 \u1100 \u1077 \u1084 \\n\u1058 \u1099  \u1076 \u1091 \u1096 \u1072  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1099 .")\
\}\
\
user_data = \{\}\
\
@dp.message_handler(commands=['start'])\
async def start(message: types.Message):\
    user_data[message.from_user.id] = \{\
        "scores": defaultdict(int),\
        "q": 0,\
        "early_scores": defaultdict(int),\
        "name": message.from_user.first_name\
    \}\
\
    await message.answer("
\f1 \uc0\u55358 \u56670 
\f0  \uc0\u1044 \u1086 \u1073 \u1088 \u1086  \u1087 \u1086 \u1078 \u1072 \u1083 \u1086 \u1074 \u1072 \u1090 \u1100  \u1074  \u1090 \u1077 \u1089 \u1090  \'ab\u1050 \u1072 \u1082 \u1086 \u1081  \u1090 \u1099  \u1084 \u1072 \u1089 \u1083 \u1077 \u1085 \u1080 \u1095 \u1085 \u1099 \u1081  \u1073 \u1083 \u1080 \u1085 ?\'bb\\n\\n\u1054 \u1090 \u1074 \u1077 \u1090 \u1100  \u1085 \u1072  10 \u1074 \u1086 \u1087 \u1088 \u1086 \u1089 \u1086 \u1074  \u1080  \u1091 \u1079 \u1085 \u1072 \u1077 \u1096 \u1100  \u1089 \u1074 \u1086 \u1102  \u1088 \u1086 \u1083 \u1100  \u1074  \u1082 \u1086 \u1084 \u1072 \u1085 \u1076 \u1077  
\f1 \uc0\u10024 
\f0 ")\
    await send_question(message)\
\
async def send_question(message):\
    data = user_data[message.from_user.id]\
    q_index = data["q"]\
\
    if q_index >= TOTAL_QUESTIONS:\
        await show_result(message)\
        return\
\
    question, answers = questions[q_index]\
    keyboard = types.InlineKeyboardMarkup()\
\
    for text, typ in answers:\
        keyboard.add(types.InlineKeyboardButton(text=text, callback_data=typ))\
\
    await message.answer(question, reply_markup=keyboard)\
\
@dp.callback_query_handler()\
async def handle_answer(callback: types.CallbackQuery):\
    user_id = callback.from_user.id\
    data = user_data[user_id]\
\
    if callback.data == "restart":\
        user_data[user_id]["scores"] = defaultdict(int)\
        user_data[user_id]["q"] = 0\
        await send_question(callback.message)\
        return\
\
    data["scores"][callback.data] += 1\
\
    if data["q"] < 5:\
        data["early_scores"][callback.data] += 1\
\
    data["q"] += 1\
\
    await callback.answer()\
    await send_question(callback.message)\
\
async def show_result(message):\
    data = user_data[message.from_user.id]\
    scores = data["scores"]\
\
    await message.answer("
\f1 \uc0\u9203 
\f0  \uc0\u1057 \u1095 \u1080 \u1090 \u1072 \u1077 \u1084  \u1090 \u1074 \u1086 \u1081  \u1088 \u1077 \u1079 \u1091 \u1083 \u1100 \u1090 \u1072 \u1090 ...")\
    await asyncio.sleep(2)\
\
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)\
\
    main = sorted_scores[0][0]\
    secondary = sorted_scores[1][0]\
\
    if sorted_scores[0][1] == sorted_scores[1][1]:\
        early = data["early_scores"]\
        if early[secondary] > early[main]:\
            main, secondary = secondary, main\
\
    percent = int((scores[main] / TOTAL_QUESTIONS) * 100)\
\
    image_path, description = results[main]\
\
    caption = f"\{data['name']\}, \uc0\u1090 \u1074 \u1086 \u1081  \u1088 \u1077 \u1079 \u1091 \u1083 \u1100 \u1090 \u1072 \u1090 :\\n\\n\{description\}\\n\\n
\f1 \uc0\u55357 \u56522 
\f0  \uc0\u1057 \u1086 \u1074 \u1087 \u1072 \u1076 \u1077 \u1085 \u1080 \u1077 : \{percent\}%"\
\
    if scores[secondary] > 0:\
        caption += f"\\n
\f1 \uc0\u10024 
\f0  \uc0\u1042 \u1085 \u1091 \u1090 \u1088 \u1077 \u1085 \u1085 \u1080 \u1081  \u1086 \u1090 \u1090 \u1077 \u1085 \u1086 \u1082 : \{results[secondary][1].splitlines()[0]\}"\
\
    keyboard = types.InlineKeyboardMarkup()\
    keyboard.add(types.InlineKeyboardButton("
\f1 \uc0\u55357 \u56577 
\f0  \uc0\u1055 \u1088 \u1086 \u1081 \u1090 \u1080  \u1079 \u1072 \u1085 \u1086 \u1074 \u1086 ", callback_data="restart"))\
    keyboard.add(types.InlineKeyboardButton("
\f1 \uc0\u55357 \u56548 
\f0  \uc0\u1055 \u1086 \u1076 \u1077 \u1083 \u1080 \u1090 \u1100 \u1089 \u1103 ", switch_inline_query=caption))\
\
    with open(image_path, "rb") as photo:\
        await bot.send_photo(message.chat.id, photo, caption=caption, reply_markup=keyboard)\
\
if __name__ == '__main__':\
    executor.start_polling(dp, skip_updates=True)\
}
