# coding: utf-8

import urllib.request
from datetime import datetime

import os
import codecs
import decimal
import postgresql
import re
import sys

# url = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/index.html'
url = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/csv/A1021264.CSV'

base_url = 'https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/csv/A102'

with urllib.request.urlopen(url) as response:
    filename = os.path.basename(url)
    urllib.request.urlretrieve(url, filename)
    # response.encoding = response.apparent_encoding
    # html = response.read()
    # print(response.encoding)

csv_file = codecs.open(filename, 'r', 'shift_jis')
for line in csv_file:
    print(line[:-1])

csv_file.close()

# print(html)

