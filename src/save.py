from json import dumps

def save_json(profile, output):
	if output[-1] != '/':
		output += '/'
	if profile != None:
		data = dumps(profile)
		name = profile[3]
		if isinstance(name, tuple): name = name[0]
		name = "%s_%s-%s-%s" %(name, profile[0].tm_year, profile[0].tm_mon, profile[0].tm_mday)
		with open(output + name, 'w') as page:
			page.write(data)
