import csv
import db_mysql
from _datetime import datetime
from loto_data import LotoData, BuyData


class MigrationFromCsv:
    def __init__(self):
        self.mysql_db = db_mysql.Loto()

    def execute(self, csv_filename):

        with open(csv_filename) as csv_fs:
            csv_file_reader = csv.reader(csv_fs)

            for idx, row in enumerate(csv_file_reader):

                if 'id' == row[0]:
                    continue

                loto_data = LotoData()
                loto_data.lottery_date = datetime.strptime(row[1], '%Y-%m-%d')
                loto_data.times = row[2]
                loto_data.num_set = row[3]
                loto_data.one_unit = row[4]
                loto_data.one_amount = row[5].replace('.0', '')
                loto_data.two_unit = row[6]
                loto_data.two_amount = row[7].replace('.0', '')
                loto_data.three_unit = row[8]
                loto_data.three_amount = row[9].replace('.0', '')
                loto_data.four_unit = row[10]
                loto_data.four_amount = row[11].replace('.0', '')
                loto_data.five_unit = row[12]
                loto_data.five_amount = row[13].replace('.0', '')

                if len(row) == 20:
                    loto_data.kind = 7
                    loto_data.six_unit = row[14]
                    loto_data.six_amount = row[15].replace('.0', '')
                    loto_data.sales = row[17]
                    loto_data.carryover = row[16]
                    loto_data.created_at = datetime.strptime(row[18], '%Y-%m-%d %H:%M:%S.%f')
                    loto_data.updated_at = datetime.strptime(row[19], '%Y-%m-%d %H:%M:%S.%f')
                else:
                    loto_data.kind = 6
                    loto_data.sales = row[14]
                    loto_data.carryover = row[15]
                    try:
                        loto_data.created_at = datetime.strptime(row[16], '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError:
                        loto_data.created_at = None
                    try:
                        loto_data.updated_at = datetime.strptime(row[17], '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError:
                        loto_data.created_at = None
                    loto_data.six_unit = None
                    loto_data.six_amount = None

                self.mysql_db.export_lotteries(loto_data)

                # print('{} {}'.format(loto_data.created_at, row))

                # if idx > 1:
                #     break

    def execute_buy(self, csv_filename):

        with open(csv_filename) as csv_fs:
            csv_file_reader = csv.reader(csv_fs)

            for idx, row in enumerate(csv_file_reader):

                if 'id' == row[0]:
                    continue

                buy_data = BuyData()
                buy_data.csv_id = row[0]
                buy_data.target_date = datetime.strptime(row[1], '%Y-%m-%d')
                if len(row[2]) > 0:
                    buy_data.times = row[2]
                else:
                    buy_data.times = 0
                buy_data.num_set = row[3]
                buy_data.kind = row[4]
                buy_data.winning = row[5]
                buy_data.created_at = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S.%f')
                buy_data.updated_at = datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S.%f')

                self.mysql_db.buy_tmp_export(buy_data)

                # print('{} {}'.format(loto_data.created_at, row))

                # if idx > 1:
                #     break

    def move_buy(self):
        date_list = self.mysql_db.get_date_list()

        for target_date in date_list:
            buy_tmp_list = self.mysql_db.get_list_from_target_date(target_date)

            if len(buy_tmp_list) != 5:
                print('5件ではない {} {}'.format(target_date, len(buy_tmp_list)))

            for idx, buy_tmp_data in enumerate(buy_tmp_list):
                buy_tmp_data.seq = idx + 1
                self.mysql_db.buy_export(buy_tmp_data)
                # print(buy_tmp_data.num_set)


if __name__ == '__main__':
    migration_from_csv = MigrationFromCsv()
    migration_from_csv.execute('backup_csv/seven_lotteries20210116.csv')
    migration_from_csv.execute('backup_csv/lotteries20210116.csv')
    # migration_from_csv.execute_buy('backup_csv/buy20210116.csv')
    # migration_from_csv.move_buy()
