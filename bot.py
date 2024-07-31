from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto , ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiocryptopay import AioCryptoPay, Networks
from config import *
from random import randint , choice
from pythonping import ping
from time import sleep
from colorama import Fore 
import string 
import logging
import os
import shutil
import asyncio
import psutil
import sys
import traceback
import requests
import datetime
import threading
import aiohttp
from bs4 import BeautifulSoup
import time
import requests
from telethon.sync import TelegramClient
from telethon import functions, types


    



async def start_cicle(number):
    file = open(f"status.txt", "r", encoding="utf-8")
    status = file.read()
    file.close()
    
    async with aiohttp.ClientSession(trust_env=True) as session:
        while status == "Work":
            start_time = time.time()
            good_links = []
            print(f"Cicle {number} start")
            file = open(f"bd.txt", "r" , encoding="utf-8")
            bd = file.read()
            file.close()
            print(bd)
            bd = bd.split("\n")

            
            for link in bd:
                print(link)
                
                file = open(f"status.txt", "r", encoding="utf-8")
                status = file.read()
                file.close()
                if status == "Work":
                    try:
                        async with session.get(link) as response:
                            if response.status == 200:
                                # Используйте response.text() как функцию для асинхронного вызова
                                soup = BeautifulSoup(await response.text(), 'html.parser')
                                user_info = soup.find('div', {'class': 'tgme_page_title'})
                                if not user_info:
                                    print(f"NO USER {link}")
                                    await bot.send_message(5282299482, f'{link}')
                                    await bot.send_message(6900311048, f'{link}')
                                else:
                                    print(f"EXISTS USER {link}")
                    except:
                        print("error")
                    sleep(0.3)

            file = open(f"status.txt", "r", encoding="utf-8")
            status = file.read()
            file.close()

def start_cicle_thread(number):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_cicle(number))





bot = Bot(token=token)
dp = Dispatcher()












class States:
    FIRST_STATE = "state: 1"
class Newbd(StatesGroup):
    stage1 = State()
# class Dellink(StatesGroup):
#     stage1 = State()


@dp.message()
async def delete_number(message: types.Message):
    if message.text:
        if message.chat.id == 5282299482 or message.chat.id == 6550258397 or message.chat.id == 5901778338 or message.chat.id == 6900311048:
            if message.text[:7].lower() == "удалить":
                todell = message.text.split("\n")
                todell.pop(0)

                file = open("bd.txt" , "r" , encoding="utf-8")
                cur_bd = file.read()
                file.close()
                cur_bd = cur_bd.split("\n")

                to_add = []
                deleted = []

                for link in cur_bd:
                    if link not in todell:
                        to_add.append(link)
                    else:
                        deleted.append(link)

                to_add = "\n".join(to_add)
                deleted = ", ".join(deleted)


                file = open("bd.txt" , "w" , encoding="utf-8")
                file.write(to_add)
                file.close()


                await bot.send_message(chat_id=message.chat.id, text=f"🔗 Ссылки: {deleted} удалены")

            elif message.text[:8].lower() == "добавить":
                mmessage = message.text.split("\n")
                mmessage.pop(0)
                new_link = "\n".join(mmessage)

                file = open("bd.txt" , "a" , encoding="utf-8")
                file.write(f"\n{new_link}")
                file.close()

                await bot.send_message(chat_id=message.chat.id, text=f"🔗 Ссылки:\n{new_link}\nдобавлены")
                
            elif message.text == "/start":
                file = open(f"bd.txt", "r" , encoding="utf-8")
                bd = file.read()
                file.close()
                bd_n = bd.split("\n")
                file = open(f"status.txt", "r" , encoding="utf-8")
                status = file.read()
                file.close()
                menu = []
                if bd == "":
                    bd_n = []
                if status == "Stop":
                    status = "Остановлен❌"
                    menu.append([
                    InlineKeyboardButton(text="✅Старт", callback_data="mamenu)start")
                    ])
                elif status == "Work":
                    status = "Работает✅"
                    menu.append([
                    InlineKeyboardButton(text="Стоп❌", callback_data="mamenu)stop")
                    ])
                else:
                    status = "Error"
            
        
                menu.append([
                    InlineKeyboardButton(text="🗂Выкачать", callback_data="downlo")
                    ])
                
 
                inline_buttons = InlineKeyboardMarkup(inline_keyboard=menu)
        
                await bot.delete_message(message.chat.id, message.message_id)
                await bot.send_message(chat_id=message.from_user.id, text=f"💡 Главное меню\n\n⚙️ Статус цикла: {status}\n📊 Объём базы данных: {len(bd_n)}", reply_markup=inline_buttons)
            elif message.text[:5].lower() == "старт":
                file = open(f"status.txt", "w" , encoding="utf-8")
                file.write("Work")
                file.close()
                asyncio.create_task(start_cicle(1))
                await bot.send_message(chat_id=message.from_user.id, text=f"Цикл запущен")
            elif message.text[:4].lower() == "стоп":
                file = open(f"status.txt", "w" , encoding="utf-8")
                file.write("Stop")
                file.close()
                await bot.send_message(chat_id=message.from_user.id, text=f"Цикл остановлен")
    if message.document:
        if message.chat.id == 5282299482 or message.chat.id == 6550258397 or message.chat.id == 5901778338 or message.chat.id == 6900311048:
            print("1")
            fillee = message.document
            file_id = fillee.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            file = await bot.download_file(file_path)
    
            if file_info.file_path.endswith('.txt'):
                print("2")
                print(f"FILEIF: {file_info.file_id}")
    
                file.seek(0)
                with open("bd.txt", 'wb') as new_file:
                    new_file.write(file.read())
    
                file = open(f"bd.txt", "r" , encoding="utf-8")
                bd = file.read()
                file.close()
                new_links_n = bd.split("\n")
    
                await bot.send_message(chat_id=message.from_user.id, text=f"📋 Новая База Данных установлена, количество ссылок: {len(new_links_n)}")
            else:
                await bot.send_message(chat_id=message.from_user.id, text=f"❌ Ошибка: База Данных должна быть в .txt формате")




@dp.callback_query(lambda callback_query: True)
async def maincall(callback: CallbackQuery, state: FSMContext):
    
    callback_data = callback.data
    full_call = callback_data[6:]
    command = callback_data[:6]
    call_message_id = callback.message.message_id
    call_message_chat_id = callback.message.chat.id
    call_from_user = callback.from_user.id
    user = callback.from_user
    data_main_list = (callback_data[6:]).split(")")
    await state.set_state(None)
    if command == "mamenu":
        if data_main_list[1] == "start":
            file = open(f"status.txt", "w" , encoding="utf-8")
            file.write("Work")
            file.close()
            # threading.Thread(target=start_cicle_thread, daemon=True).start()
            # global accounts
            # for index, item in enumerate(accounts):
            asyncio.create_task(start_cicle(1))
            await callback.answer("Цикл запущен✅")
        elif data_main_list[1] == "stop":
            file = open(f"status.txt", "w" , encoding="utf-8")
            file.write("Stop")
            file.close()
            await callback.answer("Цикл остановлен❌")
        else:
            pass


        file = open(f"bd.txt", "r" , encoding="utf-8")
        bd = file.read()
        file.close()
        bd_n = bd.split("\n")
        file = open(f"status.txt", "r" , encoding="utf-8")
        status = file.read()
        file.close()
        menu = []
        if bd == "":
            bd_n = []
        if status == "Stop":
            status = "Остановлен❌"
            menu.append([
            InlineKeyboardButton(text="✅Старт", callback_data="mamenu)start")
            ])
        elif status == "Work":
            status = "Работает✅"
            menu.append([
            InlineKeyboardButton(text="Стоп❌", callback_data="mamenu)stop")
            ])
        else:
            status = "Error"

        menu.append([
            InlineKeyboardButton(text="🗂Выкачать", callback_data="downlo")
            ])



        inline_buttons = InlineKeyboardMarkup(inline_keyboard=menu)
        await bot.edit_message_text(chat_id=call_message_chat_id, message_id=call_message_id , text=f"💡 Главное меню\n\n⚙️ Статус цикла: {status}\n📊 Объём базы данных: {len(bd_n)}", reply_markup=inline_buttons)
    elif command == "downlo":
        file = FSInputFile('bd.txt')
        await bot.send_document(chat_id=call_message_chat_id, document=file)






if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)
