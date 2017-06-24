#The following fuction will take the following parameters:
#A HTML page with the fame info

#And it will produce:
#A timestamp of when the fuction was executed in Universal Time in a form of struct_time
#The type of data produced by the function in a form of a string "fame"
#The ocean the fame page is located in a form of a string
#Page title in a form of a string
#For pirate pages it will produce a tuple in a form of ((rank,name,standing),..())
#For crew/flag pages it will produce a tuple in a form of ((rank,(id,name),standing),..())
#A date of when the page was tabulated in a form of a string

from bs4 import BeautifulSoup
from datetime import datetime

def fame_parse(page, url):
	
	timest = datetime.utcnow().utctimetuple()
	page_type = "fame"
	loc = ""
	fame_name = ""
	table = []
	tab_date = ""

	soup = BeautifulSoup(page, "html.parser")
	
	loc = url[url.index('/')+2:url.index('.')]
	
	fame_name = url[url.index('e_')+2:url.index('.h')]
	if fame_name == "97": fame_name = "CREW_FAME"
	if fame_name == "112": fame_name = "FLAG_FAME"
	
	rows = soup.tr.find_all('tr')	

	if "PIRATE" not in fame_name:
		for i in rows:
			td = i.find_all('td')
			r = ["",[0,""],""]
			r[0] = td[0].get_text()
			r[1][0] = td[1].a.get("href")[td[1].a.get("href").index('=')+1:]
			r[1][1] = td[1].get_text()
			r[2] = td[2].get_text()
			table.append(r)
	else:
		for i in rows:
			td = i.find_all('td')
			r = ["","",""]
			r[0] = td[0].get_text()
			r[1] = td[1].get_text()
			r[2] = td[2].get_text()
			table.append(r)
	
	tab_date = soup.find_all("font")[-1].get_text()

	final = (timest, page_type, loc, fame_name, table, tab_date)
	return final
