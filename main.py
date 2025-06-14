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

    def create_song_obj(self, song, songpath, flag):
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

        CurSong  = Song(songpath, song, flag)
        print(f"New song playing : {CurSong.name}")
        CurSong.playsong(flag)

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
        shuffling = True

        top_three = []
        top_three_genres = []
        order = None

        Recommened_Song = None

        # To be made : Order system for songs. Based on multiple genre musics order.

        if not shuffling:
            for i in self.topten[:3]:
                top_three.append(i[1]["genre"])

            randomgenre = random.Random().randint(a=0, b=2)
            for music in self.notListened:
                pass

        if shuffling:
            randomgenre = random.Random().randint(a=0, b=2)
            for music in self.songsListened:
                if randomgenre == music[1]["genre"]:
                    return music
                    




class Song():
    def __init__(self, path, name, flag):
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

    def playsong(self, flag):
        print("Playing ", self.name)
        self.song = pydub.AudioSegment.from_file(self.path)
        play_thread = threading.Thread(target=play, args=(self.song, lambda: running,))
        play_thread.daemon = True
        
        return play_thread


if __name__ == "__main__":
    files = RetrieveFiles()

    running = True
    
    CurUser = User("Gabriel")
    CurSong = None

    CurUser.load()

    SongObj2 = None

    playing = False 
    paused = False




    while running:
        userinput = input("CMD: Pause (pause), Play (song name ), List (list)")
        if userinput == "list":
            for file in files:
                print(file)
        elif userinput == "play":
            usersong = input("song? ")
            if usersong in files.keys():
                if playing == True:
                    del(SongObj2)

                SongObj = CurUser.create_song_obj(usersong, files[usersong], playing)
            
                
                SongObj2 = SongObj.playsong(flag=playing)

                SongObj2.start()
                playing = True


