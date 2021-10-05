try:
    import configparser
except ImportError:
    import ConfigParser as configparser



config = configparser.ConfigParser()
config.read("settings.ini")

XYANDEXAPIKEYWEATHER = config.get("Settings","XYANDEXAPIKEYWEATHER")
XYANDEXAPIKEYDIR = config.get("Settings","XYANDEXAPIKEYDIR")
URLWEATHER = config.get("Settings","URLWEATHER")
URLDIR = config.get("Settings","URLDIR")
BOTAPI = config.get("Settings","BOTAPI")