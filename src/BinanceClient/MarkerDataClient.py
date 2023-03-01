import configparser
import requests

BASE_URL = "https://api.binance.com/api/v3/"

class MarkerDataClient:

    def __init__(self) -> None:
        self.endpoints = {'time': f'{BASE_URL}time',
                          'exchange_info': f'{BASE_URL}exchangeInfo?symbol=BNBBTC',
                          'depth' : f'{BASE_URL}depth?'
                         }
 
    def get_server_time(self) -> int:
        r = requests.get(self.endpoints['time'])
        if r.status_code == 200:
            return r.json()['serverTime']
        else:
            raise ValueError("Unexcepted error while fetching data")
        
    def get_exchange_info(self): # parse info 
        r = requests.get(self.endpoints['exchange_info'])
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError("Unexcepted error while fetching data")
        
    def get_order_book(self, symbol: str='BTCUSDT', limit: int=1):
        query_string = f"{self.endpoints['depth']}symbol={symbol}&limit={str(limit)}"
        print(query_string)
        r = requests.get(query_string)
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError("Unexcepted error while fetching data")


    

