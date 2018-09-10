#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 18:53:24 2018

@author: zibski
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import smtplib
    
    
#Otwórz strone LUX MED
driver = webdriver.Firefox()
driver.get("https://portalpacjenta.luxmed.pl")

try:
    myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'Login')))
    print("Driver gotowy, strona otwarta!")
except TimeoutException:
    print("Error: Timeout.")

#warto dodać assert

def send_email(FROM, TO, SUBJECT, TEXT):
    
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, TO, SUBJECT, TEXT)
    
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(get_credentials(login)[0], get_credentials(login)[1])
    server.sendmail(FROM, TO, message)
    server.close()
    print('\nEmail został wysłany.')

def get_credentials(file_name):
    f = open('login', 'r')
    x = f.read().split('\n')
    f.close()
    return x

#Zaloguj się do systemu
login = driver.find_element_by_name("Login")
login.clear()
login.send_keys(get_credentials(login)[2])
pswrd = driver.find_element_by_id("TempPassword")
pswrd.clear()
driver.execute_script(str.format("document.getElementById('Password').value='{0}';",get_credentials(login)[3]))
driver.find_element_by_class_name("button.large.green").click()

#Po drodze będzie pytanie o aktualizacje danych

#Wejdź do zakładki z wizytami
driver.find_element_by_class_name("button.accept.calendar.bg-green").click()
time.sleep(1)
driver.find_element_by_xpath('//*[@class="activity_button btn btn-default" and @datacategory="Pozostałe usługi"]').click()
time.sleep(3)
#Wprowadź parametry wyszukiwania
#wprowadź miasto
driver.find_element_by_class_name("column.column1").find_element_by_class_name("caption").click()
driver.find_element_by_class_name("search-select").send_keys("Warszawa")
#driver.find_element_by_class_name("search-select").send_keys(Keys.RETURN)
driver.find_element_by_xpath('//*[@data-value="1"]').click()
#Wprowadź rodzaj badania
time.sleep(1)
driver.find_element_by_class_name("column.column2").find_element_by_class_name("caption").click()
driver.find_element_by_class_name("search-select").send_keys("Konsultacja neurologa - dzieci")
driver.find_element_by_xpath('//*[@data-value="7056"]').click()
el = driver.find_element_by_id("__selectOverlay")

action = webdriver.common.action_chains.ActionChains(driver)
action.move_to_element_with_offset(el, 5, 5)
action.click()
action.perform()

#Wprowadź dane lekarza
time.sleep(1)
driver.find_element_by_class_name("column.column2").find_element_by_xpath('(//*[@class="_select widget undefined"])[4]').click()
driver.find_element_by_class_name("search-select").send_keys("Malinowska")
driver.find_element_by_xpath('//*[@data-value="17252-7056-0"]').click()
action.perform()
#wyszukaj
driver.find_element_by_id("reservationSearchSubmitButton").click()


try:
    while driver.find_element_by_class_name("noReservationResultInfo"):
        print("nie znaleziono szukanych wyników, podejme próbę za 1 minute")
        time.sleep(60)
        driver.find_element_by_id("reservationSearchSubmitButton").click()
except NoSuchElementException:
    print('\nZnaleziono termin szukanej wizyty, wysyłam maila...')
    FROM = 'z.fortunski@gmail.com'
    TO = 'z.fortunski@gmail.com'
    SUBJECT = '!!! WOLNY TERMIN !!!'
    TEXT = 'Neurolog dzieciecy - Malinowska'
    send_email(FROM, TO, SUBJECT, TEXT)