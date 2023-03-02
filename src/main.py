from BinanceClient.MarkerDataClient import MarkerDataClient

import requests


def main():
    if __name__ == "__main__":
        Client = MarkerDataClient('TEST', requests.get)
        obj =  Client.get_order_book()
        print(obj.asks)
    
            
main()