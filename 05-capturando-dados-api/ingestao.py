#%%
from abc import ABC, abstractmethod
import requests
import logging
import datetime
import json
from typing import List
import os
from schedule import repeat, every, run_pending
import time
from backoff import on_exception , expo
import ratelimit
#%%
# Teste para verificar se a api está funcionando
# print(requests.get("https://www.mercadobitcoin.net/api/BTC/day-summary/2022/2/2").json())

#%%
logger = logging.getLogger(__name__) #__name__ - retorna o nome do script que está sendo executado
logging.basicConfig(level=logging.INFO)

class MercadoBitcoinApi(ABC):

    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = "https://www.mercadobitcoin.net/api"
    
    # Metodo abstrato, não defino essa função e deixo com a responsabilidade para os filhos
    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass

    # Metodo para buscar os dados de fato
    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=29, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    

class DaySummaryApi(MercadoBitcoinApi):
    type = "day-summary"


    def _get_endpoint(self, date: datetime.date) -> str:
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"


class TradesApi(MercadoBitcoinApi):
    type = "trades"

    def _get_unix_epoch(self, date: datetime.datetime) -> int:
        return int(date.timestamp())
    
    def _get_endpoint(self, date_from: datetime.datetime = None, date_to: datetime.datetime = None) -> str:
        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}"
        elif date_from and date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to = self._get_unix_epoch(date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"

        return endpoint

class DataTypeNotSuppoetedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Data Type {type(data)} is not supported for ingestion"
        super().__init__(self.message)


class DataWriter():
    def __init__(self, coin: str, api: str) -> None:
        self.coin = coin
        self.api = api
        self.filename = f"{self.api}/{self.coin}/{datetime.datetime.now()}.json"
    
    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok = True)
        # insere os dados no modo append
        with open(self.filename, "a") as f:
            f.write(row)
    
    def write(self, data: [List, dict]):
        # isinstance verifica a classe do tipo data
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSuppoetedForIngestionException(data)

class DataIngestor(ABC):
    def __init__(self, writer: DataWriter, coins: List[str], default_start_date: datetime.date) -> None:
        self.coins = coins
        self.default_start_date = default_start_date
        self.writer = writer
        self._checkpoint = self._load_checkpoint()
    
    @property
    def _checkpoint_filename(self) -> str:
        return f"{self.__class__.__name__}.checkpoint"
        
    def _write_checkpoint(self):
        with open(self._checkpoint_filename, "w") as f:
            f.write(f"{self._checkpoint}")
    
    def _load_checkpoint(self) -> datetime.date:
        try:
            with open(self._checkpoint_filename, "r") as f:
                return datetime.datetime.strptime(f.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return None
            
    def _get_checkpoint(self):
        if not self._checkpoint:
            return self.default_start_date
        else:
            return self._checkpoint
        
    def _update_checkpoint(self, value):
        self._checkpoint = value
        self._write_checkpoint()
    
    @abstractmethod
    def ingest(self) -> None:
        pass

class DaysummaryIngestor(DataIngestor):
       
    def ingest(self) -> None:
        date = self._get_checkpoint()
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
            self._update_checkpoint(date + datetime.timedelta(days=1))
                
# print(DaySummaryApi(coin="BTC").get_data(date=datetime.date(2021,11, 5)))
# TradesApi(coin="BTC").get_data()
# TradesApi(coin="BTC").get_data(date_from=datetime.datetime(2021, 11, 2))
# print(TradesApi(coin="BTC").get_data(date_from=datetime.datetime(2021, 11, 2), date_to=datetime.datetime(2021, 11, 3)))
# Testando o Writer
# data = DaySummaryApi("BTC").get_data(date=datetime.date(2022, 3, 29))
# writer = DataWriter('day-summary.json')
# writer.write(data)

# data = TradesApi("BTC").get_data()
# writer = DataWriter('trades.json')
# writer.write(data)
# %%

ingestor = DaysummaryIngestor(writer = DataWriter, coins = ["BTC", "ETH", "LTC"], default_start_date=datetime.date(2021, 6, 2))
ingestor.ingest()

@repeat(every(1).seconds)
def job():
    ingestor.ingest()

while True:
    run_pending()
    time.sleep(0.5)