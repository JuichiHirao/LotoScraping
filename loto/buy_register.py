import re
import csv
import sys
import db_mysql
from loto_data import BuysData, BuyData
from datetime import datetime


class LineParse:

    year = datetime.now().year

    def get_array_date(self, array_date):

        arr_date = []
        for mon_day in array_date:
            if re.match("[2][0][0-9][0-9]", mon_day):
                # print("year " + row[0])
                new_year_date = datetime.strptime(mon_day, '%Y/%m/%d')
                arr_date.append(new_year_date)
                self.year = new_year_date.year
                continue

            str_date = str(self.year) + '/' + mon_day
            arr_date.append(datetime.strptime(str_date, '%Y/%m/%d'))

        return arr_date

    def get_array_num_set(self, num_set):

        return ",".join(num_set)


class BuyRegister:
    def __init__(self):
        self.mysql_db = db_mysql.Loto()
        idx = 0

    def execute(self):
        """
        # 2021-02-04
        # 2021-02-05
        3/26 3/30 4/2 4/6 4/09 4/13 4/16 4/20 4/23 4/27
        02 07 11 14 20 27
        03 16 23 28 30 42
        08 16 24 29 32 42
        01 09 15 16 25 35
        06 08 22 26 35 41
        """
        line_parse = LineParse()
        buys_data = BuysData()
        with open("loto/buy_text_data.csv", "r", errors="", newline="") as csv_fs:
            csv_file_reader = csv.reader(csv_fs, delimiter=" ", skipinitialspace=True)

            for line_row in csv_file_reader:

                if len(line_row) <= 0:
                    buys_data.parse()

                    for buy_data in buys_data.buy_list:
                        buy_data.print()
                    continue

                if re.match("[0-9]*/[0-9]*", line_row[0]) or re.match("[2][0][0-9][0-9]", line_row[0]):
                    buys_data.date_list = line_parse.get_array_date(line_row)
                    # print(buys_data.arr_target_date)
                elif re.match("[0-4][0-9]", line_row[0]):
                    # print("num_set " + row[0])
                    buys_data.num_set_list.append(line_parse.get_array_num_set(line_row))
                else:
                    print("no match data" + line_row[0])

        buys_data.parse()

        for buy_data in buys_data.buy_list:
            self.mysql_db.buy_export(buy_data)
            buy_data.print()

        return
        ''''''
        arr_data = []
        data = BuyData()
        # line_parse = LineParse()
        for row in csv_file_reader:
            if len(row) <= 0:
                continue
            if re.match("[0-9]*/[0-9]*", row[0]) or re.match("[2][0][0-9][0-9]", row[0]):
                if len(data.arr_target_date) > 0:
                    arr_data.append(data)
                data = BuyData()
                data.arr_target_date = line_parse.get_array_date(row)
            elif re.match("[0-4][0-9]", row[0]):
                # print("num_set " + row[0])
                data.arr_num_set.append(line_parse.get_array_num_set(row))
            else:
                print("no match data" + row[0])

        if len(data.arr_target_date) > 0:
            arr_data.append(data)

        for data in arr_data:
            data.parse()
            for detail in data.arr_buy_detail:
                db_loto.buy_export(detail)


'''
def main():
    args = sys.argv


    csv_file = open("loto/test_data", "r", errors="", newline="")

    f = csv.reader(csv_file, delimiter=" ", skipinitialspace=True)

    arr_data = []
    data = BuyData()
    parse = LineParse()
    for row in f:
        if len(row) <= 0:
            continue
        if re.match("[0-9]*/[0-9]*", row[0]) or re.match("[2][0][0-9][0-9]", row[0]):
            if len(data.arr_target_date) > 0:
                arr_data.append(data)
            data = BuyData()
            data.arr_target_date = parse.get_array_date(row)
        elif re.match("[0-4][0-9]", row[0]):
            # print("num_set " + row[0])
            data.arr_num_set.append(parse.get_array_num_set(row))
        else:
            print("no match data" + row[0])

    if len(data.arr_target_date) > 0:
        arr_data.append(data)

    for data in arr_data:
        data.parse()
        for detail in data.arr_buy_detail:
            db_loto.buy_export(detail)

'''

if __name__ == '__main__':
    buy_register = BuyRegister()
    buy_register.execute()
    # main()

