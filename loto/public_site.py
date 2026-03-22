import urllib.request
import codecs
import re
import csv
from loto_data import LotoData
from datetime import datetime
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Loto:
    def __init__(self):
        self.max_time = 0

        # 現在の作業ディレクトリを取得
        self.download_dir = os.getcwd()

    def selenium_init(self):
        chrome_options = Options()

        # ヘッドレスモード（画面を表示しない）にする場合は以下を有効に
        # chrome_options.add_argument('--headless')

        # ダウンロード設定のカスタマイズ
        prefs = {
            "download.default_directory": self.download_dir,  # 保存先を現在のフォルダに
            "download.prompt_for_download": False,  # 保存確認ダイアログを表示しない
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True  # セーフブラウジングを有効に
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # 自動操作特有のフラグを消して検知されにくくする設定
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        # ※chromedriverのパスが通っていない場合は service=Service('パス') を指定
        self.driver = webdriver.Chrome(options=chrome_options)


    def get_max_time(self, check_url, continue_str, index_url):
        """
        みずほ銀行の公式サイトで公開されている最新の回数を取得
        """

        self.selenium_init()
        try:
            print(f"案内ページへアクセス中... {index_url}")
            self.driver.get(index_url)
            time.sleep(5)  # ページが完全に読み込まれるのを待つ

            print(f"対象サイトへアクセスします... {check_url}")
            self.driver.get(check_url)

            # ダウンロード完了まで待機（ファイルサイズが小さいので数秒で十分です）
            print("ダウンロード完了を待機中...")
            time.sleep(5)

            # 保存されたか確認
            filename = os.path.basename(check_url)
            expected_file = os.path.join(self.download_dir, filename)
            if os.path.exists(expected_file):
                print(f"成功！ファイルが保存されました: {expected_file}")
            else:
                print(f"ファイルが見つかりません。ダウンロードに失敗した可能性があります。 {expected_file}")

        finally:
            # ブラウザを閉じる
            self.driver.quit()

        csv_file = codecs.open(filename, 'r', 'shift_jis')

        times = -1
        for idx, line in enumerate(csv_file):
            l = line[:-1].strip()
            if l.find(continue_str) >= 0:
                continue

            times = re.sub(u'(第|回.*)', "", l)
            if len(times) > 0:
                break

        csv_file.close()

        self.max_time = int(times)
        print(f'最新 {times}回')

        os.remove(filename)

        return self.max_time

    def parse(self, url, times):

        # 第1264回ロト６,数字選択式全国自治宝くじ,平成30年3月29日,東京 宝くじドリーム館
        # 支払期間,平成30年3月30日から平成31年3月29日まで
        # 本数字,01,06,27,33,35,43,ボーナス数字,15

        self.data = LotoData()

        self.selenium_init()

        filename = os.path.basename(url)
        try:
            print("対象サイトへアクセスします...")
            # 直接CSVのURLを叩く
            # csv_url = "https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto7/csv/loto7.csv"
            self.driver.get(url)

            # ダウンロード完了まで待機（ファイルサイズが小さいので数秒で十分です）
            print("ダウンロード完了を待機中...")
            time.sleep(5)

            # 保存されたか確認
            expected_file = os.path.join(self.download_dir, filename)
            if os.path.exists(expected_file):
                print(f"成功！ファイルが保存されました: {expected_file}")
            else:
                print(f"ファイルが見つかりません。ダウンロードに失敗した可能性があります。 {url}")

        finally:
            # ブラウザを閉じる
            self.driver.quit()

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

        csv_file.close()

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

