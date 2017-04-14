"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.
"""

author = ["Thorkill"]
version = "0.1.1"

#The following fuction will take the following parameters:
#A HTML page with the island info

#And it will produce:
#A timestamp of when the fuction was executed in Universal Time in a form of struct_time
#The type of data produced by the function in a form of a string "isld"
#The yoweb location of the page in a form of a tuple (ocean, id)
#Island name in a form of a tuple of strings (isld_name, arch)
#Population in a form of an int
#Ruler in a form of a tuple of strings (flag_name, flag_id)
#Exports in a form of a tuple of strings (exprt*)
#If at any point the fuction dicovers that a valid island page was not provided it will return None

from bs4 import BeautifulSoup
from datetime import datetime

def isld_parse(page, url):
	timest = datetime.utcnow().utctimetuple()
	page_type = "isld"
	loc = ["", ""]
	isld = ["", ""]
	pop = 0
	ruler = ["", ""]
	exprt = []
	
	soup = BeautifulSoup(page, "html.parser")
	
	loc[0] = url[url.index('/')+2:url.index('.')]
	loc[1] = url[url.index('=')+1:]
	
	if soup.title.get_text() != "Island info":
		print("Invalid Island Page")
		return None
	
	name = soup.font
	err = ("Shiver me timbers: No such colonized island", "Shiver me timbers: The island is uncolonized.")
	if name.get_text() in err :
		print("Invalid Island Page")
		return None
	else:
		isld[0] = name.get_text()
	
	info = soup.center
	isld_info = info.center.get_text()
	isld_info = isld_info.split('\n')
	pop = isld_info[2][12:]
	isld[1] = isld_info[3]
	isld[1] = isld[1][isld[1].index("in the ")+7:isld[1].index(" archipelago")]
	
	ruler[0] = info.a.get_text()
	ruler[1] = info.a.get('href')
	ruler[1] = ruler[1][ruler[1].index('=')+1:ruler[1].index('&')]
	
	exports = info.get_text().split('\n')
	exports = exports[exports.index("Exports:")+1:]
	for x in exports:
		if x.strip(' ') not in ('', ','):
			exprt.append(x.strip(' '))
	
	final = (timest, page_type, tuple(loc), tuple(isld), int(pop), tuple(ruler), tuple(exprt))
	return final
