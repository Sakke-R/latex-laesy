import os
import struct

from subprocess import Popen
from io import StringIO
from PIL import Image



class Bookletizer:
    def __init__(self):
        self.song_path = os.getcwd() + '/laulut'
        self.img_path = os.getcwd() + '/kuvat'
        self.initializeLibrary()

    def formSongDictionary(self, file_list):
        # For all available titles extract the song title from the
        # filename and link them in a dictionary
        if not file_list:
            return {}
        title_to_file = dict({(' '.join((map(lambda word: word.capitalize(), file_name.split('.')[0].split('-')))), file_name)
            for file_name in file_list})
        return title_to_file

    def initializeLibrary(self):
        fin_songs = (os.listdir(self.song_path))
        fin_songs.remove("international")
        int_songs = os.listdir(self.song_path + "/international/")
        self.finnish_songs = self.formSongDictionary(fin_songs)
        self.international_songs = self.formSongDictionary(int_songs)
        self.all_songs = self.formSongDictionary(fin_songs + int_songs)

        self.images = (os.listdir(self.img_path))

        #self.images = dict({file_name, Image.open(self.img_path+'/'+file_name).size} for file_name in images)
        print("Initialization done. Self.images: ")
        print(self.images)

    def generateTexFile(self, widget_list):
        with open("projects/song_selector/a4_half.tex", 'r') as f:
            contents = f.readlines()
        
        for i, widget in enumerate(widget_list):
            line = ""
            centering = widget.getCentering()
            if centering:
                line += "\\begin{center}"

            if widget.getType() == "vspace":
                line += f"\\vspace{{ {widget.getSize()}cm}}\n"
            elif widget.getType() == "pagebreak":
                line += "\\vfill\n"
                line += "\\pagebreak\n"
            elif widget.getType() == "image":
                if widget.getOffset() != 0:
                    line += "\n\\hspace{" + str(widget.getOffset()) + "cm}\n"
                line += "\\includegraphics[width=" + str(widget.getScale()) + "\\textwidth]{kuvat/" + widget.getTitle() + "}\n\n"
            else:
                line += "\\input{laulut/" + self.all_songs[widget.getTitle()] + "}\n"

            if centering:
                line += "\\end{center}"
            
            contents.insert(63 + i, line) # UGLY HARDCODING. Get rid of this if possible

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
        return title_string in self.getAllTitles()

    def getFinnishSongs(self):
        return self.finnish_songs

    def getInternationalSongs(self):
        return self.international_songs
    
    def getAllSongTitles(self):
        return list(self.finnish_songs.keys()) + list(self.international_songs.keys())

    def getAllImageTitles(self):
        return self.images
    
    def getAllTitles(self):
        return self.getAllSongTitles() + self.getAllImageTitles()



""" Efficient helper fn. Courtesy https://stackoverflow.com/questions/1507084/how-to-check-dimensions-of-all-images-in-a-directory-using-python"""
def getImageInfo(data):
    data = str(data)
    size = len(data)
    height = -1
    width = -1
    content_type = ''

    # handle GIFs
    if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
        # Check to see if content_type is correct
        content_type = 'image/gif'
        w, h = struct.unpack("<HH", data[6:10])
        width = int(w)
        height = int(h)

    # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
          and (data[12:16] == 'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and data.startswith('\377\330'):
        content_type = 'image/jpeg'
        jpeg = StringIO.StringIO(data)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = jpeg.read(1)
                while (ord(b) == 0xFF): b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass

    return width, height