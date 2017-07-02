#The following fuction will take the following parameters:
#A HTML page with the pirate info

#And it will produce:
#A timestamp of when the fuction was executed in Local Time in a form of struct_time
#The type of data produced by the function in a form of a string "pirt"
#The ocean the pirate is located in a form of a string
#Pirate name in a form of a string
#The pirates crew in a form a tuple of strings (rank, crew_name, crew_id)
#The pirates flag in a form a tuple of strings (rank, flag_name, flag_id)
#All the islands governed by the pirate in a form of a tuple (isld*)
#The pirates navy status in a form of a tuple (rank, isld, arch)
#The pirates reputation in a form of a tuple of strings (conq, expl, patr, magn)
#Shoppes owned/managed by the pirate in a form of a tuple of tuples of strings
#	((own_man, type, shoppe_full_name)*)
#Stalls owned/managed by the pirate in a for of a tuple of tuples of strings
#	((own_man, stall_full_name)*)
#Houses the pirate lives in a form of tuple of tuples of stings
#	((own_room, type, house_full_name)*)
#Familiars owned by the pirate in a form of a tuple of tuple of a string and a tuple
#	((name, (component, color))*)
#All the public pirates hearties in a form of a tuple of strings (heart*)
#Pirates skills in a form of a tuple of tuples of strings
#	((pirt_skills*), (carous_skills*), (craft_skills*))
#If at any point the fuction dicovers that a valid crew page was not provided it will return None
#Side on Obsidian

from bs4 import BeautifulSoup
import time

def pirt_parse(page, url):
	trophies = False
	
	timest = time.localtime()
	page_type = "pirt"
	loc = ""
	pirt_name = ""
	crew = ["", "", ""]
	flag = ["", "", ""]
	govern = []
	navy = ["", "", ""]
	rep = ["", "", "", ""]
	shoppes = []
	stalls = []
	houses = []
	fam = []
	heart = []
	skills = [[], [], []]
	side = ""
	
	soup = BeautifulSoup(page, "html.parser")
	
	loc = url[url.index('/')+2:url.index('.')]
	
	if soup.title.get_text() != "Personal Pirate Page":
		print("Invalid Pirate Page")
		return None
	
	if soup.center != None:
		print("Invalid Pirate Page")
		return None
	
	pirt_name = soup.find_all("td", align="center", height="32")[0].get_text()
	
	tables = soup.table.find_all("table")
	curr_t = tables[1]
	
	tr = curr_t.find_all("tr")
	if tr[0].get_text().strip('\n') != "Independent Pirate":
		if len(tr) >= 2:
			rank = tr[0].find_all('b')[0].get_text()
			crew_name = tr[0].find_all('b')[-1].get_text()
			crew_id = str(tr[0].a)
			crew_id = crew_id[crew_id.index("crewid=")+7:crew_id.index('&')]
			crew = (rank, crew_name, crew_id)
		if len(tr) >= 3:
			rank = tr[1].find_all('b')[0].get_text()
			flag_name = tr[1].find_all('b')[-1].get_text()
			flag_id = str(tr[1].a)
			flag_id = flag_id[flag_id.index("flagid=")+7:flag_id.index('&')]
			flag = (rank, flag_name, flag_id)
		if len(tr) == 4:
			gov = tr[2].get_text().strip('\n').split('\n')[1]
			if ',' in gov:
				for x in gov.split(','):
					govern.append(x.strip(' '))
			else:
				govern.append(gov.strip(' '))
	crew = tuple(crew)
	flag = tuple(flag)
	govern = tuple(govern)
	
	navy[0] = tr[-1].b.get_text().strip(' ')
	navy[1] = tr[-1].get_text()
	navy[2] = navy[1][navy[1].index(" Navy in the ")+13:].strip('\n').strip(' ').strip('\n')
	navy[1] = navy[1][navy[1].index(" in the ")+8:navy[1].index(" Navy in the ")]
	navy = tuple(navy)
	
	curr_t = tables[2].get_text().split('\n')
	while '' in curr_t:
		curr_t.remove('')
	rep = (curr_t[0], curr_t[1], curr_t[2], curr_t[3])
	
	curr_t = tables[3]
	if "Owns" in str(curr_t) or "Manages:" in str(curr_t):
		for x in curr_t.find_all("tr"):
			shp_type = x.img["src"][x.img["src"].index("images/")+7:x.img["src"].index(".png")]
			own_man = x.b.get_text()[:-1]
			shoppe = x.get_text().strip('\n').strip(' ').strip('\n')
			shoppe = shoppe.split(':')[1].strip(' ')
			shoppes.append((own_man, shp_type, shoppe))
	if "<b>Familiars</b>" in str(curr_t) or "<b>Familiars</b>" in str(curr_t):
		tr = curr_t.find_all("tr")
		for x in tr:
			x = str(x)
			if "<td width=\"36\">" in x:
				fam_name = x[x.index("<b>")+3:x.index("</b>")]
				fam_stat1 = x[x.index("component=")+10:x.index("char")-5]
				fam_stat2 = x[x.index("color=")+6:x.index("\" width=\"36\"")]
				fam.append((fam_name, (fam_stat1, fam_stat2)))
		if tr[-2].get_text().strip('\n') == "Hearties":
			for x in tr[-1].find_all('a'):
				heart.append(x.get_text())
	curr_t = tables[4]
	if "<b>Familiars</b>" in str(curr_t) or "<b>Familiars</b>" in str(curr_t):
		tr = curr_t.find_all("tr")
		for x in tr:
			x = str(x)
			if "<td width=\"36\">" in x:
				fam_name = x[x.index("<b>")+3:x.index("</b>")]
				fam_stat1 = x[x.index("component=")+10:x.index("char")-5]
				fam_stat2 = x[x.index("color=")+6:x.index("\" width=\"36\"")]
				fam.append((fam_name, (fam_stat1, fam_stat2)))
		if tr[-2].get_text().strip('\n') == "Hearties":
			for x in tr[-1].find_all('a'):
				heart.append(x.get_text())
	shoppes = tuple(shoppes)
	fam = tuple(fam)
	heart = tuple(heart)
	
	curr_t = tables[0].find_all('p', align="center", width="188")
	for x in curr_t:
		if "images/shop-" in str(x):
			for y in x.find_all("img"):
				if "-managed-" in y["src"]:
					stalls.append(("Manages", y["title"]))
				else:
					stalls.append(("Owns", y["title"]))
		else:
			for y in x.find_all("img"):
				house_type = y["src"][y["src"].index("images/")+7:y["src"].index(".png")]
				if "_roomate." in y["src"]:
					houses.append(("Roomate", house_type, y["title"]))
				else:
					houses.append(("Owns", house_type, y["title"]))
	stalls = tuple(stalls)
	houses = tuple(houses)
	
	curr_t = tables[-3].get_text().split('\n')
	for x in curr_t:
		if '/' in x:
			skills[0].append(x.strip(' '))
	curr_t = tables[-2].get_text().split('\n')
	for x in curr_t:
		if '/' in x:
			skills[1].append(x.strip(' '))
	curr_t = tables[-1].get_text().split('\n')
	for x in curr_t:
		if '/' in x:
			skills[2].append(x.strip(' '))
	
	skills[0], skills[1], skills[2] = tuple(skills[0]), tuple(skills[1]), tuple(skills[2])
	skills = tuple(skills)
	
	if soup.find(alt="Shadow Fleet") != None:
		side = "dark"
	elif soup.find(alt="Defiant Armada") != None:
		side = "light"
	else:
		side = None

	final = (timest, page_type, loc, pirt_name, crew, flag, govern, navy, rep, shoppes, stalls, houses, fam, heart, skills, side)
	return final
