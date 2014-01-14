#!/usr/bin/env python27
import argparse
import os
def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

print "[!] Screenshot Uploader to pomf.se [!]"

try:
    import requests
except ImportError:
    exit("Please install python-request")
plok = argparse.ArgumentParser(description='Do a screenshot and upload it to pomf.se with scrot')
plok.add_argument('--thumb', action='store_true', help='Uploading screenshot with thumbnail (20%)')
teng = plok.parse_args()
adain = which("scrot")
if not adain:
    print "Please install scrot to use this."
    exit()
babi = ".png"
jing = "pypomfscrot.png"
crot = os.path.isfile(jing)
if crot:
    nyet = 1
    lelah = "pypomfscrot_"+str(nyet)
    jing = lelah+babi
    crot = os.path.isfile(jing)
    while crot:
        nyet = nyet + 1
        lelah = "pypomfscrot_"+str(nyet)
        jing = lelah+babi
        crot = os.path.isfile(jing)
if teng.thumb:
    kontet = 20
    os.system("scrot -t "+str(kontet)+" "+jing)
    asu = lelah+"-thumb"+babi
else:
    os.system("scrot "+jing)
print "[~] Uploading - please wait..."
yay = requests.post(url="http://pomf.se/upload.php", files={"files[]":open(jing, "r")})
itte = yay.text.split(":")
hayaku = itte[1].split(",")
zenbu = hayaku[0]
if zenbu=="true":
    fak = yay.text.split('"')
    url = fak[17]
    print "[~] Upload Success!"
    print "[~] File URL: http://a.pomf.se/"+url
else:
    print "[X] Upload Failed..."
if teng.thumb:
    "[~] Uploading Thumbnail - please wait"
    yui = requests.post(url="http://pomf.se/upload.php", files={"files[]":open(asu, "r")})
    itte = yui.text.split(":")
    hayaku = itte[1].split(",")
    zenbu = hayaku[0]
    if zenbu=="true":
        fak = yui.text.split('"')
        url = fak[17]
        print "[~] Upload Success!"
        print "[~] File URL: http://a.pomf.se/"+url
    else:
        print "[X] Upload Failed..."
exit()
