import os
from subprocess import Popen

class Bookletizer:
    def __init__(self):
        self.path = os.getcwd() + '/laulut'
        self.initializeLibrary()

    def formDictionary(self, file_list):
        # For all available titles extract the song title from the
        # filename and link them in a dictionary
        if not file_list:
            return {}
        title_to_file = dict({(' '.join((map(lambda word: word.capitalize(), file_name.split('.')[0].split('-')))), file_name)
            for file_name in file_list})
        return title_to_file

    def initializeLibrary(self):
        fin_songs = (os.listdir(self.path))
        fin_songs.remove("international")
        int_songs = os.listdir(self.path + "/international/")
        self.finnish_songs = self.formDictionary(fin_songs)
        self.international_songs = self.formDictionary(int_songs)
        self.all_songs = self.formDictionary(fin_songs + int_songs)

    def generateTexFile(self, song_list):
        file = open("projects/song_selector/songs.tex", 'w')
        for song in song_list:
            tex_file = self.all_songs[song]
            line = "\\input{laulut/" + tex_file + "}\n"
            file.write(line)
        
        DEVNULL = open(os.devnull, 'wb')
        process = Popen(["./run.sh", ""], stdout=DEVNULL, stderr=DEVNULL)
        
    
    def isMatch(self, title_string):
        return title_string in (list(self.finnish_songs.keys()) + list(self.international_songs.keys()))

    def getFinnishSongs(self):
        return self.finnish_songs

    def getInternationalSongs(self):
        return self.international_songs
    
    def getAllSongTitles(self):
        return list(self.finnish_songs.keys()) + list(self.international_songs.keys())