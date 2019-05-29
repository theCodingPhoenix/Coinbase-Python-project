import websocket
import json
import csv
from pathlib import Path

# Coinbase Websocket Feed URL
URL = "wss://ws-feed.pro.coinbase.com"


# checks whether the file already exists
# if not, creates it with header
def create_file_with_header():
    trades_file = Path("btc_usd_coinbase_ws_trades.csv")
    # the file should be created
    if not trades_file.is_file():
        with open("btc_usd_coinbase_ws_trades.csv", "a", newline='') as trades:
            file_writer = csv.writer(trades)
            file_writer.writerow(['Time','Price'])


# accepts the message that needs to be processed to be printed
# opens the file in append mode, writes to file
def write_to_file(btc_message):
    with open("btc_usd_coinbase_ws_trades.csv", "a", newline='') as trades:
        file_writer = csv.writer(trades)
        file_writer.writerow([btc_message['time'], btc_message['price']])


# accepts a message, converts to json
# processes it in the format required to be written to file
def process_message_and_create_file(message):
    # line_to_write = get_line_for_file(message)
    btc_message = json.loads(message)
    if btc_message['time']:
        write_to_file(btc_message)


class CoinbaseFeed(object):

    def __init__(self):
        self.ws = websocket.WebSocketApp(URL,on_message=self.on_ws_message, on_open=self.on_ws_open)

    def run_forever(self):
        self.ws.run_forever()

    def on_ws_message(self, message):
        process_message_and_create_file(message)

    def on_ws_open(self):

        # subscribe to the ticker channel for realtime updates
        # our focus is to obtain prices for BTC-USD
        params = {
            "type": "subscribe",
            "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]
        }
        self.ws.send(json.dumps(params))

    def close_connection(self):
        self.ws.close()


if __name__ == '__main__':

    create_file_with_header()

    ws = CoinbaseFeed()
    # the feed should keep running and logging
    # the realtime updates that are obtained
    ws.run_forever()
