import websocket
import json
import csv
from pathlib import Path

# Coinbase Websocket Feed URL
URL = "wss://ws-feed.pro.coinbase.com"


# accepts the row that needs to be written to the file
# opens the file in append mode, writes to file
def write_to_file(file_writer, row):
    file_writer.writerow(row)

def average_of_list(list_of_prices):
    return sum(list_of_prices) / len(list_of_prices)

def get_moving_average_price(list_of_prices, new_price):
    list_of_prices.append(new_price)
    if len(list_of_prices) == 5:
        new_price = average_of_list(list_of_prices)
        list_of_prices.pop(0)
        print(new_price)

    return new_price

# accepts a message, converts to json
# processes it in the format required to be written to file
def process_message_and_create_file(message, file_writer, list_of_prices):
    # line_to_write = get_line_for_file(message)
    btc_message = json.loads(message)
    if btc_message['time']:
        price = get_moving_average_price(list_of_prices, float(btc_message['price']))
        write_to_file(file_writer, [btc_message['time'], price])


class CoinbaseFeed(object):

    def __init__(self):
        self.ws = websocket.WebSocketApp(URL,on_message=self.on_ws_message, on_open=self.on_ws_open)
        self.file_writer = self.write_header_to_file()
        self.list_of_prices = []

    def write_header_to_file(self):
        trades_file = Path("btc_usd_trades_moving_average.csv")
        # the file should be created
        file_exist = trades_file.is_file()
        trades = open("btc_usd_trades_moving_average.csv", "a")
        file_writer = csv.writer(trades)
        if not file_exist:
            write_to_file(file_writer, ['Time', 'Price'])
        return file_writer

    def run_forever(self):
        self.ws.run_forever()

    def on_ws_message(self, message):
        process_message_and_create_file(message, self.file_writer, self.list_of_prices)

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

    ws = CoinbaseFeed()

    # the feed should keep running and logging
    # the realtime updates that are obtained
    ws.run_forever()
