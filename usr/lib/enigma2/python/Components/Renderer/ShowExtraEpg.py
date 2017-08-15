#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2015
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#######################################################################

from Renderer import Renderer
from enigma import eLabel, eCanvas, eServiceReference, eEPGCache, eRect, eSize, gRGB, gFont, fontRenderClass, RT_HALIGN_BLOCK, RT_HALIGN_LEFT, RT_WRAP
from time import localtime
from skin import parseColor, parseFont
import re

class ShowExtraEpg(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.EPGcache = eEPGCache.getInstance()
		self.numEvents = 4
		self.numDescLines = 1
		self.testSizeLabel = None           	
		self.fcolor = gRGB(255,255,255)
		self.bcolor = gRGB(0,0,0)
		self.fdcolor = gRGB(255,255,255)
		self.timecolor = gRGB(255,255,255)
		self.used_font = gFont("Regular", 16)
		self.desc_font = gFont("Regular", 14)		
		self.W = self.H = 0
		self.lineHeight = self.lineHeight_desc = self.timeWidth = 0
            		
	GUI_WIDGET = eCanvas

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "numEvents":
				self.numEvents = int(value)
			elif attrib == "maxDescriptionLines":
				self.numDescLines = int(value)
			elif attrib == "font":
				self.used_font = parseFont(value, ((1,1),(1,1)))
			elif attrib == "foregroundColor":
				self.fcolor = parseColor(value)
			elif attrib == "foregroundColorTime":
				self.timecolor = parseColor(value)
			elif attrib == "backgroundColor":
				self.bcolor = parseColor(value)
			elif attrib == "foregroundColorDescription":
				self.fdcolor = parseColor(value)
			elif attrib == "fontDescription":
				self.desc_font = parseFont(value, ((1,1),(1,1)))
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		self.testSizeLabel.setFont(self.used_font)
		self.testSizeLabel.resize(eSize(self.W+500,20))
		self.testSizeLabel.setVAlign(eLabel.alignTop)
		self.testSizeLabel.setHAlign(eLabel.alignLeft)
		self.testSizeLabel.setNoWrap(1)
		tmp = int(fontRenderClass.getInstance().getLineHeight(self.used_font) or self.used_font.pointSize/6 + self.used_font.pointSize)
		self.testSizeLabel.setText("WQq")
		self.lineHeight = self.testSizeLabel.calculateSize().height()
		if tmp > self.lineHeight:
			self.lineHeight = tmp
		self.testSizeLabel.setText("59:59  ")
		self.timeWidth = self.testSizeLabel.calculateSize().width()+10
		self.testSizeLabel.setText("")
		self.testSizeLabel.setFont(self.desc_font)
		tmp = int(fontRenderClass.getInstance().getLineHeight(self.desc_font) or self.desc_font.pointSize/6 + self.desc_font.pointSize)
		self.testSizeLabel.setText("WQq")
		self.lineHeight_desc = self.testSizeLabel.calculateSize().height()
		if tmp > self.testSizeLabel.calculateSize().height():
			self.lineHeight_desc = tmp
		self.lineHeight_desc *= self.numDescLines
		self.testSizeLabel.setText("")
		self.testSizeLabel.resize(eSize(self.W-10,1000))
		self.testSizeLabel.setHAlign(eLabel.alignBlock)
		self.testSizeLabel.setNoWrap(0)
		return Renderer.applySkin(self, desktop, parent)

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		def cutMe(ret):
			pos = ret.rfind(' ')
			if pos != -1:
				ret = ret[:pos].rstrip(' ')
			return ret
		if self.instance:
			extEpg = "Extended EPG is not available!"
			if what[0] != self.CHANGED_CLEAR:
				self.instance.clear(self.bcolor)
				try:
					service = self.source.service
					marker = (service.flags & eServiceReference.isMarker == eServiceReference.isMarker)
					bouquet = (service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory)
					sname = service.toString()
				except:
					marker = False
					bouquet = False
					sname = self.source.text
				if not marker and not bouquet and self.EPGcache is not None:
					pos = sname.rfind(':')
					if pos != -1:
						sname = sname[:pos].rstrip(':')
						if not "::" in sname:
							try:
								info = service and self.source.info
							except: info = True
							if info is not None:
								epgList =  self.EPGcache.lookupEvent(['IBDCTSERNX', (sname, 1, -1, 1440)])
								y = 0 
								h = self.H
								for x in range(0,self.numEvents):
									try:
										t = localtime(int(epgList[x][1]))
										tmp = "%02d:%02d" % (t.tm_hour, t.tm_min)
										self.instance.writeText(eRect(0, y, self.timeWidth, self.lineHeight), self.timecolor, self.bcolor, self.used_font, tmp, RT_HALIGN_LEFT)
										self.instance.writeText(eRect(self.timeWidth, y, self.W-self.timeWidth, self.lineHeight), self.fcolor, self.bcolor, self.used_font, epgList[x][4], RT_HALIGN_LEFT)
										y += self.lineHeight+2
										tmp = extEpg
										if len(epgList[x]) > 5 and epgList[x][5]:
											tmp = '%s' % epgList[x][5]
										if len(epgList[x]) > 6 and epgList[x][6]:
											if tmp != extEpg:
												tmp += ', %s' % epgList[x][6]
											else:
												tmp = '%s' % epgList[x][6]
										if tmp != extEpg:
											tmp = tmp.replace("\r", " ").replace("\n", " ").replace("\xc2\x8a", " ")
											tmp = re.sub('[\s\t]+', ' ',tmp)
										self.testSizeLabel.setText(tmp)
										h = self.testSizeLabel.calculateSize().height()
										if h > self.lineHeight_desc:
											pos = int(len(tmp) / (int(h / self.lineHeight_desc)))
											tmp = cutMe(tmp[:pos].rstrip(' '))
											self.testSizeLabel.setText(tmp)
											h = self.testSizeLabel.calculateSize().height()
											while (h > self.lineHeight_desc):
												tmp = cutMe(tmp)
												self.testSizeLabel.setText(tmp)
												h = self.testSizeLabel.calculateSize().height()
											tmp = cutMe(tmp)
										self.instance.writeText(eRect(10, y, self.W-10, h), self.fdcolor, self.bcolor, self.desc_font, tmp, RT_HALIGN_BLOCK | RT_WRAP)
									except: pass
									y += h+6
									if y > self.H:
										break                  
                    
	def preWidgetRemove(self, instance):
		self.testSizeLabel = None

	def postWidgetCreate(self, instance):
		for (attrib, value) in self.skinAttributes:
			if attrib == "size":
				x, y = value.split(',')
				self.W, self.H = int(x), int(y)
		self.instance.setSize(eSize(self.W,self.H))
		self.testSizeLabel = eLabel(instance)
		self.testSizeLabel.hide()
		
	
		
