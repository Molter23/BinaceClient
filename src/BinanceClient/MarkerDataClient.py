import configparser
import requests
import logging

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


class AveragePrice:

    def __init__(self, time_interval: int, price: float):
        self.time_interval = time_interval
        self.price = price


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
            raise BadRequestError("ERROR 400 - check request arguments")
        case 401: # require autorization
            raise UnauthorizedError("ERROR 401 - requiere autorization")
        case 403: # permisson 
            raise PermisionError("ERROR 403 - permission require")
        case 404: # data doesn't exist 
            raise NotFoundError("ERROR 404 - data not found")
        case 408: # Timeout
            raise TimeourError("ERROR 408 - took to long to respond")
        case _:
            raise Exception(f"ERROR {error_code}")



class MarkerDataClient:
    def __init__(self, env: str, get_func: Callable[[str], requests.models.Response]) -> None:
        config = Config()
        pass
        BASE_URL = config.get_url(env)
        self.request = get_func
        self.endpoints = {'time': f'{BASE_URL}time',
                          'depth': f'{BASE_URL}depth?',
                          'avg_price': f'{BASE_URL}avgPrice?' 
                         }


    def get_server_time(self) -> int|None:
        r = self.request(self.endpoints['time'])
        try:
            validate_response_code(r.status_code)
        except (BadRequestError, UnauthorizedError, PermisionError, NotFoundError, TimeourError) as error:
            print(error)
            return None
      
        return r.json()['serverTime']

    def get_average_price(self, symbol: str='BTCUSDT') -> AveragePrice:
        query_string = f"{self.endpoints['avg_price']}symbol={symbol}"
        r = self.request(query_string)
        try:
            validate_response_code(r.status_code)
        except (BadRequestError, UnauthorizedError, PermisionError, NotFoundError, TimeourError) as error:
            # should be error log 
            return None
        
        return AveragePrice(r.json()['mins'],  r.json()['price'])
        
     
    def get_order_book(self, symbol: str='BTCUSDT', limit: int=1): # parse info
        query_string = f"{self.endpoints['depth']}symbol={symbol}&limit={str(limit)}"
        r = self.request(query_string)
        try:
            validate_response_code(r.status_code)
        except (BadRequestError, UnauthorizedError, PermisionError, NotFoundError, TimeourError) as error:
            # should be error log 
            return None
        
        return r.json() 

