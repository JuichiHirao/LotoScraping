import urllib.request
import os
import codecs
import re
import csv
from loto_data import LotoData
from datetime import datetime


class Loto:
    def __init__(self):
        self.max_time = 0

    '''
    みずほ銀行の公式サイトで公開されている最新の回数を取得
    '''
    def get_max_time(self, check_url, continue_str):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]

        urllib.request.install_opener(opener)

        filename = os.path.basename(check_url)
        urllib.request.urlretrieve(check_url, filename)

        csv_file = codecs.open(filename, 'r', 'shift_jis')

        for idx, line in enumerate(csv_file):
            l = line[:-1].strip()
            if l.find(continue_str) >= 0:
                continue

            times = re.sub(u'(第|回.*)', "", l)
            if len(times) > 0:
                break

        # print(str(times))

        self.max_time = int(times)

        os.remove(filename)

        return self.max_time

    def parse(self, url, times):

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

        self.data.times = times
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
                self.data.one_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
            if head.find('２等') == 0:
                self.data.two_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.data.two_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
            if head.find('３等') == 0:
                self.data.three_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.data.three_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
            if head.find('４等') == 0:
                self.data.four_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.data.four_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
            if head.find('５等') == 0:
                self.data.five_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.data.five_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
            if head.find('６等') == 0:
                self.data.six_unit = int(row[1].replace("該当なし", "0").replace("口", ""))
                self.data.six_amount = int(row[2].replace("該当なし", "0").replace("円", ""))
            if head.find('キャリーオーバー') == 0:
                self.data.carryover = int(row[1].replace("円", ""))
            if head.find('本数字') == 0:
                if len(row) == 9:
                    # 本数字,01,06,27,33,35,43,ボーナス数字,15
                    self.data.num_set = row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "," + row[5]\
                                        + "," + row[6] + "," + row[8]
                else:
                    # 本数字,01,06,27,33,35,43,ボーナス数字,15
                    self.data.num_set = row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "," + row[5]\
                                        + "," + row[6] + "," + row[7] + "," + row[9] + "," + row[10]
            if head.find('販売実績額') == 0:
                self.data.sales = int(row[1].replace("円", ""))
            if head.find('第') == 0:
                str_date = self.get_seireki(re.sub(r'(年|月)', "/", row[2]).replace("日", ""))
                datetime.strptime(str_date, '%Y/%m/%d')
                self.data.lottery_date = str_date

        os.remove(filename)
        return self.data

    def get_seireki(self, str_wareki):

        # 令和4年1月7日
        m_wareki_nen = re.search('(令和|平成)(?P<wareki_nen>[0-9]{1,2})/', str_wareki)

        base_year = 0
        if m_wareki_nen:
            str_wareki_nen = m_wareki_nen.group('wareki_nen')
            # 元号のbase_yearは元年の前の年を設定
            if '平成' in str_wareki:
                base_year = 1988
            elif '令和' in str_wareki:
                base_year = 2018
        else:
            raise Exception('平成 or 令和ではありません「{}」'.format(str_wareki))

        year = int(str_wareki_nen) + base_year
        str_ymd = '{}'.format(str_wareki.replace(m_wareki_nen.group(), '{}/'.format(str(year))))

        return str_ymd

