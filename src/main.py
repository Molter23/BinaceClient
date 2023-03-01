from BinanceClient.MarkerDataClient import MarkerDataClient


def main():
    if __name__ == "__main__":
        Client = MarkerDataClient('TEST')
        try: 
            obj =  Client.get_average_price()
            print(f"Server time: {obj.price} {obj.time_interval}")
        except ValueError as err:
            print("Handling run-time error: ", err)
            

main()