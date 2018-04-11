from datetime import datetime

import sys
import decimal
import postgresql

argvs = sys.argv
argv_user = argvs[1]
argv_password = argvs[2]
argv_hostname = argvs[3]
argv_dbname = argvs[4]


class WinningCheck:
    conn_str = 'pq://' + argv_user + ':' + argv_password + '@' + argv_hostname + ':5432/' + argv_dbname
    db = postgresql.open(conn_str)

    get_lotteries = db.prepare("SELECT times, lottery_date, num_set FROM lotteries ORDER BY times")
    # input = "02,07,11,14,20,27".split(",")
    input = "05,20,26,27,28,33".split(",")
    with db.xact():
        cnt = 0
        for row in get_lotteries():
            arr_num = row["num_set"].split(',')
            num = arr_num[0:6]
            result = set(num) & set(input)
            bonus = arr_num[6:7]
            bonus_result = set(input) & set(bonus)

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
