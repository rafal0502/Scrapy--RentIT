import pandas as pd

path_to_file = "3flats_all.csv"

df = pd.read_csv(path_to_file)


df["kategoria"]
df["liczba_pieter"]
df["nr_oferty_na_stronie"]
df["rok_budowy"]

print(list(df["dzielnica"].unique()))

dzielnice_prawidlowe=['Wola','Mokotów', 'Wesoła', 'Żoliborz', 'Ursynów', 'Włochy', 'Śródmieście','Praga-Południe',
                           'Wawer', 'Białołęka', 'Ochota', 
                           'Wilanów',  'Ursus', 'Bemowo', 'Bielany', 'Praga-Północ', 'Rembertów', 'Targówek']

df = df[df.dzielnica.isin(dzielnice_prawidlowe)]

print(df)

print(list(df["dzielnica"].unique()))



df.to_csv('output.csv', sep=',', encoding='utf-8-sig',index=False)


