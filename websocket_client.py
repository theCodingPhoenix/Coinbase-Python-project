from websocket import WebSocketApp
from json import dumps, loads


def on_message(ws, message):
    trades = open("trades.txt", "a")
    trades.write("\n")
    trades.write(message)
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



