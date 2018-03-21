import configparser

def read_db_config(filename='config.ini',section='mysql'):
	parser = configparser.ConfigParser()
	parser.read(filename)
	
	db = {}
	if parser.has_section(section):
		items = parser.items(section)
		for item in items:
			#print(item)
			db[item[0]] = item[1]
	else:
		raise Exception('{0} section not found in {1} file'.format(section,filename))
	
	return db
