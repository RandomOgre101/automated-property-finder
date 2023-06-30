from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests



URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.70318068457031%2C%22east%22%3A-122.16347731542969%2C%22south%22%3A37.61800196820298%2C%22north%22%3A37.93224701381495%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
headers = {
    'User-Agent': --,
    'Accept-Language': --
}

response = requests.get(url=URL, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

links_raw = soup.find_all(class_='property-card-link')
links_all = [x.get('href') for x in links_raw]
links_dup = []

for link in links_all:
    if(link[0] != 'h'):
        link2 = 'https://www.zillow.com'+link
        links_dup.append(link2)
    else:
        links_dup.append(link)

links=[]
[links.append(x) for x in links_dup if x not in links]

address_raw = soup.find_all(name='address')
addresses = [x.getText() for x in address_raw]

price_raw = soup.find_all('span', attrs={'data-test': 'property-card-price'})
prices = [x.getText()[0:6] for x in price_raw]


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, service=Service(executable_path="C:\Development\chromedriver.exe", log_path="NUL"))

for i in range(0, len(prices)):
    driver.get('https://docs.google.com/forms/d/e/1FAIpQLSe9FVt-SiRXEbqeZ7Cxc_Rfdxdc3sABjYV4Rx73moLWJi3vbg/viewform?usp=sf_link')
    time.sleep(1)

    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(addresses[i])

    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(prices[i])

    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(links[i])

    submit_btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_btn.click()

driver.close()

