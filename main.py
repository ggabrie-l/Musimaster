# This was inserted with Vim :)

import os 
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
import numpy as np

import random
import numpy as np

ep = 0.5

class Arm:
    def __init__(self, song_name, listens):
        self._listens = listens
        self.click_curve = 0
        self.true_mean = np.random.uniform(1, 10)
        self.song_name = song_name

    @property
    def listens(self):
        return self._listens

    @listens.setter
    def listens(self, new_value):
        self._listens += new_value
        self.click_curve = np.random.normal(self.true_mean)
        
    def average(self):
        return self.click_curve / self._listens

class MultiArmedBandit:
    def __init__(self, arms):
        self.arms = arms

    # If a random number between 0 and 1 is less than epsilon, the function chooses a random arm to explore.

    def compute_best(self, ep):
        if np.random.rand() < ep:
            best = np.random.choice(range(3)) # Exploration
  
            return self.arms[best]                       
        else:                                                               # VS 
            max_arm = max(arm.average() for arm in self.arms) # Exploitation
            
            maxes = []
            for index, value in enumerate(self.arms):
                if value.average() == max_arm:
                    maxes.append(index)
            
            if len(maxes) > 1:
                return self.arms[np.random.choice(maxes)]
            else:
                print(maxes)

                print("Best Song is |")
                return self.arms[maxes[0]]

CurSong = None

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
        self.arms = []
        self.MAB = None
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
                arm = Arm(i, data[i]['timeslistened'])
                self.arms.append(arm)

            print("Songs Listened ", self.songsListened)

            #self.songsListened = sorted(self.songsListened)
            self.topten = self.songsListened[:10]

        with open(self.genrespath, 'r+') as file:
            jsonstring = file.read()
            data = json.loads(jsonstring)

            for i in data:
                self.genresListened.append([i, data[i]])

            self.toptengenres = self.genresListened[:10]

        if self.MAB == None:
            self.MAB = MultiArmedBandit(self.arms)
            print("Created MAB")

        print("Listened genres ", self.genresListened)

    def recommend(self):
        # To be made : Order system for songs. Based on multiple genre musics order.
        shuffling = 2

        top_three = []
        top_three_genres = []
        order = None

        Recommended_Song = MAB.compute_best(ep=0.3 * 2)
        return Recommended_Song
                    
class Song():
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.paused = False
        self.time = 0
        self.song = None
        self.setName = "SongThread"
        self.play_thread = None

    def pause(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def playsong(self):
        print("Playing ", self.name)
        self.song = pydub.AudioSegment.from_file(self.path)
        play_thread = threading.Thread(target=play, args=(self.song,))
        play_thread.daemon = True
        
        return play_thread


if __name__ == "__main__":
    files = RetrieveFiles()

    running = True
    
    CurUser = User("Gabriel")
    CurUser.load()

    AudioObj = None
    SongObj = None

    MAB = MultiArmedBandit(CurUser.arms)

    recommended = CurUser.recommend()
    print("RECOMMENDED SONG ", recommended.song_name)

    while running:
        userinput = input("CMD: Pause (pause), Play (song name ), List (list)")
        if userinput == "list":
            for file in files:
                print(file)
        elif userinput == "play":
            usersong = input("song? \n")

            # se der erro você deve ter colocado um nome que nao existe no diretorio.
            AudioObj = CurUser.create_song_obj(usersong, files[usersong])
        
            SongObj = AudioObj.playsong()
            SongObj.start()



