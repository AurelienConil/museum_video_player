# SOFTWARE museum_video_player 

# OS - login
works on Buster 32 bits
console on boot, logged on PI
user = pi
password = raspberry

# Dependencies
```
pip install pathlib
pip install PyOSC
sudo apt-get install libdbus-1-dev libdbus-glib-1-dev -y
sudo pip install omxplayer-wrapper
```

# How to clean the console screen
change  cmdLine.txt and create a backup

`logo.nologo vt.global_cursor_default=0` : **remove cursor**

## Remove login blabla

`touch ~/.hushlogin` 

`sudo nano /etc/systemd/system/getty@tty1.service.d/autologin.conf`

change
```
ExecStart=-/sbin/agetty --autologin pi --noclear %I xterm-256color
```

with:

```
ExecStart=-/sbin/agetty --skip-login --noclear --noissue --login-options "-f pi" %I $TERM
```

## Remove secutiry  ssh msg 

Remove the file `/etc/profile.d/sshpasswd.sh`
 (`sshpwd.sh`
 for stretch)


## Remove bash prompt ( now this not removed, this is a '$') 

If you want to remove even the bash prompt (e.g. “pi@raspberrypi:~ $”), open .bashrc file.

```
nano ~/.bashrc
```

Then add the line below at the bottom of the file.

```
PS1=""
```



# OSC message

Note that port In and Out are part of user settings

## Video
`/video/status/ 0`  Print status player on console and callback in osc too
* WAITING = 0
* ASKPLAYING MAIN VIDEO = 1
* PLAYING MAIN VIDEO = 2
* END MAIN VIDEO = 3
* ASK PLAYING SECOND = 4
* PLAYING SECOND VIDEO = 5
* END SECOND 2D SCREEN = 6 ( 2nd screen is over, but the the 1st screen)

note that PAUSE is not a status

`/video/playmain` Play the main video

`/video/playwait` Play the secondary video. Works only if state is WAITING or PLAYING MAIN VIDEO

`/video/stop` Stop everything, go to waiting mode

## RPI
`/rpi/startx` start X desktop in background

`/rpi/reboot`

`/rpi/shutdown`

## APP
`/app/ispi` write on console is machine is considered as raspberry pi arm

`/app/quit`quit app

`/app/test` write test on console and give back OSC test message



-----------
# IMAGE museum_video_player

# Disk Location
program is : /home/Document/museum_video_player/main2.py

fat32 is /media/fat32/

userSettings file has to be : /media/fat32/settings/userSettings.json

# Start automatically vs manually
## stop app
 `sudo systemctl stop museum.service`
## deactivate autostart
 `sudo systemctl disable museum.service`
## activate autostart
  `sudo systemctl enable museum.service`
  `sudo reboot`
## Quitting app
use OSC command /app/quit 
## Start mannually the app
`cd /home/pi/Documents/museum_video_player`

`python main2.py`


# Test programm
 ## Test if json is correct
 `python json_tester.py`

 ## Omxplayer test main.mp4 & wait.mp4 files
 `python omxplayer_tester.py`  note : sound is not configurated


 

# Start NDI
first start desktop, using keyboard `startx`  or   `/rpi/startx` OSC message
open a browser, then open _ip_of_raspberry_

 
# Random Mode
Random mode allows you to play randomly a couple of main.mp4 / wait.mp4
What is needed ?
1. Activate random by adding new line on Json file : 
"random": {
        "nbFolder": X (where X is a number)
    }
2. Add X couples of main.mp4/wait.mp4 located in folder "1" , "2", "3" .... "X"
3. Check that everything is fine, user `python json_tester.py`
4. Double check on log when app is starting :
```
===== init settings ====
SETTINGS : user setting
==== playlist =====
/media/fat32/main.mp4
/media/fat32/wait.mp4
VideoPlayer RANDOM Mode activated
Set Random Folder
New Random Folder =3
 ===== OSC SERVER ====
 ```

 deactivate Random mode in removing the random key inside the json folder



