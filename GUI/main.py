import os
from tkinter import *
from tkinter import filedialog
latexlassy = Tk()
latexlassy.title('Latex Lassy')
latexlassy.geometry('480x575+700+200')
latexlassy.resizable(False,False)

# Song select stuff
def browseClick():
    file = filedialog.askopenfiles(mode='r', filetypes=[('Laulut', '*.tex')])
    if file:
        for i in file:
            songList.insert(END, os.path.basename(i.name).replace(".tex", ""))

def clearClick():
    songList.insert(END, "Clear Page")

def emptyClick():
    songList.insert(END, "Empty Page")

def upClick():
    print("")

def downClick():
    print("")

def deleteClick():
    songList.delete(songList.curselection())

selectLabel = Label(latexlassy, text="Select songs:").place(x=60,y=10)
browseButton = Button(latexlassy, text="Browse...", command=browseClick).place(x=60,y=35)
songList = Listbox(latexlassy, height=22, width=27, selectmode=SINGLE)
songList.place(x=10,y=70)
clearpageButton = Button(latexlassy, text="Clear Page", command=clearClick).place(x=10,y=500)
emptypageButton = Button(latexlassy, text="Empty Page", command=emptyClick).place(x=103,y=500)
upButton = Button(latexlassy, text="↑", command=upClick).place(x=205,y=225)
downButton = Button(latexlassy, text="↓", command=downClick).place(x=205,y=260)
deleteButton = Button(latexlassy, text="Delete Selection", command=deleteClick).place(x=40,y=535)


# PDF Settings
#pdfLabel = Label(latexlassy, text="PDF Settings").place(x=310,y=10)

# Preview
previewPage = 1
def prevClick():
    global previewPage
    if previewPage > 1:
        previewPage = previewPage - 1
        pageLabel.config(text=f"Current page: {previewPage}")

def nextClick():
    global previewPage
    if previewPage >= 1:
        previewPage = previewPage + 1
        pageLabel.config(text=f"Current page: {previewPage}")

previewLabel = Label(latexlassy, text="PDF Preview").place(x=311,y=10)
prevButton = Button(latexlassy, text="<-", command=prevClick).place(x=310,y=35)
nextButton = Button(latexlassy, text="->", command=nextClick).place(x=350,y=35)
pageLabel = Label(latexlassy, text=f"Current page: {previewPage}")
pageLabel.place(x=311,y=505)

# Starting GUI

latexlassy.mainloop()
