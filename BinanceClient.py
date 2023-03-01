import requests

class BinanceClient:

    @staticmethod
    def get_server_time(query: str) -> int:
        r = requests.get(f'https://api.binance.com/api/v3/time')
        if r.status_code == 200:
            return r.json()['serverTime']
        else:
            raise ValueError("Unexcepted error while fetching data")
    
