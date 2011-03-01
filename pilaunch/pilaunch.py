#!/usr/bin/python2

import pygtk
pygtk.require('2.0')
import gtk
import subprocess
import os 
import sys
import re
import shutil
sys.path.append(os.path.expanduser("~/.config/pilaunch/"))
sys.path.append("/usr/share/pilaunch/")
try:
    import piconfig
except ImportError:
    print "Add piconfig file to ~/.config/pilaunch/ or /usr/share/pilaunch/"
if piconfig.mpd == True:
    from mpd import MPDClient, MPDError
    from socket import error as SocketError


class pilauncher:

    #delete event
    def delete_event(self, widget, event, data=None):
        return False

    #destroy function
    def destroy(self, widget, data=None):
        gtk.main_quit()
            
    #function to run selection or text input
    def runC(self, widget, data=None):

        #open url
        if self.isHttp == True:
            val = self.entry.get_text()
            val = self.browser + " " + val
            valArr = val.split(" ")
            subprocess.Popen(valArr).pid
            self.destroy(widget, data=None)
            return

        #web search
        if self.websearch == True:
            val = self.entry.get_text()
            val = val.replace(" ", "+")
            valArr = []
            valArr.append(self.browser)
            valArr.append(piconfig.searchengine + val)
            subprocess.Popen(valArr).pid
            self.destroy(widget, data=None)
            return
        
        #calculator
        if self.calc == True:
            if self.acpi != None:
                self.acpi.set_text("")
                self.acpi.hide()
                self.acpi = None
            expr = self.entry.get_text()
            ase = re.split("[\*\-\/\+\(\)\%]", expr)
            for a in ase:
                if "." not in a and a != "":
                    expr = expr.replace(a, a+".0")
                    while a in ase:
                        ase.remove(a)
            try:
                expr =  eval(expr)
            except:
                expr = "Expression not well formed"
            self.acpi = gtk.Label(expr)
            self.bbox.pack_start(self.acpi, False, False, 5)
            self.acpi.show()
            self.entry.set_text("")
            return

        own = False
        if self.nItr != None:
            val = self.tree.get_value(self.nItr, 0)
            #open with terminal
            if self.term == True:
                val = piconfig.terminal + " -e " + val + " &"
            #execute with sudo
            if self.isSudo == True:
                val = "sudo " + val
            own = False
        else:
            val = self.entry.get_text()
            if self.term == True:
                val = piconfig.terminal + " -e " + val + " &"
            if self.isSudo == True:
                val = "sudo " + val
            valArr = val.split(" ")            
            own = True

        #write selection to history file and only 50 entries long
        if self.hist != None:
            histFile = []
            f = open(self.hist)
            for l in f:
                histFile.append(l.strip())
            if val in histFile:
                histFile.remove(val)
            while len(histFile) >= 50:
                histFile.pop(0)
            histFile.append(val)
            f.close()
            f = open(self.hist, "w")
            for line in histFile:
                f.write(line + "\n")
            f.close()
            # i = 0
            # while i < len(histFile) and i < 50:
            #     f.write(histFile[i] + "\n")
            #     i = i + 1
            # f.close()
            
        if piconfig.saveHistory == True:
            self.saveHist()

        if own == False:
            subprocess.Popen(val, shell=True).pid
        elif own == True:
            subprocess.Popen(valArr).pid
        self.destroy(widget, data=None)

    #grabs key values to do various things
    def submitKey(self, widget, event):
        #print event.keyval
        if self.music == True and self.current == True:
            if event.keyval==65367: #end
                self.delcur = True
                self.artist = False
                self.album = False
                self.tracks = False
                self.current = False
                self.mpdCmd()

        if event.keyval==65293: #enter/return
            if self.music == False:
                try:
                    self.runC(widget, data=None)
                except:
                    print "Error running selection or nothing selected"
                    self.destroy(widget, data=None)
            else:
                self.mpdCmd()
            
        elif event.keyval==65535: #delete
            if self.music == True:
                self.mclient.clear()
                if self.current == True:
                    self.getMusic()

        elif event.keyval==65307: #escape
            if self.music == True:
                self.mclient.disconnect()
            self.destroy(widget, data=None)

        elif event.keyval==65363: #right
            if self.music == False:
                if self.window.get_focus()!=self.entry and self.window.get_focus()!=self.rbox:
                    self.window.set_focus(self.rbox)
                    self.entry.set_text(self.tree.get_value(self.nItr, 0))
            else:
                self.window.set_focus(self.rbox)
                if self.current == True:
                    return
                if self.artist == True:
                    self.artist = False
                    self.album = True
                elif self.album == True:
                    self.album = False
                    self.tracks = True
                elif self.tracks == True:
                    self.current = True
                    self.tracks = False
                self.getMusic()                    

        elif event.keyval==65361: #left
            if self.music == False:
                if self.window.get_focus() != self.entry:
                    self.entry.set_text(self.tree.get_value(self.nItr, 0))
                    self.window.set_focus(self.entry)
                    self.entry.set_position(self.entry.get_text_length())
            else:
                if self.artist == True:
                    self.current = True
                    self.artist = False
                elif self.current == True:
                    self.current = False
                    self.artist = True
                elif self.album == True:
                    self.album = False
                    self.artist = True
                elif self.tracks == True:
                    self.album = True
                    self.tracks = False
                self.nItr = None
                self.getMusic()

        elif event.keyval==65514: #alt
            self.saveHist()
            if self.isShow == False:
                self.isShow = True
                stdout = ""
                if os.path.exists(self.info):
                    stdout = subprocess.Popen([self.info], shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
                    if self.acpi != None:
                        self.acpi.set_text("")
                        self.acpi.hide()
                        self.acpi = None
                    self.acpi = gtk.Label(stdout)
                    self.acpi.set_justify("left")
                    self.acpi.set_line_wrap(True)
                    self.bbox.pack_start(self.acpi, False, False, 5)
                    self.acpi.show()
            else:
                self.acpi.hide()
                self.acpi = None
                self.isShow = False
                size = self.window.get_default_size()
                self.window.resize(size[0], size[1])

        elif event.keyval==65289: #tab
            if self.music == True:

                if self.current == True:
                    self.current = False
                    self.options = True
                elif self.artist == True:
                    self.current = True
                    self.artist = False
                elif self.options == True:
                    self.artist = True
                    self.options = False
                else:
                    self.album = False
                    self.tracks = False
                    self.current = True
                
                self.getMusic()
             
        elif event.keyval!=65289 and event.keyval!=65364 and event.keyval!=65362 and self.music == False:
            if self.entry.get_text()!="": 
                self.getDatabase()
            else:
                self.getHist()
                self.rbox.scroll_to_cell('0')
                self.rbox.set_cursor('0', focus_column=None)
                size = self.window.get_default_size()
                self.window.resize(size[0], size[1])

    #submit certain keys on press as opposed to release            
    def submitArrowKey(self,widget, event):
        if event.keyval==65362: #up
            if self.nItr == None and self.music == True:
                return
            if self.window.get_focus() != self.rbox:
                self.window.set_focus(self.rbox)        
            if len(self.prevArr) != 0:
                self.nItr = self.prevArr.pop()

        elif event.keyval==65364: #down 
            if self.nItr == None and self.music == True:
                return
            if self.window.get_focus() != self.rbox:
                self.window.set_focus(self.rbox)
            if self.tree.iter_next(self.nItr) != None:
                self.prevArr.append(self.nItr)
                self.nItr = self.tree.iter_next(self.nItr)

        elif event.keyval==65288: #backspace
            if self.music == True:
                self.lbox.show()
                self.music = False
            if self.window.get_focus() != self.entry:
                self.window.set_focus(self.entry)
                self.entry.set_position(self.entry.get_text_length())
            if self.entry.get_position() == 0:
                self.sudo.hide()
                self.music = False
                self.isSudo = False
                self.calc = False
                self.isHttp = False
                self.websearch = False
                self.term = False

        elif event.keyval!=65361: #left
            if self.window.get_focus() != self.entry and self.music == False:
                self.window.set_focus(self.entry)
                self.entry.set_position(self.entry.get_text_length())


    #gets history if present
    def getHist(self):
        if self.calc == False and self.isHttp == False and self.websearch == False:
            self.tree.clear()
            if self.hist != None:
                file = open(self.hist)
                self.prevArr = []
                for line in file.readlines():
                    self.tree.prepend([line.strip()])
                file.close()
                self.scrollbox.show()
                self.window.set_focus(self.rbox)
                self.window.set_focus(self.entry)
                self.entry.set_position(self.entry.get_text_length())
                self.nItr = self.tree.get_iter_root()
                
            else:
                self.scrollbox.hide()

    #populate database with contents of $PATH
    def getDatabase(self):
        self.tree.clear()
        query = self.entry.get_text()
        #for sudo
        if query.startswith(piconfig.sudo + " "):
            self.isSudo = True
            self.sudo.set_text("sudo")
            self.sudo.show()
            query = ""
            self.entry.set_text("")
        #web search
        if query.startswith(piconfig.websearch + " "):
            self.websearch = True
            self.sudo.set_text("websearch")
            self.sudo.show()
            query = ""
            self.entry.set_text("")
        #check of web
        if query.startswith(piconfig.web + " "):
            self.isHttp = True
            self.sudo.set_text("url")
            self.sudo.show()
            query = ""
            self.entry.set_text("")
        #check for calc
        if query.startswith(piconfig.calculator + " "):
            self.calc = True
            self.sudo.set_text("calculator")
            self.sudo.show()
            query = ""
            self.entry.set_text("")
        #run in terminal
        if query.startswith(piconfig.term + " "):
            self.term = True
            self.sudo.set_text("terminal")
            self.sudo.show()
            query = ""
            self.entry.set_text("")
            
        if query.startswith(piconfig.music + " "):
            if piconfig.mpd == True:
                self.music = True
                self.current = True
                self.artist = False
                self.album = False
                self.tracks = False
                self.options = False
                self.hasFormer = False
                self.sudo.set_text("music")
                self.sudo.show()
                query = ""
                self.entry.set_text("")
                self.getMusic()
                return
        #need this here for posterity
        if self.calc == True or self.isHttp == True or self.websearch == True:
            self.scrollbox.hide()
            return
        match = []
        for i in self.path.split(":"):
            i = i.strip()
            try:
                for filename in os.listdir(i):
                    if filename.startswith(query):
                        if os.path.isfile(i + "/" + filename):
                            filename = filename.strip()
                            match.append(filename)
            except OSError:
                print i + "not found"
        match.sort()
                
        #add history to beginning
        if os.path.exists(self.hist):
            file = open(self.hist)
            for line in file.readlines():
                if line.startswith(query):
                    line = line.strip()
                    if line in match:
                        match.remove(line)
                    match.insert(0, line)
                    
        #add preferred programs to beginning (before history)
        if len(piconfig.preferredApps) > 0:
            for app in piconfig.preferredApps:
                if app.startswith(query):
                    if app in match:
                        match.remove(app)
                    match.insert(0, app)

        if len(match)!=0:
            for k in match:
                self.tree.append([k])
            self.prevArr = []
            self.scrollbox.show()
            self.rbox.scroll_to_cell('0', column=None)
            self.rbox.set_cursor('0', focus_column=None)
            self.window.set_focus(self.rbox)
            self.window.set_focus(self.entry)
            self.entry.set_position(self.entry.get_text_length())
        else:
            self.scrollbox.hide()
            size = self.window.get_default_size()
            self.window.resize(size[0], size[1])
        self.nItr = self.tree.get_iter_root()

    def getMusic(self):
        self.mclient = MPDClient()
        self.connected = False
        self.delcur = False
        if self.connected == False:
            try:
                self.mclient.connect(piconfig.mpdcon['host'], piconfig.mpdcon['port'])
                self.connected = True
            except:
                self.connected = False
                print "failed to connect"
                return
        if self.current == True:
            playlist =  self.mclient.playlistinfo()
            if len(playlist) > 0:
                self.list = {}
                self.tree.clear()
                curr = self.mclient.currentsong()['id']
                count = 0
                fcount = 0
                for s in playlist:
                    if curr == s['id']:
                        self.tree.append([s['title'] + "\t...[Now playing]..."])
                        self.rbox.set_cursor(str(count), focus_column=None)
                        self.rbox.scroll_to_cell(str(count), column=None)
                        fcount = count
                    else:
                        self.tree.append([s['title']])
                    self.list[s['title']] = s['id']
                    count = count + 1
            else:
                self.current = False
                self.artist = True
                self.getMusic()
                return
        elif self.artist == True:
            artists = self.mclient.list("artist")
            artists.sort()
            self.tree.clear()
            for a in artists:
                if a != "":
                    self.tree.append([a])
                if self.hasFormer == True:
                    self.rbox.set_cursor(str(self.lartist), focus_column=None)
                    self.rbox.scroll_to_cell(str(lartist), column=None)
        elif self.album == True:
            if self.nItr != None:
                #self.curartist = self.tree.get_value(self.nItr, 0)
                self.curartist = self.tree.get_value(self.tree.get_iter_from_string(str(self.rbox.get_cursor()[0][0])), 0)
            albums = self.mclient.list("album", self.curartist)
            self.tree.clear()
            for al in albums:
                if al != "":
                    self.tree.append([al])
        elif self.tracks == True:
            if self.nItr != None:
                #self.curalbum = self.tree.get_value(self.nItr, 0)
                self.curalbum = self.tree.get_value(self.tree.get_iter_from_string(str(self.rbox.get_cursor()[0][0])), 0)
            tracks = self.mclient.find("album", self.curalbum)
            self.tree.clear()
            for t in tracks:
                self.tree.append([t['title']])
        elif self.options == True:
            self.tree.clear()
            options = self.mclient.status()
            if options['consume'] == '0':
                self.tree.append(["Toggle consume [off]"])
            else:
                self.tree.append(["Toggle consume [on]"])
            if options['repeat'] == '0':
                self.tree.append(["Toggle repeat [off]"])
            else:
                self.tree.append(["Toggle repeat [on]"])
            if options['random'] == '0':
                self.tree.append(["Toggle random [off]"])
            else:
                self.tree.append(["Toggle random [on]"])
            if options['single'] == '0':
                self.tree.append(["Toggle single [off]"])
            else:
                self.tree.append(["Toggle single [on]"])
        size = self.window.get_default_size()
        self.window.resize(size[0], size[1]+50)
        self.lbox.hide()
        self.scrollbox.show()
        self.window.set_focus(self.rbox)
        self.nItr = self.tree.get_iter_root()


    def mpdCmd(self):
        if self.current == True:
            songTitle = self.tree.get_value(self.tree.get_iter_from_string(str(self.rbox.get_cursor()[0][0])), 0)
            songTitle = songTitle.split("\t")[0]
            songid = self.list[songTitle]
            self.mclient.playid(songid)
            self.music = False
            self.mclient.disconnect()
            self.destroy(self, data=None)

        elif self.artist == True:
            #artist = self.tree.get_value(self.nItr, 0)
            artist = self.tree.get_value(self.tree.get_iter_from_string(str(self.rbox.get_cursor()[0][0])), 0)
            self.mclient.add(artist)
            self.mclient.play()

        elif self.album == True:
            #album = self.tree.get_value(self.nItr, 0)
            album = self.tree.get_value(self.tree.get_iter_from_string(str(self.rbox.get_cursor()[0][0])), 0)
            self.mclient.findadd("album", album)
            self.mclient.play()

        elif self.tracks == True:
            #track = self.tree.get_value(self.nItr, 0)
            track = self.tree.get_value(self.tree.get_iter_from_string(str(self.rbox.get_cursor()[0][0])), 0)
            self.mclient.findadd("title", track)
            self.mclient.play()

        elif self.delcur == True:
            track = self.tree.get_value(self.nItr, 0)
            self.mclient.deleteid(self.list[track])
            self.current = True
            self.delcur = False
            self.getMusic()
        
        elif self.options == True:
            option = self.tree.get_value(self.nItr, 0)
            if "consume" in option and "off" in option:
                self.mclient.consume(1)
            elif "consume" in option and "on" in option:
                self.mclient.consume(0)
            elif "repeat" in option and "off" in option:
                self.mclient.repeat(1)
            elif "repeat" in option  and "on" in option:
                self.mclient.repeat(0)
            elif "random" in option and "off" in option:
                self.mclient.random(1)
            elif "random" in option and "on" in option:
                self.mclient.random(0)
            elif "single" in option and "off" in option:
                self.mclient.single(1)
            elif "single" in option and "on" in option:
                self.mclient.single(0)
            self.getMusic()

    def saveHist(self):
        shutil.copyfile(self.hist, self.fhist)

    def __init__(self):

        #window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.window.set_default_size(350, 100)
        self.window.set_title("pilaunch")
        self.window.set_modal(True)
        self.window.stick()
        self.window.set_decorated(False)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_events(gtk.gdk.KEY_RELEASE_MASK)
        self.window.set_events(gtk.gdk.KEY_PRESS_MASK)
        self.window.present()
        self.window.set_keep_above(True)
        self.window.set_focus_on_map(True)
        self.window.connect("key_release_event", self.submitKey)
        self.window.connect("key_press_event", self.submitArrowKey)

        self.box = gtk.HBox(False, 10)
        self.window.add(self.box)
        
        #other variables
        self.isSudo = False
        self.isShow = False
        self.calc = False
        self.acpi = None
        self.isHttp = False
        self.websearch = False
        self.term = False
        self.music = False

        #Env variables
        self.info = os.path.expanduser("~/.config/pilaunch/pilaunchextra.py")
        self.fhist = os.path.expanduser("~/.config/pilaunch/pilaunch.hist")
        if os.path.exists("/dev/shm/.pilaunch.hist"):
            self.hist = "/dev/shm/.pilaunch.hist"
        elif os.path.exists("/dev/shm"):
            self.hist = "/dev/shm/.pilaunch.hist"
            if os.path.exists(self.fhist):
                shutil.copyfile(self.fhist, self.hist)
            else:
                open(self.hist, "w").close()
        else:
            self.hist = None
        self.path = piconfig.path
        self.browser = piconfig.browser
        self.editor = piconfig.editor
        self.terminal = piconfig.terminal
        
        #left box
        self.lbox = gtk.VBox(False, 5)
        self.box.pack_start(self.lbox)
        
        #right box
        self.tree = gtk.ListStore(str)
        self.rbox = gtk.TreeView(self.tree)
        self.rbox.set_enable_search(True)
        self.render = gtk.CellRendererText()
        self.col = gtk.TreeViewColumn()
        self.rbox.append_column(self.col)
        self.col.pack_start(self.render,expand=True)
        self.col.add_attribute(self.render, 'text', 0)
        self.col.set_spacing(0)
        self.rbox.set_headers_visible(False)
        #self.rbox.set(horizontal-separators, 0)
        self.scrollbox = gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        self.scrollbox.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.scrollbox.set_size_request(150, 80)
        self.box.pack_start(self.scrollbox)
        self.scrollbox.add(self.rbox)
        
        #left bottom and top box
        self.bbox = gtk.HBox(False, 0)
        self.tbox = gtk.HBox(False, 0)
        self.lbox.pack_start(self.tbox)
        self.lbox.pack_start(self.bbox)

        #text entry on top left
        self.sudo = gtk.Label()
        self.sudo.set_use_markup(True)
        self.entry = gtk.Entry(max=0)
        self.tbox.pack_start(self.sudo, False, False, 0)
        self.tbox.pack_start(self.entry, True, True, 5)

        #show textbox
        self.entry.show()
        #show boxes
        self.rbox.show()
        self.lbox.show()
        self.tbox.show()
        self.bbox.show()
        self.box.show()
        #show window
        self.window.show()
        self.window.set_focus(self.entry)
        self.entry.set_position(0)
        self.getHist()

    def main(self):
        gtk.main()


if __name__=="__main__":
    win = pilauncher()
    win.main()
