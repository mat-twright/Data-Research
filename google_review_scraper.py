
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

###export PATH=$PATH:/Users/School/Desktop/expression
###python google_review_scraper.py


#https://www.google.com/maps/search/?api=1&query=Google&query_place_id=ChIJ--og4A_yeEgRjisQX6e3eGc


def scrape_reviews(id, name):
    path = name.lower().replace(' ', '_')

    driver = webdriver.Firefox()


    #url = 'https://www.google.co.uk/maps/place/RUN/@50.8310487,-0.196608,14z/data=!4m11!1m2!2m1!1sRUN+near+Hove!3m7!1s0x4875854f21dc23df:0x79237306f12c5b27!8m2!3d50.8313269!4d-0.1751212!9m1!1b1!15sCg1SVU4gbmVhciBIb3ZlWg8iDXJ1biBuZWFyIGhvdmWSAQ1ydW5uaW5nX3N0b3JlmgEjQ2haRFNVaE5NRzluUzBWSlEwRm5TVVJST0MxNk9GUm5FQUU'
    #url = 'https://www.google.co.uk/maps/place/FOURTH+AND+CHURCH/@50.827608,-0.1728357,17z/data=!3m1!4b1!4m5!3m4!1s0x4875854635f8feb3:0x68d6126b37d87e69!8m2!3d50.827608!4d-0.170647'
    url = 'https://www.google.com/maps/search/?api=1&query=Google&query_place_id=' + id
    driver.get(url)




    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button').click()#to make sure content is fully loaded we can use time.sleep() after navigating to each page

    time.sleep(3)

    driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span[1]/span[2]/span[1]/button').click()

    time.sleep(3)

    i = 0
    #Find the total number of reviews
    total_number_of_reviews = driver.find_element(By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]').text.split(" ")[0]
    total_number_of_reviews = int(total_number_of_reviews.replace(',','')) if ',' in total_number_of_reviews else int(total_number_of_reviews)#Find scroll layout
    scrollable_div = driver.find_element(By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]')#Scroll as many times as necessary to load all reviews
    for i in range(0,(round(total_number_of_reviews/10 - 1))+5):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',
                    scrollable_div)
            more_buttons = driver.find_elements(By.CLASS_NAME, 'w8nwRe.gXqMYb-hSRGPd')
            try:
                for b in more_buttons: b.click()
            except:
                i += 1
            time.sleep(2)

    print('####I = {}'.format(i))


    response = BeautifulSoup(driver.page_source, 'html.parser')

    response.find()

    f = open('t.txt', 'w')
    #r = response.get_text('\n')
    f.write(response.prettify())
    f.close()

    ratings = response.find_all(class_="ODSEW-ShBeI-H1e3jb")
    RATINGS = [str(x)[19] for x in ratings]



    texts = response.find_all(class_='ODSEW-ShBeI-ShBeI-content')
    TEXTS = []
    for i in texts:
        try:
            TEXTS.append(str(i).split('">')[-1].replace('\n', '//'))
        except:
            TEXTS.append('No text for review')
    print(len(texts), len(TEXTS))



    dates = response.find_all(class_='ODSEW-ShBeI-RgZmSc-date')
    DATES = [str(x).split('">')[-1][:-6].replace('\n', '').replace('<','').replace('  ', '') for x in dates]



    f =  open(path + '.tsv', 'w')
    for i in range(len(RATINGS)): f.write(DATES[i] + '\t' + RATINGS[i] + '\t' + TEXTS[i] +'\n')
    f.close()
