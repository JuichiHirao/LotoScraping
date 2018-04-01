# coding: utf-8

from loto import public_site
from loto import db

import sys

# url = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/index.html'
url = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto7/csv/A1021264.CSV'

check_url = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto7/csv/loto7.csv'

base_url = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto7/csv/A103'

args = sys.argv

site_loto = public_site.Loto()
# みずほ銀行からCSVを取得して最新の回数を設定
site_loto.set_max_time(check_url, "A53")
print(site_loto.max_time)

# postgresqlの最新の回数を取得
db_loto = db.Loto(args[1], args[2], args[3], args[4], "seven_lotteries")
print(db_loto.max_time)

for idx in range(db_loto.max_time+1, site_loto.max_time+1):
    num = '%04d' % idx

    url = base_url + num + ".CSV"

    site_loto.parse(url, idx)
    db_loto.export_seven(site_loto.data)
    #print("data one_unit " + str(site_loto.data.one_amount))mport sys
