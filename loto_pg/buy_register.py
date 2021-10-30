# coding: utf-8

import re
import csv
import sys
from loto_pg import db
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


class BuyData:

    def __init__(self):
        self.arr_target_date = []
        self.arr_num_set = []
        self.arr_buy_detail = []

    def parse(self):
        for target_date in self.arr_target_date:
            for num_set in self.arr_num_set:
                detail = BuyDetailData()
                detail.target_date = target_date
                detail.num_set = num_set
                detail.kind = len(detail.num_set.split(","))

                self.arr_buy_detail.append(detail)


class BuyDetailData:

    def __init__(self):
        self.id = 0
        self.target_date = datetime.now()
        self.num_set = ''
        self.times = 0
        self.winning = 0
        self.kind = 0

        return


def main():
    args = sys.argv

    db_loto = db.Loto()

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


if __name__ == '__main__':
    main()

