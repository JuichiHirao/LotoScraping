# coding: utf-8

import re
import csv
import sys
import postgresql
from loto import db
from datetime import datetime


class LineParse:

    year = 2018

    def get_array_date(self, array_date):

        arr_date = []
        for mon_day in array_date:
            str_date = str(self.year) + '/' + mon_day
            arr_date.append(datetime.strptime(str_date, '%Y/%m/%d'))

        return arr_date

    def get_array_num_set(self, num_set):

        return ",".join(num_set);


class BuyData:

    def __init__(self):
        self.arr_buy_date = []
        self.arr_num_set = []
        self.arr_buy_detail = []

    def parse(self):
        detail = BuyDetailData()
        for buy_date in self.arr_buy_date:
            for num_set in self.arr_num_set:
                detail = BuyDetailData()
                detail.buy_date = buy_date
                detail.num_set = num_set
                #print(str(detail.buy_date) + ' ' + str(detail.num_set))
                self.arr_buy_detail.append(detail)


class BuyDetailData:

    def __init__(self):
        self.id = 0
        self.buy_date = datetime.now()
        self.num_set = ''
        self.times = 0
        self.winning = 0

        return


def main():
    args = sys.argv

    db_loto = db.Loto(args[1], args[2], args[3], args[4])

    csv_file = open("loto/test_data", "r", errors="", newline="")

    f = csv.reader(csv_file, delimiter=" ", skipinitialspace=True)

    arr_data = []
    data = BuyData()
    parse = LineParse()
    for row in f:
        if len(row) <= 0:
            continue
        if re.match("[0-9]*/[0-9]*", row[0]):
            # print("date " + row[0])
            if len(data.arr_buy_date) > 0:
                arr_data.append(data)
            data = BuyData()
            data.arr_buy_date = parse.get_array_date(row)
        elif re.match("[2][0][0-9][0-9]", row[0]):
            print("year " + row[0])
        elif re.match("[0-4][0-9]", row[0]):
            # print("num_set " + row[0])
            data.arr_num_set.append(parse.get_array_num_set(row))
        else:
            print("no match data" + row[0])

    if len(data.arr_buy_date) > 0:
        arr_data.append(data)

    for data in arr_data:
        data.parse()
        for detail in data.arr_buy_detail:
            db_loto.buy_export(detail)

        #for buy_date in data.arr_buy_date:
        #    print(str(buy_date))
        #for num_set in data.arr_num_set:
        #    print(num_set)


