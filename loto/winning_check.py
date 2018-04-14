# coding: utf-8

import sys
import postgresql
from loto import buy_register
from datetime import datetime

argvs = sys.argv
argv_user = argvs[1]
argv_password = argvs[2]
argv_hostname = argvs[3]
argv_dbname = argvs[4]


class WinningCheck:

    def __init__(self, argv_user, argv_password, argv_hostname, argv_dbname):
        conn_str = 'pq://' + argv_user + ':' + argv_password + '@' + argv_hostname + ':5432/' + argv_dbname
        self.db = postgresql.open(conn_str)

    def main(self):

        target_date = datetime.strptime(argvs[5], '%Y/%m/%d')
        print(target_date)
        get_target_buy = self.db.prepare("SELECT buy_date, times, num_set FROM buy WHERE buy_date = $1 ORDER BY times")

        arr_detail = []

        for row in get_target_buy(target_date):
            detail = buy_register.BuyDetailData()
            detail.buy_date = row[0]
            detail.times = row[1]
            detail.num_set = row[2]

            arr_detail.append(detail)

        get_lotteries = self.db.prepare("SELECT times, lottery_date, num_set FROM lotteries WHERE lottery_date = $1 ORDER BY times")
        target_numset = arr_detail[0].num_set.split(",")
        print(target_numset)

        for row in get_lotteries(target_date):
            print(str(row))
            arr_num = row["num_set"].split(',')
            num = arr_num[0:6]
            result = set(num) & set(target_numset)
            bonus = arr_num[6:7]
            bonus_result = set(target_numset) & set(bonus)

            res_len = len(result)
            if res_len == 3 and len(bonus_result) <= 0:
                print("winning 6 " + str(row["lottery_date"]) + " " + str(row["times"]) + " " + str(res_len) + " " + str(result))
            if res_len == 3 and len(bonus_result) == 1:
                print("winning 5 " + str(row["lottery_date"]) + " " + str(row["times"]) + " " + str(res_len) + " " + str(result) + str(bonus_result))
            if res_len == 4:
                print("winning 4 " + str(row["lottery_date"]) + " " + str(row["times"]) + " " + str(res_len) + " " + str(result))
            if res_len == 5 and len(bonus_result) <= 0:
                print("winning 3 " + str(row["lottery_date"]) + " " + str(row["times"]) + " " + str(res_len) + " " + str(result))
            if res_len == 5 and len(bonus_result) == 1:
                print("winning 2 " + str(row["lottery_date"]) + " " + str(row["times"]) + " " + str(res_len) + " " + str(result) + str(bonus_result))
            if res_len == 6:
                print("winning 1 " + str(row["lottery_date"]) + " " + str(row["times"]) + " " + str(res_len) + " " + str(result))
            if res_len < 3:
                print("lose " + str(row["lottery_date"]) + " " + str(row["times"]) + " " + str(res_len) + " " + str(result))


if __name__ == '__main__':
    check = WinningCheck(argv_user, argv_password, argv_hostname, argv_dbname)
    check.main()

exit(0)
