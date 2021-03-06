#!/usr/bin/env python3

from sys import argv
from json import load
from src.reader import read
from src.fetch import fetch_all
from src.fetch import fetch
from src.fetch import build
from src.fetch import simple_fetch
from os.path import isdir
from os.path import exists

def main(args):
	if args[1] in ("meri", "ceru", "emer", "obsi"):
		ocean = args[1]
		page = args[2]
		ids = args[3:-1]
		output = argv[-1]
		if page == "isld":
			fetch((build((ocean, page), [""]))[0], page, output)
			return True
		elif page == "fact":
			fetch((build((ocean, page), [""]))[0], page, output)
			return True
		elif page == "sall" and len(ids) < 1:
			fetch_all((ocean, "stat"), [0,2,3,31,4,29,5,6,27,30,32,14,18,16,15,12,13,1,21,24,25,26] ,output)
		elif page == "stat":
			if len(ids) > 1:
				fetch_all((ocean, page), ids, output)
			else:
				fetch(build((ocean, page), ids)[0], page, output)
			return True
		elif page == "fame":
			if len(ids) > 1:
				fetch_all((ocean, page), ids, output)
			else:
				fetch(build((ocean, page), ids)[0], page, output)
			return True

		if ocean not in ("meri", "ceru", "emer", "obsi"):
			print("Invalid Ocean")
			return False
		elif page not in ("isld", "flag", "crew", "pirt", "trph", "dorm", "batt", "fact"):
			print("Invalid Page")
			return False
		elif isdir(output) == False:
			print("Invalid Output Directory")
			return False
		if len(ids) > 1:
			fetch_all((ocean, page), ids, output)
		else:
			fetch(build((ocean, page), ids)[0], page, output)

# D E P R E D A T E D
"""
	if args[1] == "read":
		if len(args) != 3:
			print("Invalid Command")
		if exists(args[2]):
			read(load(open("%s" %(args[2]), 'r')))
		else:
			print("Invalid File")
	if args[1] == "info":
		ocean = args[2]
		page = args[3]
		ids = args[4:]
		if ocean not in ("meri", "emer", "ceru"):
			print("Invalid Ocean")
			return False
		elif page not in ("isld", "flag", "crew", "pirt", "thrp"):
			print("Invalid Page")
			return False
		else:
			read(simple_fetch(build((ocean, page), ids)[0], page))
"""

if __name__	== "__main__":
	main(argv)
