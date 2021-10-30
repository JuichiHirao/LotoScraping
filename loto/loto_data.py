from datetime import datetime


class LotoData:

    def __init__(self):
        self.lottery_date = datetime.strptime('1900/1/1', '%Y/%m/%d')
        self.times = 0
        self.num_set = ''
        self.kind = 0
        self.one_unit = 0
        self.one_amount = 0
        self.two_unit = 0
        self.two_amount = 0
        self.three_unit = 0
        self.three_amount = 0
        self.four_unit = 0
        self.four_amount = 0
        self.five_unit = 0
        self.five_amount = 0
        self.six_unit = 0
        self.six_amount = 0
        self.carryover = 0
        self.sales = 0
        self.created_at = None
        self.updated_at = None


class BuyData:

    def __init__(self):
        self.csv_id = 0
        self.target_date = None
        self.seq = 0
        self.times = 0
        self.num_set = ''
        self.kind = 0
        self.winning = 0
        self.created_at = None
        self.updated_at = None
