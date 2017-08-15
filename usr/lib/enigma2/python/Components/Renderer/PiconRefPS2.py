# -*- coding: utf-8 -*-
# coders Nikolasi
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Renderer import Renderer
from enigma import ePixmap, loadPic, eTimer, iServiceInformation, iPlayableService, eDVBFrontendParametersSatellite, eDVBFrontendParametersCable
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Components.config import *
from Components.Converter.Poll import Poll

class PiconRefPS2(Renderer, Poll):
    searchPaths = ('/usr/share/enigma2/%s/', '/media/ba/%s/', '/media/hdd/%s/', '/media/sda1/%s/', '/media/sda/%s/', '/media/usb/%s/')

    def __init__(self):
        Poll.__init__(self)         
        Renderer.__init__(self)
        self.control = 1
        self.piconWidth = 100
        self.piconHeight = 60        
        self.path = 'picon'
        self.nameCache = {}
        self.nameCache1 = {}
        self.nameCache2 = {}
        self.pngname = ''
        self.pngname1 = ''
        self.pngname2 = ''
        self.timerpicsPS = eTimer()
        self.timerpicsPS.callback.append(self.timerpicsPSEvent)
        self.timerpicsPS1 = eTimer()
        self.timerpicsPS1.callback.append(self.timerpicsPSEvent1)
        
    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'path':
                self.path = value
            elif attrib == 'piconWidth':
                self.piconWidth = int(value)
            elif attrib == 'piconHeight':
                self.piconHeight = int(value)
            elif attrib == 'control':
                self.control = int(value)                
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        self.poll_interval = 3000
        self.poll_enabled = True        
        sname = ''
        sname_ref = ''
        sname_rpov = ''
        sname_sat = ''        
        if self.instance:
            pngname = ''    
            if what[0] != self.CHANGED_CLEAR:
                text = self.source.text
                if text:
                    self.path = 'picon'
                    if ',,,' in text:
                        sname_ref, sname_rpov, sname_sat = text.split(',,,')
                    else:
                        sname_ref = text
                    swt = True
                    if swt == True:
                        sname2 = '%s' % (sname_ref)
                        pos = sname_ref.rfind(':')
                        if pos != -1:
                            sname = '_'.join(sname_ref.split(':', 10)[:10])
                        pngname = self.nameCache.get(sname, '')
                        if pngname == '':
                            pngname = self.findPicon(sname)
                            if pngname != '':
                                self.nameCache[sname] = pngname
                        if pngname == '':
                            pngname = self.nameCache.get('default', '')
                            if pngname == '':
                                pngname = self.findPicon('picon_default')
                                if pngname == '':
                                    tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                                    if fileExists(tmp):
                                        pngname = tmp
                                    else:
                                        pngname = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')
                                self.nameCache['default'] = pngname
                        if self.pngname != pngname:
                            self.pngname = pngname
                        if SCOPE_CURRENT_SKIN:
                                provname = sname_rpov 
                                pngname1 = ''
                                #provname = '%s' % (provname)
                                if 'tvshka' in sname2:
                                    sname = "SCHURA"
                                elif 'vsadmin' in sname2:
                                    sname = "Vsadmin"
                                else:    
                                    if provname.startswith('T-K'):
                                        sname = 'T-KABEL'
                                    elif provname == 'T-Systems/MTI':
                                        sname = 'T-SYSTEMS'
                                    else:
                                        sname = provname.upper()
                                pngname1 = self.nameCache1.get(sname, '')
                                self.path = 'piconProv'
                                if pngname1 == '':
                                    pngname1 = self.findPicon(sname)
                                    if pngname1 != '':
                                        self.nameCache1[sname] = pngname1
                                if pngname1 == '':
                                    pngname1 = self.nameCache1.get('default', '')
                                    if pngname1 == '':
                                        pngname1 = self.findPicon('picon_default')
                                        if pngname1 == '':
                                            tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                                            if fileExists(tmp):
                                                pngname1 = tmp
                                            else:
                                                pngname1 = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')
                                        self.nameCache1['default'] = pngname1
                                if self.pngname1 != pngname1:
                                    self.pngname1 = pngname1
                                if 'http' in sname2:
                                       sname = "00E"
                                else:       
                                       sname = sname_sat
                                       sname = sname.replace('.', '').replace('°', '')
                                pngname2 = self.nameCache2.get(sname, '')
                                self.path = 'piconSat'
                                if pngname2 == '':
                                    pngname2 = self.findPicon(sname)
                                    if pngname2 != '':
                                        self.nameCache2[sname] = pngname2
                                if pngname2 == '':
                                    pngname2 = self.nameCache2.get('default', '')
                                    if pngname2 == '':
                                        pngname2 = self.findPicon('picon_default')
                                        if pngname2 == '':
                                            tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                                            if fileExists(tmp):
                                                pngname2 = tmp
                                            else:
                                                pngname2 = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')
                                        self.nameCache2['default'] = pngname2
                                if self.pngname2 != pngname2:
                                    self.pngname2 = pngname2
                                if self.control == 1:    
                                    self.runanim2(pngname, pngname1, pngname2)
                                else:
                                    self.runanim1(pngname1, pngname2)


    def findPicon(self, serviceName):
        for path in self.searchPaths:
            pngname = path % self.path + serviceName + '.png'
            if fileExists(pngname):
                return pngname

        return ''

    def runanim1(self, pic1, pic2):
        self.slide = 2
        self.steps = 9
        self.pics = []
        self.pics.append(loadPic(pic1, self.piconWidth, self.piconHeight, 0, 0, 0, 1))
        self.pics.append(loadPic(pic2, self.piconWidth, self.piconHeight, 0, 0, 0, 1))
        self.timerpicsPS1.start(100, True)

    def timerpicsPSEvent1(self):
        if self.steps != 0:
            self.timerpicsPS1.stop()
            self.instance.setPixmap(self.pics[self.slide - 1])
            self.steps = self.steps - 1
            self.slide = self.slide - 1
            if self.slide == 0:
                self.slide = 2
            self.timerpicsPS1.start(1000, True)
        else:
            self.timerpicsPS1.stop()
            self.instance.setScale(1)              
            self.instance.setPixmapFromFile(self.pngname)    

    def runanim2(self, pic1, pic2, pic3):
        self.slide = 3
        self.steps = 9
        self.pics = []
        self.pics.append(loadPic(pic3, self.piconWidth, self.piconHeight, 0, 0, 0, 1))
        self.pics.append(loadPic(pic2, self.piconWidth, self.piconHeight, 0, 0, 0, 1))
        self.pics.append(loadPic(pic1, self.piconWidth, self.piconHeight, 0, 0, 0, 1))
        self.timerpicsPS.start(100, True)

    def timerpicsPSEvent(self):
        if self.steps != 0:
            self.timerpicsPS.stop()
            self.instance.setPixmap(self.pics[self.slide - 1])
            self.steps = self.steps - 1
            self.slide = self.slide - 1
            if self.slide == 0:
                self.slide = 3
            self.timerpicsPS.start(1000, True)
        else:
            self.timerpicsPS.stop()
            self.instance.setScale(1)              
            self.instance.setPixmapFromFile(self.pngname)

