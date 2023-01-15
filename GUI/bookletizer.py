import os
import time
from subprocess import Popen

import pylatex


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

    def generateTexFile(self, widget_list):
        with open("projects/song_selector/a4_half.tex", 'r') as f:
            contents = f.readlines()
        
        for i, widget_name in enumerate(widget_list):
            line = ""
            if "Vert space" in widget_name:
                line += "\\vspace{}".format(widget_name.split(':')[1]) + "}\n"
            elif "Page break" == widget_name:
                line += "\\pagebreak"
            else:
                line += "\\input{laulut/" + self.all_songs[widget_name] + "}\n"
            contents.insert(63 + i, line)

        with open("projects/song_selector/a4_half_generated.tex", 'w') as f:
            f.writelines(contents)
        
        #os.environ["TEXMFHOME"] = "library/latex-libraries"
        #doc = pylatex.Document(document_options=["projects/song_selector/a4_half.tex"])
        #doc.generate_pdf("a4_half_2", compiler="bin/texlive/2022/bin/x86_64-linux/pdflatex")
        

        DEVNULL = open(os.devnull, 'wb')
        process = Popen(["./run.sh"])
        process.wait(5)

        return process.returncode
        
    
    def isMatch(self, title_string):
        return title_string in (list(self.finnish_songs.keys()) + list(self.international_songs.keys()))

    def getFinnishSongs(self):
        return self.finnish_songs

    def getInternationalSongs(self):
        return self.international_songs
    
    def getAllSongTitles(self):
        return list(self.finnish_songs.keys()) + list(self.international_songs.keys())