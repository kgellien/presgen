import sys
#from PresentationClasses import Slide, Paragraph # does not work as expected!?!
import PresentationClasses

def getContentSlides(sectionsOrSlides, title):
	contentSlides = []
	singleColumn = 1
	entries = []
	for sectionOrSlide in sectionsOrSlides:
		paragraph = PresentationClasses.Paragraph('Bullet', sectionOrSlide.title)
		entries.append(paragraph)
	page = 1
	while entries:
		entries, contentSlide = __getContentSlide(title, entries, page, singleColumn)
		contentSlides.append(contentSlide)
		page += 1
	return contentSlides

def __getContentSlide(title, entries, page, singleColumn):
	if page > 1:
		title += '-' + repr(page)
	contentSlide = PresentationClasses.Slide('Heading1', title)
	for paragraph in entries[:10]:
		contentSlide.addParagraph(paragraph, 0)
	if singleColumn:
		entries = entries[11:]
	else:
		for paragraph in entries[10:20]:
			contentSlide.addParagraph(paragraph, 1)
		entries = entries[21:]
	return entries, contentSlide


class PresentationHelper:

	def getAsPythonPoint(self, presentation):
		import PythonPointPresentation
		return PythonPointPresentation.PythonPointPresentation(presentation)

	def getAsPowerPoint(self, presentation):
		import PowerPointPresentation
		return PowerPointPresentation.PowerPointPresentation(presentation)

	def getAsBeamer(self, presentation):
		import BeamerPresentation
		return BeamerPresentation.BeamerPresentation(presentation)

	def writePresentation(self, presentation, style, outFilePrefix, template, withSectionToc):
		presMethod = getattr(PresentationHelper, 'getAs%s' % style)
		pres = presMethod(self, presentation) # crash if no such method
		pres.writePresentation(outFilePrefix, template, withSectionToc)
