#!/usr/bin/python2

import subprocess
import os

#play/pause
#emails
#

def getNet():
    ifconfig = subprocess.Popen(["ifconfig"], stdout = subprocess.PIPE).communicate()[0]
    iwconfig1 = subprocess.Popen(["iwconfig", "wlan0"], stdout = subprocess.PIPE).communicate()[0]
    address = ifconfig[ifconfig.find("inet addr:")+10:ifconfig.find("Bcast:")-2]
    # if address.startswith("127.0"):
    #     address =
    ifconfig = subprocess.Popen(["ifconfig", "eth0"], stdout = subprocess.PIPE).communicate()[0]
    output = ""

    if "ESSID:off" not in iwconfig1:
        address = address[address.find("inet addr:")+10:]
        essid = iwconfig1.find("ESSID")
        essid_end = iwconfig1.find("Mode")
        essid_name = iwconfig1[essid+7:essid_end-14]
        strength = iwconfig1.find("Quality")
        strength_end = iwconfig1.find("Signal")
        strength_num = iwconfig1[strength+8:strength_end-2]
        strength = int(strength_num[:2])
        strength_total = int(strength_num[3:])
        s = str(int(100 * (strength / float(strength_total))))
        output = address + "- " + s + "%"
        #output = essid_name + "- " + s + "%\nip: " + address
    elif "inet addr" in ifconfig:
        output = address
    else:
        return "ip: No connection"

    return "ip:" + output.strip()

def getVol():
    stdout = subprocess.Popen(["amixer"], stdout = subprocess.PIPE).communicate()[0]
    point1 = stdout.find("'Master'")
    point2 = stdout.find("Simple mixer control 'Headphone',0")
    used = stdout[point1:point2]
    volume = used.find("%")
    rocky = used[volume-4:volume+3]
    volume1 = used[volume-2:volume]

    if "[" in rocky and "]" in rocky:
	volume2 = rocky[1:4]
	if "[" in volume2:
            volume3 = volume2[1:]
            if "[" in volume3:
                volume4 = volume3[1:]
                noise = volume4 + "%"
            else:	
                noise = volume3 + "%"
	else:	
		noise = volume2 + "%"
		
    mute = used.find(noise)
    mute1 = used[mute:]
    if "off" in mute1:
	noise = "Mute"

    return "Volume: " + noise.strip()

def getBat():
    stdout = subprocess.Popen(["acpi"], shell=True, stdout=subprocess.PIPE).communicate()[0]
    batt = stdout[:stdout.find(":")-5] + stdout[stdout.find(":"):]
    if "Discharging" in batt:
        batt = batt[:batt.find("Discharging")] + batt[batt.find("Discharging")+12:]
        batt = batt.replace("remaining", "left")
    elif "Full" in batt:
        batt = batt[:batt.find("Full")+4]
    return batt.strip()

def getHDD():
    stdout = subprocess.Popen(["df -h|grep -E --regexp='(/)$|(home)'|sed 's/\/$/\/root/'|awk '{print $6 \"  \" $5 }'"], stdout=subprocess.PIPE, shell=True).communicate()[0]
    stdout = stdout.replace("\n", "\t")
    return stdout.strip()

print getVol() + "\t\t" + getNet() + "\n" + getBat() + "\n" + getHDD()

