import asyncio
import json
import logging
import sqlite3
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

# Siz taqdim etgan yangi bot tokeni va admin ID
API_TOKEN = '8236839928:AAE7X3ObgWc0iZz-OMHirZ_svpy_30GvbYc'
ADMIN_ID = 8372285180

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

CONFIG_FILE = 'group_config.json'

# --- O‘ZBEKISTONNING BARCHA VILOYAT VA TUMANLARI ---
REGIONS_DATA = {
    "Qoraqalpog'iston Respublikasi": [
        'Nukus sh.',
        'Amudaryo t.',
        'Beruniy t.',
        'Chimboy t.',
        'Ellikqal’a t.',
        'Kegeyli t.',
        'Mo‘ynoq t.',
        'Nukus t.',
        'Qanliko‘l t.',
        'Qorao‘zak t.',
        'Qo‘ng‘irot t.',
        'Shumanay t.',
        'Taxtako‘pir t.',
        'To‘rtko‘l t.',
        'Xo‘jayli t.',
    ],
    'Toshkent shahri': [
        'Bektemir t.',
        'Chilonzor t.',
        'Mirobod t.',
        'Mirzo Ulug‘bek t.',
        'Sergeli t.',
        'Uchtepa t.',
        'Yashnobod t.',
        'Yunusobod t.',
        'Yakkasaroy t.',
        'Yangihayot t.',
    ],
    'Toshkent viloyati': [
        'Angren sh.',
        'Bekobod sh.',
        'Chinoz t.',
        'Chirchiq sh.',
        'Olmaliq sh.',
        'Ohangaron t.',
        'Bo‘ka t.',
        'Bo‘stonliq t.',
        'Kibray t.',
        'Quyi Chirchiq t.',
        'Parkent t.',
        'Piskent t.',
        'Toshkent t.',
        'O‘rta Chirchiq t.',
        'Yangiyo‘l t.',
        'Yuqori Chirchiq t.',
        'Zangiota t.',
    ],
    'Samarqand viloyati': [
        'Samarqand sh.',
        'Kattaqo‘rg‘on sh.',
        'Bulung‘ur t.',
        'Jomboy t.',
        'Ishtixon t.',
        'Kattaqo‘rg‘on t.',
        'Qo‘shrabot t.',
        'Narpay t.',
        'Nurobod t.',
        'Payariq t.',
        'Pastdarg‘om t.',
        'Paxtachi t.',
        'Samarqand t.',
        'Tayloq t.',
        'Urgut t.',
    ],
    'Farg‘ona viloyati': [
        'Farg‘ona sh.',
        'Qo‘qon sh.',
        'Marg‘ilon sh.',
        'Quva sh.',
        'Beshariq t.',
        'Bog‘dod t.',
        'Buvayda t.',
        'Dang‘ara t.',
        'Farg‘ona t.',
        'Furqat t.',
        'Oltiariq t.',
        'Rishton t.',
        'So‘x t.',
        'Toshloq t.',
        'Uchko‘prik t.',
        'Yozyovon t.',
    ],
    'Andijon viloyati': [
        'Andijon sh.',
        'Xonobod sh.',
        'Oltinko‘l t.',
        'Andijon t.',
        'Asaka t.',
        'Baliqchi t.',
        'Bo‘z t.',
        'Buloqboshi t.',
        'Jalaquduq t.',
        'Izboskan t.',
        'Marhamat t.',
        'Paxtaobod t.',
        'Shahrixon t.',
        'Ulug‘nor t.',
        'Xo‘jaobod t.',
    ],
    'Namangan viloyati': [
        'Namangan sh.',
        'Chortoq t.',
        'Chust t.',
        'Kosonsoy t.',
        'Mingbuloq t.',
        'Namangan t.',
        'Norin t.',
        'Pop t.',
        'To‘raqo‘rg‘on t.',
        'Uchqo‘rg‘on t.',
        'Uychi t.',
        'Yangiqo‘rg‘on t.',
    ],
    'Qashqadaryo viloyati': [
        'Qarshi sh.',
        'Shahrisabz sh.',
        'Chiroqchi t.',
        'Dehqonobod t.',
        'G‘uzor t.',
        'Kasbi t.',
        'Kitob t.',
        'Koson t.',
        'Mirishkor t.',
        'Muborak t.',
        'Nishon t.',
        'Qamashi t.',
        'Qarshi t.',
        'Yakkabog‘ t.',
    ],
    'Surxondaryo viloyati': [
        'Termiz sh.',
        'Angor t.',
        'Boysun t.',
        'Denov t.',
        'Jarqo‘rg‘on t.',
        'Qiziriq t.',
        'Qumqo‘rg‘on t.',
        'Muzrabot t.',
        'Oltinsoy t.',
        'Sariosiyo t.',
        'Sherobod t.',
        'Sho‘rchi t.',
        'Termiz t.',
        'Uzun t.',
    ],
    'Buxoro viloyati': [
        'Buxoro sh.',
        'Kogon sh.',
        'Buxoro t.',
        'G‘ijduvon t.',
        'Jondor t.',
        'Qorako‘l t.',
        'Qorovulbozor t.',
        'Peshku t.',
        'Romitan t.',
        'Shofirkon t.',
        'Vobkent t.',
    ],
    'Navoiy viloyati': [
        'Navoiy sh.',
        'Zarafshon sh.',
        'G‘ozg‘on sh.',
        'Konimex t.',
        'Qiziltepa t.',
        'Navbahor t.',
        'Nurota t.',
        'Tamdi t.',
        'Uchquduq t.',
        'Xatirchi t.',
    ],
    'Xorazm viloyati': [
        'Urganch sh.',
        'Xiva sh.',
        'Bog‘ot t.',
        'Gurlan t.',
        'Qo‘shko‘pir t.',
        'Shovot t.',
        'Urganch t.',
        'Xazorasp t.',
        'Xiva t.',
        'Yangibozor t.',
        'Yangiariq t.',
    ],
    'Jizzax viloyati': [
        'Jizzax sh.',
        'Arnasoy t.',
        'Baxmal t.',
        'Do‘stlik t.',
        'Forish t.',
        'G‘allaorol t.',
        'Sharof Rashidov t.',
        'Mirzacho‘l t.',
        'Paxtakor t.',
        'Yangiobod t.',
        'Zafarobod t.',
        'Zarbdor t.',
    ],
    'Sirdaryo viloyati': [
        'Guliston sh.',
        'Shirin sh.',
        'Yangiyer sh.',
        'Boyovut t.',
        'Guliston t.',
        'Mirzaobod t.',
        'Oqoltin t.',
        'Sardoba t.',
        'Sayxunobod t.',
        'Sirdaryo t.',
        'Xovos t.',
    ],
}


class MurojaatState(StatesGroup):
  waiting_for_region = State()
  waiting_for_district = State()
  waiting_for_mfy = State()
  waiting_for_phone = State()
  waiting_for_message = State()


def init_db():
  conn = sqlite3.connect('murojaatlar.db')
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            phone TEXT,
            region TEXT,
            district TEXT,
            mfy TEXT,
            message TEXT,
            status TEXT DEFAULT 'Yangi'
        )
    """)
  # Eskirgan bazalarda mfy ustuni yo'q bo'lsa, avtomatik qo'shib qo'yadi
  try:
    cursor.execute('ALTER TABLE requests ADD COLUMN mfy TEXT;')
  except sqlite3.OperationalError:
    pass

  conn.commit()
  conn.close()


init_db()


def save_group_id(chat_id):
  with open(CONFIG_FILE, 'w') as f:
    json.dump({'group_id': chat_id}, f)


def load_group_id():
  try:
    with open(CONFIG_FILE, 'r') as f:
      return json.load(f).get('group_id')
  except FileNotFoundError:
    return None


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
  await message.answer(
      "👋 Assalomu alaykum! Murojaat va taklif yuborish botiga xush"
      " kelibsiz.\n\nMurojaat yo'llash uchun /murojaat buyrug'ini bosing."
  )


@dp.message(Command('setgroup'))
async def set_group(message: types.Message):
  if message.from_user.id != ADMIN_ID:
    await message.answer(
        "❌ Kechirasiz, bu buyruqni faqat asosiy admin ishlata oladi!"
    )
    return

  if message.chat.type in ['group', 'supergroup']:
    save_group_id(message.chat.id)
    await message.answer(
        "✅ Ushbu guruh murojaatlar kelib tushadigan maxfiy guruh sifatida"
        " muvaffaqiyatli ulandi!"
    )
  else:
    await message.answer(
        "❌ Bu buyruqni faqat maxfiy guruh ichida yozish kerak!"
    )


@dp.message(Command('murojaat'))
async def start_murojaat(message: types.Message, state: FSMContext):
  regions = list(REGIONS_DATA.keys())
  keyboard = ReplyKeyboardMarkup(
      keyboard=[
          [KeyboardButton(text=regions[i]), KeyboardButton(text=regions[i + 1])]
          for i in range(0, len(regions) - 1, 2)
      ],
      resize_keyboard=True,
      one_time_keyboard=True,
  )
  await message.answer(
      "🗺 Iltimos, ro'yxatdan o'zingizga tegishli **viloyat yoki"
      " respublikani** tanlang:",
      reply_markup=keyboard,
      parse_mode='MARKDOWN',
  )
  await state.set_state(MurojaatState.waiting_for_region)


@dp.message(MurojaatState.waiting_for_region)
async def process_region(message: types.Message, state: FSMContext):
  region_name = message.text
  if region_name not in REGIONS_DATA:
    await message.answer(
        "⚠️ Iltimos, tugmalardan to'g'ri viloyat yoki respublikani tanlang!"
    )
    return

  await state.update_data(region=region_name)
  districts = REGIONS_DATA[region_name]

  keyboard_layout = []
  for i in range(0, len(districts), 2):
    row = [KeyboardButton(text=districts[i])]
    if i + 1 < len(districts):
      row.append(KeyboardButton(text=districts[i + 1]))
    keyboard_layout.append(row)

  keyboard = ReplyKeyboardMarkup(
      keyboard=keyboard_layout, resize_keyboard=True, one_time_keyboard=True
  )
  await message.answer(
      f"📍 **{region_name}** bo'yicha tuman yoki shaharni tanlang:",
      reply_markup=keyboard,
      parse_mode='MARKDOWN',
  )
  await state.set_state(MurojaatState.waiting_for_district)


@dp.message(MurojaatState.waiting_for_district)
async def process_district(message: types.Message, state: FSMContext):
  district_name = message.text
  await state.update_data(district=district_name)

  await message.answer(
      f"🏡 **{district_name}** bo'yicha o'zingizning **mahalla (MFY)**"
      " nomingizni \n(masalan: *‘Nurobod’ MFY* yoki mahalla nomini) matn"
      " ko'rinishida yozib yuboring:",
      reply_markup=ReplyKeyboardRemove(),
      parse_mode='MARKDOWN',
  )
  await state.set_state(MurojaatState.waiting_for_mfy)


@dp.message(MurojaatState.waiting_for_mfy)
async def process_mfy(message: types.Message, state: FSMContext):
  mfy_text = message.text.strip()
  if not mfy_text:
    await message.answer("⚠️ Mahalla nomi bo'sh bo'lishi mumkin emas!")
    return

  await state.update_data(mfy=mfy_text)

  keyboard = ReplyKeyboardMarkup(
      keyboard=[[
          KeyboardButton(
              text="📞 Telefon raqamni yuborish", request_contact=True
          )
      ]],
      resize_keyboard=True,
      one_time_keyboard=True,
  )
  await message.answer(
      "📱 Aloqaga chiqishimiz uchun pastdagi tugmani bosing va telefon"
      " raqamingizni ulashing:",
      reply_markup=keyboard,
  )
  await state.set_state(MurojaatState.waiting_for_phone)


@dp.message(MurojaatState.waiting_for_phone, F.contact)
async def process_phone_contact(message: types.Message, state: FSMContext):
  phone = message.contact.phone_number
  await state.update_data(phone=phone)
  await message.answer(
      "✍️ Endi murojaatingiz matnini batafsil yozib yuboring (majburiy):",
      reply_markup=ReplyKeyboardRemove(),
  )
  await state.set_state(MurojaatState.waiting_for_message)


@dp.message(MurojaatState.waiting_for_phone, F.text)
async def process_phone_text(message: types.Message, state: FSMContext):
  phone = message.text
  await state.update_data(phone=phone)
  await message.answer(
      "✍️ Endi murojaatingiz matnini batafsil yozib yuboring (majburiy):",
      reply_markup=ReplyKeyboardRemove(),
  )
  await state.set_state(MurojaatState.waiting_for_message)


@dp.message(MurojaatState.waiting_for_message)
async def process_message(message: types.Message, state: FSMContext):
  user_text = message.text.strip()
  if not user_text:
    await message.answer(
        "⚠️ Murojaat matni bo'sh bo'lishi mumkin emas! Iltimos, matn"
        " kiriting:"
    )
    return

  data = await state.get_data()
  region = data.get('region')
  district = data.get('district')
  mfy = data.get('mfy')
  phone = data.get('phone')

  user_id = message.from_user.id
  username = (
      message.from_user.username if message.from_user.username else 'Nomaʼlum'
  )

  group_id = load_group_id()
  if not group_id:
    await message.answer(
        "⚠️ Xatolik: Murojaatlar yuboriladigan maxfiy guruh hali sozlangan emas!"
    )
    await state.clear()
    return

  conn = sqlite3.connect('murojaatlar.db')
  cursor = conn.cursor()
  cursor.execute(
      """
        INSERT INTO requests (user_id, username, phone, region, district, mfy, message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
      (user_id, username, phone, region, district, mfy, user_text),
  )
  conn.commit()
  req_id = cursor.lastrowid
  conn.close()

  text = (
      f"📩 **Yangi murojaat! (#{req_id})**\n\n"
      f"👤 **Foydalanuvchi:** @{username} (ID: `{user_id}`)\n"
      f"📞 **Telefon raqam:** `{phone}`\n"
      f"🗺 **Hudud/Viloyat:** {region}\n"
      f"📍 **Tuman/Shahar:** {district}\n"
      f"🏡 **Mahalla (MFY):** {mfy}\n\n"
      f"📝 **Matn:**\n{user_text}\n\n"
      f"📌 **Status:** 🟡 Yangi"
  )

  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[[
          InlineKeyboardButton(
              text="✅ Hal qilish (Yopish)", callback_data=f'resolve_{req_id}'
          )
      ]]
  )

  await bot.send_message(
      chat_id=group_id, text=text, parse_mode='MARKDOWN', reply_markup=keyboard
  )
  await message.answer(
      f"✅ Murojaatingiz muvaffaqiyatli qabul qilindi! Murojaat raqami:"
      f" **#{req_id}**\nTez orada ko'rib chiqiladi.",
      parse_mode='MARKDOWN',
  )
  await state.clear()


@dp.callback_query(F.data.startswith('resolve_'))
async def resolve_request(callback: types.CallbackQuery):
  req_id = callback.data.split('_')[1]
  admin_name = callback.from_user.full_name

  conn = sqlite3.connect('murojaatlar.db')
  cursor = conn.cursor()
  cursor.execute(
      "UPDATE requests SET status = 'Hal qilindi' WHERE id = ?", (req_id,)
  )
  conn.commit()
  conn.close()

  new_text = callback.message.text.replace(
      '📌 **Status:** 🟡 Yangi',
      f'📌 **Status:** ✅ Hal qilindi ({admin_name} tomonidan)',
  )
  await callback.message.edit_text(new_text, parse_mode='MARKDOWN')
  await callback.answer("Murojaat bajarilgan deb belgilandi!")


async def main():
  logging.basicConfig(level=logging.INFO)
  print('Bot ishga tushdi...')
  await dp.start_polling(bot)


if __name__ == '__main__':
  asyncio.run(main())
