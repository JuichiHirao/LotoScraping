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

db_loto = db.Loto("seven_lotteries")

if len(args) == 2:
    start = int(args[1])
    end = start + 1
elif len(args) > 2:
    start = int(args[1])
    end = int(args[2])
else:
    start = db_loto.max_time + 1
    end = site_loto.max_time + 1

print("start " + str(start) + "  end " + str(end))

# postgresqlの最新の回数を取得

# for idx in range(db_loto.max_time+1, site_loto.max_time+1):
for idx in range(start, end):
    num = '%04d' % idx

    url = base_url + num + ".CSV"

    site_loto.parse(url, idx)
    db_loto.export_seven(site_loto.data)
