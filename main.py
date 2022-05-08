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
import sys

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
        global isPlayingMovie
        global runningApp
        global omx_player1
        global omx_player2  
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
                print("Start video message")
                if(isPi) and len(data)>0:
                    print("Play video on PI:"+data[0]+".mp4")
                    playVideo(data[0])

            if(splitAddress[2] == "test"):
                print("Start video TEST message")
                if(isPi):
                    if(not(omx_player1 is None)):
                        omx_player1.quit()
                    omx_player1 = OMXPlayer(Path(VIDEOFILE_PATH+"/test.mp4"))

            if(splitAddress[2] == "status"):
                print("Get Status of video player1")
                if(not(omx_player1 is None)):
                    sendToMaster("status", omx_player1.playback_status())
                else :
                    sendToMaster("status", "none")
            
            if(splitAddress[2] == "stop"):
                print("Stop video TEST message")
                if(isPi):
                    if(not(omx_player1 is None)):
                        if(omx_player1.canQuit()):
                            omx_player1.quit()
                    if(not(omx_player2 is None)):
                        if(omx_player2.canQuit()):
                            omx_player2.quit()
        
            if(splitAddress[2] == "pause"):
                print("Pause video TEST message")


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

# Video player works with 1 or 2 screen according to setting file
# With 1 screen data[0].mp4 is played
# With 2 screns data[0].mp4 and data[0]2.mp4 is played
# File existing test is only testing the first file : be carefull !
def playVideo(videoFileName):
    global omx_player1
    global omx_player2
    global userSettingsData

    nbScreen = userSettingsData["video"]["screenNumber"]
    path = VIDEOFILE_PATH+"/"+videoFileName
    fileExist = os.path.exists(path+".mp4")
    print("PLAY VIDEO FILE :"+videoFileName)
    print("complete path: "+path)
    if(fileExist):
        print(" File exist :YES")
    else:
        print(" File exist :NO")


    if(nbScreen == 1 and fileExist):
        print("Play video : 2 screens")
        if(not(omx_player1 is None)):
            omx_player1.quit()
        omx_player1  = OMXPlayer(Path(path+".mp4"))

    elif(nbScreen == 2 and fileExist):
        print("Play video : 2 screens")
        if(not(omx_player1 is None)):
            omx_player1.quit()
        if(not(omx_player2 is None)):
            omx_player2.quit()
        omx_player1 = OMXPlayer(path+".mp4", dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['--no-osd','--no-keys','-b','--display=2','-o','local'])
        omx_player2 = OMXPlayer(path+"2.mp4", dbus_name='org.mpris.MediaPlayer2.omxplayer2', args=['--no-osd','--no-keys','-b','--display=7',])

    else:
        print("ERROR : NbScreen is wrong or file does not exist ! Playing aborted")
    


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
    # TODO test minimum configuration is available, otherwise, kill with error message 
    initSettings()


    # OSC SERVER
    # myip = get_ip()
    print(" ===== OSC SERVER ====")
    myip = "0.0.0.0"
    print("IP adress is : "+myip)
    try:
        server = SimpleServer((myip, 12344))
        print("server created")
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

    # OMX PLAYER INSTANCE
    global omx_player1
    global omx_player2
    omx_player1 = None
    omx_player2 = None



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
