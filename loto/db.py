# coding: utf-8
import postgresql
from datetime import datetime


class Loto:

    def __init__(self, user, password, hostname, dbname, table_name):
        self.max_time = 0
        self.table_name = table_name

        conn_str = 'pq://' + user + ':' + password + '@' + hostname + ':5432/' + dbname

        self.db = postgresql.open(conn_str)

        max_time = self.db.prepare("SELECT max(times) FROM " + table_name)
        for row in max_time():
            self.max_time = int(row[0])

    def export(self, data):

        get_lotteries = self.db.prepare("SELECT created_at FROM lotteries WHERE times = $1")
        cnt = 0
        for row in get_lotteries(data.times):
            cnt += 1

        if cnt > 0:
            print("DATABASE EXIST " + data.times + " [" + str(row["created_at"]) + "]")
            return

        sql = "INSERT INTO lotteries( " \
            + "lottery_date, times, num_set " \
            + ", one_unit, one_amount, two_unit, two_amount " \
            + ", three_unit, three_amount, four_unit, four_amount " \
            + ", five_unit, five_amount, carryover, sales " \
            + ", created_at, updated_at " \
            + ") " \
            + "VALUES (" \
            + " $1, $2, $3" \
            + ", $4, $5, $6, $7" \
            + ", $8, $9, $10, $11 " \
            + ", $12, $13, $14, $15 " \
            + ", $16, $17);"

        with self.db.xact():
            make_lotteries = self.db.prepare(sql)

            make_lotteries(datetime.strptime(data.lottery_date, '%Y/%m/%d'), data.times, data.num_set
                           , data.one_unit, data.one_amount, data.two_unit, data.two_amount
                           , data.three_unit, data.three_amount, data.four_unit, data.four_amount
                           , data.five_unit, data.five_amount, data.carryover, data.sales
                           , datetime.now(), datetime.now())

        print("export " + str(data.times))
