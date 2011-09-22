def setFromDict(myDict, line, default=''):
	result = ''
	for key, regExp in myDict.iteritems():
		if regExp.search(line):
			result = key
			break
	if not result:
		result = default
		msg.write('no match found; set to >' + default + '<\n')
	return result

def readFile(fileName):
	ein = open(fileName, 'r')
	zeilen = ein.readlines()
	ein.close()
	return [zeile.rstrip() for zeile in zeilen]

def getFileList(args):
	files = []
	if args:
		files.extend(args)
	return files
