from multiprocessing.pool import Pool
import requests
from time import time
from .save import save_json
from .pirt_parse import pirt_parse
from .crew_parse import crew_parse
from .flag_parse import flag_parse
from .isld_parse import isld_parse
from .trph_parse import trph_parse

def build(page_type, urls):
	#Builds a yoweb URL
	#Expects a tuple (ocean, type) and the island index, flag/crew id or a pirate name
	types = {"isld":"island/info.wm?showAll=true", "flag":"flag/info.wm?flagid=", 
		"crew":"crew/info.wm?crewid=", "pirt":"pirate.wm?target=", "trph":"trophy/?pirate="}
	ocean = {"meri":"http://meridian", "emer":"http://emerald", "ceru":"http://cerulean"}
	page = ".puzzlepirates.com/yoweb/"
	for x in range(len(urls)):
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
	print("Fetched %s in %s" %(data[3], final))
	
def simple_fetch(url, page_type):
	reqs = requests.get(url)
	html = reqs.text
	func = {"pirt" : pirt_parse, "crew" : crew_parse, "flag" : flag_parse, "isld" : isld_parse, "trph" : trph_parse}
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
