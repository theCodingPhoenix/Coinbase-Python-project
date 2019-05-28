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

def test_coinbase_ws_feed_is_file_created():
    # this establishes the connection and checks the on_message method to ensure
    # a file is created by the name trades.csv
    ws = coinbase_ws_feed.CoinbaseFeed()
    ws.on_ws_message(get_example_trade())
    trades_file = Path("trades.csv")
    # the file should be created
    assert trades_file.is_file() == True
    # the file should not be empty
    assert is_file_empty('trades.csv') == False


