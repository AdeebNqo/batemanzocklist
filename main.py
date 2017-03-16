from bs4 import BeautifulSoup
import requests
import string

BatemanListUrl = 'http://www.nlg-wiki.org/systems/Table_of_NLG_systems'

def get_page(url):
	r  = requests.get(url)
	return BeautifulSoup(r.text, 'lxml')

def get_headers(row):
	return get_cells(row, 'th')

def get_values(row):
	return get_cells(row, 'td')

def get_languages(somestring):
	languages = []
	left = 0
	for i in range(1,len(somestring)):
		if str(somestring[i]).isupper():
			languages.append(somestring[left:i])
			left = i
	return languages

def get_cells(row, tmp):
	return_vals = []
	vals = row.find_all(tmp)
	i=0
	for val in vals:
		if i==3 and tmp=='td':
			return_vals.append(get_languages(val.text))
		else:
			return_vals.append(val.text)
		i = i +1
	return return_vals

def get_batemanlist():
	systems = []
	table_page_soup = get_page(BatemanListUrl)
	tables = table_page_soup.find_all('table', attrs={'class':'smwtable'})
	table = tables[0] if len(tables)==1 else None 
	if table:
		rows = table.find_all('tr')
		headers = get_headers(rows[0])
		for i in range(1,len(rows)):
			values = get_values(rows[i])
			systems.append(dict(zip(headers, values)))
	return systems

if __name__=='__main__':
	import json
	print json.dumps(get_batemanlist())