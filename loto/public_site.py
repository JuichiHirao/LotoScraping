# coding: utf-8
import urllib.request
import os
import codecs
import re
import csv
from datetime import datetime


class LotoData:

    def __init__(self):
        self.lottery_date = datetime.strptime('1900/1/1', '%Y/%m/%d')
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

class Loto:
    def __init__(self):
        self.max_time = 0

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

        # 第1264回ロト６,数字選択式全国自治宝くじ,平成30年3月29日,東京 宝くじドリーム館
        # 支払期間,平成30年3月30日から平成31年3月29日まで
        # 本数字,01,06,27,33,35,43,ボーナス数字,15

        self.data = LotoData()
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
                self.data.one_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.one_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
                self.data.one_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
                # print(str(self.one_unit) + " " + str(self.one_amount))
                print(str(self.data.one_unit) + " " + str(self.data.one_amount))
            if head.find('２等') == 0:
                self.two_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.two_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
                # print(str(self.two_unit) + " " + str(self.two_amount))
            if head.find('３等') == 0:
                self.three_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.three_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
                # print(str(self.three_unit) + " " + str(self.three_amount))
            if head.find('４等') == 0:
                self.four_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.four_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
                # print(str(self.four_unit) + " " + str(self.four_amount))
            if head.find('５等') == 0:
                self.five_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.five_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
                # print(str(self.five_unit) + " " + str(self.five_amount))
            if head.find('キャリーオーバー') == 0:
                self.carryover = int(row[1].replace("円", ""))
                # print(str(self.carryover))
            if head.find('販売実績額') == 0:
                self.sales = int(row[1].replace("円", ""))
                # print(str(self.sales))
            # if re.search("第\d回ロト６", head):
            if head.find('第') == 0:
                str_date = self.get_seireki(re.sub(r'(年|月)', "/", row[2]).replace("日", ""))
                datetime.strptime(str_date, '%Y/%m/%d')
                self.lottery_date = self.data.lottery_date = str_date
                # print(str(self.data.lottery_date))

        # 第1264回ロト６,数字選択式全国自治宝くじ,平成30年3月29日,東京 宝くじドリーム館
    def get_seireki(self, str_wareki):
        if str_wareki.find("平成29") == 0:
            return str_wareki.replace("平成29", "2017")
        if str_wareki.find("平成30") == 0:
            return str_wareki.replace("平成30", "2018")
        return ""

