#The following fuction will take the following parameters:
#A HTML page with the fame info

#And it will produce:
#A timestamp of when the fuction was executed in Universal Time in a form of struct_time
#The type of data produced by the function in a form of a string "stat"
#The ocean the fame page is located in a form of a string
#Page title in a form of a string
#A tuple of tuples for standings in a form of ((rank,name,standing)*)
##A tuple of tuples for experience in a form of ((rank,name,experience)*)
#A date of when the page was tabulated in a form of a string

from bs4 import BeautifulSoup
from datetime import datetime

def stat_parse(page, url):
	
	timest = datetime.utcnow().utctimetuple()
	page_type = "fame"
	loc = ""
	stat_name = ""
	stand_table = []
	exp_table = []
	tab_date = ""
	
	soup = BeautifulSoup(page, "html.parser")
	
	loc = url[url.index('/')+2:url.index('.')]

	stat_name = soup.font.get_text()

	table = soup.find_all('tr')[1:]
	for i in table:
		if i.get_text() == "No one has yet achieved Ultimate standing.":
			stand_table = [None]
			exp_table = [None]
			break
		j = i.find_all('td')
		stand_table.append((j[0].get_text(),j[1].get_text(),j[2].get_text()))
		if '\xa0' not in [j[4].get_text(),j[5].get_text()]:
			exp_table.append((j[0].get_text(),j[4].get_text(),j[5].get_text()))

	tab_date = soup.find_all("font")[-1].get_text()

	final = (timest, page_type, loc, stat_name, stand_table, exp_table, tab_date)
	print(final)
	return final
