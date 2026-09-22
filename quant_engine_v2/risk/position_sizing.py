class PositionSizer:
    def __init__(self, account_balance=10000):
        self.balance = account_balance

    def calculate_size(self, risk_percent, entry_price, sl_price):
        if not sl_price or sl_price == entry_price:
            return 0
            
        risk_amount = self.balance * risk_percent
        stop_loss_dist = abs(entry_price - sl_price)
        
        if stop_loss_dist == 0:
            return 0
            
        position_size = risk_amount / stop_loss_dist
        return position_size

    def update_balance(self, new_balance):
        self.balance = new_balance
