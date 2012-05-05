# -*- coding: iso-8859-1 -*-
import sys, PresentationHelper
msg = sys.stderr

class BeamerPresentation:

	def __init__(self, presentation):
		self.presentation = presentation
		self.footerLeft = presentation.footerLeft
		self.footerMiddle = presentation.footerMiddle
		self.footerRight = presentation.footerRight
		self.title = self.presentation.prefix['Title']
		self.subtitle = self.presentation.prefix['Subtitle']
		self.author = self.presentation.prefix['Author']
		self.date = self.presentation.prefix['Date']
		languages = {'en': 'english', 'de': 'german'}
		self.language = languages[self.presentation.prefix['Language']]

	def writePresentation(self, outFilePrefix, template, withSectionToc):
		out = open(outFilePrefix+'.tex', 'w')
		for line in self.getPresentation(template, withSectionToc):
			out.write(line + '\n')
		out.close()

	def getPresentation(self, template, withSectionToc):
		global pageNo
		result = []
		result.append('\\documentclass{beamer}')
		result.append('\\mode<presentation>')
		if template:
			result.append('\\usetheme{' + template + '}')
		result.append('\\usepackage[latin1]{inputenc}')
		result.append('\\usepackage[german]{babel}')
		result.append('\\usepackage[T1]{fontenc} % Necessary for hyphenation with e.g. german umlaut')
		result.append('\\usepackage{times}')
		result.append('\\title[' + self.title + ']{' + self.title + '%')
		if self.subtitle:
			result.append('  \\\\  ' + self.subtitle + '%')
		result.append('}')
		result.append('\\author{' + self.author + '}')
		result.append('\\date{' + self.date + '}')
		result.append('\\begin{document}')
		result.append('\\begin{frame}')
		result.append('  \\titlepage')
		result.append('\\end{frame}')
		sectionContent = PresentationHelper.getContentSlides(self.presentation.sections, self.presentation.contentName)
		if len(self.presentation.sections) > 1:
			for slide in sectionContent:
				result.extend(self.getSlide(slide))
		for section in self.presentation.sections:
			result.extend(self.getSection(section, withSectionToc))
		result.append('\\end{document}')
		return result

	def getSection(self, section, withContent):
		result = []
		result.append('\\section{' + section.title + '}')
		if withContent:
			result.extend(self.getSectionContent(section))
		for slide in section.slides:
			result.extend(self.getSlide(slide))
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
		result = []
		result.append('\n\\begin{frame}')
		result.append('\\frametitle{' + slide.titleParagraph.getAsLine() + '}')
		depth = 0
		for paragraph in slide.paragraphs:
			if   paragraph.style in ['Bullet', 'BulletSequence']:
				if   depth == 0:
					result.append('  \\begin{itemize}')
					depth = 1
				elif depth == 2:
					result.append('    \\end{itemize}')
					depth = 1
			elif paragraph.style == 'Bullet2':
				if   depth == 1:
					result.append('    \\begin{itemize}')
					depth = 2
				elif depth == 0:
					msg.write('Bullet2 should be preceeded by Bullet!\n')
					result.append('  \\begin{itemize}')
					result.append('    \\begin{itemize}')
					depth = 2
			else:
				result, depth = self.reduceDepth(result, depth)
			result.extend(self.getParagraph(paragraph, depth))
		result, depth = self.reduceDepth(result, depth)
		result.append('\\end{frame}\n')
		return result

	def getParagraph(self, paragraph, depth):
		insert = ' '*(2+depth*2)
		result = []
		if paragraph.lines:
			if   paragraph.style == 'Image':
				result.append('  \\includegraphics<1>[height=6cm, width=10cm]{' + paragraph.lines[0] + '}')
			else:
				if not paragraph.style in ['BulletSequence', 'Bullet', 'Bullet2', 'Normal', 'BigCentered']:
					result.append('  %paragraph.style="' + paragraph.style + '"')
				if   paragraph.style in ['Bullet', 'Bullet2']:
					result.append(insert + '\\item')
				elif   paragraph.style in ['BulletSequence']:
					result.append(insert + """\pause \item""")
				elif paragraph.style == 'Normal':
					result.append('')
				elif paragraph.style == 'BigCentered':
					result.append(insert + '\\begin{center}\Large')
				for line in paragraph.lines:
					result.append(insert + self.encode(line) + '')
				if paragraph.style == 'BigCentered':
					result.append(insert + '\\end{center}')
		else:
			msg.write('Paragraph empty; ignore\n')
		return result

	specialChars = ['#', '$', '_'] # TODO: complete list
	def encode(self, line):
		result = []
		for char in line:
			if char in self.specialChars: # TODO: check preceeding char
				result.append('\\')
			result.append(char)
		return ''.join(result)
		
	def reduceDepth(self, result, depth):
		if depth == 2:
			result.append('    \\end{itemize}')
			depth = 1
		if depth == 1:
			result.append('  \\end{itemize}')
		return result, 0
