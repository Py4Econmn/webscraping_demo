# pip install selenium
# chromium driver: https://googlechromelabs.github.io/chrome-for-testing/

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
# chrome_options.add_argument("--headless") # do not open browser

driver = webdriver.Chrome(options=chrome_options) # open chrome, name the object as driver

# browse BoM home page
bom_main_page = "https://www.mongolbank.mn/mn"
driver.get(bom_main_page)

policy_rate = driver.find_element(By.XPATH,'/html/body/main/section[2]/div/div[1]/div/div/div/div/a/h2').text
usd_rate    = driver.find_element(By.XPATH,'/html/body/main/section[2]/div/div[3]/div/div/a[1]/div/div[3]').text

# multiple elements
usd_rate_info    = driver.find_elements(By.XPATH,'//*[@id="app"]/main/section[2]/div/div[3]/div/div/a[1]/div/div')
usd_rate = usd_rate_info[2].text
usd_date = usd_rate_info[3].text
usd_label = usd_rate_info[1].text
usd_flag = usd_rate_info[0].text

# sub element search
fx_info    = driver.find_element(By.XPATH,'//*[@id="app"]/main/section[2]/div/div[3]')
usd_rate = fx_info.find_element(By.XPATH,'div/div/a[1]/div/div[3]').text


## Loop through exchange rates
daily_fx_page = "https://www.mongolbank.mn/mn/currency-rate"
driver.get(daily_fx_page)

all_rates_path = '//*[@id="page_currency_rate"]/div/div[1]/article/div[1]/div[2]/div' 
all_rates = driver.find_elements(By.XPATH, all_rates_path)                      
rates_list = []

for i in range(len(all_rates)):
    rate = all_rates[i].find_element(By.XPATH,"div/div[2]/div/div[2]/div[1]").text # A fx rate
    rate_en = all_rates[i].find_element(By.XPATH,"div/div[2]/div/div[1]/div[1]/strong").text 
    rate_mn = all_rates[i].find_element(By.XPATH,"div/div[2]/div/div[1]/div[2]").text # MN long description of FX code
    print(rate,rate_mn,rate_en, i)
    rates_list.append([rate,rate_mn,rate_en])


# export to excel
df = pd.DataFrame(rates_list, columns=['Rate', 'MN', 'EN'])
df['Rate'] = pd.to_numeric(df['Rate'].str.replace(',',''))
df.to_excel('result/bom_rate.xlsx', index=False)


# Daily rate
driver.get(daily_fx_page)
driver.find_element(By.XPATH,'//*[@id="page_currency_rate"]/div/div[1]/article/ul/li[2]/a').click() # switch to historical rate panel

# text insert
def clean_insert(driver, xpath, message):
    # when not empty, the box brings back the old date even after deleting, so need to clear twice with click in between
    driver.find_element(By.XPATH, xpath).clear()
    driver.find_element(By.XPATH, xpath).click()
    driver.find_element(By.XPATH, xpath).clear()
    driver.find_element(By.XPATH, xpath).send_keys(message)

# start date
xpath = '//*[@id="page_currency_rate"]/div/div[1]/article/div[2]/div[3]/div[1]/div/div/input'
message = "2024-01-01"
clean_insert(driver, xpath, message)

# end date
xpath = '//*[@id="page_currency_rate"]/div/div[1]/article/div[2]/div[3]/div[2]/div/div/input'
message = "2024-05-19"
clean_insert(driver, xpath, message)

# button 
driver.find_element(By.XPATH, '//*[@id="page_currency_rate"]/div/div[1]/article/div[2]/div[3]/div[3]/button[1]').click()


### Additional

# multiple tabs
driver.execute_script('''window.open();''')

# switch between tabs
driver.switch_to.window(driver.window_handles[0])
driver.switch_to.window(driver.window_handles[3])
driver.switch_to.window(driver.window_handles[1])
driver.switch_to.window(driver.window_handles[2])
driver.switch_to.window(driver.window_handles[-1])

driver.get(daily_fx_page)
driver.maximize_window()

# navigating history
driver.back()      # previous page in browser history
driver.forward()   # next page in browser history

## Other attributes 
# find by tag name 
h1 = driver.find_element(By.TAG_NAME,"h1")
print(h1.text)
h1 = driver.find_elements(By.TAG_NAME,"h1")
print(h1[0].text)

span1 = driver.find_element(By.TAG_NAME,"span")

spans = driver.find_elements(By.TAG_NAME,"span")
print(spans[0].text)
print(spans[1].text)

# find by css selector - Inspect, Copy, Copy Selector 
header_date = driver.find_element(By.CSS_SELECTOR,"#page_currency_rate > div > div.col-12.col-lg-9.mt-4 > article > h1") 
print(header_date.text) 

# Attributes
# Хайх товчлуурын attributes-ыг харах //*[@id="header"]/div/form/input
driver.find_element(By.XPATH,'//*[@id="header"]/div/form/input').get_attribute("type")
driver.find_element(By.XPATH,'//*[@id="header"]/div/form/input').get_attribute("name")
driver.find_element(By.XPATH,'//*[@id="header"]/div/form/input').get_attribute("class")
driver.find_element(By.XPATH,'//*[@id="header"]/div/form/input').get_attribute("placeholder")


driver.get(daily_fx_page)

# Элемент доторх утгаар хайх
driver.get(daily_fx_page)
found = driver.find_element(By.XPATH,"//*[contains(text(), 'Швед')]").text
found = driver.find_element(By.XPATH,"//*[contains(text(), 'хаалтын')]").text
found = driver.find_elements(By.XPATH,"//*[contains(text(), 'зарласан')]")[8].text

# find by link_text
rate_link = driver.find_element(By.LINK_TEXT,"Түүхэн ханш")
rate_link.click()
rate_link = driver.find_element(By.LINK_TEXT,"Өдрийн хаалтын ханш")
rate_link.click()

driver.get(daily_fx_page)
# find by partial_link_text
rate_link = driver.find_element(By.PARTIAL_LINK_TEXT,"хаалтын")
rate_link.click()

# enter value to input box and search //*[@id="header"]/div/form/input
driver.get(bom_main_page)
driver.find_element(By.CLASS_NAME, "form-control").send_keys("бодлогын хүү") 
driver.find_element(By.CLASS_NAME, "form-control").send_keys(Keys.ENTER)

driver.quit()