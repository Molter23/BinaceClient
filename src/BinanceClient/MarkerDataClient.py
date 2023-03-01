import configparser
import requests

class Config:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('API.ini')
        self.config = config
        
    def get_url(self):
        return self.config['TEST']['URL']
        


class MarkerDataClient:

    def __init__(self) -> None:
        config = Config()
        BASE_URL = config.get_url()
       
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
        r = requests.get(query_string)
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError("Unexcepted error while fetching data")


    

