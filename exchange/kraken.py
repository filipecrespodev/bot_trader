import krakenex
import calendar
import datetime


class KrakenAPI:
  def __init__(self, key, secret):
    self.api = krakenex.API(key, secret)

  def query_public(self, method, data = {}):
    return self.api.query_public(method, data)

  def query_private(self, method, data = {}):
    return self.api.query_private(method, data)


def get_crypto_data(pair, since):
  return api.query_public("OHLC", data = {'pair': pair, 'since': since, 'interval': 15})

def get_balance():
  return api.query_private('Balance')

def get_trades_history():
  req_data = {
    'type': 'all',
    'trades': 'true',
    'start': str(calendar.timegm(start_date.timetuple()))
  }
  return api.query_private('TradesHistory', req_data)

def add_sell_order(pair, volume):
  req_data = {
    'ordertype': 'market',
    'type': 'sell',
    'pair': pair,
    'volume': volume,
    'starttm': 0
  }
  return api.query_private('AddOrder', req_data)

def add_buy_order(pair, volume):
  print(volume)
  req_data = {
    'ordertype': 'market',
    'type': 'buy',
    'pair': pair,
    'volume': volume,
    'starttm': 0
  }
  return api.query_private('AddOrder', req_data)

api = krakenex.API()
api.load_key('kraken.key')
start_date = datetime.datetime(2021,7,4)
