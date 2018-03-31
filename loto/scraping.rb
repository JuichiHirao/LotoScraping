
require 'open-uri'	# URLにアクセスするためのライブラリの読み込み
require 'nokogiri'	# Nokogiriライブラリの読み込み
require 'pg'

#SSL connection (protocol: TLSv1.2, cipher: DHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
db = PG::connect(:host=> "ec2-54-235-76-206.compute-1.amazonaws.com", :user => "mzjivpssypuclr", :dbname => "d5vd5nc7ktbd13", :password => "P95R4xh4H4rL-27ytzWQtrwCr6",:port => 5432, :sslmode => "require")

# スクレイピング先のURL
#url = 'http://www.mizuhobank.co.jp/takarakuji/loto/backnumber/lt6-201603.html'
url = 'https://www.mizuhobank.co.jp/takarakuji/loto/loto6/index.html'
charset = nil
html = open(url) do |f|
	#charset = f.charset # 文字種別を取得
	f.read # htmlを読み込んで変数htmlに渡す
end
# p html

# htmlをパース(解析)してオブジェクトを生成
doc = Nokogiri::HTML.parse(html, nil, charset)

sql = "insert into lotteries( " \
	+ "lottery_date, times, num_set " \
	+ ", one_unit, one_amount, two_unit, two_amount " \
	+ ", three_unit, three_amount, four_unit, four_amount " \
	+ ", five_unit, five_amount, carryover, sales " \
	+ ", created_at, updated_at " \
	+ ") " \
	+ "values (" \
	+ " $1, $2, $3" \
	+ ", $4, $5, $6, $7" \
	+ ", $8, $9, $10, $11 " \
	+ ", $12, $13, $14, $15 " \
	+ ", $16, $17);"

db.prepare("insertsql", sql)

doc.xpath('//table[@class="typeTK"]').each do |node|
	idxNum = 0
	lt_num = 'A'
	times = ''
	lottery_date = ''
	one_unit = ''
	one_amount = ''
	two_unit = ''
	two_amount = ''
	three_unit = ''
	three_amount = ''
	four_unit = ''
	four_amount = ''
	five_unit = ''
	five_amount = ''
	sales = ''
	num_set = ''
	carryover = ''
	node.xpath('//th').each do |th|
		class_name = th["class"]
	end
	#node.xpath('//td').each do |td|
	node.xpath('//td | //th').each do |td|
		class_name = td["class"]
		if class_name == 'alnCenter bgf7f7f7' then
			times = td.inner_text.gsub(/(第|回)/, "")
		end
		if class_name == 'alnCenter' then
			p td.inner_text
			lottery_date = td.inner_text.gsub(/(月|年)/, "/").gsub(/日/, "")
		end
		if class_name == 'alnCenter extension' then
			#p '01 ' + td.inner_text
			if idxNum == 0 then
				lt_num = td.inner_text
			end
			if idxNum == 1 then
				lt_num = lt_num + ' ' + td.inner_text
				#p '02 ' + td.inner_text
			end
			if idxNum == 2 then
				lt_num = lt_num + ' ' + td.inner_text
			end
			if idxNum == 3 then
				lt_num = lt_num + ' ' + td.inner_text
			end
			if idxNum == 4 then
				lt_num = lt_num + ' ' + td.inner_text
			end
			if idxNum == 5 then
				lt_num = lt_num + ' ' + td.inner_text
			end
			idxNum = idxNum + 1
		end
		if class_name == 'alnCenter extension green' then
			#p 'B  ' + td.inner_text
			p lt_num + '  B ' + td.inner_text
			num_set = lt_num.gsub(/ /, ",") + td.inner_text.gsub(/  B /, "").gsub(/\)/, "").gsub(/\(/,",")
			p num_set
			lt_num = ''
			idxNum = 0
		end
		if class_name == 'alnRight' then
			if idxNum == 0 then
				one_unit = td.inner_text.gsub(/(口|,)/, "").gsub(/該当なし/, "0")
			end
			if idxNum == 1 then
				one_amount = td.inner_text.gsub(/(円|,)/, "").gsub(/該当なし/, "0")

			end
			if idxNum == 2 then
				two_unit = td.inner_text.gsub(/(口|,)/, "").gsub(/該当なし/, "0")

			end
			if idxNum == 3 then
				two_amount = td.inner_text.gsub(/(円|,)/, "").gsub(/該当なし/, "0")

			end
			if idxNum == 4 then
				three_unit = td.inner_text.gsub(/(口|,)/, "").gsub(/該当なし/, "0")

			end
			if idxNum == 5 then
				three_amount = td.inner_text.gsub(/(円|,)/, "").gsub(/該当なし/, "0")

			end
			if idxNum == 6 then
				four_unit = td.inner_text.gsub(/(口|,)/, "").gsub(/該当なし/, "0")

			end
			if idxNum == 7 then
				four_amount = td.inner_text.gsub(/(円|,)/, "").gsub(/該当なし/, "0")

			end
			if idxNum == 8 then
				five_unit = td.inner_text.gsub(/(口|,)/, "").gsub(/該当なし/, "0")

			end
			if idxNum == 9 then
				five_amount = td.inner_text.gsub(/(円|,)/, "").gsub(/該当なし/, "0")

			end
			if idxNum == 10 then
				sales = td.inner_text.gsub(/(円|,)/, "")

			end
			if idxNum == 11 then
				carryover = td.inner_text.gsub(/(円|,)/, "")

			end
			idxNum = idxNum + 1
		end
		if idxNum >= 12 then
			result = 0
			cnt = 0
			result = db.exec(
					  "SELECT COUNT(*) AS times_cnt FROM lotteries WHERE times = $1", [times]
					)
			cnt = result[0]['times_cnt']
			if 0 < cnt.to_i then
				msg = times << 'times exist row[' << result[0]['times_cnt'] << ']'
				p msg
			else
				msg = times << 'times nothing!!'
				p msg
				createupdate_date = Time.now
				db.exec_prepared("insertsql", [lottery_date, times.to_i, num_set \
								, one_unit, one_amount, two_unit, two_amount \
								, three_unit, three_amount, four_unit, four_amount \
								, five_unit, five_amount, carryover, sales \
								, createupdate_date, createupdate_date] )
			end

			#one = one_unit << ' ' << one_amount
			#two = two_unit << ' ' << two_amount
			#three = three_unit << ' ' << three_amount
			#four = four_unit << ' ' << four_amount
			#five = five_unit << ' ' << five_amount
			#p times
			#p lottery_date
			#p one
			#p two
			#p three
			#p four
			#p five
			#p sales
			#p carryover

			idxNum = 0
		end
	end
#	p 'end typeTK loop'
	break
	#p node.css('td')["center bgf7f7f7"].inner_text
	# p node.css('td').inner_text
end

# タイトルを表示
#p doc.title
