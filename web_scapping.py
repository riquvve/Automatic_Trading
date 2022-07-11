from webbrowser import Chrome
from xml.dom.minidom import Element
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager # my own
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import datetime

def xpath_element(xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        element = []
    return element

def real_time_price(stock_code):
    url = 'https://ca.finance.yahoo.com/quote/' + stock_code + '?p=' + stock_code + '&.tsrc=fin-srch'
    driver.get(url)
    
    ##################################################
    
    xpath = '//*[@id="quote-header-info"]/div[3]/div[1]/div[1]'
    stock_price_info = xpath_element(xpath)
    if stock_price_info != []:
        stock_price_temp = stock_price_info.text.split()[0]
        if stock_price_temp.find('+')!=-1:
            price = stock_price_temp.split('+')[0]
            try:
                change = '+' + stock_price_temp.split('+')[1] + ' ' + stock_price_info.text.split()[1]
            except IndexError:
                change = []
        elif stock_price_temp.find('-')!=-1:
            price = stock_price_temp.split('-')[0]
            try:
                change = '-' + stock_price_temp.split('-')[1] + ' ' + stock_price_info.text.split()[1]
            except IndexError:
                change = []
        else:
            price, change = [], []
    else:
        price, change = [], []
        
    ##################################################
    xpath = '//*[@id="quote-summary"]/div[1]'
    volume_temp = xpath_element(xpath)
    print(volume_temp.text.split())
    if volume_temp != []:
        #Approach 1 - volume = volume_temp.text.split()[-4]
        #Approach 2
        for i, text in enumerate(volume_temp.text.split()):
            if text == 'Volume':
                volume = volume_temp.text.split()[i+1]
                break
            else:
                volume = []
    else:
        volume = []
    ##################################################
    
    xpath = '//*[@id="quote-summary"]/div[2]'
    target_temp = xpath_element(xpath)
    print(target_temp.text.split())
    if target_temp != []:
        for i, text in enumerate(target_temp.text.split()):
            if text == 'Est':
                if target_temp.text.split()[i+1] != 'N/A':
                    one_year_target = target_temp.text.split()[i+1]
                else:
                    one_year_target= []
                break
            else:
                one_year_target = []
    else:
        one_year_target = []
    
    latest_pattern = []
    return price, change, volume, latest_pattern, one_year_target
    ##################################################
    
    

chrome_options = Options()
chrome_options.add_argument("--headless") # not show the chrome window
PATH = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(PATH, options=chrome_options)

price, change, volume, latest_pattern, one_year_target = real_time_price('BRK-B')

Stock = ['BRK-B', 'PYPL', 'TWTR', 'AAPL', 'AMZN', 'MSFT', 'FB',  'GOOG']

while(True):
    info = []
    time_stamp = datetime.datetime.now()
    time_stamp = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
    
    for stock_code in Stock:
        price, change, volume, latest_pattern, one_year_target = real_time_price(stock_code)
        info.append(price)
        info.extend([change])
        info.extend([volume])
        info.extend([latest_pattern])
        info.extend([one_year_target])
        
    col = [time_stamp]
    col.extend(info)
    df = pd.DataFrame(col)
    df = df.T
    
    df.to_csv(time_stamp[0:11] + 'stock data.csv', mode = 'a', header=False)
    print(col)
    
driver.quit()