import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

URL = "https://www.reddit.com/r/wallstreetbets/hot/"
driver = webdriver.Chrome("C:/Users/krish/Downloads/chrome-win64")
page = driver.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="2x-container")

result = results.find("div", class_="md")
print(result)

