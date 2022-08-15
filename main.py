import csv
from os import getenv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

remote_host = getenv('REMOTE_HOST')
volume_path = getenv('VOLUME_PATH')

# wait for selenium container to start chrome
sleep(3)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# scrape ride data from rcdb
with open(f"{volume_path}/rides.csv", 'w') as f:
    writer = csv.writer(f, delimiter=',')
    with webdriver.Remote(remote_host, options=chrome_options) as wd:
        base_url = 'http://rcdb.com'
        
        for id in range(1, 100):
            wd.get(f"{base_url}/{id}.htm")
            
            feature_xpath = "//section[@id='objdiv']/div[@id='demo']/div[@id='feature']"
            name = wd.find_element(by=By.XPATH, value=f"{feature_xpath}/div/h1").text
            park = wd.find_element(by=By.XPATH, value=f"{feature_xpath}/div/a").text

            row = [id, name, park]
            writer.writerow(row)
