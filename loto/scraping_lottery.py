from loto import public_site
import db_mysql


class ScrapingLottery:

    def __init__(self):
        self.check_url_seven = ''
        self.base_url_seven = ''
        self.index_url_seven = ''
        self.check_url_six = ''
        self.base_url_six = ''
        self.index_url_six = ''

        self.mysql_db = db_mysql.Loto()
        self.site_loto = public_site.Loto()

        self.max_time_7_db = 0
        self.max_time_7_site = 0
        self.init_seven()

        self.max_time_6_db = 0
        self.max_time_6_site = 0
        self.init_six()

    def init_seven(self):
        # みずほ銀行からCSVを取得して最新の回数を設定
        self.check_url_seven = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto7/csv/loto7.csv'
        self.base_url_seven = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto7/csv/A103'
        self.index_url_seven = "https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto7/index.html"

    def init_six(self):
        # みずほ銀行からCSVを取得して最新の回数を設定
        self.check_url_six = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/csv/loto6.csv'
        self.base_url_six = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/csv/A102'
        self.index_url_six = "https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/index.html"

    def execute_six(self):
        self.max_time_6_db = self.mysql_db.get_max_time(6)
        self.max_time_6_site = self.site_loto.get_max_time(self.check_url_six, "A52", self.index_url_six)

        start = self.max_time_6_db + 1
        self.export(start, self.max_time_6_site, self.base_url_six, 6, self.index_url_six)

    def execute_seven(self):
        self.max_time_7_db = self.mysql_db.get_max_time(7)
        self.max_time_7_site = self.site_loto.get_max_time(self.check_url_seven, "A53", self.index_url_seven)

        start = self.max_time_7_db + 1
        self.export(start, self.max_time_7_site, self.base_url_seven, 7, self.index_url_seven)

    def export(self, start, end, url, kind, index_url):

        for idx in range(start, end + 1):
            num = '%04d' % idx

            csv_url = '{}{}.CSV'.format(url, num)

            loto_data = self.site_loto.parse(csv_url, idx)
            loto_data.kind = kind
            if kind == 6:
                loto_data.six_unit = None
                loto_data.six_amount = None
            loto_data.print()
            self.mysql_db.export_lotteries(loto_data)


if __name__ == '__main__':
    scraping_lottery = ScrapingLottery()
    scraping_lottery.execute_seven()
    scraping_lottery.execute_six()
