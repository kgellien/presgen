import re
from common import setFromDict

paragraphStyleDict = {
   'Heading1':re.compile('^( |r)H'), 'Heading2':re.compile('^( |r)h')
 , 'BigCentered':re.compile('^( |r)~')
 , 'Normal':re.compile('^( |r)\.'),    'BodyText':re.compile('^( |r)\+')
 , 'Bullet':re.compile('^( |r)-[^-]'), 'Bullet2':re.compile('^( |r)--')
 , 'Indent':re.compile('^( |r)>'),     'Code':re.compile('^( |r)c')
 , 'Image':re.compile('^( |r)g') # in this early version considered as paragraph!
 , 'Note':re.compile('^ n')
}
slideStyleDict = {
   'Heading1':re.compile('^=H'), 'Heading2':re.compile('^=h'), 'Ignore':re.compile('^=I')
}
sectionStyleDict = {
   'Section':re.compile('^S'), 'Prefix':re.compile('^P'), 'Ignore':re.compile('^I')
}

def getSectionStyle(zeile):
	return setFromDict(sectionStyleDict, zeile, default='Ignore')

def getSlideStyle(zeile):
	return setFromDict(slideStyleDict, zeile, default='Heading1')

def getParagraphStyle(zeile):
	return setFromDict(paragraphStyleDict, zeile, default='Normal')
