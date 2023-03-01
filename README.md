# Binance Client

Project created for learning purposes. 

## Requirements

To use Binance Client Python 3.10 is required and requirements installed.


### Linux:
```python

pip install -r requirements.txt
```
## Usage Example

```python
Client = MarkerDataClient('TEST', requests.get)
time =  Client.get_server_time()
print(f"Server time: {time}")
```