#by Nikolasi
from Renderer import Renderer
from enigma import ePixmap, ePicLoad, eDVBCI_UI, eDVBCIInterfaces, eEnv, eTimer, loadPic
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Components.Converter.Poll import Poll

class Cicontrol4(Renderer, Poll):
    searchPaths = (eEnv.resolve('${datadir}/enigma2/%s/'),
				'/media/hdd/%s/',
				'/media/usb/%s/')
    def __init__(self):
        Poll.__init__(self)        
        Renderer.__init__(self)
        self.path = 'module'
	self.nameCache = { }
        self.png = ''
        self.picon = ePicLoad()
        self.timerpics = eTimer()
        self.timerpics.callback.append(self.timerpicsEvent)
        self.timerpics2 = eTimer()
        self.timerpics2.callback.append(self.timerpicsEvent2)          

    def applySkin(self, desktop, parent):
	attribs = []
	for (attrib, value,) in self.skinAttributes:
	    if attrib == 'path':
		self.path = value		
	    else:
		attribs.append((attrib, value))			
	self.skinAttributes = attribs
	return Renderer.applySkin(self, desktop, parent)    

    GUI_WIDGET = ePixmap

    def changed(self, what):
        self.poll_interval = 4000
        self.poll_enabled = True        
        if self.instance:
            pngname = ''
            pngname1 = ''
            pngname2 = ''
            pngname3 = ''
            name = ''
            name1 = ''
            name2 = ''
            name3 = ''
            if what[0] != self.CHANGED_CLEAR:
                service = self.source.service
                if service:
                    NUM_CI = eDVBCIInterfaces.getInstance().getNumOfSlots()
                    if NUM_CI > 0:
                        if NUM_CI == 1:
                             state = eDVBCI_UI.getInstance().getState(0)
                             if state != -1:
	                            name = self.getPiconname(state, 1)
	                     else:
		                        name = "NOMODULE_SLOT1"
		             pngname = self.getPiconFilename(name)           
		        elif NUM_CI == 2:
                             state = eDVBCI_UI.getInstance().getState(0)
                             if state != -1:
	                            name = self.getPiconname(state, 1)
	                     else:
		                        name = "NOMODULE_SLOT1"
		             pngname = self.getPiconFilename(name)           
                             state1 = eDVBCI_UI.getInstance().getState(2)
                             if state1 != -1:
	                            name1 = self.getPiconname(state1, 2)
	                     else:
		                        name1 = "NOMODULE_SLOT2"
		             pngname1 = self.getPiconFilename(name1)           
		        else:
                             state = eDVBCI_UI.getInstance().getState(0)
                             if state != -1:
	                            name = self.getPiconname(state, 1)
	                     else:
		                        name = "NOMODULE_SLOT1"
		             pngname = self.getPiconFilename(name)           
                             state1 = eDVBCI_UI.getInstance().getState(1)
                             if state1 != -1:
	                            name1 = self.getPiconname(state1, 2)
	                     else:
		                        name1 = "NOMODULE_SLOT2"
		             pngname1 = self.getPiconFilename(name1)           
                             state2 = eDVBCI_UI.getInstance().getState(2)
                             if state2 != -1:
	                            name2 = self.getPiconname(state2, 3)
	                     else:
		                        name2 = "NOMODULE_SLOT3"
		             pngname2 = self.getPiconFilename(name2)           
                             state3 = eDVBCI_UI.getInstance().getState(3)
                             if state3 != -1:
	                            name3 = self.getPiconname(state3, 4)
	                     else:
		                        name3 = "NOMODULE_SLOT4"
		             pngname3 = self.getPiconFilename(name3)           
                        if NUM_CI == 1:
		            size = self.instance.size()
                            self.picon.setPara((size.width(), size.height(), 1, 1, False, 1, '#00000000'))
                            self.picon.startDecode(pngname, 0, 0, False)               
                            self.png = self.picon.getData()				
	                    self.instance.setPixmap(self.png)                        
                        elif NUM_CI == 2:   
                            self.runanim2(pngname, pngname1)
                        else:
                            self.runanim(pngname, pngname1, pngname2, pngname3)

    def getPiconname(self, state, slot):
            name = ''
	    if state == 0:
		name = "NOMODULE_SLOT%d" %(slot)
	    elif state == 1:
		name = "INITMODULE_SLOT%d" %(slot)
	    elif state == 2:
		name = "READY_SLOT%d" %(slot)              
            return name	 		

        
    def getPiconFilename(self, sRef):
        pngname = ''
        pngname = self.nameCache.get(sRef, '')
        if pngname == '':
            pngname = self.findPicon(sRef)
            if pngname != '':
                self.nameCache[sRef] = pngname
            if pngname == '':
                pngname = self.nameCache.get('default', '')
                if pngname == '':
                    pngname = self.findPicon('picon_default')
                    if pngname == '':
                        tmp = resolveFilename(SCOPE_CURRENT_SKIN, "picon_default.png")
                        if fileExists(tmp):
                            pngname = tmp
                        else:
                            pngname = resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/picon_default.png")
                    self.nameCache['default'] = pngname              
        return pngname	

    def findPicon(self, serviceName):
	for path in self.searchPaths:
		pngname = (path % self.path) + serviceName + ".png"
		if fileExists(pngname):
			return pngname
	return ""

    def runanim2(self, pic1, pic2):
        size = self.instance.size()
        self.slide2 = 2
        self.pics2 = []
        self.pics2.append(loadPic(pic1, size.width(), size.height(), 0, 0, 0, 1))        
        self.pics2.append(loadPic(pic2, size.width(), size.height(), 0, 0, 0, 1))
        self.timerpics2.start(100, True)

    def timerpicsEvent2(self):
            if self.slide2 == 0:
                self.slide2 = 2
            self.timerpics2.stop()
            self.instance.setPixmap(self.pics2[self.slide2 - 1])
            self.slide2 = self.slide2 - 1
            self.timerpics2.start(2000, True)

    def runanim(self, pic1, pic2, pic3, pic4):
        size = self.instance.size()
        self.slide = 4
        self.pics = []
        self.pics.append(loadPic(pic1, size.width(), size.height(), 0, 0, 0, 1))        
        self.pics.append(loadPic(pic2, size.width(), size.height(), 0, 0, 0, 1))
        self.pics.append(loadPic(pic3, size.width(), size.height(), 0, 0, 0, 1))        
        self.pics.append(loadPic(pic4, size.width(), size.height(), 0, 0, 0, 1))        
        self.timerpics.start(100, True)

    def timerpicsEvent(self):
            if self.slide == 0:
                self.slide = 4
            self.timerpics.stop()
            self.instance.setPixmap(self.pics[self.slide - 1])
            self.slide = self.slide - 1
            self.timerpics.start(4000, True)            
