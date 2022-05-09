import json
import os

MAIN_PATH = "/home/pi/Documents/museum_video_player"
VIDEOFILE_PATH = "/home/pi/Videos" # Long term in fat32 partition
USER_SETTINGS_PATH = VIDEOFILE_PATH+"/settings/userSettings.json" # better close to the video file : fat32 editing
DEFAULT_SETTINGS_PATH = MAIN_PATH+"/settings/defaultSettings.json"

settingsFilePath = DEFAULT_SETTINGS_PATH
if(os.path.exists(USER_SETTINGS_PATH)):
    settingsFilePath = USER_SETTINGS_PATH
    print("SETTINGS : user setting")
else:
    print("SETTING : default ")

with open(settingsFilePath, 'r') as userFp:
    userSettingsData = json.load(userFp)

print("Master IP")
print(userSettingsData["master"]["ip"])

print("Master port")
print(userSettingsData["master"]["port"])

print("Raspberry pi name")
print(userSettingsData["identity"]["name"])

print("Raspberry pi video screen number")
print(userSettingsData["video"]["screenNumber"])

print("Main media file name")
print(userSettingsData["playlist"]["mainMediaPath"]+".mp4")

print("Secondary media file name")
print(userSettingsData["playlist"]["waitingMediaPath"]+".mp4")