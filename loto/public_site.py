# coding: utf-8
import urllib.request
import os
import codecs
import re
import csv


class Loto:
    def __init__(self):
        self.max_time = 0
        # self.lottery_date
        self.times = 0
        self.num_set = ''
        self.one_unit = 0
        self.one_amount = 0
        self.two_unit = 0
        self.two_amount = 0
        self.three_unit = 0
        self.three_amount = 0
        self.four_unit = 0
        self.four_amount = 0
        self.five_unit = 0
        self.five_amount = 0
        self.carryover = 0
        self.sales = 0

    '''
    みずほ銀行の公式サイトで公開されている最新の回数を取得
    '''
    def set_max_time(self, check_url, continue_str):
        filename = os.path.basename(check_url)
        urllib.request.urlretrieve(check_url, filename)

        csv_file = codecs.open(filename, 'r', 'shift_jis')

        for idx, line in enumerate(csv_file):
            l = line[:-1]
            if l.find(continue_str) >= 0:
                continue

            times = re.sub(u'(第|回.*)', "", line[:-1])
            if len(times) > 0:
                break

        # print(str(times))

        self.max_time = int(times)

    def parse(self, url):
        filename = os.path.basename(url)
        try:
            urllib.request.urlretrieve(url, filename)
        except urllib.error.URLError as e:
            if e.code == 404:
                print("404 error " + url)
                return
            print(str(e.code) + " " + e.reason)

        csv_file = open(filename, "r", encoding="ms932", errors="", newline="")
        f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        for row in f:
            head = row[0]
            if len(row) < 2:
                continue
            if row[1].find('申込数字が') == 0:
                continue

            if head.find('１等') == 0:
                self.one_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.one_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
                # print(str(self.one_unit) + " " + str(self.one_amount))
            if head.find('２等') == 0:
                self.two_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.two_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
                # print(str(self.two_unit) + " " + str(self.two_amount))
            if head.find('３等') == 0:
                self.three_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.three_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
                #print(str(self.three_unit) + " " + str(self.three_amount))
            if head.find('４等') == 0:
                self.four_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.four_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
                #print(str(self.four_unit) + " " + str(self.four_amount))
            if head.find('５等') == 0:
                self.five_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.five_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
                #print(str(self.five_unit) + " " + str(self.five_amount))
            if head.find('キャリーオーバー') == 0:
                self.carryover = int(row[1].replace("円", ""))
                #print(str(self.carryover))
            if head.find('販売実績額') == 0:
                self.sales = int(row[1].replace("円", ""))
                #print(str(self.sales))

