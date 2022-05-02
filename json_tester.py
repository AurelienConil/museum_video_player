import json

MAIN_PATH = "/Users/adminmac/Boulot/JeanGiraudoux/GIT/museum_video_player"
DEFAULT_SETTINGS_PATH = MAIN_PATH+"/settings/defaultSettings.json"

with open(DEFAULT_SETTINGS_PATH, 'r') as userFp:
    userSettingsData = json.load(userFp)

print("Master IP")
print(userSettingsData["metadata"]["master"]["ip"])

print("Master port")
print(userSettingsData["metadata"]["master"]["port"])

print("Raspberry pi name")
print(userSettingsData["metadata"]["identity"]["name"])