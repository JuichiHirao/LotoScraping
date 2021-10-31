from datetime import datetime


class LotoData:

    def __init__(self):
        self.id = -1
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

    def print(self):
        print('{} {} {} one {}/{} two {}/{} three {}/{} four {}/{} five {}/{} six {}/{} {} {}'.format(
            self.times, self.lottery_date, self.num_set
            , self.one_unit, self.one_amount, self.two_unit, self.two_amount
            , self.three_unit, self.three_amount, self.four_unit, self.four_amount
            , self.five_unit, self.five_amount, self.six_unit, self.six_amount
            , self.carryover, self.sales))


class BuysData:

    def __init__(self):
        self.date_list = []
        self.num_set_list = []
        self.buy_list = []

    def parse(self):
        for target_date in self.date_list:
            for idx, num_set in enumerate(self.num_set_list):
                buy_data = BuyData()
                buy_data.target_date = target_date
                buy_data.num_set = num_set
                buy_data.kind = len(buy_data.num_set.split(","))
                buy_data.seq = idx + 1

                self.buy_list.append(buy_data)


class BuyData:

    def __init__(self):
        self.id = -1
        self.csv_id = 0
        self.target_date = None
        self.seq = 0
        self.times = 0
        self.num_set = ''
        self.kind = 0
        self.winning = 0
        self.created_at = None
        self.updated_at = None

    def print(self):
        # loto_data.lottery_date = datetime.strptime(row[1], '%Y-%m-%d')
        print('{} seq [{}] {} kind [{}]'.format(self.target_date.strftime('%Y-%m-%d'), self.seq, self.num_set, self.kind))
