# coding: utf-8

import urllib.request
from datetime import datetime

import decimal
import postgresql
import re
import sys
from bs4 import BeautifulSoup

# url = 'http://www.mizuhobank.co.jp/takarakuji/loto/backnumber/lt6-201712.html'
url = 'https://www.mizuhobank.co.jp/takarakuji/loto/loto6/index.html'


with urllib.request.urlopen(url) as response:
    html = response.read()

html_soup = BeautifulSoup(html, "html.parser")

type_tk = html_soup.find_all('table', class_="typeTK")

argvs = sys.argv

argv_user = argvs[1]
argv_password = argvs[2]
argv_hostname = argvs[3]
argv_dbname = argvs[4]

conn_str = 'pq://' + argv_user + ':' + argv_password + '@' + argv_hostname + ':5432/' + argv_dbname

for i, table in enumerate(type_tk):
    print(str(i+1) + "件")

    times_html = table.find_all('th', class_="alnCenter bgf7f7f7")
    for time in times_html:
        # times = time.text.replace(u"第", "").replace(u"回", "")
        # times = re.sub(u"第回", "", times_html)
        times = re.sub(u'(第|回)', "", time.text)
        print(str(times) + " [" + time.text + "]")

    date_jp_html = table.find_all('td', class_="alnCenter", colspan="6")
    for dt in date_jp_html:
        lotteries_date = re.sub(r'(年|月)', "/", dt.text).replace("日", "")
        print(lotteries_date + " [" + dt.text + "]")

    lottery_num = []
    extension_list = table.find_all('td', class_="alnCenter extension")
    for idx, ext in enumerate(extension_list):
        lottery_num.append(ext.text)

    ext_green_list = table.find_all('td', class_="alnCenter extension green")
    for ext in ext_green_list:
        bonus_num = ext.text.replace(")", "").replace("(", "")
        lottery_num.append(bonus_num)
        # print("B " + str(ext.text.replace(")", "").replace("(", "")))

    print(str(lottery_num))

    aln_right_list = table.find_all('td', class_="alnRight")
    lottery_info = []
    one_info = ["", ""]
    for idx, ext in enumerate(aln_right_list):
        n = (idx / 2) + 1
        if idx & 1:
            one_info[1] = ext.text.replace("該当なし", "0").replace("円", "").replace(",", "")
        else:
            one_info[0] = ext.text.replace("該当なし", "0").replace("円", "").replace("口", "").replace(",", "")

        if len(one_info[1]) > 0:
            lottery_info.append(one_info)
            one_info = ["", ""]

    carry_over = decimal.Decimal(lottery_info[5][0])
    print(lottery_info)

    db = postgresql.open(conn_str)

    get_lotteries = db.prepare("SELECT created_at FROM lotteries WHERE times = $1")

    with db.xact():
        cnt = 0
        for row in get_lotteries(int(times)):
            cnt += 1

        if cnt > 0:
            print("DATABASE EXIST " + times + " [" + str(row["created_at"]) + "]")
        else:
            print("DATABASE NOT EXIST " + times)

            sql = "INSERT INTO lotteries( " \
                + "lottery_date, times, num_set " \
                + ", one_unit, one_amount, two_unit, two_amount " \
                + ", three_unit, three_amount, four_unit, four_amount " \
                + ", five_unit, five_amount, carryover, sales " \
                + ", created_at, updated_at " \
                + ") " \
                + "VALUES (" \
                + " $1, $2, $3" \
                + ", $4, $5, $6, $7" \
                + ", $8, $9, $10, $11 " \
                + ", $12, $13, $14, $15 " \
                + ", $16, $17);"

            make_lotteries = db.prepare(sql)
            make_lotteries(datetime.strptime(lotteries_date, '%Y/%m/%d'), int(times), ",".join(lottery_num),
                             int(lottery_info[0][0]), int(lottery_info[0][1]), int(lottery_info[1][0]), int(lottery_info[1][1]),
                             int(lottery_info[2][0]), int(lottery_info[2][1]), int(lottery_info[3][0]), int(lottery_info[3][1]),
                             int(lottery_info[4][0]), int(lottery_info[4][1]), carry_over, int(lottery_info[5][1]),
                             datetime.now(), datetime.now())

'''
0 <td class="alnRight" colspan="3">3口</td>
1 <td class="alnRight" colspan="3"><strong>298,063,900円</strong></td>
2 <td class="alnRight" colspan="3">9口</td>
3 <td class="alnRight" colspan="3"><strong>11,314,800円</strong></td>
4 <td class="alnRight" colspan="3">328口</td>
5 <td class="alnRight" colspan="3"><strong>335,200円</strong></td>
6 <td class="alnRight" colspan="3">15,141口</td>
7 <td class="alnRight" colspan="3"><strong>7,600円</strong></td>
8 <td class="alnRight" colspan="3">236,909口</td>
9 <td class="alnRight" colspan="3"><strong>1,000円</strong></td>
10 <td class="alnRight" colspan="6">2,009,699,400円</td>
11 <td class="alnRight" colspan="6"><strong>0円</strong></td>
'''
