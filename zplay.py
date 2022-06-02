# image recognition
# mostly using template matching (i.e. cv.matchTemplate)
import cv2 as cv
import numpy as np

# clicks and screenshots
import pyautogui

# sleep
import time

def main():
    while(True):
        #classRestrict()
        host()
        #joiner() # if class restricted only use classRestrict
        cleric()        
        stageEnd()

def cleric():
    turn = 1
    while(matchCnt("stage2.PNG", 0.9)):
        targetsDead = matchCnt("dead.PNG", 0.645)
        targetST = matchCnt("stRez.PNG", 0.7)
        targetAOE = matchCnt("aoeRez.PNG")
        targetDK = matchCnt("dk.PNG")
        print(targetsDead, targetST, targetAOE, targetDK)
        if targetsDead == 1 and targetST and targetDK: # only on turn 4?
            clickBestTarget(convert("dead.PNG"))
            time.sleep(0.125)
            clickBestTarget(convert("dk.PNG"))
            time.sleep(0.125)
            clickBestTarget(convert("stRez.PNG"))
            time.sleep(3)
            continue 
        elif targetsDead > 1 and targetAOE and targetDK:
            clickBestTarget(convert("dk.PNG"))
            time.sleep(0.25)
            clickBestTarget(convert("aoeRez.PNG"))
            time.sleep(3)
            continue 

        if turn == 1:
            clickBestTarget(convert("item1.PNG"))
            turn += 1
            time.sleep(3.25)
        elif turn == 2:
            clickBestTarget(convert("itemPoison.PNG"))
            turn += 1
            time.sleep(3.25)
        elif turn == 3:
            clickBestTarget(convert("item3.PNG"))
            turn += 1
            time.sleep(3.25)
        elif turn == 4:
            clickBestTarget(convert("item4.PNG"))
            turn = 1
            time.sleep(3.25)

def guardian():
    pass

def archer():
    pass

def mage():
    pass

def host():
    while(True):
        if matchCnt("orb.PNG", 0.7):
            clickBestTarget(convert("orb.PNG"))
            break
        
    while(True):
        if matchCnt("lvl.PNG"):
            clickBestTarget(convert("lvl.PNG"))
            break

    while(True):
        if matchCnt("hostStart.PNG"):
            clickBestTarget(convert("hostStart.PNG"))
            break

    while(True):
        if matchCnt("stage2.PNG", 0.9):
            break        

def joiner():
    while(True):
        if matchCnt("ready.PNG"):
            clickBestTarget(convert("ready.PNG"))
            break
        elif matchCnt("start.PNG"):
            clickBestTarget(convert("start.PNG"))
            break
    
    while(True):
        if matchCnt("stage2.PNG", 0.93):
            break

def classRestrict():
    while(True):
        if matchCnt("confirm.PNG"):
            clickBestTarget(convert("confirm.PNG"))
            break

def stageEnd():
    while(True):
        if matchCnt("next1.PNG", 0.7):
            clickBestTarget(convert("next1.PNG"))
            break

    while(True):
        if matchCnt("next2.PNG", 0.7):
            clickBestTarget(convert("next2.PNG"))
            break
        elif matchCnt("orb.PNG", 0.7):
            break

    while(True):
        if matchCnt("tier.PNG", 0.7):
            clickBestTarget(convert("tier.PNG"))
            break
        elif matchCnt("orb.PNG", 0.7):
            break
    
    while(True):
        if matchCnt("tier.PNG", 0.7):
            clickBestTarget(convert("tier.PNG"))
            break
        elif matchCnt("orb.PNG", 0.7):
            break

    while(True):
        if matchCnt("tier.PNG", 0.7):
            clickBestTarget(convert("tier.PNG"))
            break
        elif matchCnt("orb.PNG", 0.7):
            break

def clickBestTarget(trgt):
    (x, y, w, h, max_val) = findBestMatch(trgt)
    if max_val > 0.60:
        pyautogui.click(clicks=2, x=x + h/2, y=y + w/2)

def matchCnt(image, thrsh = None):
    if thrsh is not None:
        return len(findMatches(convert(image), thrsh))
    else:
        return len(findMatches(convert(image)))

# can change thrsh holds to fine tune detection
def findMatches(trgt, thrsh = 0.6):
    ss = screenshot()

    # TM_CCOEFF_NORMED mostly aribitrary rn
    rslt = cv.matchTemplate(trgt, ss, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(rslt)

    print(max_val)

    yloc, xloc = np.where(rslt >= thrsh)

    rctngls = []
    for (x, y) in zip(xloc, yloc):
        rctngls.append([int(x), int(y), int(trgt.shape[0]), int(trgt.shape[1])]) # duplicate for group rectangles
        rctngls.append([int(x), int(y), int(trgt.shape[0]), int(trgt.shape[1])])

    rctngls, weights = cv.groupRectangles(rctngls, 1, 0.2)

    return rctngls # list of targets in rectangle form with x, y at the center

def findBestMatch(trgt):
    ss = screenshot()

    # TM_CCOEFF_NORMED mostly aribitrary rn
    rslt = cv.matchTemplate(trgt, ss, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(rslt)

    print(max_val)

    return (max_loc[0], max_loc[1], int(trgt.shape[0]), int(trgt.shape[1]), max_val)

def screenshot():
    img = pyautogui.screenshot()
    img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR) # normalize to a standard format cv expects
    return img

def convert(image):
    converted = cv.imread(image, cv.IMREAD_UNCHANGED)
    converted = cv.cvtColor(np.array(converted), cv.COLOR_RGB2BGR) # normalize to a standard format cv expects
    return converted

if __name__ == "__main__":
    main()