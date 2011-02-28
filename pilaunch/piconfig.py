#!/usr/bin/python2

import os

#desktop defaults
browser = "chromium"
searchengine = "http://www.google.com/search?q="
editor = "emacs"
path = os.path.expandvars("$PATH") # + ":/home/vince/.scripts
terminal = "urxvt"


#keywords-- these will only be activated by typing them in, followed by a space
calculator = "c" #"calc"
web = "u" #"url"
websearch = "w" #"web"
sudo = "su"
term = "t" #"term" #bring up a new terminal running it
music = "m" #"music" #support for mpd

#preferred applications-- will appear at the beginning of any matching search
preferredApps = ["chromium", "urxvt", "pidgin", "xbindkeys_config", "google-chrome", "lxappearance", "wicd-curses", "emacs", "susplock.py", "slock", "thunar", "ncmpcpp", "gvim"]

#whether or not to use connect to mpd
mpd = False
mpdcon = {'host':"/home/$USER/.mpd/socket", 'port':"6600"}

#Write history to hd- may make marginally slower, if you don't consider setting a hook
# in order to save the file before shutdown, command below
saveHistory = False

#cp /dev/shm/.pilaunch.hist ~/.config/pilaunch/pilaunch.hist
