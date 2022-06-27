#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import sys
import time
from webdriver_manager.chrome import ChromeDriverManager


# %%
cep = sys.argv[1]

if cep:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver = webdriver.Chrome('./src/chromedriver')
    # %%
    # Acessando o site da How
    # driver.get('https://howedu.com.br/')
    # driver.find_element_by_xpath('//*[@id="onesignal-slidedown-cancel-button"]').click()
    # driver.find_element(by = By.XPATH, value='//*[@id="menu-1-739815d"]/li[2]/a').click()

    # %%
    driver.get('https://buscacepinter.correios.com.br/app/endereco/index.php?t')
    elem_cep = driver.find_element(by = By.ID, value = 'endereco')
    elem_cmb = driver.find_element(by = By.NAME, value = 'tipoCEP')
    #%%
    elem_cep.clear()
    elem_cep.send_keys(cep)
    elem_cmb.click()
    # driver.find_element(by = By.XPATH, value='//*[@id="formulario"]/div[2]/div/div[2]/select/option[6]').click()

    # %%
    driver.find_element(by = By.ID, value = 'btn_pesquisar').click()
    time.sleep(1)
    # %%
    logradouro = driver.find_element(by = By.XPATH, value='//*[@id="resultado-DNEC"]/tbody/tr/td[1]').text
    logradouro = logradouro.split(' - ')[0]
    bairro = driver.find_element(by = By.XPATH, value='//*[@id="resultado-DNEC"]/tbody/tr/td[2]').text
    localidade = driver.find_element(by = By.XPATH, value='//*[@id="resultado-DNEC"]/tbody/tr/td[3]').text
    # %%
    driver.close()
    print("""
    Para o CEP {} temos: 
    Endereço: {}
    Bairro: {}
    Localidade: {}
    """.format(cep, logradouro, bairro, localidade))
# %%
