from PIL import ImageGrab
from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageTk
import pytesseract
from tkinter import *
from tkinter import ttk
import webbrowser
import tempfile
import subprocess

root = Tk()

ocr_str = StringVar()
rollangle = DoubleVar()
enlargerate = IntVar()
brightnessrate = DoubleVar()
contrastrate = DoubleVar()
langset = StringVar()
tkimg = ""

rollangle.set(0)
enlargerate.set(2)
brightnessrate.set(1.0)
contrastrate.set(1.0)
langset.set('heb')

frame = ttk.Frame(root, padding=(5,5,5,5))
frame.grid(column=0, row=0, sticky=(N, W, E, S))

textwidget = Text(frame, width=100, height=10)
textwidget.grid(column=1, row=1, rowspan=5, sticky=(W, E))

imglbl = ttk.Label(frame, image=tkimg, width=1)
imglbl.grid(column=1, row=6, sticky=(W, E))


def org_img(event=None):
    
    img = ImageGrab.grabclipboard()

    if img == None:
        return
    #

    img = ImageEnhance.Color(img).enhance(0.0)  # turn black and white

    if rollangle.get() != 0: #roll
        img = img.rotate(rollangle.get())
    else:
        pass
    #

    img = img.resize((img.size[0]*enlargerate.get(), img.size[1]*enlargerate.get())) #enlarge

    if brightnessrate.get() < 0.0 or brightnessrate.get() == 1.0: #brighten
        pass
    else:
        img = ImageEnhance.Brightness(img).enhance(brightnessrate.get())
    # 

    if contrastrate.get() < 0.0 or contrastrate.get() == 1.0: #contrast
        pass
    else:
        img = ImageEnhance.Contrast(img).enhance(contrastrate.get())
    #

    addlang = ''

    if langset.get() != '' and langset.get().find('+',0,1) == -1: #prevent state of +'' or ++'...'
        addlang = '+' + langset.get()
    #
    elif langset.get() != '':
        addlang = langset.get()
    #
    ocr_str.set(pytesseract.image_to_string(img, lang='eng'+addlang)) #do OCR

    textwidget.delete("0.0","end") #remove existing text

    textwidget.insert('end', ocr_str.get()) #insert text into text-widget

    if textwidget.search('[א-ת]',"0.0",regexp = True) != "": #if hebrew, align right
        
        textwidget.tag_add("align","0.0",'end')
        textwidget.tag_config("align",justify = RIGHT)
    #

    if img.size[0] > root.winfo_screenwidth()*2/3: #prevent from picture to get wider than 2/3 of screen width
        presentimg = img.resize((int(root.winfo_screenwidth()*2/3),img.size[1]))
    else:
        presentimg = img
    #
    
    tkimg = ImageTk.PhotoImage(presentimg) #convert PIL img to TK img
    imglbl.configure(image = tkimg)
    imglbl.image = tkimg  #update img in image label "imglbl"
#

def to_clip():
    root.clipboard_clear()
    txt = textwidget.get("0.0","end")
    txt = txt.strip()
    root.clipboard_append(txt)
#

def to_notepad():
    fd = tempfile.TemporaryDirectory()
    fp = open(fd.name + "\\tempfile.txt", "w")
    txt = textwidget.get("0.0","end")
    txt = txt.strip()
    fp.write(txt)
    subprocess.Popen(["notepad", fp.name])
    fp.close
    fd.cleanup
#

def linksite():
    webbrowser.open('https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html')
#

try:
    org_img() #run first time
#
finally:
    ttk.Label(frame, text="Roll angle", padding=(2,2,2,2)).grid(column=2, row=1, sticky=W)
    ttk.Label(frame, text="Enlarge by", padding=(2,2,2,2)).grid(column=2, row=2, sticky=W)
    ttk.Label(frame, text="Brighten by", padding=(2,2,2,2)).grid(column=2, row=3, sticky=W)
    ttk.Label(frame, text="Contrast by", padding=(2,2,2,2)).grid(column=2, row=4, sticky=W)
    ttk.Label(frame, text="OCR langs", padding=(2,2,2,2)).grid(column=2, row=5, sticky=W)

    ttk.Entry(frame, width=3, textvariable=rollangle).grid(column=3, row=1, sticky=(W, E))
    ttk.Entry(frame, width=2, textvariable=enlargerate).grid(column=3, row=2, sticky=(W, E))
    ttk.Entry(frame, width=3, textvariable=brightnessrate).grid(column=3, row=3, sticky=(W, E))
    ttk.Entry(frame, width=3, textvariable=contrastrate).grid(column=3, row=4, sticky=(W, E))
    ttk.Entry(frame, width=8, textvariable=langset).grid(column=3, row=5, sticky=(W, E))

    ttk.Button(frame, text="Retry", command=org_img).grid(column=2, row=6, sticky=(W, E, N))
    ttk.Button(frame, text="Copy", command=to_clip).grid(column=3, row=6, sticky=(W, E, N))
    ttk.Button(frame, text="Notepad", command=to_notepad).grid(column=4, row=6, sticky=(W, E, N))
    ttk.Button(frame, text="OCR langs", command=linksite).grid(column=4, row=5, sticky=(W, E, N))

    root.bind('<Return>',org_img)
    
    root.mainloop()
