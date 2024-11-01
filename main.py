import os
import time
try:
    from PIL import Image, ImageEnhance, ImageFilter
    import pyautogui
    import keyboard
    import pytesseract
except:
    import sys
    pyPath = sys.executable
    print("Libraries not installed. Unable to continue...")
    print(f"Please run '{pyPath} -m pip install pillow pyautogui keyboard pytesseract'")
    if input("Try to install? (Y/n)\n:").lower() != "n":
        os.system(f"{pyPath} -m pip install pillow pyautogui keyboard pytesseract")
        from PIL import Image, ImageEnhance, ImageFilter
        import pyautogui
        import keyboard
        import pytesseract
    else:
        input("Press enter to exit...")
        exit(1)
try:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #Change this to your tesseract install location
    print("Tesseract version: " + str(pytesseract.get_tesseract_version()).split("\n")[0])
except:
    print("Tesseract OCR not installed or path is wrong (default: C:Program Files/Tesseract-OCR/tesseract.exe).\nUnable to continue...")
    print("Please download Tesseract from:\n'https://github.com/tesseract-ocr/tessdoc/blob/main/Installation.md'\nand set path correctly in line 23.")
    input("Press enter to exit...")
    exit(1)

version = "3"

print(f"Application version: {version}\n")

#USELESS ////
numbersLocation = [0,0,0,0]
numbersLocationd = [0,0,0,0]
playLocations = [(0,0),(0,0),(0,0)]
waitTriggerLocation = [0,0]
waitTriggerColor = [0,0,0] # R G B 0-255
#//// 

waitCheckFrequency = 1 #seconds wait
waitCheckColorTolerance = 1

locationsFile = "data/locations.txt"

onBind = "o"
offBind = "p"

global debug
debug = True

if debug:
    logging = True
    removePics = False
else:
    logging = False
    removePics = True

logFile = "data/bjLogs.txt"
tempImagePathBase = f"data/pics/temp"
dealerTempBase = f"data/pics/dealerTemp"

def loadLocationsFile(filename):
    if os.path.exists(filename):
        with open(filename,"r") as f:
            lines = f.readlines()
        numbersLocationSTR = lines[0].replace("[","").replace("]","").replace("\n","").replace(" ","").split(",")
        numbersLocation = []
        for x in numbersLocationSTR:
            numbersLocation.append(int(x))

        numbersLocationSTRd = lines[1].replace("[","").replace("]","").replace("\n","").replace(" ","").split(",")
        numbersLocationd = []
        for x in numbersLocationSTRd:
            numbersLocationd.append(int(x))
        
        pl = lines[2].replace("(","").replace("[","").replace("]","").replace("\n","").replace(" ","")[:-1]
        plSplit = pl.split(")")
        hitString = plSplit[0].split(",")
        hit = []
        for x in hitString:
            hit.append(int(x))
        standString = plSplit[1][1:].split(",")
        stand = []
        for x in standString:
            stand.append(int(x))
        doubleString = plSplit[2][1:].split(",")
        double = []
        for x in doubleString:
            double.append(int(x))

        waitTriggerLocationSTR = tuple(lines[3].replace("(","").replace(")","").replace("\n","").replace(" ","").split(","))
        waitTriggerLocation = []
        for x in waitTriggerLocationSTR:
            waitTriggerLocation.append(int(x))

        waitTriggerColorSTR = tuple(lines[4].replace("(","").replace(")","").replace("\n","").replace(" ","").split(","))
        waitTriggerColor = []
        for x in waitTriggerColorSTR:
            waitTriggerColor.append(int(x))

        betSTR = tuple(lines[5].replace("(","").replace(")","").replace("\n","").replace(" ","").split(","))
        bet = []
        for x in betSTR:
            bet.append(int(x))

        version = lines[6]

        return numbersLocation,numbersLocationd,[hit,stand,double],waitTriggerLocation,waitTriggerColor,bet,version
    else:
        raise FileNotFoundError
    
def writeLocationsFile(filename,numbersLocation,numbersLocationd,playLocations,waitTriggerLocation,waitTriggerColor,bet,version):
    with open(filename,"w") as f:
        f.write(str(f"{numbersLocation}\n{numbersLocationd}\n{playLocations}\n{waitTriggerLocation}\n{waitTriggerColor}\n{bet}\n{version}"))

def getLocationOnKeypress(key):
    keyboard.wait(key)
    return pyautogui.position()

def log(data,path,logging,terminal):
    if terminal:
        print(data)
    if logging:
        with open(path,"a") as f:
            f.write(data + "\n")

def filterNumbers(inStrRaw):
    if debug:
        print(inStrRaw)
    numbers = ["1","2","3","4","5","6","7","8","9","0"]

    if "/" in inStrRaw:
        ace = True
    else:
        ace = False

    inStrRaw = str(inStrRaw).split("/")

    outList = []
    for inStr in inStrRaw:
        out = ""
        for x in inStr:
            if x in numbers:
                out = out + x

        if len(out) != 0:
            outList.append(int(out))
    
    if len(outList) == 0:
        outList.append(0)

    if debug:
        print(str(outList) + "|" + str(ace))
    
    return outList, ace

def bjDecider(total,dealerHand,handAce,dealerAce,lastPlay):
    #return 0 hit | 1 stand | 2 double
    if dealerAce:
        dealerHandPlay = 1
    else:
        dealerHandPlay = dealerHand[0]
    if handAce:
        if total[0] > 11 and total[0] < 20:
            totalPlay = total[1]
        else:
            totalPlay = total[0]
    else:
        totalPlay = total[0]
    playStyle = ""
    if dealerHandPlay > 6:
        #Agressive playstyle
        playStyle = "Agressive"
        if totalPlay > 100:
            return 0,playStyle
        elif totalPlay > 16:
            return 1,playStyle
        elif totalPlay == 10 and lastPlay != 0:
            return 2,playStyle
        elif totalPlay == 11 and lastPlay != 0:
            return 2,playStyle
        elif totalPlay == 0:
            return 3,playStyle
        elif totalPlay < 17:
            return 0,playStyle
        else:
            return 3,playStyle
    else:
        #Anti bust playstyle
        playStyle = "Anti bust"
        if totalPlay > 100:
            return 0,playStyle
        elif totalPlay > 11:
            return 1,playStyle
        elif totalPlay == 10 and lastPlay != 0:
            return 2,playStyle
        elif totalPlay == 11 and lastPlay != 0:
            return 2,playStyle
        elif totalPlay == 0:
            return 3,playStyle
        elif totalPlay < 12:
            return 0,playStyle
        else:
            return 3,playStyle


def waitNewRound(location, color, frequency, tolerance,logFile,logging):
    timePassed = 0
    while True:
        if pyautogui.pixelMatchesColor(location[0],location[1],color,tolerance):
            break
        time.sleep(frequency)
        timePassed += frequency
        if timePassed > 3:
            if debug:
                print("STUCK...")
            return 1
    time.sleep(2.5)

#Change name to formatImage and all calls
def formatImage2(path):
    imgRaw = Image.open(path).convert("RGBA")

    scale_factor = 8
    new_size = (imgRaw.width * scale_factor, imgRaw.height * scale_factor)
    imgRaw = imgRaw.resize(new_size, Image.LANCZOS)
    """
    pixels = imgRaw.load()

    imgMode = imgRaw.mode
    imgSize = imgRaw.size

    tolerance = 15
    
    pixelWhiteness = 255 - tolerance

    if debug:
        whitened = 0
        blackened = 0

    img = Image.new(mode=imgMode,size=imgSize)

    for y in range(imgSize[1]):
        for x in range(imgSize[0]):
            pixel = pixels[x, y]
            if pixel[2] > pixelWhiteness and pixel[1] > pixelWhiteness and pixel[0] > pixelWhiteness:
                img.putpixel([x,y],(0,0,0,255))
                if debug:
                    whitened += 1
            else:
                img.putpixel([x,y],(255,255,255,255))
                if debug:
                    blackened += 1
    if debug:
        print(f"Pixels whitened: {str(whitened)}")
        print(f"Pixels blackened:{str(blackened)}")
    
    #img = ImageEnhance.Contrast(img).enhance(3)  
    #img = img.filter(ImageFilter.GaussianBlur(1))  
    #img = img.filter(ImageFilter.SHARPEN)

    #print(list(imgRaw.getdata()))
    """
    imgRaw.save(path, dpi=(300, 300)) 

def getLocations():
    #left, top, width, and height

    print("Hover over bet and press k")
    bet = getLocationOnKeypress("k")
    print("Hover over top left corner of number area and press k")
    lta = getLocationOnKeypress("k")
    left = lta[0]
    top = lta[1]
    print("Hover over bottom right corner of number area and press k")
    rba = getLocationOnKeypress("k")
    width = rba[0]-lta[0]
    height = rba[1]-lta[1]
    numbersLocation = [left,top,width,height]

    print("Hover over top left corner of dealer number area and press k")
    ltad = getLocationOnKeypress("k")
    leftd = ltad[0]
    topd = ltad[1]
    print("Hover over bottom right corner of dealer number area and press k")
    rbad = getLocationOnKeypress("k")
    widthd = rbad[0]-ltad[0]
    heightd = rbad[1]-ltad[1]
    numbersLocationd = [leftd,topd,widthd,heightd]

    print("Hover over a wait trigger location (Checks color when round is started) and press k")
    trigger = getLocationOnKeypress("k")
    triggerColor = pyautogui.pixel(trigger[0],trigger[1])

    print("Hover over hit and press k")
    hit = getLocationOnKeypress("k")
    print("Hover over stand and press k")
    stand = getLocationOnKeypress("k")
    print("Hover over double and press k")
    double = getLocationOnKeypress("k")

    return numbersLocation,numbersLocationd,[tuple(hit),tuple(stand),tuple(double)],tuple(trigger),tuple(triggerColor),tuple(bet)

if os.path.exists("data") == False:
    os.mkdir("data")
if os.path.exists("data/pics") == False:
    os.mkdir("data/pics")

if debug:
    print("Debugging turned on.\nLogs will be created and temporary picture files won't be deleted.")

print("Monopoly poker blackjack bot.")

selection = input("1:Load settings from file. 2:Input new settings.\n:")
if selection == "1":
    numbersLocation,numbersLocationd,playLocations,waitTriggerLocation,waitTriggerColor,bet,locVersion = loadLocationsFile(locationsFile)
elif selection == "2":
    locVersion = version
    numbersLocation,numbersLocationd,playLocations,waitTriggerLocation,waitTriggerColor,bet = getLocations()
    sels = input("Save settings? [Y/n]\n:").lower()
    if sels != "n":
        writeLocationsFile(locationsFile,numbersLocation,numbersLocationd,playLocations,waitTriggerLocation,waitTriggerColor,bet,version)
else:
    raise SyntaxError

if locVersion != version:
    print("VERSION MISMATCH!\nLocation file version and application version are different.\nPROGRAM MIGHT NOT RUN CORRECTLY!")
    print(f"Location file: {locVersion} | App version: {version}")
    if input("Continue? (y/N)\n:").lower() != "y":
        print("Exiting...")
        exit(1)

play = 1
print("Starting... Press o to begin. Hold p to stop.")
log(f"Program run... {time.ctime()}",logFile,logging,False)
while True:
    keyboard.wait(onBind)
    log("Started.",logFile,logging,True)
    while keyboard.is_pressed(offBind) == False:
        if play == 1:
            time.sleep(7)
            pyautogui.click(bet[0],bet[1])
        isStuck = waitNewRound(waitTriggerLocation,waitTriggerColor,waitCheckFrequency,waitCheckColorTolerance,logFile,logging)
        if isStuck:
            play = 1
            continue
        #log("New round.",logFile,logging,False)
        if logging:
            print("NEWROUND")
        tempImagePath = f"{tempImagePathBase}{str(time.monotonic())}.png"
        dealerTemp = f"{dealerTempBase}{str(time.monotonic())}.png"
        pyautogui.screenshot(imageFilename=tempImagePath,region=numbersLocation)
        pyautogui.screenshot(imageFilename=dealerTemp,region=numbersLocationd)
        formatImage2(tempImagePath)
        formatImage2(dealerTemp)
        #r'--oem 3 --psm 6 -c tessedit_char_whitelist="0123456789/"' altarnate config to detect aces
        #r'--oem 3 --psm 6 outputbase digits' only detects digits ACES WONT WORK
        hand, handAce = filterNumbers(pytesseract.image_to_string(tempImagePath,config=r'--oem 3 --psm 6 -c tessedit_char_whitelist="0123456789/"'))
        dealerHand, dealerAce = filterNumbers(pytesseract.image_to_string(dealerTemp,config=r'--oem 3 --psm 6 -c tessedit_char_whitelist="0123456789/"'))
        if removePics:
            os.remove(tempImagePath)
            os.remove(dealerTemp)
        play,playStyle = bjDecider(hand,dealerHand,handAce,dealerAce,play)
        if play == 3:
            continue
        if logging:
            log(f"Hand:{str(hand)}|Dealers hand:{str(dealerHand)}|Play:{str(play)}|Play style:{playStyle}.",logFile,logging,True)
        else:
            print(f"Hand:{str(hand)}|Dealers hand:{str(dealerHand)}|Play:{str(play)}|Play style:{playStyle}.")
        if debug and removePics == False:
            os.rename(tempImagePath,tempImagePathBase+f"-Hand:{str(hand)}-Dealers hand:{str(dealerHand)}-Play:{str(play)}-Play style:{playStyle}-{str(time.monotonic())}.png".replace("[","").replace("]","").replace("/","-").replace(":"," ").replace(","," "))
            os.rename(dealerTemp,dealerTempBase+f"-Hand:{str(hand)}-Dealers hand:{str(dealerHand)}-Play:{str(play)}-Play style:{playStyle}-{str(time.monotonic())}.png".replace("[","").replace("]","").replace("/","-").replace(":"," ").replace(","," "))
        pyautogui.click(playLocations[play][0],playLocations[play][1])

    log("stopped.",logFile,logging,True)