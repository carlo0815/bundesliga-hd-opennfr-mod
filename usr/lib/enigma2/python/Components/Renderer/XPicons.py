# Mod by Maggy
from Renderer import Renderer
from enigma import ePixmap
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Tools.Alternatives import GetWithAlternative
from Components.config import config

class XPicons(Renderer):
	searchPaths = ('/usr/share/enigma2/XPicons/%s/', '/media/sde1/%s/', '/media/cf/%s/', '/media/sdd1/%s/', '/media/usb/%s/', '/media/usb/XPicons/%s/', '/media/hdd/XPicons/%s/', '/media/usb1/%s/', '/media/ba/%s/', '/mnt/ba/%s/', '/media/sda/%s/', '/etc/%s/')

	def __init__(self):
		Renderer.__init__(self)
		self.path = "XPicons"
		self.size = None
		self.nameCache = { }
		self.pngname = ""

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "path":
				self.path = value
			else:
				attribs.append((attrib,value))
			if attrib == "size":
				value = value.split(',')
				if len(value) == 2:
					self.size = value[0] + "x" + value[1]
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			pngname = ""
			if what[0] != self.CHANGED_CLEAR:
				sname = self.source.text
				if sname.startswith("1:134"):
					sname = GetWithAlternative(self.source.text)
				pos = sname.rfind(':http')
				if pos != -1:
					sname = sname.split('http')[0]
				# strip all after last :
				pos = sname.rfind(':')
				if pos != -1:
					sname = sname[:pos].rstrip(':').replace(':','_')
				pngname = self.nameCache.get(sname, "")
				if pngname == "":
					pngname = self.findPicon(sname)
					if pngname != "":
						self.nameCache[sname] = pngname
			if pngname == "": # no XPicons for service found
				self.instance.hide()
			else:
				self.instance.show()
			if pngname != "" and self.pngname != pngname:
				self.instance.setPixmapFromFile(pngname)
				self.pngname = pngname

	def findPicon(self, serviceName):
		if self.path == "XPicons":
			path_normal = config.usage.picon_dir.value + "/"
			path_size = config.usage.picon_dir.value + "_" + self.size + "/"
			for path in (path_size, path_normal):
				pngname = path + serviceName + ".png"
				if fileExists(pngname):
					return pngname
		for path in self.searchPaths:
			if self.size:
				mypath = self.path + "_" + self.size
				pngname = (path % mypath) + serviceName + ".png"
				if fileExists(pngname):
					return pngname
			pngname = (path % self.path) + serviceName + ".png"
			if fileExists(pngname):
				return pngname
		return ""
