import base64
import json
from PIL import ImageGrab
from PIL import ImageFilter
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import io
import os

CODESTR = "ocrit"

def myfunc(queryobj):

    currentfolder =  os.path.dirname(os.path.realpath(__file__))

    tesdic = os.listdir(currentfolder + "\\tesseract")

    tesexec = currentfolder + "\\tesseract\\" + tesdic[0] + "\\tesseract.exe"

    print(tesexec)

    pytesseract.pytesseract.tesseract_cmd = tesexec

    postdict = queryobj._POST()
    print("POST = " + str(postdict) + "\n")
       
    img = ImageGrab.grabclipboard()

    if img == None:
        return json.dumps(['Error','No image got from clipboard']).encode('UTF-8')
    #

    img = ImageEnhance.Color(img).enhance(0.0)  # turn black and white

    if postdict['rollangle_in'] != "0": #roll
        img = img.rotate(float(postdict['rollangle_in']))
    else:
        pass
    #

    enlargerate = int(postdict['enlarge_in'])

    img = img.resize((img.size[0]*enlargerate, img.size[1]*enlargerate)) #enlarge

    if float(postdict['brighten_in']) < 0.0 or float(postdict['brighten_in']) == 1.0: #brighten
        pass
    else:
        img = ImageEnhance.Brightness(img).enhance(float(postdict['brighten_in']))
    # 

    #if float(postdict['contrast_in']) < 0.0 or  float(postdict['contrast_in']) == 1.0: #contrast
    #    pass
    #else:
    #    img = ImageEnhance.Contrast(img).enhance(float(postdict['contrast_in']))
    #

    addlang = ''

    if postdict['lang_in'] != '' and postdict['lang_in'].find('+',0,1) == -1: #prevent state of +'' or ++'...'
        addlang = '+' + postdict['lang_in']
    #
    elif postdict['lang_in'] != '':
        addlang = postdict['lang_in']
    #

    addconfigs = ''

    #if postdict['configs_in'] != '':
    #    addconfigs = ' ' + postdict['configs_in']
    #

    addconfigs = '--textord_tablefind_recognize_tables'

    ocr_str = pytesseract.image_to_string(img, lang='eng'+addlang, config=addconfigs) #do OCR #config=addconfigs

   


    #filesdict = queryobj._FILES()
    #print("FILES = " + str(filesdict) + "\n")

    # reply message should be encoded to be sent back to browser ----------------------------------------------
    # encoding to base64 is used to send ansi hebrew data. it is decoded to become string and put into json.
    # json is encoded to be sent to browser.

    imgbuffer = io.BytesIO()
    img.save(imgbuffer,"JPEG")

    file64enc = base64.b64encode(imgbuffer.getvalue())
    file64dec = file64enc.decode()

    replymsg = json.dumps(['success',ocr_str,file64dec]).encode('UTF-8')

    return replymsg
#