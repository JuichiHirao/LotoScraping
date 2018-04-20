# coding: utf-8

import sys
from loto import buy_register
from loto import db
from datetime import datetime

class WinningCheck:

    def __init__(self, str_target_date):
        self.times = 0
        db_loto = db.Loto()
        self.db = db_loto.get_conn()

        try:
            self.target_date = datetime.strptime(str_target_date, '%Y/%m/%d')
        except ValueError as e:
            print("paramter invalid. can not date format [" + str_target_date + "]")
            self.target_date = datetime(1900, 1, 1)
            return

    def main(self):

        weekday = self.target_date.weekday()

        if weekday == 0 or weekday == 3:
            table_name = "lotteries"
        else:
            table_name = "seven_lotteries"

        print(table_name)
        get_lotteries = self.db.prepare("SELECT times, lottery_date, num_set FROM "
                                        + table_name + " WHERE lottery_date = $1 ORDER BY times")

        str_lottery_numset = ""
        for row in get_lotteries(self.target_date):
            str_lottery_numset = row["num_set"]
            self.times = int(row["times"])

        if len(str_lottery_numset) <= 0:
            print("not lottery")
            return

        print(datetime.strftime(self.target_date, '%Y/%m/%d') + ' ' + str_lottery_numset)
        get_target_buy = self.db.prepare("SELECT id, target_date, times, num_set FROM buy WHERE target_date = $1 ORDER BY times")

        arr_detail = []

        for row in get_target_buy(self.target_date):
            detail = buy_register.BuyDetailData()
            detail.id = row[0]
            detail.target_date = row[1]
            detail.times = row[2]
            detail.num_set = row[3]

            arr_detail.append(detail)

        for detail in arr_detail:

            if detail.times is not None and detail.times > 0:
                if detail.winning == 0:
                    print("  checked lose " + str(detail.winning) + " " + str(detail.num_set))
                else:
                    print("  checked winning 6 " + str(detail.winning) + " " + str(detail.num_set))
                continue

            if detail.kind == 6:
                detail.winning = self.check_six(str_lottery_numset, detail)
            else:
                detail.winning = self.check_seven(str_lottery_numset, detail)
            detail.times = self.times

            sql = "UPDATE buy " \
                + "  SET times = $1 " \
                + "    , winning = $2 " \
                + "    , updated_at = $3 " \
                + "  WHERE ID = $4"

            with self.db.xact():
                make_buy = self.db.prepare(sql)

                make_buy(self.times, detail.winning, datetime.now(), detail.id)

    def check_six(self, lottery_numset, detail):

        arr_lottery = lottery_numset.split(',')
        arr_target = detail.num_set.split(',')
        arr_lottery_six = arr_lottery[0:6]
        result = set(arr_lottery_six) & set(arr_target)
        bonus = arr_lottery[6:7]
        bonus_result = set(arr_target) & set(bonus)
        result_winning = 0

        res_len = len(result)
        if res_len == 3:
            print("  winning 5 " + str(len(result)) + " " + str(detail.num_set))
            result_winning = 5
        if res_len == 4:
            print("  winning 4 " + str(len(result)) + " " + str(detail.num_set))
            result_winning = 4
        if res_len == 5 and len(bonus_result) <= 0:
            print("  winning 3 " + str(len(result)) + " " + str(detail.num_set))
            result_winning = 3
        if res_len == 5 and len(bonus_result) == 1:
            print("  winning 2 " + str(len(result)) + " " + str(detail.num_set))
            result_winning = 2
        if res_len == 6:
            print("  winning 1 " + str(len(result)) + " " + str(detail.num_set))
            result_winning = 1
        if res_len < 3:
            print("  lose match" + str(len(result)) + " " + str(detail.num_set))

        return result_winning

    def check_seven(self, lottery_numset, detail):

        arr_lottery = lottery_numset.split(',')
        arr_target = detail.num_set.split(',')
        arr_lottery_seven = arr_lottery[0:7]
        result = set(arr_lottery_seven) & set(arr_target)
        bonus = arr_lottery[7:9]
        bonus_result = set(arr_target) & set(bonus)
        result_winning = 0

        res_len = len(result)
        if res_len == 3 and len(bonus_result) > 0:
            print("  winning 6 " + str(len(result)) + " " + str(detail.num_set))
            result_winning = 6
        if res_len == 4:
            print("  winning 5 " + str(len(result)) + " " + str(detail.num_set))
            result_winning = 5
        if res_len == 5:
            print("  winning 4 " + str(len(result)) + " " + str(detail.num_set))
            result_winning = 4
        if res_len == 6 and len(bonus_result) <= 0:
            print("  winning 3 " + str(len(result)) + " " + str(detail.num_set))
            result_winning = 3
        if res_len == 6 and len(bonus_result) > 0:
            print("  winning 2 " + str(len(result)) + " " + str(detail.num_set))
            result_winning = 2
        if res_len == 7:
            print("  winning 1 " + str(len(result)) + " " + str(detail.num_set))
            result_winning = 1
        if result_winning == 0:
            print("  lose match" + str(len(result)) + " " + str(detail.num_set))

        return result_winning


if __name__ == '__main__':
    argvs = sys.argv
    check = WinningCheck(argvs[1])

    if check.target_date.year == 1900:
        exit(-1)

    check.main()
