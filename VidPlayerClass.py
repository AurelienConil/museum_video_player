import sys
import os
import platform
from pathlib import Path
isPi = not(platform.machine().startswith("x86"))
if(isPi):
    from omxplayer.player import OMXPlayer

class VidPlayer():
    def __init__(self, s, playlist):
        self.nbScreen = s
        self.WAITING = 0
        self.ASKPLAYINGMAIN = 1
        self.PLAYINGMAIN = 2
        self.ENDMAIN= 3
        self.ASKPLAYINGSECOND = 4
        self.PLAYINGSECOND = 5
        self.ENDSECOND = 6
        self.state = self.WAITING
        self.omxPlayer1 = None
        self.omxPlayer2 = None
        self.listOfMovies = playlist
        if(len(self.listOfMovies)==0 ):
            print("WARNING ! Playlist empty")

    def playMain(self):

        if(self.state != self.WAITING ):
            self.stop()

        if(len(self.listOfMovies)>0):
            self.playVideo(self.listOfMovies[0], False) 
            self.state = self.PLAYINGMAIN
            print("State is now playing")
        else:
            print("ERROR playMain: playlist if empty")

    def playSec(self):
        if(len(self.listOfMovies)>1):
            self.playVideo(self.listOfMovies[1], False) #loop is made mannually with Event function
            self.state = self.PLAYINGSECOND
        else:
            print("ERROR play Secondary movie: playlist if empty")

    def stopAll(self):
        self.stop()
        self.state = self.WAITING

    def stop(self):

        if(not(self.omxPlayer2 is None)):
            try:
                self.omxPlayer2.quit()
                print("omxplayer2 quit")
            except :
                print(" ERROR : quitting omxplayer2")
                print("Unexpected error:", sys.exc_info()[0])

        if(not(self.omxPlayer1 is None)):
            try:
                self.omxPlayer1.quit()
                print("omxplayer 1 : quit")
            except :
                print(" ERROR : quitting omxplayer1")
                print("Unexpected error:", sys.exc_info()[0])

            

        
        self.omxPlayer1 = None
        self.omxPlayer2 = None

    def playVideo(self,path, isLoop):

        fileExist = os.path.exists(path+".mp4")
        print("PLAY VIDEO FILE path :"+path)
        if(fileExist):
            print(" File exist :YES")
        else:
            print(" File exist :NO")


        if(self.nbScreen == 1 and fileExist):
            print("Play video : 1 screen")
            if(not(self.omxPlayer1 is None)):
                self.omxPlayer1.quit()
            
            listOfArgs = ['--no-osd','--no-keys','-b','-o','local'] # local mean audio local, can be replaced with hdmi
            if(isLoop):
                listOfArgs.append('--loop')
            self.omxPlayer1 = OMXPlayer(Path(path+".mp4"),dbus_name='org.mpris.MediaPlayer2.omxplayer1',args=listOfArgs)
            self.omxPlayer1.stopEvent += lambda _, exit_code: self.endOfMovie(exit_code)
            self.omxPlayer1.exitEvent += lambda _, exit_code: self.endOfMovie(exit_code)


        elif(self.nbScreen == 2 and fileExist):
            print("Play video : 2 screens")
            if(not(self.omxPlayer1 is None)):
                self.omxPlayer1.quit()
            if(not(self.omxPlayer2 is None)):
                self.omxPlayer2.quit()
            listOfArgs1 = ['--no-osd','--no-keys','-b', '--display=2', '-o', 'local'] # local mean audio local, can be replaced with hdmi
            listOfArgs2 = ['--no-osd','--no-keys','-b', '--display=7']
            if(isLoop):
                listOfArgs.append('--loop')
            self.omxPlayer1 = OMXPlayer(Path(path+".mp4"), dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=listOfArgs1)
            self.omxPlayer2 = OMXPlayer(Path(path+"2.mp4"), dbus_name='org.mpris.MediaPlayer2.omxplayer2', args=listOfArgs2)
            self.omxPlayer1.stopEvent += lambda _, exit_code: self.endOfMovie(exit_code)
            self.omxPlayer1.exitEvent += lambda _, exit_code: self.endOfMovie(exit_code)
        else:
            print("ERROR : NbScreen is wrong or file does not exist ! Playing aborted")

    def endOfMovie(self, exitCode):
        print("EVENT : This is the end of the movie")
        if(self.state == self.PLAYINGMAIN):
            print("::end of the main movie")
            self.stop()
            self.state = self.ASKPLAYINGSECOND
        if(self.state == self.PLAYINGSECOND):
            print("::end of the secondary movie")
            self.stop()
            self.state = self.ASKPLAYINGSECOND




    def printState(self):
        print("VidPlayer state = "+str(self.state))




            

