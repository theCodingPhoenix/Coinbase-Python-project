import websocket
import json


URL = "wss://ws-feed.pro.coinbase.com"


class CoinbaseFeed(object):

    def __init__(self):
        print("Running Now")
        self.ws = websocket.WebSocketApp(URL,on_message=self.on_ws_message, on_open=self.on_ws_open)

    def run_forever(self):
        self.ws.run_forever()

    def on_ws_message(self, message):
        print(message)
        btc_message = json.loads(message)
        trades = open("trades.csv", "a")
        trades.write("\n")
        trades.write("Time: " + btc_message['time'] + ", Price: " + btc_message['price'])
        trades.close()
        print("Writing into file")

    def on_ws_open(self):
        print("Opening connection")
        params = {
            "type": "subscribe",
            "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]
        }
        self.ws.send(json.dumps(params))

    def close_connection(self):
        self.ws.close()


if __name__ == '__main__':
    ws = CoinbaseFeed()
    ws.run_forever()
