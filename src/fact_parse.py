#The following fuction will take the following parameters:
#A HTML page with the island info

#And it will produce:
#A timestamp of when the fuction was executed in Local Time in a form of struct_time
#The type of data produced by the function in a form of a string "fact"
#The yoweb location of the page in a form of a string "ocean"
#A tuple of tuples in a form of ((light_total, light_online, light_island), (dark_total, dark_online, dark_island))
#A tuple of tuples in a form of 
#	((time, (atc_fact, atc_ship), (def_fact, def_ship), (isld_1, isld_2), (winner, cond))*)

from bs4 import BeautifulSoup
import time

def fact_parse(page, url):

	timest = time.localtime()
	page_type = "fact"
	loc = ""
	faction_control = []
	battles = []
	soup = BeautifulSoup(page, "html.parser")
	
	loc = url[url.index('/')+2:url.index('.')]
	
	if soup.title.get_text() != "Balance of Power":
		print("Invalid Faction Page")
		return None

	stats = [x.find_all("td") for x in soup.find_all("table")[1].find_all("tr")[3:]]
	faction_control = ((stats[0][1].get_text(), stats[1][1].get_text(), stats[2][1].get_text()),
		(stats[0][2].get_text(), stats[1][2].get_text(), stats[2][2].get_text()))
	
	battle_table = soup.find_all("table")[4].find_all("tr")
	
	for i in battle_table:
		atc, defn = [(x.img.get("src")[19:-7], x.get_text()[1:]) for x in i.find_all("b")]
		for j in i.find_all("b"): j.replaceWith("")
		text = i.get_text().split('\n')
		battle_time = text[6].strip()[:-1]
		battle_place = text[7].strip()[18:-1].split(" and ")
		winner = text[9].strip()[4:-1].split(" vessel ")
		winner[0] = 0 if winner[0] == "attacking" and winner[1] != "was sunk" else 1
		winner[1] = {"won":"battle", "disengaged":"disengage", "was sunk":"sink"}[winner[1]]
		battles.append((battle_time, atc, defn, battle_place, winner))

	return (timest, page_type, loc, loc + "_stats", faction_control, battles)
