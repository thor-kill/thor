from bs4 import BeautifulSoup
from datetime import datetime

def trph_parse(page, url):

	timest = datetime.utcnow().utctimetuple()
	page_type = "trph"
	loc = ""
	pirt_name = ""
	trophies = []
	
	soup = BeautifulSoup(page, "html.parser")

	loc = url[url.index('/')+2:url.index('.')]

	pirt_name = url[url.index('=')+1:url.index('&')]

	for i in soup.find_all("td", valign="top", align="center", width="100"):
		trophies.append(i.find_all("b")[0].get_text())
	

	final = (timest, page_type, loc, pirt_name, trophies)
	return final
