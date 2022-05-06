import json

MAIN_PATH = "/home/pi/Documents/museum_video_player"
VIDEOFILE_PATH = "/home/pi/Videos" # Long term in fat32 partition
USER_SETTINGS_PATH = VIDEOFILE_PATH+"/settings/UserSettings.json" # better close to the video file : fat32 editing
DEFAULT_SETTINGS_PATH = MAIN_PATH+"/settings/defaultSettings.json"

with open(DEFAULT_SETTINGS_PATH, 'r') as userFp:
    userSettingsData = json.load(userFp)

print("Master IP")
print(userSettingsData["metadata"]["master"]["ip"])

print("Master port")
print(userSettingsData["metadata"]["master"]["port"])

print("Raspberry pi name")
print(userSettingsData["metadata"]["identity"]["name"])

print("Raspberry pi video screen number")
print(userSettingsData["video"]["screenNumber"])