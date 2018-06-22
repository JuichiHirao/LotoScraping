# coding: utf-8

from loto import public_site
from loto import db

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
db_loto = db.Loto("lotteries")
print(db_loto.max_time)

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

# for idx in range(db_loto.max_time+1, site_loto.max_time+1):
for idx in range(start, end):
    num = '%04d' % idx

    url = base_url + num + ".CSV"

    site_loto.parse(url, idx)

    if site_loto.data.times == 0:
        continue

    db_loto.export(site_loto.data)
    #print("data one_unit " + str(site_loto.data.one_amount))
