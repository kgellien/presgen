import sys, PresentationHelper
import codecs
msg = sys.stderr

class PythonPointPresentation:

	def __init__(self, presentation):
		self.presentation = presentation
		self.withBorder = presentation.withBorder
		self.background = presentation.background
		self.footerLeft = presentation.footerLeft
		self.footerMiddle = presentation.footerMiddle
		self.footerRight = presentation.footerRight
		self.copyright = presentation.prefix['Copyright']

	def writePresentation(self, outFilePrefix, template, withSectionToc, eol='\n'):
		outFile = open(outFilePrefix+'.xml', 'w')
		out = codecs.EncodedFile(outFile, 'iso-8859-1', 'utf-8')
		out.write(eol.join(self.getPresentation(template, withSectionToc))+eol)
		outFile.close()

	def getPresentation(self, template, withSectionToc):
		result = []
		result.append('<?xml version="1.0" encoding="utf-8"?>') # iso-8859-1|utf-8
		result.append('<presentation filename="PythonPoint.pdf">\n')
		result.append('  <stylesheet module="' + template + '" function="getParagraphStyles"/>')
		result.extend(self.getMainSection())
		for section in self.presentation.sections:
			result.extend(self.getSection(section, withSectionToc))
		result.append('</presentation>')
		return result

	def getMainSection(self):
		global pageNo
		result = []
		result.append('  <section name="Main">')
		if self.background:
			result.append('   <fixedimage filename="' + self.background + '" height="595" width="850" y="0" x="0"/>\n')
		pageNo = 1
		if self.presentation.titleSlide:
			result.extend(self.getSlide(self.presentation.titleSlide))
		sectionContent = PresentationHelper.getContentSlides(self.presentation.sections, self.presentation.contentName)
		if len(self.presentation.sections) > 1:
			for slide in sectionContent:
				result.extend(self.getSlide(slide))
		result.append('  </section>')
		return result

	def getSection(self, section, withSectionToc):
		result = []
		result.append('  <section name="' + section.title + '">')
		if self.background:
			result.append('   <fixedimage filename="' + self.background + '" height="595" width="850" y="0" x="0"/>\n')
		if withSectionToc:
			result.extend(self.getSectionContent(section))
		for slide in section.slides:
			result.extend(self.getSlide(slide))
		result.append('  </section>')
		return result

	def getSectionContent(self, section):
		result = []
		slideTitle = self.presentation.sectionName + ' ' + section.title
		if len(self.presentation.sections) == 1:
			slideTitle = self.presentation.contentName
		for slide in PresentationHelper.getContentSlides(section.slides, slideTitle):
			result.extend(self.getSlide(slide))
		return result



	def getSlide(self, slide):
		global pageNo
		result = []
		pageNoStr = repr(pageNo).zfill(3)
		result.append('<slide title="' + pageNoStr + '-' + slide.title + '" id="Slide' + pageNoStr + '">')
		result.extend(self.getFrame([slide.titleParagraph], height=60, width=760, y=490, x=40))
		result.extend(self.getSlideContent(slide))
		result.extend(self.getFooter(pageNoStr))
		result.append('</slide>\n')
		pageNo += 1
		return result

	def getParagraph(self, paragraph):
		result = []
		style = paragraph.style
		if style == 'Ignore':
			style = 'Heading1' # Default
		if True: #paragraph.lines:		#if paragraph.lines:
			if   style == 'Image':
				result.append('  <image filename="' + paragraph.lines[0] + '" width="600" height="400"/>')
			else:
				tagName = 'para'
				if style == 'Code':
					tagName = 'prefmt'
				result.append('  <' + tagName + ' style="' + style + '">')
				for line in paragraph.lines:
					result.append('    ' + line + '')
				result.append('  </' + tagName + '>')
		else:		#if not paragraph.lines:
			msg.write('Paragraph empty; ignore\n')
		return result

	def getFooter(self, pageNoStr):
		result = []
		result.append(' <string y="18" x="5" align="left" size="14">' + pageNoStr + '</string>')
		result.append(' <string y="18" x="60" align="left" size="14">' + chr(169) + ' ' + self.copyright + '</string>')
		result.append(' <string y="18" x="375" align="center" size="14">' + self.footerMiddle + '</string>')
		result.append(' <string y="18" x="680" align="right" size="14">' + self.footerLeft + '</string>')
		return result

	def getSlideContent(self, slide):
		result = []
		if not slide.paragraphsRight:
			result.extend(self.getFrame(slide.paragraphs, height=465, width=760, y=25, x=40))
		else:
			result.extend(self.getFrame(slide.paragraphs, height=465, width=380, y=25, x=40))
			result.extend(self.getFrame(slide.paragraphsRight, height=465, width=380, y=25, x=420))
		return result

	def getFrame(self, paragraphs, height, width, y, x):
		result = []
		result.append(' <frame border="' + self.withBorder + '" height="' + repr(height) +
		  '" width="' + repr(width) + '" y="' + repr(y) + '" x="' + repr(x) + '">')
		for paragraph in paragraphs:
			result.extend(self.getParagraph(paragraph))
		result.append(' </frame>')
		return result
