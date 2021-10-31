import sys
import db_mysql
from loto_data import LotoData
from datetime import datetime
from decimal import Decimal


class NumberPrize:

    def __init__(self, unit, amount):
        self.unit = int(unit)
        self.amount = int(amount)

    def get_unit(self):

        return "{:,d}".format(self.unit).rjust(8)

    def get_amount(self):

        return "{:,d}".format(self.amount).rjust(15)


class WinningCheck:

    def __init__(self):

        self.mysql_db = db_mysql.Loto()

    def execute(self):

        no_winning_list = self.mysql_db.get_list_from_no_check_winning()

        before_date = None
        for no_winning_data in no_winning_list:

            lottery_data = self.mysql_db.get_lotteries_data_from_target_date(no_winning_data.target_date)

            if lottery_data is None:
                print('no match data')
                no_winning_data.print()

            one = NumberPrize(lottery_data.one_unit, lottery_data.one_amount)
            two = NumberPrize(lottery_data.two_unit, lottery_data.two_amount)
            three = NumberPrize(lottery_data.three_unit, lottery_data.three_amount)
            four = NumberPrize(lottery_data.four_unit, lottery_data.four_amount)
            five = NumberPrize(lottery_data.five_unit, lottery_data.five_amount)
            six = None
            if no_winning_data.kind == 7:
                six = NumberPrize(lottery_data.six_unit, lottery_data.six_amount)

            if before_date != no_winning_data.target_date:
                str_date = lottery_data.lottery_date.strftime("%Y-%m-%d")
                print('')
                str_kind = 'SEVEN' if lottery_data.kind == 7 else 'SIX'
                print('{} {}回 {}'.format(str_kind, lottery_data.times, str_date))
                print('{}'.format(lottery_data.num_set))
                print('1 {} {}'.format(one.get_unit(), one.get_amount()))
                print('2 ' + two.get_unit() + ' ' + two.get_amount())
                print('3 ' + three.get_unit() + ' ' + three.get_amount())
                print('4 ' + four.get_unit() + ' ' + four.get_amount())
                print('5 ' + five.get_unit() + ' ' + five.get_amount())

                if no_winning_data.kind == 7:
                    print('6 ' + six.get_unit() + ' ' + six.get_amount())
                print('sales ' + '{:,}'.format(Decimal(lottery_data.sales)))
                print('carry ' + '{:,}'.format(Decimal(lottery_data.carryover)))
                print('')

            if no_winning_data.kind == 6:
                no_winning_data.winning = self.check_six(lottery_data, no_winning_data)
            else:
                no_winning_data.winning = self.check_seven(lottery_data, no_winning_data)

            no_winning_data.times = lottery_data.times
            before_date = no_winning_data.target_date

            self.mysql_db.update_winning(lottery_data.times, no_winning_data.id, no_winning_data.winning)

        return

    def check_six(self, lottery_data, detail):

        arr_lottery = lottery_data.num_set.split(',')
        arr_target = detail.num_set.split(',')
        arr_lottery_six = arr_lottery[0:6]
        result = set(arr_lottery_six) & set(arr_target)
        bonus = arr_lottery[6:7]
        bonus_result = set(arr_target) & set(bonus)

        result_winning = 0
        result_amount = 0

        res_len = len(result)
        if res_len == 3:
            result_winning = 5
            result_amount = lottery_data.five_amount

        if res_len == 4:
            result_winning = 4
            result_amount = lottery_data.four_amount

        if res_len == 5 and len(bonus_result) <= 0:
            result_winning = 3
            result_amount = lottery_data.three_amount

        if res_len == 5 and len(bonus_result) == 1:
            result_winning = 2
            result_amount = lottery_data.two_amount

        if res_len == 6:
            result_winning = 1
            result_amount = lottery_data.one_amount

        if result_winning == 0:
            print("  {} lose match {}".format(detail.seq, len(result), detail.num_set))

        else:
            print('  {} winning {}等({:,d}) {}'.format(detail.seq, result_winning, result_amount, detail.num_set))

        return result_winning

    def check_seven(self, lottery_data, detail):

        arr_lottery = lottery_data.num_set.split(',')
        arr_target = detail.num_set.split(',')
        arr_lottery_seven = arr_lottery[0:7]
        result = set(arr_lottery_seven) & set(arr_target)
        bonus = arr_lottery[7:9]
        bonus_result = set(arr_target) & set(bonus)
        result_winning = 0
        result_amount = 0

        res_len = len(result)
        if res_len == 3 and len(bonus_result) > 0:
            # print("  winning 6 " + str(len(result)) + " " + str(detail.num_set))
            result_winning = 6
            result_amount = lottery_data.six_amount
        if res_len == 4:
            result_winning = 5
            result_amount = lottery_data.five_amount

        if res_len == 5:
            result_winning = 4
            result_amount = lottery_data.four_amount

        if res_len == 6 and len(bonus_result) <= 0:
            result_winning = 3
            result_amount = lottery_data.three_amount

        if res_len == 6 and len(bonus_result) > 0:
            result_winning = 2
            result_amount = lottery_data.two_amount

        if res_len == 7:
            result_winning = 1
            result_amount = lottery_data.one_amount

        if result_winning == 0:
            print("  {} lose match {} {}".format(detail.seq, len(result), detail.num_set))
        else:
            print('  {} winning {}等({:,d}) {}'.format(detail.seq, result_winning, result_amount, detail.num_set))

        return result_winning


if __name__ == '__main__':
    winning_check = WinningCheck()
    winning_check.execute()
