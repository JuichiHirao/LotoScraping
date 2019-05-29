# Loto Six and Seven Scraping

postgresqlに購入情報、公式サイトからの取得を登録

|file| subject|
|:---:|:---|
|winning_check|購入履歴から、当選かをチェックする|
|buy_register|購入履歴を登録する|
|six_csv|公式が新たにCSV形式での取得に変わったので、合わせて修正|
|seven_csv|公式が新たにCSV形式での取得に変わったので、合わせて修正|

### 当選チェック
引数に日付を指定で、dbから日付でLoto6, 7を判定して当選チェック
```
PYTHONPATH=. python loto/winning_check.py 2018/06/14
```

### 購入履歴登録
loto配下のtest_dataのファイルから決まった形式で購入履歴として登録する  
数字の個数でLoto6かLoto7は自動判定
```
6/22 6/29 7/6 7/13 7/20
02 07 11 14 20 27 37
02 03 09 11 12 14 27
06 12 17 28 33 35 36
02 15 18 22 25 33 36
02 14 18 29 32 35 36
```
```
PYTHONPATH=. python loto/buy_register.py
```

### Loto6
[Loto6の公式サイト](https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto6/index.html)では461回から取得可能  

#### Loto6 最新の取得
dbの最大を取得して、そこから取得されていないデータを全て取得
```
PYTHONPATH=. python loto/six_csv.py
```

##### 指定回数の取得
  ※ BeautifulSoapで取得するのは未対応 
```
PYTHONPATH=. python loto/six_csv.py 461 480
```

### Loto7
[Loto7の公式サイト](https://www.mizuhobank.co.jp/retail/takarakuji/loto/loto7/index.html)で1回から取得可能

##### 最新の取得
dbの最大を取得して、そこから取得されていないデータを全て取得
```
PYTHONPATH=. python loto/seven_csv.py
```

##### 指定回数の取得
```
PYTHONPATH=. python loto/seven_csv.py
```

```
(venv) HIRAOnoMacBook-Pro:LotoScraping juichihirao$ pip freeze
beautifulsoup4==4.7.0
iso8601==0.1.12
javcore==0.1.8
mysql-connector-python==8.0.13
protobuf==3.6.1
py-postgresql==1.2.1
PyYAML==3.13
selenium==3.141.0
six==1.12.0
soupsieve==1.6.2
urllib3==1.24.1
(venv) HIRAOnoMacBook-Pro:LotoScraping juichihirao$ 
```
