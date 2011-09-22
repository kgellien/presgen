#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#Function: convert simple textformat into pdf resp. ppt presentation
import getopt, os, re, sys
from common import readFile, getFileList
import Style
import PresentationClasses # i.e. Presentation, Slide, Paragraph

msg = sys.stderr
usage = """usage: [python] %s [-s style] -o outFilePrefix file1.txt [file2.txt ...]
valid styles: %s""" %(sys.argv[0], PresentationClasses.Presentation.validStyles)

commentRe = re.compile('^#')
emptyRe  = re.compile('^$')
newSectionRe = re.compile('^(S|P|I)')
newSlideRe = re.compile('^=')
newParagraphRe = re.compile('^( |r)(H|h|~|\.|-|\+|>|c|g|n)') # note treated as paragraph
rightRe = re.compile('^r')
continuationRe = re.compile('^( |r) ')

def addToPrefix(line):
	columns = line.split('=')
	if len(columns) != 2:
		msg.write('ignore line; line must contain entries in the form >key = value<; got: >' + line + '<\n')
	else:
		prefix[columns[0].strip()] = columns[1].strip()

def endCurrentSlide():
	global currentSection, currentSlide
	if currentSlide:
		endCurrentParagraph()
		if currentSlide.style != 'Ignore' or withIgnoredParts:
			currentSection.addSlide(currentSlide)
	currentSlide = None

def endCurrentParagraph():
	global currentSlide, currentParagraph, right
	if currentParagraph:
		if currentParagraph.style != 'Note':
			currentSlide.addParagraph(currentParagraph, right)
		else:
			currentSlide.addNote(currentParagraph)
	currentParagraph = None
	right = False

def transformLine(line, presentation):
	global currentSection, currentSlide, currentParagraph, right, prefix
	lineType = line[:3]
	entry = line[3:]
	if   commentRe.search(line) or emptyRe.search(line):
		endCurrentParagraph()
	elif newSectionRe.search(line):
		endCurrentSlide()
		if currentSection and currentSection.style != 'Prefix' and (currentSection.style != 'Ignore' or withIgnoredParts):
			presentation.addSection(currentSection)
		style = Style.getSectionStyle(line)
		currentSection = PresentationClasses.Section(style, entry)
	elif currentSection.style == 'Prefix':
		addToPrefix(line)
	elif newSlideRe.search(line):
		endCurrentSlide()
		currentSlide = PresentationClasses.Slide(Style.getSlideStyle(line), entry)
	elif currentSlide:
		if   newParagraphRe.search(line):
			endCurrentParagraph()
			currentParagraph = PresentationClasses.Paragraph(Style.getParagraphStyle(line), entry)
			if rightRe.search(line):
				right = True
		elif continuationRe.search(line):
			currentParagraph.addLine(entry)
		else:
			msg.write( 'Line >' + line + '< not in Para! (ignored)\n')
	else:
		msg.write( 'Line >' + line + '< not in Slide! (ignored)\n')
	return presentation

def transform(file, presentation):
	global currentSection, currentSlide, currentParagraph, right, prefix
	prefix = {}
	currentSection = None
	currentSlide = None
	currentParagraph = None
	right = False
	for line in readFile(file):
		presentation = transformLine(line, presentation)
	endCurrentSlide()
	if currentSection and currentSection.title != 'Prefix':
		presentation.addSection(currentSection)
	presentation.addPrefix(prefix)
	return presentation

def buildPresentation(files, withBorder, background):
	presentation = PresentationClasses.Presentation(withBorder, background)
	for file in files:
		presentation = transform(file, presentation)
	return presentation

def main():
	global withIgnoredParts
	withIgnoredParts = False
	outFilePrefix = 't2p-default'
	withSectionToc = False
	style = 'Beamer' # valid: 'PowerPoint' 'PythonPoint' 'Beamer'
	withBorder = 'false'
	template = '' #None
	background = '' #None	
	(opts, args) = getopt.getopt(sys.argv[1:], "ho:bg:t:s:ui")
	for opt, arg in opts:
		if   opt == '-h':
			msg.write( usage + '\n' )
			return 0
		elif opt == '-o':
			outFilePrefix = arg
		elif opt == '-b':
			withBorder = 'true'
		elif opt == '-g':
			background = arg
		elif opt == '-s':
			style = arg
		elif opt == '-t':
			template = arg
		elif opt == '-u':
			withSectionToc = True # create Table of Contents for each section
		elif opt == '-i':
			withIgnoredParts = True # include ignored slides/content
	if style in PresentationClasses.Presentation.validStyles:
		files = getFileList(args)
		presentation = buildPresentation(files, withBorder, background)
		presentation.writePresentation(style, outFilePrefix, template, withSectionToc)
		return 0
	else:
		msg.write('style >' + style + '< not yet recognised; abort\n')
		return -1

if __name__ == "__main__":
	sys.exit( main() )
