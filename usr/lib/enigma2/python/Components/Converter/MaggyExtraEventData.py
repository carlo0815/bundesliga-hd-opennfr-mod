# License: this is closed source!
# you are not allowed to use this Converter or parts of it outside of Fluid Skin
# you are not allowed to use this Converter or parts of it  on any other image than VTI
# you are not allowed to use this Converter or parts of it  on NON VU Hardware
# Copyright: hmmmmdada 2016
from Components.Converter.Converter import Converter
from Components.Element import cached
import json
import HTMLParser
class MaggyExtraEventData(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = str(type).split()
	
	@cached
	def getText(self):
		h = HTMLParser.HTMLParser()
		if self.type != '':
			rets = []
			ret = ""
			gotevent = False
			try:
				if str(self.source.text) != '':
					values = json.loads(str(self.source.text))
					gotevent = True
			except:
				try:
					if str(self.source) != '':
						values = json.loads(str(self.source))
						gotevent = True
				except Exception:
					pass
			if gotevent:
				for field in self.type:
					if field == "IMAGE":
						if len(str(values['id']).strip()) > 0:
							return str(values['id']).strip()
					elif field == "TITLE":
						if len(str(values['title']).strip()) > 0:
							rets.append(str(values['title']).strip())
					elif field == "SUBTITLE":
						if len(str(values['subtitle']).strip()) > 0:
							rets.append(str(values['subtitle']).strip())
					elif field == "SERIESINFO":
						if 'season' in values and 'episode' in values:
							if len(str(values['season']).strip()) > 0 and len(str(values['episode']).strip()) > 0:
								rets.append("S%sE%s" % (str(values['season']).zfill(2), str(values['episode']).zfill(2)))
					elif field == "CATEGORY":
						if 'categoryName' in values:
							if len(str(values['categoryName']).strip()) > 0:
								rets.append(str(values['categoryName']).strip())
					elif field == "GENRE":
						if 'genre' in values:
							if len(str(values['genre']).strip()) > 0:
								rets.append(str(values['genre']).strip())
					elif field == "AGE":
						if 'ageRating' in values:
							if len(str(values['ageRating']).strip()) > 0:
								rets.append(str(values['ageRating']).strip())
					elif field == "YEAR":
						if 'year' in values:
							if len(str(values['year']).strip()) > 0:
								rets.append(str(values['year']).strip())
					elif field == "COUNTRY":
						if 'country' in values:
							if len(str(values['country']).strip()) > 0:
								rets.append(str(values['country']).strip())
				sep = " %s " % str(h.unescape('&#xB7;'))
				ret = sep.join(rets)
		return ret
		
	text = property(getText)