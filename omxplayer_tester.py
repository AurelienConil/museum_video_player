
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

VIDEO_PATH = Path("/home/pi/Video/test.mp4")

player = OMXPlayer(VIDEO_PATH)

sleep(5)

player.quit()