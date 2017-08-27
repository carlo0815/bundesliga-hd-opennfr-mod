from Components.ActionMap import ActionMap
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Sources.List import List
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Screens.PluginBrowser import PluginBrowser
from Components.ScrollLabel import ScrollLabel
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap
from Components.Console import Console as iConsole
from os import environ
from enigma import getDesktop
import os
import gettext
lang = language.getLanguage()
environ['LANGUAGE'] = lang[:2]
gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain('enigma2')
gettext.bindtextdomain('BundesligaHD', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'Extensions/BundesligaHD/locale/'))

def _(txt):
    t = gettext.dgettext('BundesligaHD', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


config.plugins.hdbundesliga = ConfigSubsection()
config.plugins.hdbundesliga.style = ConfigSelection(default='fc', choices=[('fc', _('fc')),
 ('bvb', _('bvb')),
 ('s04', _('s04')),
 ('vfb', _('vfb')),
 ('wb', _('wb')),
 ('rbl', _('rbl')),
 ('scf', _('scf')), 
 ('fsv05', _('fsv05')),
 ('96', _('96')),
 ('fcb', _('fcb')),
 ('tsg', _('tsg')),
 ('bsc', _('bsc')),
 ('vflw', _('vflw')),
 ('sv98', _('sv98')),
 ('fc04', _('fc04')),
 ('fc', _('fc')),
 ('fca', _('fca')),
 ('ef', _('ef')),
 ('bmg', _('bmg')),
 ('bl04', _('bl04'))])

class BundesligaHDConfig(ConfigListScreen, Screen):
    skin = '\n<screen name="BundesligaHDConfig" position="center,110" size="750,520" title="Bundesliga HD sKIn setup">\n  <widget position="15,10" size="720,75" name="config" scrollbarMode="showOnDemand" />\n  <ePixmap position="10,475" zPosition="1" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BundesligaHD/images/red.png" alphatest="blend" />\n  <widget source="red_key" render="Label" position="45,477" zPosition="2" size="165,25" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />\n  <ePixmap position="215,475" zPosition="1" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BundesligaHD/images/green.png" alphatest="blend" />\n  <widget source="green_key" render="Label" position="250,477" zPosition="2" size="165,25" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />\n  <ePixmap position="420,475" zPosition="1" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/BundesligaHD/images/yellow.png" alphatest="blend" />\n  <widget source="yellow_key" render="Label" position="455,477" zPosition="2" size="200,25" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />\n  <widget name="CSPreview" position="175,120" size="400,225" zPosition="5" alphatest="blend" />\n</screen>'

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self.setTitle(_('BundesligaHD Skin Setup'))
        self.iConsole = iConsole()
        self.list = []
        self.list.append(getConfigListEntry(_('Select you skin style'), config.plugins.hdbundesliga.style))
        ConfigListScreen.__init__(self, self.list)
        self['CSPreview'] = Pixmap()
        self['red_key'] = StaticText(_('Close'))
        self['green_key'] = StaticText(_('Save'))
        self['yellow_key'] = StaticText(_('Restart GUI'))
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'red': self.cancel,
         'cancel': self.cancel,
         'green': self.save,
         'yellow': self.restart,
         'ok': self.save}, -2)
        self.onLayoutFinish.append(self.CSPreview)

    def CSPreview(self):
        self['CSPreview'].instance.setPixmapFromFile('/usr/lib/enigma2/python/Plugins/Extensions/BundesligaHD/preview/%sstyle.png' % config.plugins.hdbundesliga.style.value)

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.CSPreview()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.CSPreview()

    def exit(self):
        self.close()

    def cancel(self):
        for i in self['config'].list:
            i[1].cancel()

        self.session.openWithCallback(self.exit, MaggyAboutScreen)

    def save(self):
        if config.osd.language.value == 'de_DE':
            self.iConsole.ePopen('tar -C/ -xzpvf /usr/share/enigma2/Bundesliga_HD/tgz/buttons_de.tar.gz', self.saveColorStyle)
        else:
            self.iConsole.ePopen('tar -C/ -xzpvf /usr/share/enigma2/Bundesliga_HD/tgz/buttons_en.tar.gz', self.saveColorStyle)

    def saveColorStyle(self, result, retval, extra_args):
        self.iConsole.ePopen('tar -C/ -xzpvf /usr/share/enigma2/Bundesliga_HD/tgz/%sstyle.tar.gz' % config.plugins.hdbundesliga.style.value)
        config.plugins.hdbundesliga.style.save()
        configfile.save()
        self.mbox = self.session.open(MessageBox, _('configuration is saved'), MessageBox.TYPE_INFO, timeout=4)

    def restart(self):
        self.session.open(TryQuitMainloop, 3)

    def about(self):
        self.session.openWithCallback(self.exit, MaggyAboutScreen)


class MaggyAboutScreen(Screen, ConfigListScreen):
    DESKTOP_WIDTH = getDesktop(0).size().width()
    DESKTOP_HEIGHT = getDesktop(0).size().height()
    skin = '\n\t\t<screen name="MaggyAbout" position="%d,%d" size="650,280" title="%s" >\n\t\t\t<widget name="pluginInfo" position="5,65" size="640,280" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;30"/>\n\t\t\t</screen>' % ((DESKTOP_WIDTH - 650) / 2, (DESKTOP_HEIGHT - 280) / 2, _('About Bundesliga HD by Maggy'))

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['SetupActions'], {'cancel': self.exit,
         'ok': self.exit}, -1)
        self.info = 'BundesligaHD\nDeveloper: Maggy \nmod by openNFR'
        self['pluginInfo'] = Label(self.info)

    def exit(self):
        self.close()


def main(session, **kwargs):
    session.open(BundesligaHDConfig)


def Plugins(**kwargs):
    return PluginDescriptor(name=_('BundesligaHDConfig setup'), description=_('BundesligaHDConfig setup'), where=[PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU], icon='BundesligaHD.png', fnc=main)