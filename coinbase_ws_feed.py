import websocket
import json


def on_message(ws, message):
    btc_message = json.loads(message)
    trades = open("trades.csv", "a")
    trades.write("\n")
    trades.write("Time: " + btc_message['time'] + ", Price: " + btc_message['price'])
    trades.close()


def on_open(socket):
    params = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]
    }
    socket.send(json.dumps(params))


def main():
    ws = websocket.WebSocketApp("wss://ws-feed.pro.coinbase.com", on_open=on_open, on_message=on_message)
    ws.run_forever()


if __name__ == '__main__':
    main()



