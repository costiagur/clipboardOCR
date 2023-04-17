
from PIL import ImageGrab
from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import os
from tempfile import NamedTemporaryFile
import subprocess

def myfunc():

    currentfolder =  os.path.dirname(os.path.realpath(__file__))

    tesdic = os.listdir(currentfolder + "\\tesseract")

    tesexec = currentfolder + "\\tesseract\\" + tesdic[0] + "\\tesseract.exe"

    pytesseract.pytesseract.tesseract_cmd = tesexec

    #os.environ['TESSDATA_PREFIX'] = currentfolder + "\\tesseract\\" + tesdic[0] + "\\tessdata"
    tessdata = currentfolder + "\\tesseract\\" + tesdic[0] + "\\tessdata"

    img = ImageGrab.grabclipboard()

    if img == None:
        print("No image supplied")
    #

    img = ImageEnhance.Color(img).enhance(0.0)  # turn black and white

    #if postdict['rollangle_in'] != "0": #roll
    #    img = img.rotate(float(postdict['rollangle_in']))
    #else:
    #    pass
    #

    #enlargerate = int(postdict['enlarge_in'])

    #img = img.resize((img.size[0]*enlargerate, img.size[1]*enlargerate)) #enlarge

    #if float(postdict['brighten_in']) < 0.0 or float(postdict['brighten_in']) == 1.0: #brighten
    #    pass
    #else:
    #    img = ImageEnhance.Brightness(img).enhance(float(postdict['brighten_in']))
    # 

    #if float(postdict['contrast_in']) < 0.0 or  float(postdict['contrast_in']) == 1.0: #contrast
    #    pass
    #else:
    #    img = ImageEnhance.Contrast(img).enhance(float(postdict['contrast_in']))
    #

    addlang = ''

    #if postdict['lang_in'] != '' and postdict['lang_in'].find('+',0,1) == -1: #prevent state of +'' or ++'...'
    #    addlang = '+' + postdict['lang_in']
    #
    #elif postdict['lang_in'] != '':
    #    addlang = postdict['lang_in']
    #

    #addconfigs = ''

    #if postdict['configs_in'] != '':
    #    addconfigs = ' ' + postdict['configs_in']
    #

    addconfigs = '--psm 11 pdf' + ' --tessdata-dir"' + tessdata + '"' 

    ocr_str = pytesseract.image_to_string(img, lang='eng+heb', config=addconfigs) #do OCR #config=addconfigs
      
    with NamedTemporaryFile("w",delete=False) as txtfile:
        txtfile.write(ocr_str)
        txtfile.seek(0)
        print(txtfile.name)
    #

    subprocess.call("Notepad " + txtfile.name)

    os.unlink(txtfile.name)

    return ocr_str
#

myfunc()