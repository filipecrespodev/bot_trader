import krakenex
import json
import time
import datetime
import calendar

def get_crypto_data(pair, since):
  return api.query_public("OHLC", data = {'pair': pair, 'since': since})['result'][pair]


def analyse(pair, since):
  data = get_crypto_data(pair[0]+pair[1], since)

  lowest = 0
  highest = 0

  for prices in data:
    balance = get_fake_balance()
    last_trade = get_last_trade(pair[0]+pair[1])
    print(last_trade)
    last_trade_price = float(last_trade['price'])

    open_ = float(prices[1])
    high_ = float(prices[2])
    low_ = float(prices[3])
    close_ = float(prices[4])

    did_sell = False

    try:
      balance[pair[0]]
      # if we  own any of the pair currency that we are then check sell
      selling_point_win = last_trade_price * 1.005
      selling_point_loss = last_trade_price * 0.995

      # selling at a win
      if open_ >= selling_point_win or close_ >= selling_point_win:
        print('sell at a profit')
        did_sell = True
        fake_sell(pair, close_, last_trade)
      elif open_ <= selling_point_loss or close_ <= selling_point_loss:
        print('sell at a loss')
        did_sell = True
        fake_sell(pair, close_, last_trade)
    except:
        pass

    # logic for if we shouold buy
    if not did_sell and float(balance['USD.HOLD']) > 0:
      if low_ < lowest or lowest == 0:
        lowest = low_
      if high_ > highest:
        highest = high_

      price_to_buy = 1.0005

      if highest/lowest >= price_to_buy and low_ <= lowest:
        available_money = balance['USD.HOLD']
        print('buy')
        fake_buy(pair, available_money, close_, last_trade)

def fake_buy (pair, dollar_amount, close_, last_trade):
  print('fake buy')
  trades_history = get_fake_trades_history()
  last_trade['price'] = str(close_)
  last_trade['type'] =  'buy'
  last_trade['cost'] = dollar_amount
  last_trade['time'] = datetime.datetime.now().timestamp()
  last_trade['vol'] = str(float(dollar_amount)/close_)

  trades_history['result']['trades'][str(datetime.datetime.now().timestamp())] = last_trade
  print(trades_history)
  with open('tradeshistory.json', 'w') as f:
    json.dump(trades_history, f, indent=4)
    fake_update_balance(pair, dollar_amount, close_, False)

def fake_sell(pair, close_, last_trade):
  print('fake sell')
  trades_history = get_fake_trades_history()

  last_trade['price'] = str(close_)
  last_trade['type'] =  'sell'
  last_trade['cost'] = str(float(last_trade['vol'])*close_)
  last_trade['time'] = datetime.datetime.now().timestamp()

  trades_history['result']['trades'][str(datetime.datetime.now().timestamp())] = last_trade

  with open('tradeshistory.json', 'w') as f:
    json.dump(trades_history, f, indent=4)
    fake_update_balance(pair, float(last_trade['cost']), close_, True)

def fake_update_balance(pair, dollar_amount, close_, was_sold):
	balance = get_fake_balance()
	prev_balance = float(balance['USD.HOLD'])
	new_balance = 0
	if was_sold:
		new_balance = prev_balance + float(dollar_amount)
		del balance[pair[0]]
	else:
		new_balance = prev_balance - float(dollar_amount)
		balance[pair[0]] = str(float(dollar_amount)/close_)
	balance['USD.HOLD'] = str(new_balance)

	with open('balance.json', 'w') as f:
		json.dump(balance, f, indent=4)

def get_fake_balance():
  with open('balance.json', 'r') as f:
    return json.load(f)

def get_balance():
  return api.query_private('Balance')

def get_last_trade(pair):
  trades_history = get_fake_trades_history()['result']['trades']

  last_trade = {}

  for trade in trades_history:
    trade = trades_history[trade]
    if trade['pair'] == pair and trade['type'] == 'buy':
      last_trade = trade
  return last_trade

def get_fake_trades_history():
  with open('tradeshistory.json', 'r') as f:
    return json.load(f)

def get_trades_history():
  start_date = datetime.datetime(2021,7,4)
  end_date = datetime.datetime.today()
  return api.query_private('TradesHistory', req(start_date, end_date, 1))['result']['trades']

def date_nix(str_date):
    return calendar.timegm(str_date.timetuple())

def req(start, end, ofs):
  req_data = {
    'type': 'all',
    'trades': 'true',
    'start': str(date_nix(start)),
    'end': str(date_nix(end)),
    'ofs': str(ofs)
  }
  return req_data

def list_crypt():
  # return api.query_public("OHLC", data = {'pair': pair, 'since': since})['result'][pair]
  pair = "ZUSD"
  all = api.query_public('AssetPairs')['result']
  list = []
  for crypt in all:
    if all[crypt]['quote'] == pair:
      list.append(crypt)

  return list

def surpassed_historic_top():
  crypts = list_crypt()
  print(crypts)
  for pair in crypts:
    history = get_history(pair)
    if len(history) > 0:
      top_price, top_price_time = last_top_price(history)
      last_price, last_price_time = now_price(history)
      print(pair, top_price, last_price)

      if int(last_price_time) != int(top_price_time) and float(last_price) > float(top_price):
        print(pair)

def crypts():
  with open('crypt.json', 'r') as f:
    return json.load(f)

def get_history(pair):
  response = api.query_public("OHLC", data = {'pair': pair, 'interval': 1440})
  if 'result' in response:
    return response['result'][pair]
  else:
    return []

def now_price(history):
  last_price = history[len(history)-1][4]
  last_price_time = history[len(history)-1][0]
  return last_price, last_price_time

def last_top_price(history):
  top_price = 0.00
  top_price_time = 0
  for candel in history:
    if float(candel[2]) > float(top_price):
      top_price = float(candel[2])
      top_price_time = candel[0]
  return top_price, top_price_time

def get_pairs():
  with open('crypt.json', 'r') as f:
    return json.load(f)


if __name__ == '__main__':
  api = krakenex.API()
  api.load_key('kraken.key')
  since = str(int(time.time() - 3600))
  pair = ("XETH", "ZUSD")
  analyse(pair, since)

  # print(surpassed_historic_top())

