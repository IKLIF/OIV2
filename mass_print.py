import telebot
from telebot import types

import time

from match import istoria_out
from datetime import datetime

def bot_api():
    API = '7322937059:AAHWbYHdmMXhZxNuBK8ujPC8agYuFScxTkw'#-2481950212
    bot = telebot.TeleBot(API)
    return bot

kanal = -1002476767072#-4534721083#-4531224961 #

def mass_binance(params):
    bot = bot_api()

    markup = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(text='TV',
                                    url=f"https://ru.tradingview.com/chart/{params['s']}.P")
    b2 = types.InlineKeyboardButton(text='CG',
                                    url=f"https://www.coinglass.com/tv/ru/Binance_{params['s']}")
    b3 = types.InlineKeyboardButton(text='ПЕРЕХОД В БОТ',
                                    url=f"https://t.me/+JnErqgdsSuBmZWRi")
    markup.add(b1, b2)
    markup.add(b3)


    print(params)
    photo = open(f'img/{params["s"]}.png', 'rb')

    if params['OI4h'] > 0:
        OI4h_st = '↗️'
    else:
        OI4h_st = '↘️'

    TXT = (f"{params['box']}<code>{params['s']}</code>\n"
           f"{params['s#']}\n"
           f"#{params['s']}  #{params['direction']}\n"
           f"\n"
           f"📍Открытый интерес: 👉 {params['pr']}%\n"
           f"\n"
           f"📌Volume: 👉 {params['volume']}%\n"
           f"📌Trades:(8h) 👉 {params['trades']}\n"
           f"\n"
           f"<i>{OI4h_st}OI: Chg % 4h=</i> <b><u>{params['OI4h']}%</u></b>\n"
           f"<i>Сoin: Chg % 24h=</i> <b><u>{params['CoinCHG24h']}%</u></b>\n"
           f" За 8ч: {params['kol_vo_nam']}")

    bot.send_photo(kanal, photo,
                   caption=TXT,
                   parse_mode='HTML', reply_markup=markup)

def mass_bybit(params):
    bot = bot_api()
    markup = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(text='TV',
                                    url=f"https://ru.tradingview.com/chart/{params['s']}.P")
    b2 = types.InlineKeyboardButton(text='CG',
                                    url=f"https://www.coinglass.com/tv/ru/Bybit_{params['s']}")
    b3 = types.InlineKeyboardButton(text='ПЕРЕХОД В БОТ',
                                    url=f"https://t.me/+JnErqgdsSuBmZWRi")
    markup.add(b1, b2)
    markup.add(b3)


    print(params)
    photo = open(f'img/{params["s"]}.png', 'rb')

    if params['OI4h'] > 0:
        OI4h_st = '↗️'
    else:
        OI4h_st = '↘️'

    TXT = (f"{params['box']}<code>{params['s']}</code>\n"
           f"{params['s#']}\n"
           f"#{params['s']}  #{params['direction']}\n"
           f"\n"
           f"📍Открытый интерес: 👉 {params['pr']}%\n"
           f"\n"
           f"📌Volume: 👉 {params['volume']}%\n"
           f"\n"
           f"<i>{OI4h_st}OI: Chg % 4h=</i> <b><u>{params['OI4h']}%</u></b>\n"
           f"<i>Сoin: Chg % 24h=</i> <b><u>{params['CoinCHG24h']}%</u></b>\n"
           f" За 8ч: {params['kol_vo_nam']}")

    bot.send_photo(kanal, photo,
                   caption=TXT,
                   parse_mode='HTML', reply_markup=markup)

def history():
    kol_vo = istoria_out()
    symbol = []
    for i in kol_vo:
        if i['symbol'] in symbol:
            pass
        else:
            symbol.append(i['symbol'])

    symbol_quantity = []

    for i in symbol:
        z = 0

        time = None

        for l in kol_vo:
            if l['symbol'] == i:
                z += 1
                if time == None:
                    time = l['time']
                else:
                    if time < l['time']:
                        time = l['time']
        symbol_quantity.append({'symbol':i, 'quantity': z, 'time': time})

    symbol_quantity_sorted = sorted(symbol_quantity, key=lambda p: p['time'])
    symbol_quantity_sorted.reverse()
    txt = ''
    for i in symbol_quantity_sorted:
    #    txt = txt + f"{i['quantity']} | <code>{i['symbol']}</code>, #{i['symbol']} | {datetime.fromtimestamp(i['time']).strftime("%A, %d, %I:%M:%S")}\n"#datetime.fromtimestamp(i['time']).strftime("%A, %B %d, %Y %I:%M:%S"
    #    txt = txt + (f"<code>{i['symbol']}</code>, #{i['symbol']}\n"
    #                 f"{i['quantity']} | {datetime.fromtimestamp(i['time']).strftime("%d, %I:%M:%S")}\n")
        txt = txt + f"| {i['quantity']} | <code>{i['symbol']}</code> | {datetime.fromtimestamp(i['time']).strftime('%A, %I:%M:%S')}\n"#datetime.fromtimestamp(i['time']).strftime("%A, %B %d, %Y %I:%M:%S"
    bot = bot_api()
    bot.send_message(kanal, txt, parse_mode='HTML')

#t_volue}\n{result_trades}\n\n{txt_pr_4h}<i>Сoin: Chg % 24h=</i> <b><u>{priceChangePercent}%</u></b>\n За 8ч: {kol_vo_nam}", parse_mode='HTML', reply_markup=markup )
