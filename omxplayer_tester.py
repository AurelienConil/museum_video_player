
from omxplayer.player import OMXPlayer
from time import sleep
from pathlib import Path

VIDEO_PATH = Path("/home/pi/Videos/test.mp4")

player = OMXPlayer(VIDEO_PATH)

sleep(5)
print("Quit right now")
player.quit()
