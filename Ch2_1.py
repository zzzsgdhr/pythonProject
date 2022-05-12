import pymysql.cursors
import requests
from bs4 import BeautifulSoup
import arrow

urls = [
	u'https://news.so.com/ns?q=北京&pn={}&tn=newstitle&rank=rank&j=0&nso=10&tp=11&nc=0&src=page'
		.format(i) for i in range(10)
]
for i, url in enumerate(urls):
	r = requests.get(url)
	bs1 = BeautifulSoup(r.text)
	items = bs1.find_all('a', class_='news_title')

	t_list = []
	for one in items:
		t_item = []
		if '360' in one.get('href'):
			continue
		t_item.append(one.get('href'))
		t_item.append(one.text)
		date = [one.next_sibling][0].find('span', class_='pdate').text

		if len(date) < 6:
			date = arrow.now().replace(days=-int(date[:1])).date()
		else:
			date = arrow.get(date[:10], 'YYYY-MM-DD').date()

		t_item.append(date)

		t_list.append(t_item)

	connection = pymysql.connect(host='localhost',
	                             user='scraper1',
	                             password='password',
	                             db='DBS',
	                             charset='utf8',
	                             cursorclass=pymysql.cursors.DictCursor)

	try:
		with connection.cursor() as cursor:
			for one in t_list:
				try:
					sql_q = "INSERT INTO `newspost` (`post_title`, `post_url`,`news_postdate`,) VALUES (%s, %s,%s)"
					cursor.execute(sql_q, (one[1], one[0], one[2]))
				except pymysql.err.IntegrityError as e:
					print(e)
					continue

		connection.commit()

	finally:
		connection.close()
