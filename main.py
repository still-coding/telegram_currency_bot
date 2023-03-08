#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Currency conversion telegram bot with basic commands. Uses data from CoinGecko API.
"""
from aiogram import Bot, Dispatcher, executor, types

from bot_api_token import TOKEN
from converter import CurrencyConverter
from exceptions import *
from exchange_rates_parser import ExchangeRatesParser
from user_query_parser import UserQueryParser

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

start_message = """Hi!
I'm Currency Bot and I can help you to convert different assest.

Enter your conversion query in following format:
<em>amount \t src_currency</em> \t to \t <em>dst_currency</em>
or
<em>amount \t src_currency</em> \t в \t <em>dst_currency</em>

Examples:
100 usd to rub
777 рублей в евро
2 биткоина в долларах

Enter /list command to see all of the supported assets.

Please note that the conversion result <b>won't include any fees</b>."""


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.answer_chat_action("typing")
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns_text = ("/help", "/list")
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    await message.reply(start_message, reply_markup=keyboard_markup, parse_mode="HTML")


@dp.message_handler(commands=["list"])
async def send_list(message: types.Message):
    await message.answer_chat_action("typing")
    try:
        _, rates = ExchangeRatesParser.get_rates()
        by_type = {}
        for ticker, data in rates.items():
            typ = data["type"].capitalize()
            if typ in by_type:
                t = ticker.upper()
                u = data["unit"]
                if t == u:
                    by_type[typ].append(f"\t• {data['name']}: {t}\n")
                else:
                    by_type[typ].append(f"\t• {data['name']}: {t} ({u})\n")
            else:
                by_type[typ] = []
    except DataFetchError:
        await message.reply("Something went wrong with excange data, sorry 🥺")
    else:
        currency_list = "List of supported assets:\n"
        for category, lst in by_type.items():
            currency_list += f"<b>{category}</b>\n"
            for currency in lst:
                currency_list += currency
        await message.reply(currency_list, parse_mode="HTML")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def convert(message: types.Message):
    await message.answer_chat_action("typing")
    try:
        units, rates = ExchangeRatesParser.get_rates()
    except DataFetchError:
        await message.reply("Something went wrong with exchange data, sorry 🥺")
        return

    try:
        user_parser = UserQueryParser(list(rates.keys()), units)
        amount, src, dst = user_parser.parse(message.text)
    except UserQueryParsingError:
        await message.reply(
            "I don't understand your query, please try something else 😅"
        )
        return

    if amount.is_integer():
        amount = round(amount)

    if amount == 0:
        await message.reply("It's ZERO in every imaginable currency 🤓")
        return

    conversion_result = CurrencyConverter(rates).convert(amount, src, dst)

    if conversion_result < 0.01:
        conversion_result = format(conversion_result, ".8f")
    else:
        conversion_result = round(conversion_result, 2)

    if src == dst:
        answer = f"{amount} {src.upper()} is {amount} {dst.upper()}, silly 🙃"
    else:
        answer = f"{amount} {src.upper()} = <b>{conversion_result}</b> {dst.upper()}"

    await message.reply(answer, parse_mode="HTML")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
