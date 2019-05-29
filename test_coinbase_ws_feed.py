from pathlib import Path
import os
import coinbase_ws_feed
import csv


def test_coinbase_ws_feed_URL():
    # ensure that this is the URL of the WS we connect to
    # if it changes in the future, this needs to be updated
    assert coinbase_ws_feed.URL == "wss://ws-feed.pro.coinbase.com"


def get_example_trade():
    return '{"type":"ticker","product_id":"BTC-USD","price":"8043.15000000","time":"2019-05-25T16:19:31.290000Z","last_size":"0.01784403"}'


# accepts the file path and returns True/False if the file is empty
def is_file_empty(file_path):
    return os.stat(file_path) == 0


# tests that the file is created and is not empty
def test_coinbase_ws_feed_is_file_created():
    # this establishes the connection and checks the on_message method to ensure
    # a file is created by the name btc_usd_coinbase_ws_trades.csv
    coinbase_ws_feed.create_file_with_header()
    trades_file = Path("btc_usd_coinbase_ws_trades.csv")
    # the file should be created
    assert trades_file.is_file() == True
    # the file should not be empty
    assert is_file_empty('btc_usd_coinbase_ws_trades.csv') == False


# tests whether trades are being saved
def test_coinbase_ws_feed_saving_trades_to_csv():

    # initialise the object and start the connection
    ws = coinbase_ws_feed.CoinbaseFeed()
    ws.on_ws_message(get_example_trade())

    # open the file and read the data
    with open("btc_usd_coinbase_ws_trades.csv", "r") as trades:
        reader = csv.reader(trades, delimiter=",")
        data = list(reader)
        row_count = len(data)

    # we need to ensure that it is saving the trades and not just the header
    assert row_count > 1


