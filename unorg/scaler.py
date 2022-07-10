import pyautogui

def coordinate(x,y):
    a,b = pyautogui.size()
    u=(x*a)
    v = y*b
    pyautogui.click(u,v)