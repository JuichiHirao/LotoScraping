import yaml
import mysql.connector
from loto_data import BuyData, LotoData


class MysqlBase:

    def __init__(self, table_name='', dbname=''):
        self.max_time = 0
        self.user = ''
        self.password = ''
        self.hostname = ''
        self.dbname = ''
        self.cursor = None

        self.conn = self.get_conn()

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

    def get_max_time(self, kind):
        sql = "SELECT max(times) FROM lotteries WHERE kind = %s"

        self.cursor.execute(sql, (kind, ))

        # print('{}'.format(data.times))

        exist_row = self.cursor.fetchall()

        if exist_row:
            return exist_row[0][0]

        return -1

    def update_winning(self, times, buy_id, winning):

        sql = """
            UPDATE buy
              SET times = %s
                , winning = %s
              WHERE ID = %s
        """

        self.cursor.execute(sql, (times, winning, buy_id))

        # print("buy winning update id {} winning {}".format(buy_id, winning))
        self.conn.commit()

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
                , kind)
              VALUES (%s, %s, %s, %s
                , %s);
            """

        self.cursor.execute(sql, (data.target_date, data.seq, data.times, data.num_set
                            , data.kind))

        print("buy export {} {}".format(data.kind, data.target_date))
        self.conn.commit()

    def buy_export_mig(self, data):

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
              , sales, carryover)
            VALUES (
              %s, %s, %s, %s
              , %s, %s, %s, %s
              , %s, %s, %s, %s
              , %s, %s, %s, %s
              , %s, %s);
        """

        self.cursor.execute(sql, (data.lottery_date, data.times, data.num_set, data.kind
                            , data.one_unit, data.one_amount, data.two_unit, data.two_amount
                            , data.three_unit, data.three_amount, data.four_unit, data.four_amount
                            , data.five_unit, data.five_amount, data.six_unit, data.six_amount
                            , data.sales, data.carryover))

        print("export {}".format(data.times))
        self.conn.commit()

    def export_lotteries_mig(self, data):

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

    def get_lotteries_data_from_target_date(self, target_date):

        sql = """
            SELECT id, lottery_date, times, num_set, kind
                , one_unit, one_amount, two_unit, two_amount
                , three_unit, three_amount, four_unit, four_amount
                , five_unit, five_amount, six_unit, six_amount
                , sales, carryover
                , created_at, updated_at
              FROM lotteries
              WHERE lottery_date = %s ORDER BY times
        """

        self.cursor.execute(sql, (target_date, ))

        rows = self.cursor.fetchall()

        loto_data = None
        for row in rows:
            loto_data = LotoData()
            loto_data.id = row[0]
            loto_data.lottery_date = row[1]
            loto_data.times = row[2]
            loto_data.num_set = row[3]
            loto_data.kind = row[4]
            loto_data.one_unit = row[5]
            loto_data.one_amount = row[6]
            loto_data.two_unit = row[7]
            loto_data.two_amount = row[8]
            loto_data.three_unit = row[9]
            loto_data.three_amount = row[10]
            loto_data.four_unit = row[11]
            loto_data.four_amount = row[12]
            loto_data.five_unit = row[13]
            loto_data.five_amount = row[14]
            loto_data.six_unit = row[15]
            loto_data.six_amount = row[16]
            loto_data.sales = row[17]
            loto_data.carryover = row[18]
            loto_data.created_at = row[19]
            loto_data.updated_at = row[20]

        return loto_data

    def get_list_from_no_check_winning(self):

        buy_list = []
        sql = """
            SELECT id, target_date, seq, times, num_set, kind, created_at, updated_at
              FROM buy
              WHERE winning IS NULL AND target_date <= (SELECT MAX(lottery_date) FROM lotteries)
              ORDER BY target_date ASC, kind ASC, seq ASC;
        """

        self.cursor.execute(sql)

        rows = self.cursor.fetchall()

        for row in rows:
            buy_data = BuyData()
            buy_data.id = row[0]
            buy_data.target_date = row[1]
            buy_data.seq = row[2]
            buy_data.times = row[3]
            buy_data.num_set = row[4]
            buy_data.kind = row[5]
            buy_data.created_at = row[6]
            buy_data.updated_at = row[7]
            buy_list.append(buy_data)

        return buy_list

    def get_data_from_target_date(self, target_date):

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
