from geopy.geocoders  import Nominatim
import pandas as pd
import numpy as np
import urllib.request
from geopy.geocoders import GoogleV3


geolocator = Nominatim()
filePath= "C:\\Users\\rafal\\Desktop\\GitHub\\Scrapy- RentIT\\Scrapy spider RentIT\\RentIT_crawler\\RentIT_crawler\\dane\\mieszkania_z_dzielnicami.json"
df = pd.read_json(filePath,encoding="UTF-8")
df['wspolrzedne'] = df['wspolrzedne_lat'].astype(str) + ', ' + df['wspolrzedne_lon'].astype(str)



df["dzielnica"] = "brak"

print("Zaczynamy!")
for i in range(0, len(df)):
    try:
        df["dzielnica"][i] = geolocator.reverse(df['wspolrzedne'][i]).raw['address']['suburb']
    except:
        print("Blad")




data_frame = pd.DataFrame(data=df)
data_frame.to_json('Mieszkania_z_dzielnicami.json',orient="index")


data_frame = pd.DataFrame(data=df)    

while True:
    try:
        data_frame.to_json('Mieszkania_z_dzielnicami.json',orient="series")
    except:
        print("Blad json")
        break
    else:
        print("To wszystko")
        break






