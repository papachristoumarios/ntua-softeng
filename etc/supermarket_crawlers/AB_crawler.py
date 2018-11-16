#!/usr/bin/env python3
# Crawler for gathering data from supermarkets
# Usage: ./AB_crawler.py <path-to-chromedriver-executable>

import sys
import os
import urllib.request
import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotVisibleException
import time

def crawl_category(driver, category_name, category_url, download_images=False, all_details=False, nsamples=None, download_descriptions=False):
    driver.get(category_url)
    print('Processing', category_name)
    # Close privacy policy
    modals = driver.find_elements_by_class_name("js-modal-close")
    for b in modals:
        try:
            b.click()
        except:
            continue

    # Infinite Scroll
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    products = driver.find_elements_by_class_name('data-item')

    if nsamples == None:
        nsamples = len(products)

    try:
        os.mkdir(category_name)
    except:
        pass
    finally:
        f = open(category_name + '/data.csv', 'w+')

    if download_images:
        try:
            os.mkdir(category_name + '/images')
        except:
            pass

    data = []
    hrefs = []

    for i, p in enumerate(products[:nsamples]):
        contents = p.text.splitlines()
        href = p.find_element_by_class_name('ProductShot').get_attribute('href')
        if not all_details:
            name = contents[0]
            for field in contents:
                if field.startswith('€'):
                    price = field.strip('€').replace(',', '.')
                    break
            contents = [name, price]
        hrefs.append(href)
        data.append(contents)

        if download_images:
            try:
                img_url = p.find_element_by_tag_name('img').get_attribute('src')
                urllib.request.urlretrieve(img_url, '{}/images/{}.jpg'.format(category_name, i))
            except:
                pass

    if download_descriptions:
        for i, href in enumerate(hrefs[:nsamples]):

            driver.get(href)
            try:
                description = driver.find_element_by_class_name('is-open').find_element_by_class_name('content').text
            except:
                try:
                    [x.click() for x in driver.find_elements_by_class_name('accordion-item')]
                    description = driver.find_element_by_class_name('is-open').find_element_by_class_name('content').text
                except:
                    continue
            description = description.replace('\n', ' ').strip('Περιγραφή').split('Αναγνωριστικό:')
            description = [x.lstrip().rstrip() for x in description]
            data[i].extend(description)
            time.sleep(0.5)


    for d in data:
        f.write(', '.join(d) + '\n')

    f.close()

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(sys.argv[1], chrome_options=options)

    categories = {
        'Γαλακτοκομικά-και-Είδη-Ψυγείου' : 'https://www.ab.gr/GALAKTOKOMIKA-%26-EIDI-PsYGEIOY/c/003',
        'Έτοιμα-Γεύματα' : 'https://www.ab.gr/ETOIMA-GEYMATA/c/007',
        'Ποτά' : 'https://www.ab.gr/KRASIA%2C-POTA%2C-ANAPsYKTIKA%2C-NERA/c/008',
        'Κατεψυγμένα' : 'https://www.ab.gr/click2shop/KATEPsYGMENA-TROFIMA/c/005',
        'Είδη-Άρτου' : 'https://www.ab.gr/ARTOZAChAROPLASTEIO/c/006',
        'Τυποποιημένα-Τρόφιμα' : 'https://www.ab.gr/VASIKA-TYPOPOIIMENA-TROFIMA/c/010',
        'Είδη-Σπιτιού' : 'https://www.ab.gr/click2shop/KAThARISTIKA---ChARTIKA-%26-EIDI-SPITIOY/c/013',
        'Είδη-Πρωινού' : 'https://www.ab.gr/click2shop/PROINO---SNACKING-%26-ROFIMATA/c/009',
        'Είδη-Προσωπικής-Περιποίησης' : 'https://www.ab.gr/click2shop/EIDI-PROSOPIKIS-PERIPOIISIS/c/012'
    }

    for category_name, category_url in categories.items():
        crawl_category(driver, category_name, category_url, download_images=True, download_descriptions=True)
