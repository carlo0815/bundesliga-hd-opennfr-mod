# -*- coding: utf-8 -*-
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr
from Components.Element import cached
from Components.config import config

class ServiceNameOrbital (Converter, object):
	NAME = 0
	PROVIDER = 1
	REFERENCE = 2

	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "Provider":
			self.type = self.PROVIDER
		elif type == "Reference":
			self.type = self.REFERENCE
		else:
			self.type = self.NAME

	def getServiceInfoValue(self, info, what, ref=None):
		v = ref and info.getInfo(ref, what) or info.getInfo(what)
		if v != iServiceInformation.resIsString:
			return "N/A"
		return ref and info.getInfoString(ref, what) or info.getInfoString(what)

	@cached
	def getText(self):
		service = self.source.service
		if isinstance(service, iPlayableServicePtr):
			info = service and service.info()
			ref = None
		else: # reference
			info = service and self.source.info
			ref = service	
		if info is None:
			return ""
		if self.type == self.NAME:
			orb = ""
			if ref:
				transponder_info = info.getInfoObject(ref, iServiceInformation.sTransponderData)
			else:
				transponder_info = info.getInfoObject(iServiceInformation.sTransponderData)
			if transponder_info and "orbital_position" in transponder_info.keys():
				pos = int(transponder_info["orbital_position"])
				#print "-----------------------------------------------------"
				#print pos
				#print "-----------------------------------------------------"				
				direction = 'E'
				if pos > 1800:
					pos = 3600 - pos
					direction = 'W'					
					orb = "(%d.%d%s)" % (pos/10, pos%10, direction)
				elif pos > 0:				
					orb = "(%d.%d%s)" % (pos/10, pos%10, direction)
					#print "-----------------------------------------------------"
					#print orb
					#print "-----------------------------------------------------"					
			name = ref and info.getName(ref)
			if name is None:
				name = info.getName()
			name = name.replace('\xc2\x87', '').replace('\xc2\x86', '')
			#if config.plugins.IncubusSettings.showOrbital.value == True:
			return "%s %s" % (orb, name)
			#return orb + " " + name
			#else:
			#	return name
		elif self.type == self.PROVIDER:
			return self.getServiceInfoValue(info, iServiceInformation.sProvider, ref)
		elif self.type == self.REFERENCE:
			return self.getServiceInfoValue(info, iServiceInformation.sServiceref, ref)

	text = property(getText)

	def changed(self, what):
		if what[0] != self.CHANGED_SPECIFIC or what[1] in (iPlayableService.evStart,):
			Converter.changed(self, what)
