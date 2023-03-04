#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import telebot
from config import TOKEN
 
bot = telebot.TeleBot(TOKEN)
 
 
@bot.message_handler(commands=['start', ])
def say_hi(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'O hai!')
 


if __name__ == '__main__':
    bot.polling(none_stop=True)
