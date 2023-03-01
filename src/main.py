from BinanceClient.MarkerDataClient import MarkerDataClient

import requests


def main():
    if __name__ == "__main__":
        Client = MarkerDataClient('TEST', requests.get)
        obj =  Client.get_server_time()
        print(f"Server time: {obj}")
    
            

main()