#The following fuction will take the following parameters:
#A HTML page with the island info

#And it will produce:
#A timestamp of when the fuction was executed in Universal Time in a form of struct_time
#The type of data produced by the function in a form of a string "isld"
#The yoweb location of the page in a form of a string "ocean"
#A tuple of tuples in a form of (("isld", pop, "arch", "gov", tax, ("flagid", "ruler"), ("exp",..)),..())

from bs4 import BeautifulSoup
from datetime import datetime

def isld_parse(page, url):
	timest = datetime.utcnow().utctimetuple()
	page_type = "isld"
	loc = ""
	isld = []
	soup = BeautifulSoup(page, "html.parser")
	
	loc = url[url.index('/')+2:url.index('.')]
	
	if soup.title.get_text() != "Island info":
		print("Invalid Island Page")
		return None
	
	center = soup.center.find_all("center")
	for i in center:
		t = i.get_text().split('\n')
		isl = t[1]
		pop = int(t[2][t[2].index(':')+1:].replace(',',''))
		arch = t[3].split()[3]
		gov = t[4][t[4].index(':')+1:]
		tax = t[5][t[5].index(':')+1:-1]
		f = soup.find_all('a')[len(isld)*2+1]
		flag = [f.get("href")[f.get("href").index('d=')+2:f.get("href").index('&')],f.string]

		isld.append([isl,pop,arch,gov,tax,flag])
	
	while len(soup.center.find_all("center")) != 0:
		soup.center.center.decompose()
		soup.center.a.decompose()
	exports = soup.center.get_text().split('\n')
	exports = [i.strip() for i in exports]
	exports = [i for i in exports if i != '' and i != ',' and i != 'Ruled by']
	
	c = -1
	l = []
	for i in exports:
		if i == "Exports:":
			c = c + 1
			isld[c].append(l)
			l = []
		else:
			l.append(i)
	
	final = (timest, page_type, loc, loc + "_index", tuple(isld))
	return final
