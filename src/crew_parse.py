#The following fuction will take the following parameters:
#A HTML page with the crew info

#And it will produce:
#A timestamp of when the fuction was executed in Universal Time in a form of struct_time
#The type of data produced by the function in a form of a string "crew"
#The yoweb location of the page in a form of a tuple (ocean, id)
#Crew name in a form of a string
#The flag the crew belongs to in a form of a tuple of strings (flag_name, flag_id)
#The date the crew was founded in a form of a tuple of strings (year, month, day)
#The crews fame in a form of a string
#The crews battle rank in a form of a string
#The crew public statement in a form of a string
#The crews reputation in a form of a tuple of strings (conq, expl, patr, magn)
#The crews politics in a form of a string
#The crews booty shares in a form of a string
#The crews restocking % in a form of an int
#Crews members in a form of a tuple of tuples of strings
#	((capt*), (sen_off*), (fle_off*), (off*), (pir*), (cab*))
#Extend public statement in a form of a string
#If at any point the fuction dicovers that a valid crew page was not provided it will return None

#Optional / Not yet implamented
#Dormant members
#Battle stats

from bs4 import BeautifulSoup
from datetime import datetime

def crew_parse(page, url):
	dormant = False
	battle = False
	
	timest = datetime.utcnow().utctimetuple()
	page_type = "crew"
	loc = ["", ""]
	crew_name = ""
	flag = ["", ""]
	founded = ["", "", ""]
	fame = ""
	rank = ""
	pub_stm = ""
	rep = ["", "", "", ""]
	pol = ""
	booty = ""
	stock = 0
	members = [[], [], [], [], [], []]
	ext_stm = ""
	
	soup = BeautifulSoup(page, "html.parser")
	
	loc[0] = url[url.index('/')+2:url.index('.')]
	loc[1] = url[url.index('=')+1:]
	
	if soup.title.get_text() != "Crew Info":
		print("Invalid Crew Page")
		return None
	
	if soup.font.get_text() == "Shiver me timbers: No such crew.":
		print("Invalid Crew Page")
		return None
	
	tables = soup.table.find_all("table")
	curr_t = tables[0]
	crew_name = curr_t.b.get_text()
	for x in str(curr_t.find_all('a')).split(','):
		if "flagid" in x:
			flag = (x[x.index("\">")+2:x.index("</a>")],
			x[x.index("flagid=")+7:x.index("&")])
		elif "battleinfo.wm" in x:
			rank = x[x.index("\">")+2:x.index("</a>")]
		elif "top_fame" in x:
			fame = x[x.index("\">")+2:x.index("</a>")]
	
	founded = curr_t.find_all("font", size="-2")[0].get_text().split(' ')
	founded = (founded[4], founded[6], founded[7])
	
	if "Public Statement" in str(curr_t.find_all("font", color="#958A5F", size="-1")):
		pub_stm = curr_t.get_text().split('\n')
		while '' in pub_stm:
			pub_stm.remove('')
		pub_stm = pub_stm[-2].strip(' ')
	
	curr_t = tables[2].get_text().split('\n')
	while '' in curr_t:
		curr_t.remove('')
	rep = (curr_t[1], curr_t[2], curr_t[3], curr_t[4])
	pol = curr_t[5].split(' ')[1]
	booty = curr_t[6][14:]
	stock = int(curr_t[21][17:-2])
	
	curr_t = tables[6].get_text().split('\n')
	while '' in curr_t:
		curr_t.remove('')
	while "\xa0" in curr_t:
		curr_t.remove("\xa0")
	mode = 0
	ranks = ("Captain", "Senior Officer", "Fleet Officer", "Officer", "Pirate", "Cabin Person")
	for x in curr_t:
		if x in ranks:
			mode = ranks.index(x)
		elif x in ("Jobbing Pirate", "Dormant members"):
			break;
		else:
			members[mode].append(x)
	for x in range(6):
		members[x] = tuple(members[x])
	members = tuple(members)
	
	if "Extended Public Statement" in tables[-1].get_text():
		curr_t = tables[-1].get_text().strip('\n')
		curr_t = curr_t[curr_t.index("Extended Public Statement")+len("Extended Public Statement"):]
		curr_t = curr_t.replace("\n\n", '\n').strip('\n').strip(' ')
		ext_stm = curr_t
	
	final = (timest, page_type, tuple(loc), crew_name, flag, founded, fame, rank, pub_stm, rep, pol, booty, stock, members, ext_stm, dormant, battle)
	return final
