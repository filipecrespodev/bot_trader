
class base:
    def __init__(self):
        pass

    def get_crypto_data(pair, since):
         raise NotImplementedError

    def get_balance():
        raise NotImplementedError

    def get_trades_history():
        raise NotImplementedError

    def add_sell_order(pair, volume):
        raise NotImplementedError

    def add_buy_order(pair, volume):
        raise NotImplementedError
