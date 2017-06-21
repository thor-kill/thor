#The following fuction will take the following parameters:
#A HTML page with the island info

#And it will produce:
#A timestamp of when the fuction was executed in Universal Time in a form of struct_time
#The type of data produced by the function in a form of a string "flag"
#The yoweb location of the page in a form of a tuple (ocean, id)
#Flag name in a form of a string
#The date the flag was founded in a form of a tuple of strings (year, month, day)
#The flags fame in a form of a string
#The flag public statement in a form of a string
#The flags reputation in a form of a tuple of strings (conq, expl, patr, magn)
#The flags relation with other flags in a form of a tuple of tuples of tuples of strings
#	(((ally_w, id)*), ((ally_t, id)*), ((truce, id)*), ((dec_war, id)*), ((at_war, id)))
#Islands controlled by the flag in a form of a tuple of tuples of strings ((isld, id)*)
#The flags royalty in a form a tuple of tuples of tuple of strings
#	(((mona, crew)*), ((roya, crew)*), ((titl, crew)*))
#All the crews belonging to the flag in a form of a tuple of tuples of two strings and a tuple of ints
#	((crew, id, (c, p, o, fo, so, cap))*)
#The extended public statement in a form of a string
#If at any point the fuction dicovers that a valid flag page was not provided it will return None

from bs4 import BeautifulSoup
from datetime import datetime

def flag_parse(page, url):
	timest = datetime.utcnow().utctimetuple()
	page_type = "flag"
	loc = ["", ""]
	flag_name = ""
	founded = ["", "", ""]
	fame = ""
	pub_stm = ""
	rep = ["", "", "", ""]
	relay = [[], [], [], [], []]
	isld_ctrl = []
	royal = [[], [], []]
	flg_crw = []
	ext_stm = ""
	
	soup = BeautifulSoup(page, "html.parser")
	
	loc[0] = url[url.index('/')+2:url.index('.')]
	loc[1] = url[url.index('=')+1:]
	
	if soup.title.get_text() != "Flag Info":
		print("Invalid Flag Page")
		return None
	
	if soup.font.get_text() == "Shiver me timbers: No such flag.":
		print("Invalid Flag Page")
		return None
	
	tables = soup.table.find_all("table")
	curr_t = tables[0].get_text().split('\n')
	while "" in curr_t:
		curr_t.remove('')
	flag_name = curr_t[0]
	founded[0], founded[1], founded[2] = curr_t[1].split()[4], curr_t[1].split()[6], curr_t[1].split()[7]
	founded = tuple(founded)
	fame = curr_t[2]
	if "Public Statement" in curr_t:
		pub_stm = curr_t[4].strip(' ')
	else:
		pub_stm = ""
	
	curr_t = tables[3].get_text().split('\n')
	while "" in curr_t:
		curr_t.remove('')
	for x in range(4):
		rep[x] = curr_t[x]
	rep = tuple(rep)
	
	curr_t = tables[2].find_all("td", bgcolor="#CDCEB5", width="246", align="left")[1]
	curr_t = str(curr_t).split('\n')
	curr_t = curr_t[1:-2]
	key_wrd = ("Allied with:", "Trying to form an alliance with:", "Offering a truce to:", 
	"Declaring war against:", "At war with:", "Islands controlled by this flag:")
	mode = 0
	if len(curr_t) != 0:
		for l in range(len(curr_t)):
			titl = curr_t[l][curr_t[l].index("\">")+2:curr_t[l].index("</")]
			if curr_t[l][:2] == "<a":
				if "flagid" in curr_t[l]:
					lnk = curr_t[l][curr_t[l].index("id=")+3:curr_t[l].index('&')]
				else:
					lnk = curr_t[l][curr_t[l].index("id=")+3:curr_t[l].index('">')]
			if titl in key_wrd:
				mode = key_wrd.index(titl)
			else:
				if mode != 5:
					 relay[mode].append((titl, lnk))
				else:
					isld_ctrl.append((titl, lnk))
	relay = tuple(relay)
	isld_ctrl = tuple(isld_ctrl)
	
	curr_t = tables[4].get_text().split('\n')
	while "" in curr_t:
		curr_t.remove("")
	key_wrd = ("Monarch", "Royalty", "Titled Members")
	mode = 0
	if len(curr_t) != 0:
		for l in range(len(curr_t)):
			if curr_t[l] in key_wrd:
				mode = key_wrd.index(curr_t[l])
			else:
				royal[mode].append((curr_t[l][:curr_t[l].index(' ')], curr_t[l][curr_t[l].index('\''):-1].strip('\'')))
	royal[0], royal[1], royal[2] = tuple(royal[0]), tuple(royal[1]), tuple(royal[2])
	royal = tuple(royal)
	
	curr_t = tables[-1].find_all("tr")[1:]
	for tr in range(len(curr_t)):
		curr_t[tr] = str(curr_t[tr].find_all('td'))
		curr_t[tr] = curr_t[tr].split("</td>")[:-1]
	
	for x in curr_t[:-1]:
		i = x[0][x[0].index("id=")+3:x[0].index('&')]
		n = x[0][x[0].index("$classic\">")+10:x[0].index('</a>')]
		p = [0, 0, 0, 0, 0, 0]
		x = x[2:-1]
		for y in range(len(x)):
			if "<font" in x[y]:
				p[y] = x[y][x[y].index("-1\">")+4:x[y].index("</f")]
			else:
				p[y] = 0
		flg_crw.append((n, i, tuple(p)))
	flg_crw = tuple(flg_crw)
	
	curr_t = tables[-2]
	if curr_t.i != None:
		curr_t = curr_t.get_text()
		curr_t = curr_t[curr_t.index("Extended Public Statement")+len("Extended Public Statement"):]
		curr_t = curr_t.replace("\n\n", '\n').strip('\n').strip(' ')
		ext_stm = curr_t
	else:
		ext_stm = ""
	
	final = (timest, page_type, tuple(loc), flag_name, founded, fame, pub_stm, rep, relay, isld_ctrl, royal, flg_crw, ext_stm)
	return final
