# coding: utf-8
import postgresql
import yaml
from datetime import datetime


class Loto:

    # def __init__(self, user, password, hostname, dbname, table_name=''):
    def __init__(self, table_name=''):
        self.max_time = 0
        self.user = ''
        self.password = ''
        self.hostname = ''
        self.dbname = ''

        self.db = self.get_conn()

        # テーブル名が指定されていた場合は取得済みの回数を設定
        if len(table_name) > 0:
            self.table_name = table_name
            max_time = self.db.prepare("SELECT max(times) FROM " + table_name)
            for row in max_time():
                self.max_time = int(row[0])

    def get_conn(self):
        with open('credentials.yml') as file:
            obj = yaml.load(file, Loader=yaml.FullLoader)
            self.user = obj['user']
            self.password = obj['password']
            self.hostname = obj['hostname']
            self.dbname = obj['dbname']

        conn_str = 'pq://' + self.user + ':' + self.password + '@' + self.hostname + ':5432/' + self.dbname
        return postgresql.open(conn_str)

    def buy_export(self, data):

        exist_buy = self.db.prepare("SELECT created_at FROM buy WHERE target_date = $1 AND num_set = $2")
        cnt = 0
        for row in exist_buy(data.target_date, data.num_set):
            cnt += 1

        if cnt > 0:
            print("DATABASE EXIST " + str(data.times) + " [" + str(row["created_at"]) + "]")
            return

        sql = "INSERT INTO buy ( " \
            + "target_date, num_set, kind " \
            + ", created_at, updated_at " \
            + ") " \
            + "VALUES (" \
            + " $1, $2, $3 " \
            + ", $4, $5)"

        with self.db.xact():
            make_buy = self.db.prepare(sql)

            make_buy(data.target_date, data.num_set, data.kind, datetime.now(), datetime.now())

        print("buy export " + str(data.target_date))

    def export(self, data):

        get_lotteries = self.db.prepare("SELECT created_at FROM lotteries WHERE times = $1")
        cnt = 0
        for row in get_lotteries(data.times):
            cnt += 1

        if cnt > 0:
            print("DATABASE EXIST " + str(data.times) + " [" + str(row["created_at"]) + "]")
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

    def export_seven(self, data):

        get_lotteries = self.db.prepare("SELECT created_at FROM seven_lotteries WHERE times = $1")
        cnt = 0
        for row in get_lotteries(data.times):
            cnt += 1

        if cnt > 0:
            print("DATABASE EXIST " + str(data.times) + " [" + str(row["created_at"]) + "]")
            return

        sql = "INSERT INTO seven_lotteries( " \
            + "lottery_date, times, num_set " \
            + ", one_unit, one_amount, two_unit, two_amount " \
            + ", three_unit, three_amount, four_unit, four_amount " \
            + ", five_unit, five_amount, six_unit, six_amount " \
            + ", carryover, sales " \
            + ", created_at, updated_at " \
            + ") " \
            + "VALUES (" \
            + " $1, $2, $3" \
            + ", $4, $5, $6, $7" \
            + ", $8, $9, $10, $11 " \
            + ", $12, $13, $14, $15 " \
            + ", $16, $17" \
            + ", $18, $19);"

        with self.db.xact():
            make_lotteries = self.db.prepare(sql)

            make_lotteries(datetime.strptime(data.lottery_date, '%Y/%m/%d'), data.times, data.num_set
                           , data.one_unit, data.one_amount, data.two_unit, data.two_amount
                           , data.three_unit, data.three_amount, data.four_unit, data.four_amount
                           , data.five_unit, data.five_amount, data.six_unit, data.six_amount
                           , data.carryover, data.sales
                           , datetime.now(), datetime.now())

        print("export " + str(data.times))
