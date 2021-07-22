#      python 3.8
# -*- coding: utf-8 -*-
#          **
#         //\\
#   o==[=//==\\====>
#       **    **
#+++++++++++o++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
#       ^^*Trendy_Tweets*^^
#
# Autor:_<<Gabriel Oliveros>>_
#
# Obtiene las tendencias de Twitter, getdaytrends.com y las compila 
# El resultado se guarda en un archivo '.txt'
#+++++++++++o++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tweepy

print('Bienvenido. Lanzando Tweepy y obteniendo datos...')
print()

# Cadenas de autenticación (indica tus propias claves)
consumer_key = '' 
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# llamadas a la API de Twitter
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

''' 
Lista de WOEID solo para Venezuela

Venezuela:23424982 (por defecto)
Barcelona: 395273, Barquisimeto:468382, Caracas:,395269,
Ciudad Guayana:395275, Maracay:395271, Maturín:468384,
Turmero:395277,Valencia:395272, Maracaibo:395270

En otra aplicación te dejaré como obtener WOEID por país.
'''
t= open('tend_tweepy.txt','w')
trends = api.trends_place(23424982) #Cambia por el WOEID de tu elección
data = trends[0]
trends = data["trends"]
names = [trend["name"] for trend in trends]
trendsName = ", ".join(names)
t.write(trendsName)
t.close()
print('Se recolectaron {} tendencias con Tweepy'.format(len(names)))
print(trendsName)
print()
print()


# Raspado con Selenium
print('Lanzando Selenium y obteniendo datos de getdaytrends...')

chrome_path= r'C:\Users\x\Desktop\y\chromedriver.exe' #Sustituye por tu path 
driver= webdriver.Chrome(chrome_path)

driver.get('https://getdaytrends.com/es/venezuela/') #Sustituye por el país de tu elección

WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="trends"]/div/a'))).click()

trends = driver.find_elements_by_xpath("//div[@id='trends']/table//a")

tendencias= []
for t in trends:
    tend= t.get_attribute('text')
    tendencias.append(tend)
tendencias.sort()

while True:
    try:
        preg= int(input('¿Quieres unirlas con las tendencias de Tweeterium? (1.Sí 2.No): '))
    except ValueError:
        print('Solo puede introducir números (1 o 2)')
        continue
    if preg == 1:
        try:
            twt= open('tend_tweepy.txt')
        except FileNotFoundError:
            print('No existe el archivo "tendencias.txt". Se creará con las categorías existentes.')
            twt= open('tendencias.txt','w')
            for y in tendencias:
                twt.write(y + ', ')
            twt.close()
            print('Terminado sin compilación de Tweeterium. Adiós.')
            break
        
        nuevas= []
        for i in twt:
            pal= i.rstrip('\n')
            pal= pal.split(', ')
            for s in pal:
                if s not in tendencias:
                    nuevas.append(s)
                else:
                    continue    
        compilado= tendencias + nuevas
        compilado.sort()
        twt.close()
        twt2= open('tend_compilado.txt','w')
        for p in compilado:
            twt2.write(p + ', ')
        twt2.close()
        print(len(compilado),compilado)
        print('Terminado con compilación de Tweeterium. Adiós.')
        break
    
    elif preg == 2:
        twt= open('tend_getdaytrends.txt','w')
        for p in tendencias:
            twt.write(p + ', ')
        twt.close()
        print('Terminado sin compilar. Adiós.')
        break
       
    else:
        print('Debe introducir 1 o 2 como opción')
 
driver.quit()
