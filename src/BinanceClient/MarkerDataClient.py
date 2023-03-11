import configparser
import requests
import logging
from pydantic import BaseModel

from typing import Optional
from collections.abc import Callable

class Config:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('API.ini')
        self.config = config
        
        
    def get_url(self, env: str) -> str:
        if(env == 'TEST'):
            return self.config['TEST']['URL']
        elif(env =='PROD'):
            return self.config['PROD']['URL']
        else:
            raise NameError('There is no URL defined for this environment')


class AveragePrice(BaseModel):
    mins: int
    price: float

class OrderBook(BaseModel):
    lastUpdateId: int
    bids: list[list[float]]
    asks: list[list[float]]
    

class MarkerDataClient:
    def __init__(self, env: str, get_func: Callable[[str], requests.models.Response]) -> None:
        config = Config()
        pass
        BASE_URL = config.get_url(env)
        self.request = get_func
        self.endpoints = {'time': f'{BASE_URL}time',
                          'depth': f'{BASE_URL}depth?',
                          'avg_price': f'{BASE_URL}avgPrice?',
                          'symbol_price': f'{BASE_URL}ticker/price?'
                         }
    

    def make_request(self, query_string: str) -> requests.models.Response:
        response = self.request(query_string)
        try:
            validate_response_code(response.status_code)
        except (BadRequestError, UnauthorizedError, PermisionError, NotFoundError, TimeourError) as error:
            logging.error(error)
            return None
        
        return response
    
    def tranform_order_book(self, data: requests.models.Response) -> OrderBook:
        for i, bid in enumerate(data['bids']):
            for j, value in enumerate(bid):
                data['bids'][i][j] = float(value)

        for i, bid in enumerate(data['asks']):
            for j, value in enumerate(bid):
                data['asks'][i][j] = float(value)

        return OrderBook(**data)
      


    def get_server_time(self) -> Optional[int]:
        query_string = self.endpoints['time']
        r = self.make_request(query_string)
      
        return r.json()['serverTime']

    def get_average_price(self, symbol: str='BTCUSDT') -> AveragePrice:
        query_string = f"{self.endpoints['avg_price']}symbol={symbol}"
        r = self.make_request(query_string)  
        data = r.json() 
        return AveragePrice(**data)
        
     
    def get_order_book(self, symbol: str='BTCUSDT', limit: int=2) -> OrderBook:
        query_string = f"{self.endpoints['depth']}symbol={symbol}&limit={str(limit)}"
        r = self.make_request(query_string)      
        return self.tranform_order_book(r.json())
    
    def get_price(self, symbol: str='BTCUSDT'):
        query_string = f"{self.endpoints['symbol_price']}symbol={symbol}"
        r = self.make_request(query_string)      
        return r.json()



class BadRequestError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class PermisionError(Exception):
    pass

class NotFoundError(Exception):
    pass

class TimeourError(Exception):
    pass 

def validate_response_code(error_code: int) -> None: 
    match error_code:
        case 200:
            pass
        case 400: # autentication error
            raise BadRequestError("400 - check request arguments")
        case 401: # require autorization
            raise UnauthorizedError("401 - requiere autorization")
        case 403: # permisson 
            raise PermisionError("403 - permission require")
        case 404: # data doesn't exist 
            raise NotFoundError("404 - data not found")
        case 408: # Timeout
            raise TimeourError("408 - took to long to respond")
        case _:
            raise Exception(f"{error_code}")