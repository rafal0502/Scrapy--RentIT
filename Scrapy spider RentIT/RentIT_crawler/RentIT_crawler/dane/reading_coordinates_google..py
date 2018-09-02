import json
from pygeocoder import Geocoder
import pandas as pd
import numpy as np
import urllib.request
from geopy.geocoders import GoogleV3



filePath= "C:\\Users\\rafal\\Desktop\\GitHub\\Scrapy- RentIT\\Scrapy spider RentIT\\RentIT_crawler\\RentIT_crawler\\dane\\mieszkania_all.json"
df = pd.read_json(filePath,encoding="UTF-8")

df['wspolrzedne'] = df['wspolrzedne_lat'].astype(str) + ', ' + df['wspolrzedne_lon'].astype(str)



keys=["AIzaSyDRFkot3gFl0tipc4k0HgFspBmsxSYXmpg","AIzaSyB-9Jqhdad3WLpUkTLz3Pr5lHE0XupkWXs","AIzaSyA7bNphNbaT09TdQzJTPQveE5xPro2vnM8","AIzaSyCFiKWzhwKwFQ2Nyu73UQeVtFZQuF91D94",
      "AIzaSyCN8CzVeS08mu2z32ZeSb_NFpXFxYlJUvk","AIzaSyAp6VrylQxjS-ld8pN1OBfGPS7DBYgZ4qQ","AIzaSyD4N9A_wBaQLP8NPEkeqGTctU082jV-ZN4","AIzaSyCRhM6u5yuYLOBzljtAZRR1aj5lc_yZBjw",
      "AIzaSyA_rIyTkGfiPY7-oED206k3daL_ETw-QX8"]


import random
from pandas.io.json import json_normalize
import googlemaps



df["dzielnica"] = "brak"

print("Zaczynamy!")

for i in range(0, len(df)):
    gmaps_key=googlemaps.Client(key=random.choice(keys))
    try:
        df["dzielnica"][i] = gmaps_key.reverse_geocode(df['wspolrzedne'][i])[0]['address_components'][2]['long_name']
        print("Sukces",i)
    except:
        df["dzielnica"][i] = None
        print("Blad")


data_frame = pd.DataFrame(data=df)

values= data_frame["dzielnica"].value_counts()
print(values)


try:
    data_frame.to_json('Scrapy_flats_all.json',orient="index")
    data_frame.to_csv('Scrapy_flats_all.csv', sep=',', encoding='utf-8')
except:
    print("Blad")


