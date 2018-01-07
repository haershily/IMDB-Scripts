import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

class Film():
	def __init__(self):
		self.rank=""
		self.title=""
		self.year=""
		self.rating=""
		self.link=""
		

def get_top_250_film_list():

	driver=webdriver.Chrome('/Users/harshilyadav/Downloads/chromedriver')
	driver.get('https://www.google.com')
	sleep(1)

	search_query=driver.find_element_by_name('q')
	search_query.send_keys('IMDB')
	sleep(0.5)

	search_query.send_keys(Keys.RETURN)
	sleep(1)

	imdb_url=driver.find_element_by_tag_name('cite').text
	driver.get('https://'+imdb_url)
	sleep(1)

	driver.find_element_by_xpath('//*[@id="footer"]/div[2]/div/div[3]/div/div[1]/ul/li[2]/a').click()
	sleep(1)

	soup=BeautifulSoup(driver.page_source,'lxml')

	table=soup.find('table',class_='chart')

	film_list=[]

	for td1,td2 in zip(table.find_all('td',class_='titleColumn'),table.find_all('td',class_='ratingColumn imdbRating')):
		full_title=td1.text.strip().replace('\n','').replace('      ','')

		rank=full_title.split('.')[0]
		#print('Rank : '+rank)

		title=full_title.split('.')[1].split('(')[0]
		#print('Title : '+title)

		year=full_title.split('(')[1][:-1]
		#print('Year : '+year)

		rating=td2.text.strip()
		#print('Rating : '+rating)

		a=td1.find('a')
		#print('URL : '+a['href'])

		#print('\n')

		new_film=Film()
		new_film.rank=rank
		new_film.title=title
		new_film.year=year
		new_film.rating=rating
		new_film.link=a['href']

		film_list.append(new_film)

		writer.writerow([new_film.rank,
							new_film.title,
							new_film.year,
							new_film.rating,
							new_film.link])

	driver.quit()

	return film_list

# def get_top_250_film_poster(film_list):

# 	driver=webdriver.Chrome('/Users/harshilyadav/Downloads/chromedriver')

# 	for film in film_list:

# 		url='http://www.imdb.com/'+film.link
# 		driver.get(url)

# 		soup=BeautifulSoup(driver.page_source,'lxml')

# 		div=soup.find('div',class_='poster')

# 		a=div.find('a')

# 		#print('http://www.imdb.com/'+a['href'])

# 		url='http://www.imdb.com/'+a['href']

# 		driver.get(url)

# 		soup=BeautifulSoup(driver.page_source,'lxml')

# 		all_div=soup.find_all('div',class_='pswp__zoom-wrap')

# 		all_img=all_div[1].find_all('img')

# 		#print(all_img[1]['src'])

# 		f=open(str.encode(film.title.replace(':',''))+b'.jpg','wb')
# 		f.write(requests.get(all_img[1]['src']).content)
# 		f.close()

# 	driver.quit()


writer=csv.writer(open('Top_250_Films.csv', 'w'))
writer.writerow(['Rank','Title','Year','Rating','URL'])

film_list=get_top_250_film_list()

for film in film_list:
	print(film.title)
	print(film.rank)
	print(film.year)
	print(film.rating)
	print(film.link)
	print('\n')

#get_top_250_film_poster(film_list)



