import multiprocessing
import time
import traceback
import requests
from datetime import datetime
import sqlite3
import json

from binances import binance_get_symbols, binance_get_open_interest_5m, binance_get_open_interest_15m, binance_get_klines, binance_get_trades
from bybits import bybit_get_symbols, bybit_get_open_interest_5m, bybit_get_open_interest_15m, bybit_get_klines

from match import get_percent, istoria_in, istoria_out
from mass_print import mass_binance, mass_bybit, bot_api, history
from grafik import get_chart

from telebot import types
import telebot

conn = sqlite3.connect('OI.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS parametrs ('
               'nam FLOAT,'
               'pr_max FLOAT,'
               'pr_min FLOAT,'
               'chat_main_id INTEGER'
               ')')

cursor.execute('CREATE TABLE IF NOT EXISTS parametrs_b ('
               'nam FLOAT,'
               'pr_max FLOAT,'
               'pr_min FLOAT,'
               'chat_main_id INTEGER'
               ')')

cursor.execute('CREATE TABLE IF NOT EXISTS istoria ('
               'symbol INTEGER,'
               'data TEXT'
               ')')

x0 = 0
x1 = 3
x2 = 3
x1_ = 8
x2_ = 8
x3 = -4534721083

kolichestvo = 28800

cursor.execute('SELECT * FROM parametrs')
if cursor.fetchone() == None:
    cursor.execute('INSERT INTO parametrs (nam, pr_max, pr_min, chat_main_id) VALUES (?,?,?,?)', (x0, x1,x2,x3,))
    conn.commit()
    cursor.execute('INSERT INTO parametrs_b (nam, pr_max, pr_min, chat_main_id) VALUES (?,?,?,?)', (x0, x1_,x2_,x3,))
    conn.commit()
    json_txt_no = []
    json_txt = json.dumps(json_txt_no)
    cursor.execute('INSERT INTO istoria (symbol, data) VALUES (?,?)', (0, json_txt,))
    conn.commit()


conn.close()

def Binance():
    symbols = binance_get_symbols()

    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM parametrs WHERE nam = ?', (0,))
    result = cursor.fetchone()

    pr_max = result[1]
    pr_min = result[2]
    chat_main_id = result[3]

    conn.close()

    PARAMETERS = [
        pr_max, # x > %
        pr_min  # x < -%
    ]

    if symbols != None:
        for symbol in symbols:
            try:
                OI = binance_get_open_interest_5m(symbol['symbol'])
                #print(OI)
                if OI != []:
                    back = (float(OI[-4]['sumOpenInterest']) + float(OI[-3]['sumOpenInterest']))/2
                    now = OI[-1]['sumOpenInterest']
                    percent = get_percent(back, now)
                    print(f'Binance: {percent}')

                    percent_ok = [False]
                    if percent >= PARAMETERS[0]:
                        percent_ok[0] = True
                        percent_ok.append('UP')
                        percent_ok.append('🟩📈')
                    elif percent <= -PARAMETERS[0]:
                        percent_ok[0] = True
                        percent_ok.append('DOWN')
                        percent_ok.append('🟥📉')

                    if percent_ok[0]:
                        OI = binance_get_open_interest_15m(symbol['symbol'])
                        klines = binance_get_klines(symbol['symbol'])

                        opens, high, low, close, volume, date, OIR = [], [], [], [], [], [], []

                        for i in OI:
                            OIR.append(i['sumOpenInterest'])

                        for i in klines:
                            sec = i[0] / 1000
                            date_time = datetime.fromtimestamp(sec)

                            opens.append(float(i[1]))
                            high.append(float(i[2]))
                            low.append(float(i[3]))
                            close.append(float(i[4]))
                            volume.append(float(i[5]))
                            date.append(date_time)

                        datas = {'Open': opens, 'High': high, 'Low': low, 'Close': close, 'Volume': volume, 'OI': OIR}

                        volume_8_15m = [[volume[-i] for i in range(5,9)],[volume[-i] for i in range(1,5)]]
                        volume_8_15m_sr = []

                        for i in volume_8_15m:
                            x = 0
                            for l in i:
                                x += float(l)

                            x /= 4
                            volume_8_15m_sr.append(x)

                        percent_volume = get_percent(volume_8_15m_sr[0], volume_8_15m_sr[1])

                        kol_vo_traders = binance_get_trades(symbol['symbol'])

                        OI4h = get_percent(OIR[-16], OIR[-1])

                        kol_vo = istoria_out()
                        t = time.time()
                        kol_vo_nam = 0
                        for kol in kol_vo:
                            if kol['symbol'] == symbol['symbol'] and kol['time'] + kolichestvo >= t:
                                kol_vo_nam += 1

                        kol_vo.append({'symbol': symbol['symbol'], 'time': t, })
                        dalat = [i for i in kol_vo if i['time'] + kolichestvo < t]

                        for i in dalat:
                            kol_vo.remove(i)
                        istoria_in(kol_vo)

                        get_chart(symbol['symbol'], datas, date)
                        time.sleep(2)
                        mass_binance({
                            's':symbol['symbol'],
                            's#': '🟡#Binance',
                            'pr':percent,
                            'box':percent_ok[2],
                            'direction': percent_ok[1],
                            'volume': percent_volume,
                            'trades': kol_vo_traders,
                            'OI4h': OI4h,
                            'CoinCHG24h': round(float(symbol['priceChangePercent']), 1),
                            'kol_vo_nam': kol_vo_nam
                        })

                        time.sleep(2)
            except Exception as e:
                print('\nОшибка:\n', traceback.format_exc())



def ByBit():
    symbols = bybit_get_symbols()

    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM parametrs_b WHERE nam = ?', (0,))
    result = cursor.fetchone()

    pr_max = result[1]
    pr_min = result[2]
    chat_main_id = result[3]

    conn.close()

    PARAMETERS = [
        pr_max,  # x > %
        pr_min  # x < -%
    ]

    if symbols != None:
        for symbol in symbols:
            try:
                OI5m = bybit_get_open_interest_5m(symbol['symbol'])
                #print(OI)
                if OI5m != [] and OI5m != None:
                    back = (float(OI5m[-4]['openInterest']) + float(OI5m[-3]['openInterest']))/2
                    now = OI5m[-1]['openInterest']
                    percent = get_percent(back, now)
                    print(f'Bybit: {percent}')

                    percent_ok = [False]
                    if percent >= PARAMETERS[0]:
                        percent_ok[0] = True
                        percent_ok.append('UP')
                        percent_ok.append('🟩📈')
                    elif percent <= -PARAMETERS[0]:
                        percent_ok[0] = True
                        percent_ok.append('DOWN')
                        percent_ok.append('🟥📉')

                    if percent_ok[0]:
                        OI = bybit_get_open_interest_15m(symbol['symbol'])
                        klines = bybit_get_klines(symbol['symbol'])

                        opens, high, low, close, volume, date, OIR = [], [], [], [], [], [], []

                        for i in OI:
                            OIR.append(i['openInterest'])

                        for i in klines:
                            sec = int(i[0]) / 1000
                            date_time = datetime.fromtimestamp(sec)

                            opens.append(float(i[1]))
                            high.append(float(i[2]))
                            low.append(float(i[3]))
                            close.append(float(i[4]))
                            volume.append(float(i[5]))
                            date.append(date_time)

                        datas = {'Open': opens, 'High': high, 'Low': low, 'Close': close, 'Volume': volume, 'OI': OIR}

                        volume_8_15m = [[volume[-i] for i in range(5,9)],[volume[-i] for i in range(1,5)]]
                        volume_8_15m_sr = []

                        for i in volume_8_15m:
                            x = 0
                            for l in i:
                                x += float(l)

                            x /= 4
                            volume_8_15m_sr.append(x)

                        percent_volume = get_percent(volume_8_15m_sr[0], volume_8_15m_sr[1])

                        OI4h = get_percent(OIR[-16], OIR[-1])

                        kol_vo = istoria_out()
                        t = time.time()
                        kol_vo_nam = 0
                        for kol in kol_vo:
                            if kol['symbol'] == symbol['symbol'] and kol['time'] + kolichestvo >= t:
                                kol_vo_nam += 1

                        kol_vo.append({'symbol': symbol['symbol'], 'time': t, })
                        dalat = [i for i in kol_vo if i['time'] + kolichestvo < t]

                        for i in dalat:
                            kol_vo.remove(i)
                        istoria_in(kol_vo)

                        get_chart(symbol['symbol'], datas, date)
                        time.sleep(2)
                        mass_bybit({
                            's':symbol['symbol'],
                            's#': '⚫️#ByBit',
                            'pr':percent,
                            'box':percent_ok[2],
                            'direction': percent_ok[1],
                            'volume': percent_volume,
                            'OI4h': OI4h,
                            'CoinCHG24h': round(float(symbol['priceChangePercent']), 1),
                            'kol_vo_nam': kol_vo_nam
                        })

            except Exception as e:
                print('\nОшибка:\n', traceback.format_exc())

def Binance_main():
    while True:
        try:
            bot = bot_api()
            bot.send_message(-4565644547, '🟡:start')
            print('start Binance')
            Binance()
            #time.sleep(10000)
        except Exception as e:
            print(f"Binance process encountered an error: ", traceback.format_exc())
        time.sleep(1)  # Небольшая задержка перед перезапуском

def ByBit_main():
    while True:
        try:
            bot = bot_api()
            bot.send_message(-4565644547, '⚫️:start')
            print('start ByBit')
            ByBit()
        except Exception as e:
            print(f"ByBit process encountered an error: ", traceback.format_exc())
        time.sleep(1)  # Небольшая задержка перед перезапуском

def history_main():
    while True:
        try:
            now = datetime.now()
            current_time = now.strftime("%M")
            if int(current_time) == 60 or int(current_time) == 0:
                history()
                time.sleep(60)
            time.sleep(30)
        except:
            pass

def buttons():
    bot = bot_api()
    @bot.message_handler(commands=['start', 'help'])
    def start(message):
        bot.send_message(message.chat.id, 'Мы приветствуем тебя трейдер. На все вопросы я отвечаю в группе👍\n\n'
                                          '/PARBI - Параметры на Binance\n\n'
                                          '/UPDBI - Обновить параметры Binance\n\n'
                                          '/PARBY - Параметры на Bybit\n\n'
                                          '/UPDBY - Обновить параметры Bybit')

    @bot.message_handler(commands=['PARBI'])
    def PARAMETERS(message):
        conn = sqlite3.connect('OI.db', check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM parametrs WHERE nam = ?', (0,))
        result = cursor.fetchone()

        pr_max = result[1]
        pr_min = result[2]
        chat_main_id = result[3]

        conn.close()

        bot.send_message(message.chat.id,
                         f'NOW parameters:\n\n1: {pr_max} - x>n\n\n2: {pr_min} - x<-n\n\n3: {chat_main_id}')

    @bot.message_handler(commands=['UPDBI'])
    def UPDATE(message):
        conn = sqlite3.connect('OI.db', check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM parametrs WHERE nam = ?', (0,))
        result = cursor.fetchone()

        pr_max = result[1]
        pr_min = result[2]
        chat_main_id = result[3]

        conn.close()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton(pr_max)
        b2 = types.KeyboardButton(pr_min)
        b3 = types.KeyboardButton(chat_main_id)
        markup.add(b1, b2, b3)
        bot.send_message(message.chat.id,
                         f'NOW parameters:\n\n1: {pr_max} - x>n\n\n2: {pr_min} - x<-n\n\n3: {chat_main_id}\n\nВведите первый параметр:',
                         reply_markup=markup)
        bot.register_next_step_handler(message, UPDATE_0)

    def UPDATE_0(message):
        try:
            txt = float(message.text)
            data = [txt]

            bot.send_message(message.chat.id, 'Введите второй параметр:')
            bot.register_next_step_handler(message, UPDATE_1, data)
        except:
            bot.send_message(message.chat.id,
                             f'ERROR')
            bot.register_next_step_handler(message, UPDATE_0)

    def UPDATE_1(message, data):
        try:
            txt = float(message.text)
            data.append(txt)
            bot.send_message(message.chat.id, 'Введите третий параметр:')
            bot.register_next_step_handler(message, UPDATE_2, data)
        except:
            bot.send_message(message.chat.id,
                             f'ERROR')
            bot.register_next_step_handler(message, UPDATE_1, data)

    def UPDATE_2(message, data):
        try:
            txt = int(message.text)
            data.append(txt)
            save(message, data)
        except Exception as e:
            # print('\nОшибка:\n', traceback.format_exc())
            bot.send_message(message.chat.id,
                             f'ERROR')
            # print('ERROR')
            bot.register_next_step_handler(message, UPDATE_2, data)

    def save(message, data):
        new_nam = 0
        new_pr_max = data[0]
        new_pr_min = data[1]
        new_chat_main_id = data[2]

        conn = sqlite3.connect('OI.db', check_same_thread=False)
        cursor = conn.cursor()

        # Запрос на обновление строки с новыми параметрами
        update_query = '''
            UPDATE parametrs
            SET pr_max = ?, pr_min = ?, chat_main_id = ?
            WHERE nam = ?
        '''

        # Выполнение запроса на обновление
        cursor.execute(update_query, (new_pr_max, new_pr_min, new_chat_main_id, new_nam))

        # Сохранение изменений в базе данных
        conn.commit()
        conn.close()
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,
                         f'SAVE parameters:\n\n1: {new_pr_max} - x>n\n\n2: {new_pr_min} - x<-n\n\n3: {new_chat_main_id}',
                         reply_markup=a)

    @bot.message_handler(commands=['PARBY'])
    def PARAMETERS(message):
        conn = sqlite3.connect('OI.db', check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM parametrs_b WHERE nam = ?', (0,))
        result = cursor.fetchone()

        pr_max = result[1]
        pr_min = result[2]
        chat_main_id = result[3]

        conn.close()

        bot.send_message(message.chat.id,
                         f'NOW parameters:\n\n1: {pr_max} - x>n\n\n2: {pr_min} - x<-n\n\n3: {chat_main_id}')

    @bot.message_handler(commands=['UPDBY'])
    def UPDATE(message):
        conn = sqlite3.connect('OI.db', check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM parametrs_b WHERE nam = ?', (0,))
        result = cursor.fetchone()

        pr_max = result[1]
        pr_min = result[2]
        chat_main_id = result[3]

        conn.close()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton(pr_max)
        b2 = types.KeyboardButton(pr_min)
        b3 = types.KeyboardButton(chat_main_id)
        markup.add(b1, b2, b3)
        bot.send_message(message.chat.id,
                         f'NOW parameters:\n\n1: {pr_max} - x>n\n\n2: {pr_min} - x<-n\n\n3: {chat_main_id}\n\nВведите первый параметр:',
                         reply_markup=markup)
        bot.register_next_step_handler(message, UPDATE_0_bybit)

    def UPDATE_0_bybit(message):
        try:
            txt = float(message.text)
            data = [txt]

            bot.send_message(message.chat.id, 'Введите второй параметр:')
            bot.register_next_step_handler(message, UPDATE_1_bybit, data)
        except:
            bot.send_message(message.chat.id,
                             f'ERROR')
            bot.register_next_step_handler(message, UPDATE_0_bybit)

    def UPDATE_1_bybit(message, data):
        try:
            txt = float(message.text)
            data.append(txt)
            bot.send_message(message.chat.id, 'Введите третий параметр:')
            bot.register_next_step_handler(message, UPDATE_2_bybit, data)
        except:
            bot.send_message(message.chat.id,
                             f'ERROR')
            bot.register_next_step_handler(message, UPDATE_1_bybit, data)

    def UPDATE_2_bybit(message, data):
        try:
            txt = int(message.text)
            data.append(txt)
            save_bybit(message, data)
        except Exception as e:
            # print('\nОшибка:\n', traceback.format_exc())
            bot.send_message(message.chat.id,
                             f'ERROR')
            # print('ERROR')
            bot.register_next_step_handler(message, UPDATE_2_bybit, data)

    def save_bybit(message, data):
        new_nam = 0
        new_pr_max = data[0]
        new_pr_min = data[1]
        new_chat_main_id = data[2]

        conn = sqlite3.connect('OI.db', check_same_thread=False)
        cursor = conn.cursor()

        # Запрос на обновление строки с новыми параметрами
        update_query = '''
            UPDATE parametrs_b
            SET pr_max = ?, pr_min = ?, chat_main_id = ?
            WHERE nam = ?
        '''

        # Выполнение запроса на обновление
        cursor.execute(update_query, (new_pr_max, new_pr_min, new_chat_main_id, new_nam))

        # Сохранение изменений в базе данных
        conn.commit()
        conn.close()
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,
                         f'SAVE parameters:\n\n1: {new_pr_max} - x>n\n\n2: {new_pr_min} - x<-n\n\n3: {new_chat_main_id}',
                         reply_markup=a)

    bot.polling(none_stop=True, timeout=123)

def restart_process(target):
    while True:
        process = multiprocessing.Process(target=target)
        process.start()
        process.join()  # Ожидаем завершения процесса
        print(f"Process {target} завершился, перезапуск...")

if __name__ == '__main__':
    process1 = multiprocessing.Process(target=restart_process, args=(Binance_main,))
    process2 = multiprocessing.Process(target=restart_process, args=(ByBit_main,))
    process3 = multiprocessing.Process(target=restart_process, args=(buttons,))
    process4 = multiprocessing.Process(target=restart_process, args=(history_main,))#history_main

    process1.start()
    process2.start()
    process3.start()
    process4.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()

    print("Обе функции завершили выполнение")

