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
version = "0.1"

from .fetch import build

def month_to_number(month):
	months = { "January": '1', "February": '2', "March": '3', "April": '4', "May": '5', "June": '6', 
	"July": '7', "August": '8', "September": '9', "October": "10", "November": "11", "December": "12"}
	return months[month]

def island(json):
	print("Time Taken: %s-%s-%s %s:%s:%s UTF+0" %(tuple(x for x in json[0][:6])))
	print("Island File")
	print("Location: %s" %(build((json[2][0][:4], "isld"), [json[2][1]])[0]))
	print("Island: '%s' (%s Arch)" %(json[3][0], json[3][1]))
	print("Population: %s" %(json[4]))
	print("Ruler: '%s' (%s)" %(json[5][0], build((json[2][0][:4], "flag"), [json[5][1]])[0]))
	
	print("Exports:", end='')
	for x in json[6]: print(" '%s'" %(x), end='')
	print('')

def flag(json):
	print("Time Taken: %s-%s-%s %s:%s:%s UTF+0" %(tuple(x for x in json[0][:6])))
	print("Flag File")
	print("Location: %s" %(build((json[2][0][:4], "flag"), [json[2][1]])[0]))
	print("Name: '%s'" %(json[3]))
	
	json[4][1] = month_to_number(json[4][1])
	print("Founded: %s-%s-%s" %(tuple(x for x in json[4])))
	
	print("Fame: '%s'" %(json[5]))
	print("Public Statement: '%s'" %(json[6]))
	print("Reputation:\n\tConqueror: %s\n\tExplorer: %s\n\tPatron: %s\n\tMagnate: %s" %(tuple(x for x in json[7])))
	
	print("Flag Relations:")
	relations = ("\tAllied With:", "\tTrying to Ally With:", 
	"\tTrying to Form a Truce With:", "\tDeclaring War On:", "\tAt War With:")
	for x in range(len(json[8])):
		print(relations[x], end='')
		for y in json[8][x]: print(" %s" %(y), end='')
		print('')
	
	print("Islands Controlled:")
	for x in json[9]: print("\t'%s' (%s)" %(x[0], build((json[2][0][:4], "isld"), [x[1]])[0]))
	
	print("Flag Royalty:")
	royalty = ("\tMonarch:", "\tRoyalty:", "\tTitled Members:")
	for x in range(len(json[10])):
		print(royalty[x])
		nl = 0
		for y in json[10][x]:
			#Tabbing needs to be fixed
			if nl == 2:
				print('')
				nl = 0
			print("\t\t%s of '%s'" %(y[0], y[1]), end='')
			nl += 1
		print('')
	
	print("Member Crews:")
	for x in json[11]:
		print("\t'%s' (%s)" %(x[0], build((json[2][0][:4], "crew"), [x[1]])[0]))
		print("\t\tCP: %s P: %s O: %s FO: %s SO: %s CAP: %s" %(tuple(x[2])))
	
	print("Extended Public Statement:\n\t'%s'" %(json[12]))

def crew(json):
	print("Time Taken: %s-%s-%s %s:%s:%s UTF+0" %(tuple(x for x in json[0][:6])))
	print("Crew File")
	print("Location: %s" %(build((json[2][0][:4], "crew"), [json[2][1]])[0]))
	print("Name: '%s'" %(json[3]))
	print("Flag: '%s' (%s)" %(json[4][0], build((json[2][0][:4], "flag"), [json[4][1]])[0]))
	
	json[4][1] = month_to_number(json[5][1])
	print("Founded: %s-%s-%s" %(tuple(x for x in json[5])))
	
	print("Fame: '%s'" %(json[6]))
	print("Battle Rank: '%s'" %(json[7]))
	print("Public Statement: '%s'" %(json[8]))
	print("Reputation:\n\tConqueror: %s\n\tExplorer: %s\n\tPatron: %s\n\tMagnate: %s" %(tuple(x for x in json[9])))
	print("Politics: %s" %(json[10]))
	print("Booty Shares: '%s'" %(json[11]))
	print("Restocking Fee: %s %%" %(json[12]))
	print("Crew Numbers: CAP: %s SO: %s FO: %s O: %s P: %s CP: %s" %(tuple(len(x) for x in json[13])))
	
	ranks = ("\tCaptain:", "\tSenior Officers", "\tFleet Officers", "\tOfficers", "\tPirates", "\tCabin Persons")
	print("Crew Members:")
	for x in range(len(json[13])):
		print(ranks[x])
		nl = 0
		for y in json[13][x]:
			#Tabbing needs to be fixed
			if nl == 5:
				print('')
				nl = 0
			print("\t\t%s" %(y), end='')
			nl += 1
		print('')
	
	print("Extended Public Statement:\n\t'%s'" %(json[14]))
	
	if json[14] == False:
		print("Dormant Members Not Avaliable")
	else:
		print("Dormant Members: Feature Not Implamented")
	
	if json[15] == False:
		print("Battle Stats Not Avaliable")
	else:
		print("Battle Stats: Feature Not Implamented")

def pirate(json):
	print("Time Taken: %s-%s-%s %s:%s:%s UTF+0" %(tuple(x for x in json[0][:6])))
	print("Pirate File")
	print("Location: %s" %(build((json[2][:4], "pirt"), [json[3]])[0]))
	print("Name: %s" %(json[3]))
	print("Crew: %s of '%s' (%s)" %(json[4][0], json[4][1], build((json[2][:4], "crew"), [json[4][2]])[0]))
	print("Flag: %s of '%s' (%s)" %(json[5][0], json[5][1], build((json[2][:4], "flag"), [json[5][2]])[0]))
	
	print("Governs:", end='')
	for x in json[6]: print(" '%s'" %(x), end='')
	print('')
	
	print("Navy: '%s' of '%s' (%s)" %(tuple(x for x in json[7])))
	print("Reputation:\n\tConqueror: %s\n\tExplorer: %s\n\tPatron: %s\n\tMagnate: %s" %(tuple(x for x in json[8])))
	
	print("Shoppes:")
	for x in json[9]:
		#There is still a bug in the parser that has trouble with some edge cases
		print("\t%s '%s' (%s)" %(x[0], x[2], x[1]))
	
	print("Stalls:")
	for x in json[10]:
		print("\t%s '%s'" %(x[0], x[1]))
	
	print("Houses:")
	for x in json[11]:
		print("\t%s '%s' (%s)" %(x[0], x[2], x[1]))
	
	print("Familiars:")
	for x in json[12]:
		print("\t%s (%s, %s)" %(x[0], x[1][0], x[1][1]))
	
	print("Hearties:")
	nl = 0
	for x in json[13]:
		if nl == 6:
			print('')
			nl = 0
		print("\t%s" %(x), end='')
		nl += 1
	print('')
	
	pirt = ("\tSailing:", "\tRigging:", "\tCarpentry:", "\tPatching:", "\tBilging:", "\tGunning:", 
	"\tTreasure Haul:", "\tNavigating:", "\tBattle Navigation:", "\tSwordfighting:", "\tRumble:")
	caro = ("\tDrinking:", "\tSpades:", "\tHearts:", "\tTreasure Drop:", "\tPoker:")
	craft = ("\tDistilling:", "\tAlchemistry:", "\tShipwrightery:", "\tBlacksmithing:", 
	"\tForaging:", "\tWeaving:")
	
	print("Piracy Skills:")
	for x in range(len(pirt)):
		print("%s %s" %(pirt[x], json[14][0][x]))
	print("Carousing Skills:")
	for x in range(len(caro)):
		print("%s %s" %(pirt[x], json[14][1][x]))
	print("Crafting Skills:")
	for x in range(len(craft)):
		print("%s %s" %(pirt[x], json[14][2][x]))
	

def read(json):
	types = {"isld": island, "flag": flag, "crew": crew, "pirt": pirate}
	types[json[1]](json)
