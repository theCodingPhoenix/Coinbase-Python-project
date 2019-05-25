from pathlib import Path
import coinbase_ws_feed


def test_coinbase_ws_feed_URL():
    # ensure that this is the URL of the WS we connect to
    # if it changes in the future, this needs to be updated
    assert coinbase_ws_feed.URL == "wss://ws-feed.pro.coinbase.com"



