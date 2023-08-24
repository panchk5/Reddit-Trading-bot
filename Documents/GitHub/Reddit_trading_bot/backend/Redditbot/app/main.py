import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.reddit.com/r/wallstreetbets/hot/"

chrome_options = Options()
chrome_options.add_argument("--headless")

# Set path to the chromedriver executable
chrome_driver_path = r"path"

# Create a new Chrome instance
driver = webdriver.Chrome(service=Service(chrome_driver_path))

# Navigate to the URL
driver.get(url)

# Wait for the table element to appear
table_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "2x-container"))
)

# Extract the HTML content of the table
table_html = table_element.get_attribute("innerHTML")

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(table_html, "html.parser")

# Find the specific div element within the table
t = soup.find("div", class_="_1UXMWx5AOkqbZJ00ctnRu")
table = t.find("table")
# Print the result

# Close the browser
driver.quit()

table_data = []

for row in table.find_all("tr"):
    row_data = []
    
    # Iterate through each cell in the row (td and th tags)
    for cell in row.find_all(["td", "th"]):
        # Get the stripped text content of the cell and add it to the row data
        cell_text = cell.get_text(strip=True)
        row_data.append(cell_text)
    
    # Add the row data to the table data
    table_data.append(row_data)

df = pd.DataFrame(table_data)
print(df)

ticker_list = []
x = 9
i = 0
while x != 0:
    x -= 1
    stock = [df.loc[i+1].at[0],df.loc[i+1].at[1]]
    ticker_list.append(stock)
    i += 1

y = 9 
j = 0 

while y != 0:
    y -= 1
    stock = [df.loc[j+1].at[7],df.loc[j+1].at[8]]
    ticker_list.append(stock)
    j += 1

total_votes = 0

for val in ticker_list:
    total_votes += int(val[1])

ticker_percentages = []

for val in ticker_list:
    stock_percent = [val[0],round((int(val[1]) / total_votes) * 100,2)]
    ticker_percentages.append(stock_percent)

print(ticker_percentages)

import alpaca_trade_api as tradeapi

api_key = "PKAI4GTFN5H2U9P1MYWC"
secret = "1Zr0NmxMfugVdloccntM0HGatOzwFPoRaF2EZ0NY"
base_url = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(api_key, secret, base_url, api_version='v2')

account = api.get_account()

print(f'Account ID: {account.id}')
print(f'Cash: ${account.cash}')

# use this only once so you don't spam many buy orders

def buy_all():
    cash = 90000
    for i in range(len(ticker_percentages)):
        try:
            max_budget = cash * (ticker_percentages[i][1] / 100)
            latest_price = api.get_latest_trade(ticker_percentages[i][0]).price
            quantity = int(max_budget / latest_price)
            order = api.submit_order(
                symbol=ticker_percentages[i][0],
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
        except:
            print("Ticker " + str(ticker_percentages[i][0]) + " does not exist.")
            continue

portfolio = api.list_positions()

def sell_all():
    for position in portfolio:
        symbol = position.symbol
        quantity = position.qty
        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='gtc'
        )

def refresh():
    sell_all()
    buy_all()

refresh()
