import websocket
import json

URL = "wss://ws-feed.pro.coinbase.com"


def on_message(ws, message):
    print(ws)
    btc_message = json.loads(message)
    trades = open("trades.csv", "a")
    trades.write("\n")
    trades.write("Time: " + btc_message['time'] + ", Price: " + btc_message['price'])
    trades.close()


def on_open(socket):
    print(socket)
    params = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]
    }
    socket.send(json.dumps(params))


def main():

    ws = websocket.WebSocketApp(URL, on_open=on_open, on_message=on_message)
    ws.run_forever()


if __name__ == '__main__':
    main()



