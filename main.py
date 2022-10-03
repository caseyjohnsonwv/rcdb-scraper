import csv
from os import getenv
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

remote_host = getenv('REMOTE_HOST')
volume_path = getenv('VOLUME_PATH')
dest_filename = getenv('DEST_FILENAME')

min_rcdb_id = int(getenv('MIN_ID'))
max_rcdb_id = int(getenv('MAX_ID')) + 1 #makes max inclusive
step = 10

# wait for selenium container to start chrome
sleep(3)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')


# create empty csv file
with open(f"{volume_path}/{dest_filename}", 'w') as f:
    pass

# scrape ride data from rcdb
with webdriver.Remote(remote_host, options=chrome_options) as wd:
    base_url = 'http://rcdb.com'
    demo_xpath = "//section[@id='objdiv']/div[@id='demo']"
    feature_xpath = f"{demo_xpath}/div[@id='feature']"
    
    # continually reopen file and append to reduce memory usage
    id = min_rcdb_id
    ride_id = min_rcdb_id
    while ride_id < max_rcdb_id:
        with open(f"{volume_path}/{dest_filename}", 'a') as f:
            writer = csv.writer(f, delimiter=',')
            for id in range(ride_id, ride_id + step):
                if id >= max_rcdb_id:
                    break
                
                print(f"id = {id}")
                wd.get(f"{base_url}/{id}.htm")

                # determine if this id is a ride ... if not, it could be lots of other things (park, person, etc), so skip it
                links = wd.find_elements(by=By.XPATH, value=f"{feature_xpath}/ul")[-1].text
                if 'parks nearby' in links.lower():
                    print(f"id = {id} is a park, not a ride")
                    continue

                # picture
                try:
                    data_url = wd.find_element(by=By.XPATH, value=f"{demo_xpath}/a").get_attribute('data-url')
                    picture_url = f"{base_url}{data_url}"
                except Exception:
                    print(f"Could not find picture for id = {id}")
                    picture_url = ''
                
                # ride name
                name = wd.find_element(by=By.XPATH, value=f"{feature_xpath}/div/h1").text

                # park name
                park = wd.find_element(by=By.XPATH, value=f"{feature_xpath}/div/a").text
                
                # year opened
                date_opened = wd.find_element(by=By.XPATH, value=f"{feature_xpath}/p/time").text
                year_opened = re.findall('\d{4}', date_opened)[0]

                # status
                status = wd.find_element(by=By.XPATH, value=f"{feature_xpath}/p").text
                status = re.split('[^\w+]', status, 1)[0] #take everything up to first non-alphanumeric character

                # manufacturer
                try:
                    manufacturer = wd.find_element(by=By.XPATH, value=f"{feature_xpath}/div[@class='scroll']/p/a").text #takes first match
                except Exception:
                    print(f"Could not find manufacturer for id = {id}")
                    manufacturer = ""

                # write to csv file
                row = [id, name, park, year_opened, manufacturer, status, picture_url]
                writer.writerow(row)

        # increment
        ride_id += step
