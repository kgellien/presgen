import sys, PresentationHelper
import os, win32com.client
msg = sys.stderr

msoTrue = 1
msoFalse = 0
ppLayoutTitle = 0x1
ppLayoutText = 0x2
ppLayoutTwoColumnText = 0x3
ppLayoutTitleOnly = 0xb
ppLayoutObject = 0x10

class PowerPointPresentation:

	def __init__(self, presentation):
		self.App = win32com.client.Dispatch('PowerPoint.Application')
		self.presentation = presentation
		self.titleSlide = presentation.titleSlide
		self.Pres = self.App.Presentations.Add() # Create new presentation
		self.nextpage = 1
		self.footerLeft = presentation.footerLeft
		self.footerMiddle = presentation.footerMiddle
		self.footerRight = presentation.footerRight

	def writePresentation(self, outFilePrefix, template, withSectionToc):
		if template:
			self.LayoutTemplate(os.path.abspath(template))
		self.Footer()
		if self.titleSlide:
			self.addSlideToPresentation(self.titleSlide) # title page
		sectionContent = PresentationHelper.getContentSlides(self.presentation.sections, self.presentation.contentName)
		if len(self.presentation.sections) > 1:
			for slide in sectionContent:
				self.addSlideToPresentation(slide)
		for section in self.presentation.sections:
			slideTitle = self.presentation.sectionName + ' ' + section.title
			if len(self.presentation.sections) == 1:
				slideTitle = self.presentation.contentName
			if withSectionToc:
				for slide in PresentationHelper.getContentSlides(section.slides, slideTitle):
					self.addSlideToPresentation(slide)
			for slide in section.slides:
				self.addSlideToPresentation(slide)
		self.save(os.path.abspath(outFilePrefix+'.ppt'))
		self.close()
		self.quit()

	def quit(self):
		self.App.Quit()

	def save(self, newfilename = None):
		if newfilename:
			self.filename = newfilename
			self.Pres.SaveAs(newfilename)
		else:
			self.Pres.Save()

	def close(self):
		self.Pres.Close()

	def LayoutTemplate(self, filename):
		self.Pres.ApplyTemplate(FileName = filename)

	def newSlideWithTitle(self, layout, Title):
		Slide = self.Pres.Slides.Add(self.nextpage, Layout = layout)
		self.nextpage += 1
		Slide.Shapes('Rectangle 2').TextFrame.TextRange.Text = Title
		return Slide



	def TitlePage(self, Title, SubTitle = None):
		Slide = self.newSlideWithTitle(ppLayoutTitle, Title)
		if SubTitle:
			Slide.Shapes('Rectangle 3').TextFrame.TextRange.Text = SubTitle

	def GraphicsPage(self, Title, graphicsFile):
		Slide = self.newSlideWithTitle(ppLayoutObject, Title)
		if graphicsFile:
			Slide.Shapes.AddPicture(graphicsFile, msoFalse, msoTrue, 60, 131, 599, 278)

	def buildParagraphs(self, Slide, currentShape, paragraphs):
		parId = 1
		for paragraph in paragraphs:
			entry = paragraph.getAsLine() + '\r'
			currentTextRange = Slide.Shapes(currentShape).TextFrame.TextRange
			currentTextRange.InsertAfter(entry)
			currentParagraph = currentTextRange.Paragraphs(parId, 0)
			if   paragraph.style not in ['Bullet', 'Bullet2']:
				currentParagraph.ParagraphFormat.Bullet.Visible = msoFalse
			elif paragraph.style == 'Bullet2':
				currentParagraph.IndentLevel = 2
			parId += 1

	def BulletList(self, Title, paragraphs):
		Slide = self.newSlideWithTitle(ppLayoutText, Title)
		self.buildParagraphs(Slide, "Rectangle 3", paragraphs)

	def doubleBulletList(self, Title, paragraphs, paragraphsRight):
		Slide = self.newSlideWithTitle(ppLayoutTwoColumnText, Title)
		self.buildParagraphs(Slide, 'Rectangle 3', paragraphs)
		self.buildParagraphs(Slide, 'Rectangle 4', paragraphsRight)

	def addSlideToPresentation(self, slide):
		style = slide.style
		if style == 'Ignore':
			style = 'Heading1' # Default
		if   style == 'Title': #layout == ppLayoutTitle:
			subTitle = None
			if len(slide.paragraphs) > 0:
				subTitle = slide.paragraphs[0].getAsLineWithSoftLf()
			self.TitlePage(slide.title, subTitle)
		elif style in ['Heading1', 'Heading2']: #layout == ppLayoutText:
			if slide.paragraphs and slide.paragraphs[0].style == 'Image':
				graphicsFile = os.getcwd() + os.sep + slide.paragraphs[0].lines[0]
				self.GraphicsPage(slide.title, graphicsFile)
			elif slide.paragraphsRight:
				self.doubleBulletList(slide.title, slide.paragraphs, slide.paragraphsRight)
			else:
				self.BulletList(slide.title, slide.paragraphs)
		else:
			msg.write('Layout >' + style + '< not yet recognized\n')

	def Footer(self):
		self.Pres.SlideMaster.HeadersFooters.DateAndTime.Text = self.footerLeft
		self.Pres.SlideMaster.HeadersFooters.DateAndTime.Visible = msoTrue
		self.Pres.SlideMaster.HeadersFooters.Footer.Text = self.footerMiddle
		self.Pres.SlideMaster.HeadersFooters.Footer.Visible = msoTrue
		self.Pres.SlideMaster.HeadersFooters.SlideNumber.Visible = msoTrue
