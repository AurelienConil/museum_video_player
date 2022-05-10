import platform
import getpass
import os
import json
import subprocess
from OSC import OSCClient, OSCMessage, OSCServer
import time
import threading
import socket

import sys
from VidPlayerClass import VidPlayer

MAIN_PATH = "/home/pi/Documents/museum_video_player"
VIDEOFILE_PATH = "/home/pi/Videos" # Long term in fat32 partition
USER_SETTINGS_PATH = VIDEOFILE_PATH+"/settings/userSettings.json" # better close to the video file : fat32 editing
DEFAULT_SETTINGS_PATH = MAIN_PATH+"/settings/defaultSettings.json"

isPi = True
if (platform.machine().startswith("x86")):
    isPi = False
    if(platform.system() == "Darwin" and getpass.getuser()=='adminmac'):
        #mac os et Aurelien Conil
        MAIN_PATH = "/Users/adminmac/Boulot/JeanGiraudoux/GIT/museum_video_player"
        VIDEOFILE_PATH = "/Users/adminmac/Movies/JeanGiraudoux"
        USER_SETTINGS_PATH = VIDEOFILE_PATH+"/settings/UserSettings.json" # better close to the video file : fat32 editing
        DEFAULT_SETTINGS_PATH = MAIN_PATH+"/settings/defaultSettings.json"
    elif(platform.system() == "Darwin" and getpass.getuser()!='collor_nor'):
        #print("Martin Rossi, tu dois mettre les chemin a l'interrieur du programme python")
        #mac os et Martin Rossi (COLL OR_NOR)
        VIDEOFILE_PATH = ""

if(isPi):
    from omxplayer.player import OMXPlayer



GLOBAL_SETTINGS_PATH = MAIN_PATH+"/data/datajson.json" #NOT USED : TODO DELETE

class SimpleServer(OSCServer):
    def __init__(self, t):
        OSCServer.__init__(self, t)
        self.selfInfos = t
        self.addMsgHandler('default', self.handleMsg)

    def handleMsg(self, oscAddress, tags, data, client_address):
        global machine
        global client
        global runningApp
        global vid
        global flagToStop
        global flagToPlayMain
        print("OSC message received on : "+oscAddress)
        print("data: ")
        print(data)

        splitAddress = oscAddress.split("/")
        #print(splitAddress)    
        ############## APP itself #############
        if(splitAddress[1] == "app"):

            if(splitAddress[2] == "test"):
                print("TEST"*10)
                sendTestToMaster("TEST")
            
            if(splitAddress[2] == "ispi"):
                print("is pi ?")
                print(isPi)
                
            if(splitAddress[2]=="quit"):
                print("Quitting the app : runningApp=false")
                runningApp = False

        ############## VIDEO PLAYER, OMX #############
        if(splitAddress[1] == "video"):
            
            if(splitAddress[2] == "playmain"):
                if(not(flagToPlayMain)):
                    print("Play main file")
                    flagToPlayMain = True
                    while(vid.state != vid.PLAYINGMAIN):
                        time.sleep(10)
                    flagToPlayMain = False
                    print("Flag to false")
                else :
                    print("ERROR Main file already opening")
  

            if(splitAddress[2] == "status"):
                vid.printState()

            
            if(splitAddress[2] == "stop"):
                if(not(flagToStop)):
                    print("Stop all action, go to waiting mode")
                    flagToStop = True
                    while(vid.state != vid.WAITING):
                        time.sleep(10)
                    flagToStop = False
                    print("Flag to false")
                else :
                    print("ERROR Stop flag already operating")


        

        ############## RPI itself #############
        elif(splitAddress[1] == "rpi"):
            if(splitAddress[2] == "shutdown"):
                print("Turning off the rpi")
                #setVeille(True) # NOT IMPLETEMED YET
                #powerOff() # NOT IMPLETEMED YET
            if(splitAddress[2] == "reboot"):
                print("Reboot the machine")
                #setVeille(True) # NOT IMPLETEMED YET
                #reboot() # NOT IMPLETEMED YET

def sendTestToMaster(arg):
    global client_master
    oscmsg = OSCMessage()
    oscmsg.setAddress("/test")
    oscmsg.append(arg)
    client_master.send(oscmsg)

def sendToMaster(adress, arg):
    global client_master
    oscmsg = OSCMessage()
    oscmsg.setAddress("/"+adress)
    oscmsg.append(arg)
    client_master.send(oscmsg)

def initSettings():
    global userSettingsData
    global confSettings
    # load existing user settings

    settingsFilePath = DEFAULT_SETTINGS_PATH
    if(os.path.exists(USER_SETTINGS_PATH)):
        settingsFilePath = USER_SETTINGS_PATH
        print("SETTINGS : user setting")
    else:
        print("SETTING : default ")

    with open(settingsFilePath, 'r') as userFp:
        userSettingsData = json.load(userFp, encoding='utf-8')

def get_ip():   
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def main():

    global userSettingsData
    print(" ===== init settings ====")
    # will ensure any default settings are present in datajson/metadata
    # TODO test minimum configuration is available, otherwise, kill with error message 
    initSettings()

    #PLAYLIST
    playlist = []
    try:
        media = VIDEOFILE_PATH+"/"+userSettingsData["playlist"]["mainMediaPath"]
        playlist.append(media)
        media = VIDEOFILE_PATH+"/"+userSettingsData["playlist"]["waitingMediaPath"]
        playlist.append(media)
    
    except :
        print(" ERROR : creating playlist. Error in json file. Try json_tester.py")
        print("Unexpected error:", sys.exc_info()[0])
        #Exit or Terminate successfully
        sys.exit(0)
    
    print("playlist : ")
    print(playlist[0])
    print(playlist[1])
    global vid
    global flagToPlayMain 
    global flagToStop
    vid = VidPlayer(userSettingsData["video"]["screenNumber"], playlist)
    flagToPlayMain = False
    flagToStop = False

    # OSC SERVER
    # myip = get_ip()
    print(" ===== OSC SERVER ====")
    myip = "0.0.0.0"
    #myip = get_ip()
    myport = userSettingsData["in"]["port"]
    print("IP adress is : "+myip+" port="+str(myport))
    try:

        server = SimpleServer((myip, myport))
        print("server created on port :"+str(myport))
    except :
        print(" ERROR : creating server")
        print("Unexpected error:", sys.exc_info()[0])
        #Exit or Terminate successfully
        sys.exit(0)
        
    try:
        st = threading.Thread(target=server.serve_forever)
    except:
        print(" ERROR : creating thread")
        print("Unexpected error:", sys.exc_info()[0])
        #Exit or Terminate successfully
        sys.exit(0)
    try:
        st.start()
    except:
        print(" ERROR : starting thread")
        print("Unexpected error:", sys.exc_info()[0])
        #Exit or Terminate successfully
        sys.exit(0)

    print(" OSC server is running")

    # OSC CLIENT : send osc message
    print(" ===== OSC CLIENT ====")
    global client_master
    client_master = OSCClient()
    mip = userSettingsData["master"]["ip"]
    mport = userSettingsData["master"]["port"]
    print("Client OSC to master | ip: "+mip+"  | port: "+str(mport))
    client_master.connect((mip, mport))

    # MAIN LOOP
    global runningApp
    runningApp = True

    print(" ===== STARTING MAIN LOOP ====")
    while runningApp:
        # This is the main loop
    
        # Do something here
        
        if(flagToPlayMain):
            vid.playMain()
        if(flagToStop):
            vid.stopAll()
            flagToStop = False
        if(vid.state == vid.ASKPLAYINGMAIN):
            vid.playMain()
        if(vid.state == vid.ASKPLAYINGSECOND):
            vid.playSec()
        try:
            time.sleep(1)
        except:
            print("User attempt to close programm")
            runningApp = False

    print("Main loop is quit. Closing software")
    # Closing omx instances
    print("STOP video first")
    vid.stopAll()
    # CLOSING THREAD AND SERVER
    print(" Ending programme")
    server.running = False
    print(" Join thread")
    st.join()
    print(" Close Server")
    server.close()
    print(" End of sript . Bye Bye")


if __name__ == "__main__":
    main()
