#!/usr/bin/env python3

"""""
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
version = "0.2"

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
	if args[1] == "get":
		if len(args) < 6:
			print("Inavlid Statent")
			return False
		ocean = args[2]
		page = args[3]
		ids = args[4:-1]
		output = argv[-1]
		if ocean not in ("meri", "emer", "ceru"):
			print("Invalid Ocean")
			return False
		elif page not in ("isld", "flag", "crew", "pirt", "trph"):
			print("Invalid Page")
			return False
		elif isdir(output) == False:
			print("Invalid Output Directory")
			return False
		if len(ids) > 1:
			fetch_all((ocean, page), ids, output)
		else:
			fetch(build((ocean, page), ids)[0], page, output)
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

if __name__	== "__main__":
	main(argv)
