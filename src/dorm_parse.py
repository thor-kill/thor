#The following fuction will take the following parameters:
#A HTML page with the fame info

#And it will produce:
#A timestamp of when the fuction was executed in Universal Time in a form of struct_time
#The type of data produced by the function in a form of a string "dorm"
#The yoweb location of the page in a form of a tuple (ocean, id)
#Crew name in a form of a string
#Crews members in a form of a tuple of tuples of strings
#	((capt*), (sen_off*), (fle_off*), (off*), (pir*), (cab*))

from bs4 import BeautifulSoup
from datetime import datetime

def dorm_parse(page, url):
	
	timest = datetime.utcnow().utctimetuple()
	page_type = "crew"
	loc = ["", ""]
	crew_name = ""
	dormant = [[], [], [], [], [], []]
	
	soup = BeautifulSoup(page, "html.parser")
	
	loc[0] = url[url.index('/')+2:url.index('.')]
	loc[1] = url[url.index('=')+1:]
	
	if soup.title.get_text() != "Dormant Crew Members":
		print("Invalid Dormant Crew Page")
		return None
	
	if soup.font.get_text() == "Shiver me timbers: No such crew.":
		print("Invalid Dormant Crew Page")
		return None

	crew_name = soup.a.get_text()
	
	members = soup.get_text().split('\n')
	members = [i.strip() for i in members]
	members = [i for i in members if i != ''][3:-1]
	
	for i in range(0, len(members), 2):
		if members[i] == "Captain":
			dormant[0].append(members[i+1])
		elif members[i] == "Senior Officer":
			dormant[1].append(members[i+1])
		elif members[i] == "Fleet Officer":
			dormant[2].append(members[i+1])
		elif members[i] == "Officer":
			dormant[3].append(members[i+1])
		elif members[i] == "Pirate":
			dormant[4].append(members[i+1])
		elif members[i] == "Cabin Person":
			dormant[5].append(members[i+1])

	final = (timest, page_type, tuple(loc), crew_name, tuple(dormant))
	print(final)
	return final
