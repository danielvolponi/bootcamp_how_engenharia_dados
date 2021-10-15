#%%
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
# %%
url = 'https://www.vivareal.com.br/venda/parana/curitiba/apartamento_residencial/'
# %%
i = 1
ret = requests.get(url, params={"page": i})
soup = bs(ret.text)

# %%
soup
# %%
houses = soup.find_all('a', {'class': 'property-card__content-link js-card-title'})
qtd_imoveis = float(soup.find('strong', {'class': 'results-summary__count'}).text.replace('.',''))

# %%
len(houses)
# %%
qtd_imoveis
# %%
# Buscando os atributos de cada casa
house = houses[0]
# %%
house
#%%
descricao = house.find('span', {'class': 'property-card__title'}).text.strip()
endereco = house.find('span', {'class': 'property-card__address'}).text.strip()
area = house.find('span', {'class': 'property-card__detail-area'}).text.strip()
quartos = house.find('li', {'class': 'property-card__detail-room'}).span.text.strip()
wc = house.find('li', {'class': 'property-card__detail-bathroom'}).span.text.strip()
vagas = house.find('li', {'class': 'property-card__detail-garage'}).span.text.strip()
valor = house.find('div', {'class': 'property-card__price'}).p.text.strip()
condominio = house.find('strong', {'class': 'js-condo-price'}).text.strip()
wlink = 'https://www.vivareal.com.br' + house['href']

print(descricao)
print(endereco)
print(area)
print(quartos)
print(wc)
print(vagas)
print(valor)
print(condominio)
print(wlink)
#%%
# %%
# Criando um dataframe para armazenar informações do site
df = pd.DataFrame(
    columns=[
        'descricao',
        'endereco',
        'area',
        'quartos',
        'wc',
        'vagas',
        'valor',
        'condominio',
        'wlink'
    ]
)
i = 0
ret_headers = ret.headers
size = 0
data = {'from': size}
#%%
while qtd_imoveis > df.shape[0]:
    i += 1
    size += 36
    print(size)
    print(f"Valor de i: {i} \t\t Qtd. Imoveis: {df.shape[0]}")
    ret = requests.get(url, params={"page": i})
    # ret_headers = ret.headers
    # ret_cookies = ret.cookies
    soup = bs(ret.text)
    houses = soup.find_all('a', {'class': 'property-card__content-link js-card-title'})
    # print(url.format(i))
    # print(url.format(i-1))
    print(houses[0].find('span', {'class': 'property-card__title'}).text.strip())
    for house in houses:
        try:
            descricao = house.find('span', {'class': 'property-card__title'}).text.strip()
        except:
            descricao = None
        try:
            endereco = house.find('span', {'class': 'property-card__address'}).text.strip()
        except:
            endereco = None
        try:
            area = house.find('span', {'class': 'property-card__detail-area'}).text.strip()
        except:
            area = None
        try:
            quartos = house.find('li', {'class': 'property-card__detail-room'}).span.text.strip()
        except:
            quartos = None
        try:
            wc = house.find('li', {'class': 'property-card__detail-bathroom'}).span.text.strip()
        except:
            wc = None
        try:
            vagas = house.find('li', {'class': 'property-card__detail-garage'}).span.text.strip()
        except:
            vagas = None
        try:
            valor = house.find('div', {'class': 'property-card__price'}).p.text.strip()
        except:
            valor = None
        try:
            condominio = house.find('strong', {'class': 'js-condo-price'}).text.strip()
        except:
            condominio = None
        try:
            wlink = 'https://www.vivareal.com.br' + house['href']
        except:
            wlink = None

        df.loc[df.shape[0]] = [
            descricao,
            endereco,
            area,
            quartos,
            wc,
            vagas,
            valor,
            condominio,
            wlink]
 # %%
df[:70]
# %%
df.to_csv('banco_imoveis', sep=";", index=False)
# %%

# %%
