from BinanceClient.MarkerDataClient import MarkerDataClient


def main():
    if __name__ == "__main__":
        Client = MarkerDataClient()
        try: 
            server_time = Client.get_order_book()
            print(f"Server time: {server_time}")
        except ValueError as err:
            print("Handling run-time error: ", err)
            

main()