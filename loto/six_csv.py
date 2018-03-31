# coding: utf-8

import public_site
import db

import sys

# url = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/index.html'
url = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/csv/A1021264.CSV'

check_url = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/csv/loto6.csv'

base_url = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/csv/A102'

args = sys.argv

site_loto = public_site.Loto()
# みずほ銀行からCSVを取得して最新の回数を設定
site_loto.set_max_time(check_url, "A52")
print(site_loto.max_time)

# postgresqlの最新の回数を取得
db_loto = db.Loto(args[1], args[2], args[3], args[4], "lotteries")
print(db_loto.max_time)

