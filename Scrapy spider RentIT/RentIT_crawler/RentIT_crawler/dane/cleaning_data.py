import matplotlib.pyplot as plt 
import pandas as pd

path_to_file = "3flats_all.csv"

df = pd.read_csv(path_to_file)

df.columns

df.shape

df.info()

df.describe()



df.kategoria
df.liczba_pieter
df.rok_budowy
df.rodzaj_zabudowy
df.forma_wlasnosci


df.czynsz.plot('hist')
plt.show()
df.powierzchnia.plot('hist')
plt.show()







print(list(df.dzielnica.unique()))
print(list(df.rodzaj_zabudowy.unique()))
print(list(df.forma_wlasnosci.unique()))
print(list(df.czynsz.unique()))


print(max(df["czynsz"]))
print(max(df["cena_za_metr"]))
print(max(df["powierzchnia"]))




df.czynsz
df.rok_budowy
df.cena
df.liczba_pieter
df.nr_oferty_na_stronie
df.powierzchnia
df.rodzaj_zabudowy.unique()
df.pokoje.value_counts()



df = df[df.pokoje != "więcej niż 10"]
df = df[df.powierzchnia != 1047996]

df.pokoje = df.pokoje.astype(int)


df = df[(df.rok_budowy >= 1000) & (df.rok_budowy <= 2018)]



df.rok_budowy.value_counts()
df.rok_budowy.min()


df.rok_budowy = pd.to_numeric(df.rok_budowy,errors='coerce',downcast="signed")



plt.show()


dzielnice_prawidlowe=['Wola','Mokotów', 'Wesoła', 'Żoliborz', 'Ursynów', 'Włochy', 'Śródmieście','Praga-Południe',
                           'Wawer', 'Białołęka', 'Ochota', 
                           'Wilanów',  'Ursus', 'Bemowo', 'Bielany', 'Praga-Północ', 'Rembertów', 'Targówek']


df = df[df.dzielnica.isin(dzielnice_prawidlowe)]

print(df)

print(list(df["dzielnica"].unique()))



df.to_csv('output.csv', sep=',', encoding='utf-8-sig',index=False)


