from multiprocessing.pool import Pool
import requests
from time import time
from .save import save_json
from .pirt_parse import pirt_parse
from .crew_parse import crew_parse
from .flag_parse import flag_parse
from .isld_parse import isld_parse
from .trph_parse import trph_parse
from .fame_parse import fame_parse
from .dorm_parse import dorm_parse
from .stat_parse import stat_parse
from .batt_parse import batt_parse

def build(page_type, urls):
	#Builds a yoweb URL
	#Expects a tuple (ocean, type) and the island index, flag/crew id or a pirate name
	types = {"isld":"island/info.wm?showAll=true", "flag":"flag/info.wm?flagid=", 
		"crew":"crew/info.wm?crewid=", "pirt":"pirate.wm?target=", "trph":"trophy/?pirate=",
		"dorm":"crew/dormant_members.wm?crewid=", "batt":"crew/battleinfo.wm?crewid="}
	fame_page = {"ffam":"top_fame_112.html", "cfam":"top_fame_97.html", "pcon":"top_repute_PIRATE_CONQUEROR.html",
		"pexp":"top_repute_PIRATE_EXPLORER.html", "ppat":"top_repute_PIRATE_PATRON.html",
		"pmag":"top_repute_PIRATE_MAGNATE.html","ccon":"top_repute_CREW_CONQUEROR.html",
		"cexp":"top_repute_CREW_EXPLORER.html", "cpat":"top_repute_CREW_PATRON.html",
		"cmag":"top_repute_CREW_MAGNATE.html", "fcon":"top_repute_FLAG_CONQUEROR.html",
		"fexp":"top_repute_FLAG_EXPLORER.html", "fpat":"top_repute_FLAG_PATRON.html",
		"fmag":"top_repute_FLAG_MAGNATE.html", "stat":"top_{}_0.html"}
	ocean = {"meri":"http://meridian", "emer":"http://emerald", "ceru":"http://cerulean", "obsi":"http://obsidian"}
	page = ".puzzlepirates.com/yoweb/"
	ratings = ".puzzlepirates.com/ratings/"
	for x in range(len(urls)):
		if page_type[1] == "stat":
			urls[x] = ocean[page_type[0]] + ratings + fame_page["stat"].format(urls[x])
			continue
		if page_type[1] == "fame":
			urls[x] = ocean[page_type[0]] + ratings + fame_page[urls[x]]
			continue
		urls[x] = ocean[page_type[0]] + page + types[page_type[1]] + urls[x]
		if page_type[1] == "trph":
			urls[x] = urls[x] + "&expandAll=1"
	return urls

def fetch(url, page_type, output):
	#Fetches a yoweb page and times the request
	start = time()
	data = simple_fetch(url, page_type)
	save_json(data, output)
	final = time() - start
	#Should probaly be expressed in regular milliseconds
	if type(data) == tuple:
		print("Fetched %s in %s" %(data[3], final))
	else:
		print("Fetched Invalid in %s" %(final))
	
def simple_fetch(url, page_type):
	reqs = requests.get(url)
	html = reqs.text
	func = {"pirt":pirt_parse, "crew":crew_parse, "flag":flag_parse, "isld":isld_parse, "trph":trph_parse,
		"fame":fame_parse, "dorm":dorm_parse, "stat":stat_parse, "batt":batt_parse}
	return func[page_type](html, url)

def fetch_all(page_type, ids, output):
	#Python multithreding mess incoming
	start = time()
	pages = []
	links = build(page_type, ids)
	#Number of worker processes to start
	num_of_proc = 8
	pool = Pool(processes=num_of_proc)
	#Builds the process pool
	results = [pool.apply_async(fetch, (url, page_type[1], output,)) for url in links]
	#Proceeds to run the processes
	for result in results:
		result.get()
	print("Fetched all in %s" %(time() - start))
