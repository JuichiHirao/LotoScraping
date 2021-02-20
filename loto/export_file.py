import pandas
import psycopg2
import yaml
from datetime import datetime


class ExportFile:

    def __init__(self, table_name=''):
        self.max_time = 0
        self.user = ''
        self.password = ''
        self.hostname = ''
        self.dbname = ''

        self.db_conn = self.get_conn()

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

        # 接続情報
        connection_config = {
            'host': self.hostname,
            'port': '5432',
            'database': self.dbname,
            'user': self.user,
            'password': self.password
        }

        # 接続
        return psycopg2.connect(**connection_config)

    def execute(self):

        now = datetime.now()
        now_str_date = now.strftime("%Y%m%d")

        lotteries_df = pandas.read_sql(sql="SELECT * FROM lotteries;", con=self.db_conn, index_col='id')
        lotteries_df.to_csv('lotteries{}.csv'.format(now_str_date))

        seven_lotteries_df = pandas.read_sql(sql="SELECT * FROM seven_lotteries;", con=self.db_conn, index_col='id')
        seven_lotteries_df.to_csv('seven_lotteries{}.csv'.format(now_str_date))

        buy_df = pandas.read_sql(sql="SELECT * FROM buy;", con=self.db_conn, index_col='id')
        buy_df.to_csv('buy{}.csv'.format(now_str_date))


if __name__ == '__main__':
    export_file = ExportFile()

    export_file.execute()
