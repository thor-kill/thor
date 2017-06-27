#The following fuction will take the following parameters:
#A HTML page with the battle log info

#And it will produce:
#A timestamp of when the fuction was executed in Local Time in a form of struct_time
#The type of data produced by the function in a form of a string "dorm"
#The yoweb location of the page in a form of a tuple (ocean, id)
#Crew name in a form of a string
#Battle stats in a form of a tuple of tuples (((year,month,day),battles,wins,loss,pvp_w,pvp_l,(avg_min, avg_sec))*)
#PVP stats in a form of a tuple of tuples 
#	(((year,month,day,hour,minutes),attacking,(friedlies, enemies),
#	(enemy_crew, enemy_crew_id),(friendly_ship_type,friendly_ship_name),(enemy_ship_type,enemy_ship_name),
#	winner,victory_type))*)
#	vitory type if only of the following: "disengaged", "sunk", "{} PoE:{} Goods"

from bs4 import BeautifulSoup
import time

def batt_parse(page, url):
	
	timest = time.localtime()
	page_type = "batt"
	loc = ["",""]
	crew_name = ""
	battle_stats = []
	pvp_stats = []

	soup = BeautifulSoup(page, "html.parser")

	loc[0] = url[url.index('/')+2:url.index('.')]
	loc[1] = url[url.index('=')+1:]

	if soup.title.get_text() != "Crew Battle Records":
		print("Invalid Battle Records Page")
		return None
	
	if soup.font.get_text() == "Shiver me timbers: No such crew.":
		print("Invalid Battle Records Page")
		return None

	crew_name = soup.a.get_text()
	
	battle_table = soup.find_all("table")[0].find_all('tr')[2:]
	for i in battle_table:
		if soup.tr.get_text() != "Overall battle stats": break #breaks if there are only pvp stats
		t = []
		td = i.find_all('td')
		t.append(td[0].get_text().split('-'))
		t.append(td[1].get_text())
		t.append(td[2].get_text())
		t.append(td[3].get_text())
		t.append(td[4].get_text())
		t.append(td[5].get_text())
		if len(td[6].get_text().split()) == 2:
			t.append([td[6].get_text().split()[0]])
		else:
			t.append([td[6].get_text().split()[0],td[6].get_text().split()[2]])
		battle_stats.append(t)
	
	try:
		pvp_table = soup.find_all("table")[1].find_all('tr')
		pvp_table.pop(0)
		if len(pvp_table) == 0:
			final = (timest, page_type, tuple(loc), crew_name, tuple(battle_stats), tuple(pvp_stats))
			return final
	except:
		final = (timest, page_type, tuple(loc), crew_name, tuple(battle_stats), tuple(pvp_stats))
		return final
	
	for i in pvp_table[0].find_all('i'):
		t = i.get_text().split()
		months = ['January','February','March','April','May','June','July',
			'August','September','October','November','December']
		date = [t[1].split(':')[0], t[1].split(':')[1][:2], t[1].split(':')[1][2:]]
		if date[2] == "PM": date[0] = int(date[0]) + 12
		if date[2] == "AM" and date[0] == "12": date[0] = int(date[0]) - 12
		date[0] = str(date[0])
		pvp_stats.append([[t[-1][:-1], months.index(t[-2])+1, t[-3], date[0], date[1]]])
	
	pvp_table = pvp_table[0].find_all('td')
	for i in range(5, len(pvp_table), 6):
		pvp_table[i] = None
	while None in pvp_table:
		pvp_table.pop(pvp_table.index(None))
	
	for i in range(0, len(pvp_table), 5):
		log_loc = []
		enemy_crew = ["", ""]
		friendly_ship = ["", ""]
		enemy_ship = ["", ""]
		if crew_name == pvp_table[i+1].a.get_text():
			log_loc.append(True)
			log_loc.append([pvp_table[i+1].get_text().split()[0], pvp_table[i+3].get_text().split()[0]])
			enemy_crew[0] = pvp_table[i+3].a.get_text()
			enemy_crew[1] = pvp_table[i+3].a.get("href")[pvp_table[i+3].a.get("href").index('=')+1:
				pvp_table[i+3].a.get("href").index('&')]
			log_loc.append(enemy_crew)
			friendly_ship[0] = pvp_table[i+1].font.get_text()[pvp_table[i+1].font.get_text().index("'")+1:-1]
			friendly_ship[1] = pvp_table[i+1].font.get_text()[7:pvp_table[i+1].font.get_text().index("'")-1]
			log_loc.append(friendly_ship)
			enemy_ship[0] = pvp_table[i+3].font.get_text()[pvp_table[i+3].font.get_text().index("'")+1:-1]
			enemy_ship[1] = pvp_table[i+3].font.get_text()[7:pvp_table[i+3].font.get_text().index("'")-1]
			log_loc.append(enemy_ship)
		else:
			log_loc.append(False)
			log_loc.append([pvp_table[i+3].get_text().split()[0], pvp_table[i+1].get_text().split()[0]])
			enemy_crew[0] = pvp_table[i+1].a.get_text()
			enemy_crew[1] = pvp_table[i+1].a.get("href")[pvp_table[i+1].a.get("href").index('=')+1:
				pvp_table[i+1].a.get("href").index('&')]
			log_loc.append(enemy_crew)
			friendly_ship[0] = pvp_table[i+3].font.get_text()[pvp_table[i+3].font.get_text().index("'")+1:-1]
			friendly_ship[1] = pvp_table[i+3].font.get_text()[7:pvp_table[i+3].font.get_text().index("'")-1]
			log_loc.append(friendly_ship)
			enemy_ship[0] = pvp_table[i+1].font.get_text()[pvp_table[i+1].font.get_text().index("'")+1:-1]
			enemy_ship[1] = pvp_table[i+1].font.get_text()[7:pvp_table[i+1].font.get_text().index("'")-1]
			log_loc.append(enemy_ship)
		
		if pvp_table[i+4].parent.get("bgcolor") == "#FFFFFF":
			log_loc.append(True)
		elif pvp_table[i+4].parent.get("bgcolor") == "#CCCCCC":
			log_loc.append(False)

		if pvp_table[i+4].get_text().split()[-1] == "sunk":
			log_loc.append("sunk")
		elif pvp_table[i+4].get_text().split()[-1] == "disengaged":
			log_loc.append("disengaged")
		elif pvp_table[i+4].get_text().split()[-1] == "POE":
			log_loc.append("{} PoE:0 Goods".format(pvp_table[i+4].get_text().split()[-2]))
		else:
			log_loc.append("{} PoE:{} Goods".format(pvp_table[i+4].get_text().split()[-7].replace(',', ''), 
				pvp_table[i+4].get_text().split()[-4].replace(',', '')))
		pvp_stats[int(i/5)] = pvp_stats[int(i/5)] + log_loc

	final = (timest, page_type, tuple(loc), crew_name, tuple(battle_stats), tuple(pvp_stats))
	return final
