import requests
import config
from functools import lru_cache

XYANDEXAPIKEYWEATHER=config.XYANDEXAPIKEYWEATHER
XYANDEXAPIKEYDIR=config.XYANDEXAPIKEYDIR
URLWEATHER =config.URLWEATHER
URLDIR=config.URLDIR
WEATHER={
"clear":"ясно",
"partly-cloudy":"малооблачно",
"cloudy":"облачно с прояснениями",
"overcast":"пасмурно",
"drizzle":"морось",
"light-rain":"небольшой дождь",
"rain":"дождь",
"moderate-rain":"умеренно сильный дождь",
"heavy-rain":"сильный дождь",
"continuous-heavy-rain":"длительный сильный дождь",
"showers":"ливень",
"wet-snow":"дождь со снегом",
"light-snow":"небольшой снег",
"snow":"снег",
"snow-showers":"снегопад",
"hail":"град",
"thunderstorm":"гроза",
"thunderstorm-with-rain":"дождь с грозой",
"thunderstorm-with-hail":"гроза с градом"
}
WIND_DIR={'nw':'северо-западное',
'n':'северное',
'ne':'северо-восточное',
'e':'восточное',
'se':'юго-восточное',
's':'южное',
'sw':'юго-западное',
'w':'западное',
'с':'штиль'}
class YandexApi():

    def createHead(self,XYandexAPIKey):
        return {"X-Yandex-API-Key":XYandexAPIKey}
    def getResp(self,XYandexAPIKey:str, URL:str):
        response = requests.get(URL,
                                headers=self.createHead(XYandexAPIKey))
        return response.json()

#@lru_cache(maxsize=128)
class LocCorr():
    def __init__(self):
        self.core=''
    def parsResp(self,dt):
        try:
            for i in dt:
                try:
                    if dt['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']:
                        self.fee=dt['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                except:pass
                if i=='upperCorner' :
                    return dt[i]
                elif type(dt[i]) == dict:
                    self.core = self.parsResp(dt[i])
                elif type(dt[i]) == list:
                    for j in dt[i]:
                        self.core = self.parsResp(j)
            if self.fee:
                self.core=self.fee
            return self.core
        except:
            # print('error')
            return "error"

    def get_corr(self,city: str):
        resp=YandexApi().getResp(XYandexAPIKey=XYANDEXAPIKEYDIR,URL=URLDIR.replace('@APIKEY',XYANDEXAPIKEYDIR)+city)
        return [cor for cor in self.parsResp(resp).split(' ')]


class Weather():

    def createURL(self,lon:str,lat:str):
        return URLWEATHER.replace("@LAT",str(lat)).replace("@LON",str(lon))

    def getWeather(self,lon,lat):
        json_response =YandexApi().getResp(XYANDEXAPIKEYWEATHER,self.createURL(lat=lat,lon=lon))
        #print()
        resp={
            "Температура":str(json_response['fact']['temp'])+" °C",
            "Погода":WEATHER[json_response['fact']['condition']],
            "Скорость ветра":str(json_response['fact']['wind_speed'])+" м/с",
           # "Скорость ветра": json_response['fact'],
            "Направление ветра":WIND_DIR[json_response['fact']['wind_dir']],
            "Карта: " :json_response['info']['url'],

        }
        return resp

