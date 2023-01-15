import os
from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
from pdf2image import convert_from_path
latexlassy = Tk()
latexlassy.title('Latex Laesy')
latexlassy.geometry('553x575+700+200')
latexlassy.resizable(False,False)

#############################################################################################
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
    sel = songList.curselection()
    if not sel:
        return
    if sel[0] == 0:
        return
    seltext = songList.get(sel[0])
    songList.delete(sel[0])
    songList.insert(sel[0]-1, seltext)
    songList.select_set(sel[0]-1)

def downClick():
    sel = songList.curselection()
    if not sel:
        return
    if sel[0] == len(songList.get(0,END))-1:
        return
    seltext = songList.get(sel[0])
    songList.delete(sel[0])
    songList.insert(sel[0]+1, seltext)
    songList.select_set(sel[0]+1)

def deleteClick():
    sel = songList.curselection()
    if not sel:
        return
    songList.delete(songList.curselection())
    if sel[0] == 0:
        songList.select_set(0)
    if sel[0] == len(songList.get(0,END)):
        songList.select_set(sel[0] - 1)
    else: songList.select_set(sel[0] - 1)


selectLabel = Label(latexlassy, text="Select songs:").place(x=60,y=10)
browseButton = Button(latexlassy, text="Browse...", command=browseClick).place(x=60,y=35)
songList = Listbox(latexlassy, height=22, width=27, selectmode=SINGLE)
songList.place(x=10,y=70)
clearpageButton = Button(latexlassy, text="Clear Page", command=clearClick).place(x=10,y=500)
emptypageButton = Button(latexlassy, text="Empty Page", command=emptyClick).place(x=103,y=500)
upButton = Button(latexlassy, text="↑", command=upClick).place(x=205,y=225)
downButton = Button(latexlassy, text="↓", command=downClick).place(x=205,y=260)
deleteButton = Button(latexlassy, text="Delete Selection", command=deleteClick).place(x=40,y=535)

#############################################################################################
# PDF Settings
#pdfLabel = Label(latexlassy, text="PDF Settings").place(x=310,y=10)

#############################################################################################
# Preview
previewPage = 1
def prevClick():
    global previewPage
    global new_image
    try:
        img_new = (Image.open(f"./preview_imgs/{previewPage - 1}.jpg"))
        resized_image = img_new.resize((300,424))
        new_image = ImageTk.PhotoImage(resized_image)
        canvas.itemconfig(canvas_image,image=new_image)
        previewPage = previewPage - 1
        pageLabel.config(text=f"Current page: {previewPage}")
    except FileNotFoundError:
        return

def nextClick():
    global previewPage
    global new_image
    try:
        img_new = (Image.open(f"./preview_imgs/{previewPage + 1}.jpg"))
        resized_image = img_new.resize((300,424))
        new_image = ImageTk.PhotoImage(resized_image)
        canvas.itemconfig(canvas_image,image=new_image)
        previewPage = previewPage + 1
        pageLabel.config(text=f"Current page: {previewPage}")
    except FileNotFoundError:
        return

def generateClick():
    global previewPage
    global new_image
    previewPage = 1
    pageLabel.config(text=f"Current page: {previewPage}")
    pages = convert_from_path('a4_placement.pdf', 500)
    pagenum = 1
    for page in pages:
        page.save(f'./preview_imgs/{pagenum}.jpg', 'JPEG')
        pagenum = pagenum + 1
    img_new = (Image.open("./preview_imgs/1.jpg"))
    resized_image = img_new.resize((300,424))
    new_image = ImageTk.PhotoImage(resized_image)
    canvas.itemconfig(canvas_image,image=new_image)
    
canvas = Canvas(latexlassy, width=300, height=424)
canvas.place(x=240,y=60)
img = (Image.open("placeholder.png"))
resized_image = img.resize((300,424))
placeholder_image = ImageTk.PhotoImage(resized_image)
canvas_image = canvas.create_image(10,10, anchor=NW, image=placeholder_image)

previewLabel = Label(latexlassy, text="PDF Preview").place(x=360,y=10)
prevButton = Button(latexlassy, text="←", command=prevClick).place(x=359,y=35)
nextButton = Button(latexlassy, text="→", command=nextClick).place(x=399,y=35)
pageLabel = Label(latexlassy, text=f"Current page: {previewPage}")
pageLabel.place(x=360,y=505)
generateButton = Button(latexlassy, text="Generate preview", command=generateClick).place(x=335,y=530)


#############################################################################################
# Starting GUI
latexlassy.mainloop()
