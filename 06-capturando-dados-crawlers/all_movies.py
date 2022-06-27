#%%
from opcode import opname
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

#%%
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
time.sleep(5)
# Timer para ele aguardar por padrão
driver.implicitly_wait(10)
driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')
tabela = driver.find_element(
    by = By.XPATH, 
    value = '//*[@id="mw-content-text"]/div[1]/table[2]'
).get_attribute('innerHTML')
# driver.close()
# print(tabela)
#%%
with open('print.png', 'wb') as f:
    f.write(driver.find_element(by = By.XPATH, value = '/html/body/div').screenshot_as_png)

#%%


test_path = '//*[@id="mw-content-text"]/div[1]/table[2]'
#%%
def tem_item(xpath, driver = driver):
    try: 
        driver.find_element(by = By.XPATH, value = xpath)
        return True
    except:
        return False
    
#%%
if tem_item(test_path):
    print('Ok')

driver.close()

# %%
df = pd.read_html("<table>" + tabela + "</table>")[0]
df.to_csv("filmes_nicolas_cage.csv", sep = ";", index=False)