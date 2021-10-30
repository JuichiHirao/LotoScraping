import yaml
import mysql.connector
from loto_data import BuyData


class MysqlBase:

    def __init__(self, table_name='', dbname=''):
        self.max_time = 0
        self.user = ''
        self.password = ''
        self.hostname = ''
        self.dbname = ''
        self.cursor = None

        self.conn = self.get_conn()

        # テーブル名が指定されていた場合は取得済みの回数を設定
        if len(table_name) > 0:
            self.table_name = table_name
            max_time = self.db.prepare("SELECT max(times) FROM " + table_name)
            for row in max_time():
                self.max_time = int(row[0])

        if len(dbname) > 0:
            self.dbname = dbname

        self.cursor = self.conn.cursor()

    def get_conn(self):

        with open('credentials.yml') as file:
            obj = yaml.load(file, Loader=yaml.FullLoader)
            self.user = obj['user']
            self.password = obj['password']
            self.hostname = obj['hostname']
            if len(self.dbname) <= 0:
                self.dbname = obj['dbname']

        return mysql.connector.connect(user=self.user, password=self.password,
                                       host=self.hostname, database=self.dbname)


class Loto(MysqlBase):

    def buy_export(self, data):

        sql = "SELECT created_at FROM buy WHERE target_date = %s AND num_set = %s"

        self.cursor.execute(sql, (data.target_date, data.num_set))

        # print('{}'.format(data.times))

        exist_row = self.cursor.fetchall()

        if exist_row:
            print('exist buy {} {}'.format(data.times, exist_row))
            return

        sql = """
            INSERT INTO buy(
                target_date, seq, times, num_set
                , kind, created_at, updated_at)
              VALUES (%s, %s, %s, %s
                , %s, %s, %s);
            """

        self.cursor.execute(sql, (data.target_date, data.seq, data.times, data.num_set
                            , data.kind, data.created_at, data.updated_at))

        print("buy export {} {}".format(data.kind, data.target_date))
        self.conn.commit()

    def buy_tmp_export(self, data):

        sql = "SELECT created_at FROM buy_tmp WHERE target_date = %s AND num_set = %s"

        self.cursor.execute(sql, (data.target_date, data.num_set))

        # print('{}'.format(data.times))

        exist_row = self.cursor.fetchall()

        if exist_row:
            print('exist buy {} {}'.format(data.times, exist_row))
            return

        sql = """
            INSERT INTO buy_tmp (
                csv_id, target_date, times, num_set
                , kind, created_at, updated_at)
              VALUES (%s, %s, %s, %s
                , %s, %s, %s);
            """

        self.cursor.execute(sql, (data.csv_id, data.target_date, data.times, data.num_set
                            , data.kind, data.created_at, data.updated_at))

        print("buy export {} {}".format(data.kind, data.target_date))
        self.conn.commit()

    def export_lotteries(self, data):

        # print('{}'.format(data.times))
        sql = 'SELECT created_at FROM lotteries WHERE times = %s'

        self.cursor.execute(sql, (data.times, ))

        exist_row = self.cursor.fetchall()

        if exist_row:
            print('exist {} {}'.format(data.times, exist_row))
            return

        sql = """
          INSERT INTO lotteries(
              lottery_date, times, num_set, kind
              , one_unit, one_amount, two_unit, two_amount
              , three_unit, three_amount, four_unit, four_amount
              , five_unit, five_amount, six_unit, six_amount
              , sales, carryover
              , created_at, updated_at)
            VALUES (
              %s, %s, %s, %s
              , %s, %s, %s, %s
              , %s, %s, %s, %s
              , %s, %s, %s, %s
              , %s, %s
              , %s, %s);
        """

        self.cursor.execute(sql, (data.lottery_date, data.times, data.num_set, data.kind
                            , data.one_unit, data.one_amount, data.two_unit, data.two_amount
                            , data.three_unit, data.three_amount, data.four_unit, data.four_amount
                            , data.five_unit, data.five_amount, data.six_unit, data.six_amount
                            , data.sales, data.carryover
                            , data.created_at, data.updated_at))

        print("export {}".format(data.times))
        self.conn.commit()

    def get_date_list(self):

        date_list = []
        sql = 'SELECT target_date FROM buy_tmp GROUP BY target_date ORDER BY target_date;'

        self.cursor.execute(sql)

        rows = self.cursor.fetchall()

        for row in rows:
            date_list.append(row[0])

        return date_list

    def get_list_from_target_date(self, target_date):

        buy_tmp_list = []
        sql = """
            SELECT target_date, times, num_set, kind, created_at, updated_at
              FROM buy_tmp
              WHERE target_date = %s
              ORDER BY csv_id;
        """

        self.cursor.execute(sql, (target_date, ))

        rows = self.cursor.fetchall()

        for row in rows:
            buy_data = BuyData()
            buy_data.target_date = row[0]
            buy_data.times = row[1]
            buy_data.num_set = row[2]
            buy_data.kind = row[3]
            buy_data.created_at = row[4]
            buy_data.updated_at = row[5]
            buy_tmp_list.append(buy_data)

        return buy_tmp_list