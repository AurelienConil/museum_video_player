
from omxplayer.player import OMXPlayer
from time import sleep
from pathlib import Path
import sys

listOfArgs = ['--no-osd','--no-keys','-b','-o','hdmi'] # local mean audio local, can be replaced with hdmi
  
print("Starting /media/fat32/main.mp4")
VIDEO_PATH = Path("/media/fat32/main.mp4")

player = OMXPlayer(VIDEO_PATH,dbus_name='org.mpris.MediaPlayer2.omxplayer1',args=listOfArgs)

sleep(5)
print("Quit right now")
player.quit()

print("Starting /media/fat32/wait.mp4")
         
            
VIDEO_PATH = Path("/media/fat32/wait.mp4")

player = OMXPlayer(VIDEO_PATH,dbus_name='org.mpris.MediaPlayer2.omxplayer1',args=listOfArgs)

sleep(5)
print("Quit right now")
player.quit()

sys.exit(0)
