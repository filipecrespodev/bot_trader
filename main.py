import time
import kraken
import trander

def get_last_buy(pair):
  history = kraken.get_trades_history()['result']['trades']

  last_trade = {}
  for trade in history:
    if history[trade]['pair'] == str(pair) and history[trade]['type'] == 'buy':
      last_trade = history[trade]
      print(last_trade)
      return last_trade['price']

def execute():
  for pair in pairs:
    crypto_data = kraken.get_crypto_data(pair, since)['result'][pair]
    pair_balance = balance[pairs[pair][0]]
    if float(pair_balance) > 0.00:
      sell = trander.analyse_to_sell(crypto_data, float(get_last_buy(pair)))
      if sell:
        response = kraken.add_sell_order(pair, pair_balance)
        print(response)
    else:
      value = trander.analyse_to_buy(crypto_data)
      if  value > 0.00:
        volume = str(round(pairs[pair][2]/float(value), 8))
        response = kraken.add_buy_order(pair, volume)
        print(response)

    print('-------------------------------------------------------')

if __name__ == '__main__':
  # since = str(int(time.time() - 10800))
  since = str(int(time.time() - (60*60*30)))
  pairs = {
    "XETHZUSD": ["XETH", "ZUSD", 40.00],
    # "XXBTZUSD": ["XXBT", "ZUSD", 21.00]
    # "ADAUSD": ["ADA", "USD", 15.00],
    # "TRXUSD": ["TRX", "USD", 10.00]
    # "SOLUSD": ["SOL", "USD", 25.00],
  }

  crypto_data = kraken.get_crypto_data('XETHZUSD', since)['result']['XETHZUSD']
  print(crypto_data)
  # while True:
  #   balance = kraken.get_balance()['result']
  #   print(balance)
  #   execute()
  #   print('\n\n\n///////////////////////////////////////////////////////\n\n\n')
  #   time.sleep(60)

