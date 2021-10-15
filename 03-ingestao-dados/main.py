#%%
# Imports
import requests
import json

#%%
url = 'https://economia.awesomeapi.com.br/last/USD-BRL'

ret = requests.get(url)


#%%
# Verificando se o retorno é 200
if ret:
    print(ret)
else:
    print('Falhou')
# %%
dolar = json.loads(ret.text)['USDBRL']

# %%
print(f"20 dolares hoje custam {float(dolar['bid'])*20} reais")
# %%
# Transformando processo de conexão com a API em um Função

def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(
        f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")


# %%
cotacao(20, 'USD-BRL')
cotacao(20, 'JPY-BRL')
# %%
# Testando uma chave que não existe
try:
    cotacao(20, 'Rhuan')
except:
    pass
# %%
try:
    cotacao(20, 'Rhuan')
except Exception as e:
    print(e)
else:
    print('ok')
# %%
def multi_moedas(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(
            f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")
# %%
lst_money = [
    'USD-BRL',
    'EUR-BRL',
    'BTC-BRL',
    'JPY-BRL',
    'RPL-BRL'
]

multi_moedas(20, 'USD-BRL')
# %%

def error_check(func):
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func

@error_check
def multi_moedas(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-','')]
    print(
            f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")



#%%
multi_moedas(20, 'USD-BRL')
multi_moedas(20, 'EUR-BRL')
multi_moedas(20, 'BTC-BRL')
multi_moedas(20, 'JPY-BRL')
multi_moedas(20, 'RPL-BRL')

# %%
import backoff
import random
# Criando uma função para simular um servidor
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=10)
def test_func(*args, **kargs):
    rnd = random.random()
    print(f"""
        RND: {rnd}
        args: {args if args else 'sem args'}
        kargs: {kargs if kargs else 'sem kargs'}
    """)
    if rnd < .2:
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        raise TimeoutError('Tempo de espera excedido')
    else:
        return "Ok!"
# %%
# Executando sem argumentos
test_func()
# %%
# Executando com um argumento
test_func(42)

# %%
# Executando com vários argumentos
test_func(42, 51, nome = 'Daniel')
# %%
import logging
log = logging.getLogger()
# Definindo o level de logs
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch saída padrão do log para o terminal
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)
# %%
@backoff.on_exception(backoff.expo, (ConnectionAbortedError, ConnectionRefusedError, TimeoutError), max_tries=10)
def test_func(*args, **kargs):
    rnd = random.random()
    log.debug(f"RND: {rnd}")
    log.info(f"args: {args if args else 'sem args'}")
    log.info(f"kargs: {kargs if kargs else 'sem kargs'}")
    if rnd < .2:
        log.error('Conexão foi finalizada')
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        log.error('Conexão foi recusada')
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        log.error('Tempo de espera excedido')
        raise TimeoutError('Tempo de espera excedido')
    else:
        return "Ok!"
# %%
test_func()

# %%
test_func(42)

# %%
