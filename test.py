
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))
bot_token = '6594474232:AAF39jlHxRJepEaOYcxo9NZhe-pQgzl43lo'
chat_id = "-960438482"


def brand ():

    db = client["brands"]
    collection= db["tecno"]

    t9 = collection.find({})

    array_brand= []

    for i in t9:
        array_brand.append(i["brand"])
    print(array_brand)
    
    return array_brand


u=50

g = "Sny"


array = ['lenovo', 'Lg', 'Asus', 'Xiaomi', 'acer', 'huawei', 'TP LINK', 'razer', 'kingston', 'tp-link', 'ibm', 'intel', 'nintendo', 'dell', 'hp', 'advance', 'gigabyte', 'msi', 'xpg', 'alienware', 'SENNHEISER', 'HIKVISION', 'logitech', 'EZVIZ', 'BEHRINGER', 'dji', 'sonos', 'baseus', 'fujifilm', 'aiwa', 'microsoft', 'canon', 'Bose', 'sole', 'Ninebot', 'skullcandy', 'jbl', 'TOSHIBA', 'primus', 'beats', 'sony', 'panasonic', 'motorola', 'tcl', 'hisense', 'apple', 'casio', 'oppo', 'vivo', 'epson', 'xgimi', 'corsair', 'DREIZT', 'blaupunkt', 'samsung', 'amazfit', 'wahl', 'carinositos', 'SCOSCHE', 'sandisk', 'samsung', 'samsung', 'go pro', 'gopro', 'oster', 'jvc', 'hp', 'epson', 'indurama', 'imaco', 'bosch', 'playstation']

if u >=50 and any(item.lower() == g.lower() for item in array):

    print("pasa")