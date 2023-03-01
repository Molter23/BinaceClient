from BinanceClient.MarkerDataClient import *


def main():
    if __name__ == "__main__":
        try: 
            server_time = MarkerDataClient.get_server_time('drivers')
            print(f"Server time: {server_time}")
        except ValueError as err:
            print("Handling run-time error: ", err)
            

main()