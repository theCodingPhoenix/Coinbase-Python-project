from pathlib import Path
import coinbase_ws_feed


def test_coinbase_ws_feed_URL():
    # ensure that this is the URL of the WS we connect to
    # if it changes in the future, this needs to be updated
    assert coinbase_ws_feed.URL == "wss://ws-feed.pro.coinbase.com"


def test_coinbase_ws_feed_is_file_created():
    # this establishes the connection and checks the on_message method to ensure
    # a file is created by the name trades.csv
    ws = coinbase_ws_feed.CoinbaseFeed()
    message = '{"type":"ticker","product_id":"BTC-USD","price":"8043.15000000","time":"2019-05-25T16:19:31.290000Z","last_size":"0.01784403"}'
    ws.on_ws_message(message)
    trades_file = Path("trades.csv")
    assert trades_file.is_file() == True

