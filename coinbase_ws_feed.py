import websocket
import json

# Coinbase Websocket Feed URL
URL = "wss://ws-feed.pro.coinbase.com"


# accepts a string to write to file
# opens the file in append mode, writes and closes the file
def write_to_file(line):
    with open("trades.csv", "a") as trades:
        trades.write(line)
        trades.write("\n")
        trades.flush()

# accepts the message to be processed and written to file
# formats in the required manner
def get_line_for_file(message):
    btc_message = json.loads(message)
    line_to_write = btc_message['time'] + "," + btc_message['price']
    return line_to_write


# accepts a message, converts to json
# processes it in the format required to be written to file
def process_message_and_create_file(message):
    line_to_write = get_line_for_file(message)
    # write to file only if this is not an empty string
    if line_to_write:
        write_to_file(line_to_write)


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
    ws = CoinbaseFeed()
    # the feed should keep running and logging
    # the realtime updates that are obtained
    ws.run_forever()
