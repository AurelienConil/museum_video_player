import json
import os
import platform
import getpass

MAIN_PATH = "/home/pi/Documents/museum_video_player"
VIDEOFILE_PATH = "/media/fat32"
USER_SETTINGS_PATH = VIDEOFILE_PATH+"/settings/userSettings.json" # better close to the video file : fat32 editing
DEFAULT_SETTINGS_PATH = MAIN_PATH+"/settings/defaultSettings.json"

isPi = True
if (platform.machine().startswith("x86")):
    isPi = False
    if(platform.system() == "Darwin" and getpass.getuser()=='adminmac'):
        #mac os et Aurelien Conil
        MAIN_PATH = "/Users/adminmac/Boulot/JeanGiraudoux/GIT/museum_video_player"
        VIDEOFILE_PATH = "/Users/adminmac/Movies/JeanGiraudoux"
        USER_SETTINGS_PATH = VIDEOFILE_PATH+"/settings/userSettings.json" # better close to the video file : fat32 editing
        DEFAULT_SETTINGS_PATH = MAIN_PATH+"/settings/defaultSettings.json"
    elif(platform.system() == "Darwin" and getpass.getuser()!='collor_nor'):
        #print("Martin Rossi, tu dois mettre les chemin a l'interrieur du programme python")
        #mac os et Martin Rossi (COLL OR_NOR)
        VIDEOFILE_PATH = ""

settingsFilePath = DEFAULT_SETTINGS_PATH
if(os.path.exists(USER_SETTINGS_PATH)):
    settingsFilePath = USER_SETTINGS_PATH
    print("::SETTINGS : user setting")
else:
    print("::SETTING : default ")

with open(settingsFilePath, 'r') as userFp:
    userSettingsData = json.load(userFp)





def fileExist(path, ext, sub=""):

    finalPath = VIDEOFILE_PATH+"/"+sub+"/"+path+"."+ext
    msg = "check if file "+finalPath+" exist ?"
    if(os.path.exists(finalPath)):
        msg += "YES"
    else : 
        msg += "NO"
    print(msg)

def dirExist(path):

    finalPath = VIDEOFILE_PATH+"/"+path
    msg = "check if directory "+finalPath+" exist ?"
    exist = False
    if(os.path.isdir(finalPath)):
        msg += "YES"
        exist= True
    else : 
        msg += "NO"
    print(msg)
    return exist

print("::Master IP")
print(userSettingsData["master"]["ip"])

print("::Master port")
print(userSettingsData["master"]["port"])

print("::Raspberry pi name")
print(userSettingsData["identity"]["name"])

print("::Raspberry pi video screen number")
print(userSettingsData["video"]["screenNumber"])

print("::Main media file name")
print(userSettingsData["playlist"]["mainMediaPath"]+".mp4")
fileExist(userSettingsData["playlist"]["mainMediaPath"], "mp4")

print("::Secondary media file name")
print(userSettingsData["playlist"]["waitingMediaPath"]+".mp4")
fileExist(userSettingsData["playlist"]["waitingMediaPath"], "mp4")

if("random" in userSettingsData):
    print(":: Random Found")
    print(":: Number of random folder")
    randomNbFolder = userSettingsData["random"]["nbFolder"]
    print(randomNbFolder)
    for i in range(randomNbFolder):
        folderName = str(i+1)
        if(dirExist(folderName)):
            fileExist(userSettingsData["playlist"]["waitingMediaPath"], "mp4", folderName )
            fileExist(userSettingsData["playlist"]["waitingMediaPath"], "mp4", folderName)





else :
    print(":: NO Random found")



