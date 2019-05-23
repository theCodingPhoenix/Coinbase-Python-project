from websocket import WebSocketApp
from json import dumps, loads


def on_message(ws, message):
    btc_message = loads(message)
    trades = open("trades.csv", "a")
    trades.write("\n")
    trades.write("Time: " + btc_message['time'] + ", Price: " + btc_message['price'])
    trades.close()


def on_open(socket):
    params = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]
    }
    socket.send(dumps(params))


def main():
    ws = WebSocketApp("wss://ws-feed.pro.coinbase.com", on_open=on_open, on_message=on_message)
    ws.run_forever()


if __name__ == '__main__':
    main()



