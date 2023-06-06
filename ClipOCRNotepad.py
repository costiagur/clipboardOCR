
from PIL import ImageGrab
from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import os
from tempfile import NamedTemporaryFile
import subprocess
import argparse
import tkinter
from tkinter import messagebox 
from tkinter import simpledialog

def myfunc(roll=0.0, bright=1.0):

    root = tkinter.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    
    root.deiconify()
    asklang = simpledialog.askstring(title="ClipOCRtoNotepad",prompt='Input language',initialvalue="heb")
    root.withdraw()
    
    currentfolder =  os.path.dirname(os.path.realpath(__file__))

    tesdic = os.listdir(currentfolder + "\\tesseract")

    tesexec = currentfolder + "\\tesseract\\" + tesdic[0] + "\\tesseract.exe"

    pytesseract.pytesseract.tesseract_cmd = tesexec

    #os.environ['TESSDATA_PREFIX'] = currentfolder + "\\tesseract\\" + tesdic[0] + "\\tessdata"
    
    tessdata = currentfolder + "\\tesseract\\" + tesdic[0] + "\\tessdata"

    img = ImageGrab.grabclipboard()

    if img == None:
        print("No image supplied")
        root.deiconify()
        messagebox.showerror(title="ClipOCRtoNotepad", message="No image supplied")
        root.withdraw()
        root.destroy()
    
    else:
        img = ImageEnhance.Color(img).enhance(0.0)  # turn black and white
        
        if float(roll) != 0.0: #roll angle
            img = img.rotate(float(roll))
        else:
            pass
        #

        if float(bright) < 0.0 or float(bright) == 1.0: #brighten
           pass
        else:
            img = ImageEnhance.Brightness(img).enhance(float(bright))
        # 
        
        addconfigs = ' --tessdata-dir "' + tessdata + '"' #'--psm 11 pdf' + 

        try:
            ocr_str = pytesseract.image_to_string(img, lang=asklang, config=addconfigs) #do OCR #config=addconfigs
      
            with NamedTemporaryFile("w",delete=False) as txtfile:
                txtfile.write(ocr_str)
                txtfile.seek(0)
                print(txtfile.name)
            #

            subprocess.call("Notepad " + txtfile.name)

            os.unlink(txtfile.name)
        #
        except Exception as e:
            root.deiconify()
            messagebox.showerror(title="ClipOCRtoNotepad", message=e)
            root.withdraw()
        #

        else:
            return ocr_str
        
        finally:
            root.destroy()

    #
#   

parser = argparse.ArgumentParser()
parser.add_argument("--roll", help="optional roll angle. float.", type=float)
parser.add_argument("--bright", help="optional brighten rate higher than 1.0. float.", type=float)

args = parser.parse_args()

myfunc(args.roll if args.roll else 0.0, args.bright if args.bright else 1.0)