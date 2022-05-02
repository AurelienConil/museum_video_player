import platform
import getpass
import os
import json
import subprocess
from OSC import OSCClient, OSCMessage, OSCServer
import time
import threading
import socket
from pathlib import Path

MAIN_PATH = "/home/Documents/museum_video_player"
VIDEOFILE_PATH = "/home/Videos"
UNIVERSALMEDIAPLAYER_PATH = ""

isPi = True
if (platform.machine().startswith("x86")):
    isPi = False
    if(platform.system() == "Darwin" and getpass.getuser()=='adminmac'):
        #mac os et Aurelien Conil
        VIDEOFILE_PATH = "/Users/adminmac/Boulot/Radiologic/GIT/radiologic2"
        UNIVERSALMEDIAPLAYER_PATH = "/Users/adminmac/Boulot/Universal-Media-Player/GIT/universalMediaPlayer"
    elif(platform.system() == "Darwin" and getpass.getuser()!='collor_nor'):
        #print("Martin Rossi, tu dois mettre les chemin a l'interrieur du programme python")
        #mac os et Martin Rossi (COLL OR_NOR)
        VIDEOFILE_PATH = "/Users/collor_nor/Documents/DEV/repos/Radiologic\ Project/radiologic2"
        UNIVERSALMEDIAPLAYER_PATH = "/Users/collor_nor/Documents/DEV/repos/Radiologic\ Project/universalMediaPlayer"

if(isPi):
    from omxplayer.player import OMXPlayer

USER_SETTINGS_PATH = MAIN_PATH+"/settings/UserSettings.json"
DEFAULT_SETTINGS_PATH = MAIN_PATH+"/settings/defaultSettings.json"
GLOBAL_SETTINGS_PATH = MAIN_PATH+"/data/datajson.json"

class SimpleServer(OSCServer):
    def __init__(self, t):
        OSCServer.__init__(self, t)
        self.selfInfos = t
        self.addMsgHandler('default', self.handleMsg)

    def handleMsg(self, oscAddress, tags, data, client_address):
        global machine
        global client
        global isPlayingMovie
        global runningApp
        global omx_player
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
                runningApp = False
                
            if(splitAddress[2] == "update"):
                print("update Radiologic2")
                update()
                reboot()
        
        ############## VIDEO PLAYER, OMX #############
        if(splitAddress[1] == "video"):
            
            if(splitAddress[2] == "start"):
                print("Start video TEST message")

            if(splitAddress[2] == "test"):
                print("Start video TEST message")
                if(isPi):
                    omx_player = OMXPlayer(VIDEOFILE_PATH+"/test.mp4")

            
            if(splitAddress[2] == "stop"):
                print("Stop video TEST message")
                if(isPi):
                    omx_player.quit()
        
            if(splitAddress[2] == "pause"):
                print("Pause video TEST message")


        ############## RPI itself #############
        elif(splitAddress[1] == "rpi"):
            if(splitAddress[2] == "shutdown"):
                print("Turning off the rpi")
                setVeille(True)
                powerOff()
            if(splitAddress[2] == "reboot"):
                print("Reboot the machine")
                setVeille(True)
                reboot()

def update():
    print("========= UPDATE PYTHON SCRIPT ======")
    os.chdir(MAIN_PATH+"/script")
    subprocess.call(["./update.sh"])
    print("========= UPDATED PYTHON SCRIPT ======")

def sendTestToMaster(arg):
    global client_master
    oscmsg = OSCMessage()
    oscmsg.setAddress("/test")
    oscmsg.append(arg)
    client_master.send(oscmsg)


def initSettings():
    global userSettingsData
    global confSettings
    # load existing user settings

    settingsFilePath = DEFAULT_SETTINGS_PATH
    if(os.path.exists(USER_SETTINGS_PATH)):
        settingsFilePath = USER_SETTINGS_PATH

    with open(settingsFilePath, 'r') as userFp:
        userSettingsData = json.load(userFp)

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

    print(" ===== init settings ====")
    # will ensure any default settings are present in datajson/metadata
    initSettings()


    # OSC SERVER
    # myip = get_ip()
    myip = "0.0.0.0"
    print("IP adress is : "+myip)
    try:
        server = SimpleServer((myip, 12344))
    except:
        print(" ERROR : creating server")
    print("server created")
    try:
        st = threading.Thread(target=server.serve_forever)
    except:
        print(" ERROR : creating thread")
    try:
        st.start()
    except:
        print(" ERROR : starting thread")

    print(" OSC server is running")

    # OSC CLIENT : OPENFRAMEWORKS APP
    global client_master
    client_master = OSCClient()
    mip = userSettingsData["metadata"]["master"]["ip"]
    mport = userSettingsData["metadata"]["master"]["port"]
    client_master.connect((mip, mport))

    # OMX PLAYER INSTANCE
    global omx_player


    # MAIN LOOP
    global runningApp
    runningApp = True

    print(" ===== STARTING MAIN LOOP ====")
    while runningApp:
        # This is the main loop
        # Do something here
        try:
            time.sleep(1)
        except:
            print("User attempt to close programm")
            runningApp = False

    # CLOSING THREAD AND SERVER
    print(" Ending programme")
    server.running = False
    print(" Join thread")
    st.join()
    server.close()
    print(" This is probably the end")


if __name__ == "__main__":
    main()
