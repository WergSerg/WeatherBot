import config
from lib.YandexAPI  import Weather, LocCorr

# -*- coding: utf-8 -*-

import telebot
import json
import requests

bot = telebot.TeleBot(config.BOTAPI)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    sendMess(message.from_user.id, "я покажу тебе погоду хаха.\nПришли мне свою геопозицию",mode='Markdown')

@bot.message_handler(content_types=['location'])
def get_Location(message):
    aaa=Weather()
    lon=message.location.longitude
    lat=message.location.latitude
    res=aaa.getWeather(lat=lat,lon=lon)
    sendMess(message.from_user.id, makeMess(res=res), mode='Markdown')

@bot.message_handler(content_types=['text'])
def get_city(message):
    resp=LocCorr().get_corr(message.text)
    aaa=Weather()
    lon=resp[0]
    lat=resp[1]
    res=aaa.getWeather(lat=lat,lon=lon)
    sendMess(message.from_user.id, makeMess(res=res), mode='Markdown')

def makeMess(res):
    mess = ''
    for i in res:
        mess+=str(i)+": "+str(res[i])+'\n'
    return mess

def sendMess(id, mess, mode=None):
    bot.send_message(id, mess, parse_mode=mode)



try:
    bot.polling(none_stop=True, interval=0)
except:
    bot.polling(none_stop=True, interval=0)
