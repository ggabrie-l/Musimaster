import os, time
import wave
import pydub
import matplotlib
import io
import threading
import pyaudio
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread
import json
import random
import concurrent.futures
import asyncio
from multiprocessing import Process, Queue
from multiprocessing import Pool

import pydub.playback

CurSong = None

class CustomThread(Thread):
    def __init__(self, group = None, target = None, name = None, args = ..., kwargs = None, *, daemon = None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

        return self._return

def RetrieveFiles():
    curdir = os.getcwd()
    songs = dict()

    for file in os.listdir(curdir):
        if file.endswith(".wav"):
            songs[file] = os.path.join(curdir, file)

    return songs

class User():
    def __init__(self, name):
        self.curdir = os.getcwd()
        self.name = "Gabriel"
        self.most_played = None
        self.topten = []
        self.toptengenres = []
        self.data = None
        self.datajson = None
        self.songsListened = []
        self.genresListened = []
        self.cursong = None
        self.notListened = []

        self.jsonpath = os.path.join(os.getcwd(), "data.json")
        self.genrespath = os.path.join(os.getcwd(), "genres.json")

        with open(self.jsonpath, 'r+') as file:
            data = file.read()
            self.datajson = json.loads(data)
            
        with open(self.genrespath, 'r+') as file:
            data = file.read()
            self.genresjson = json.loads(data)
               
        for song in os.listdir(os.getcwd()):
            if song.endswith('.wav') and song not in self.songsListened and song not in self.notListened:
                self.notListened.append(song)

    def create_song_obj(self, song, songpath):
        with open(self.jsonpath, 'r+') as file:
            jsonstring = file.read()
            data = json.loads(jsonstring)
            
            #data[song] = data.get(data[song], 0) + 1
            if song not in data:
                genre = str(input("What's the genre of this new song?\nGenres " \
                "available []"))
                data[song] = {"timeslistened": 1, "genre": genre}
                file.seek(0) 
                json.dump(data, file, indent=4)
                file.truncate()
                self.songsListened.append(song)
            else:
                data[song]["timeslistened"] += 1
                genre = data[song]["genre"]
                file.seek(0) 
                json.dump(data, file, indent=4)
                file.truncate()
                with open(self.genrespath, 'r+') as file:
                    jsonstring = file.read()
                    data = json.loads(jsonstring)

                    data[genre] += 1
                    file.seek(0) 
                    json.dump(data, file, indent=4)
                    file.truncate()

        CurSong  = Song(songpath, song)

        return CurSong
        
    def load(self):
        with open(self.jsonpath, 'r') as file:
            jsonstring = file.read()
            data = json.loads(jsonstring)

            for i in data:
                self.songsListened.append([i, data[i]])
            print("Songs Listened ", self.songsListened)

            #self.songsListened = sorted(self.songsListened)
            self.topten = self.songsListened[:10]

        with open(self.genrespath, 'r+') as file:
            jsonstring = file.read()
            data = json.loads(jsonstring)

            for i in data:
                self.genresListened.append([i, data[i]])

            self.toptengenres = self.genresListened[:10]

        print("Listened genres ", self.genresListened)

    def recommend(self):
        # To be made : Order system for songs. Based on multiple genre musics order.

        top_three = []
        top_three_genres = []
        order = None

        Recommened_Song = None





class Song():
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.paused = False
        self.time = 0
        self.setName = "SongThread"
        self.play_thread = None
        self.song = pydub.AudioSegment.from_file(self.path)
        self.result = None
        self.outputplayback = []
        self.activate_song = None
        self.queue = Queue()

    def extractdata(self):
        # To be made. Used to extract the ID3 data from mp3 files.
        pass

    def pause(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def playsong(self):
        thread_play = threading.Thread(target=play, args=(self.song,))
        thread_play.daemon = True
        thread_play.start()
        #thread_play.join()
        #self.queue.get()

        time.sleep(1.5)

        active =  pydub.playback.return_active()
        return active

def main():
    files = RetrieveFiles()

    running = True
    
    CurUser = User("Gabriel")
    CurUser.load()

    while running:
        userinput = input("CMD: Pause (pause), Play (song name ), List (list)")
        if userinput == "list":
            for file in files:
                print(file)
        elif userinput == "play":
            usersong = input("song? \n")
            # se der erro você deve ter colocado um nome que nao existe no diretorio.
            AudioObj = CurUser.create_song_obj(usersong, files[usersong])
            activate_song = AudioObj.playsong()    

        elif userinput == "current":
            print(activate_song)

if __name__ == "__main__":
    main()