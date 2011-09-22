import sys
from PresentationHelper import PresentationHelper

class Presentation:
	validStyles = ['Beamer', 'PowerPoint', 'PythonPoint']
	def __init__(self, withBorder, background):
		self.author = 'author'
		self.title = 'title'
		self.footerLeft = ''
		self.footerMiddle = ''
		self.footerRight = ''
		self.withBorder = withBorder
		self.background = background
		self.sections = []
		self.prefix = {}
		self.titleSlide = None
		self.contentName = ''
		self.sectionName = ''

	def addSection(self, section):
		self.sections.append(section)

	def addPrefix(self, prefix):
		self.prefix = prefix
		self.addTitleSlide()

	def writePresentation(self, style, outFilePrefix, template, withSectionToc):
		self.setFooter()
		self.setTranslations()
		ph = PresentationHelper()
		ph.writePresentation(self, style, outFilePrefix, template, withSectionToc)

	def setFooter(self):
		self.footerLeft = self.prefix['Author']
		self.footerMiddle = self.prefix['ShortTitle']
		self.footerRight = '' # not used yet

	def setTranslations(self):
		if self.prefix['Language'] == 'en':
			self.contentName = 'Content'
			self.sectionName = 'Section'
		else:
			self.contentName = 'Inhalt'
			self.sectionName = 'Abschnitt'

	def addTitleSlide(self):
		if self.prefix:
			self.titleSlide = Slide('Title', self.prefix['Title'])
			self.titleSlide.addParagraph(Paragraph('BigCentered', self.prefix['Subtitle']))
			self.titleSlide.addParagraph(Paragraph('BigCentered', self.prefix['Author']))
			self.titleSlide.addParagraph(Paragraph('BigCentered', self.prefix['Version']))
			self.titleSlide.addParagraph(Paragraph('BigCentered', self.prefix['Date']))
			self.titleSlide.addParagraph(Paragraph('BigCentered', chr(169) + ' ' + self.prefix['Copyright']))
			self.titleSlide.addParagraph(Paragraph('BigCentered', self.prefix['License']))

class Section:
	def __init__(self, style, title):
		self.style = style
		self.title = title
		self.slides = []

	def addSlide(self, slide):
		self.slides.append(slide)

class Slide:
	def __init__(self, style, title):
		self.title = title
		self.style = style
		self.titleParagraph = Paragraph(self.style, self.title)
		self.paragraphs = []
		self.paragraphsRight = []
		self.notes = []

	def addParagraph(self, paragraph, right = False):
		if right:
			self.paragraphsRight.append(paragraph)
		else:
			self.paragraphs.append(paragraph)

	def addNote(self, paragraph):
		self.notes.append(paragraph)

class Paragraph:
	def __init__(self, style, line = None):
		self.style = style
		self.lines = []
		if line:
			self.addLine(line)

	def addLine(self, line):
		self.lines.append(line)

	def getAsLine(self, seperator = ' '):
		return seperator.join(self.lines)

	def getAsLineWithSoftLf(self):
		return self.getAsLine('\v')
