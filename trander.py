def analyse_to_sell(prices, buy_price):
  price = prices[len(prices)-1]

  price_now = float(price[4])
  high_ = float(price[2])

  selling_point_win = buy_price * 1.01
  selling_point_loss = buy_price * 0.995

  percent = price_now/float(buy_price)
  print('ANALYSE TO SELLL:')
  print('Buy at: ' + str(buy_price))
  print('Current at: ' + str(price_now))
  print('high_ at: ' + str(high_))
  print('Percent at: ' + str(percent) + ' selling_point_win: ' + str(selling_point_win))

  if price_now >= selling_point_win and high_ != price_now:
    print('PROFIT')
    return True
  elif price_now <= selling_point_loss:
    print('LOSS')
    return True
  else:
    return False

def analyse_to_buy(prices):
  price_to_buy = 1.005
  price = prices[len(prices)-1]
  print(price)

  open_ = float(price[1])
  high_ = float(price[2])
  low_ = float(price[3])
  close_ = float(price[4])

  print('Open: ' + str(open_))
  print('High: ' + str(high_))
  print('Low: ' + str(low_))
  print('Close: ' + str(close_))
  print('Percent: ' + str(close_/open_) )

  if close_ > open_ and open_ == low_ or close_/open_ >= price_to_buy:
    return close_
  else:
    return 0.00

