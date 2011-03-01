#!/usr/bin/python2

import os

# Usage:
# Begin searching for commands: use up/down arrow keys to scroll, enter executes, left 
# arrow key will move selected items text to textbox for editing.  To enter different mode 
# (e.g. calc, music, url, etc) enter keyword followed by space.  Backspace will exit special
# mode. In music, tab switches between playlist, artists, and options.  Delete clears 
# playlist and end deletes single item from playlist.  Enter adds selected to end of playlist.

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
preferredApps = ["chromium", "urxvt", "pidgin", "xbindkeys_config", "google-chrome",
"lxappearance", "wicd-curses", "emacs", "susplock.py", "thunar", "ncmpcpp", "gvim",
"firefox"]

#whether or not to use connect to mpd
mpd = False
mpdcon = {'host':"/home/$USER/.mpd/socket", 'port':"6600"}

#Write history to hd- may make marginally slower, if you don't consider setting a hook
# in order to save the file before shutdown, command below
saveHistory = False

#cp /dev/shm/.pilaunch.hist ~/.config/pilaunch/pilaunch.hist
