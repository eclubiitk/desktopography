import pyautogui
def coordinate(x,y):
    a,b=pyautogui.size()
    #mapping the coordinates to the screen
    u=(x*a)
    v=(y*b)
    pyautogui.click(u,v)

