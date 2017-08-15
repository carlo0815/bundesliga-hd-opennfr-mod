#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2011
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
#                      mod.Zombi (c)2011
#######################################################################

from Renderer import Renderer
from enigma import eLabel
from enigma import ePoint, eTimer
from Components.VariableText import VariableText
from Tools.HardwareInfo import HardwareInfo

class LcdRoller(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.direct = "R"
		self.x = 2
		self.stt = 0
		self.rep_stt = 2  
		self.oled_size = 132
		if HardwareInfo().get_device_name() == 'dm800se':
			self.oled_size = 96
		self.moveLCD1Text = eTimer()
		self.moveLCD1Text.timeout.get().append(self.__moveLCD1TextRun)

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "position":
				self.posY = int(value.strip().split(",")[1])
				attribs.append((attrib,value))
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)
                     		
	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		if what[0] == self.CHANGED_CLEAR:
			self.text = ""
		else:
			self.text = self.source.text
		if self.instance:
			text_width = self.instance.calculateSize().width()
			if self.moveLCD1Text.isActive():
				self.moveLCD1Text.stop()
			if text_width > self.oled_size:
				self.end = self.oled_size - text_width - 15
				self.x = 2
				self.direct = "R"
				self.instance.move(ePoint(self.x,self.posY))
				self.moveLCD1Text.start(2000)						
			else:
				self.instance.move(ePoint(2,self.posY)) 				 
 
	def __moveLCD1TextRun(self):
		self.moveLCD1Text.stop()
		if self.x != self.end and self.direct == "R":
			self.x = self.x-1       
		elif self.x != 2 and self.direct == "L":
			self.x = self.x+1
		elif self.x == 2:
			self.direct = "R"        
			self.stt =	self.stt + 1
		elif self.x == self.end:
			self.direct = "L"        
			self.stt =	self.stt + 1
		self.instance.move(ePoint(self.x,self.posY))
		if self.stt > self.rep_stt:                       
			self.stt = 0		
			self.text = self.text[:12] + ".."
			self.instance.move(ePoint(2,self.posY))
		else:
			self.moveLCD1Text.start(60)  		
