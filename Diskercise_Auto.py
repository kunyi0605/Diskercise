import time
import sys
import pyautogui
import warnings
import PIL
from os import environ
from pywinauto.application import Application
from pyautogui import screenshot
import os

warnings.simplefilter('ignore', category=UserWarning)
app = Application(backend="win32").start(r"D:\\Jenkins\\Diskercise\\Diskercise.exe")
window = app["Diskercise - dirve D"]
window['Edit1'].set_text(sys.argv[1])
window['Edit2'].set_text(sys.argv[2])
window['Edit3'].set_text(sys.argv[3])
window['Edit4'].set_text(sys.argv[4])
window['Edit5'].set_text(sys.argv[5])
window['Adv'].click()
settings = app['Advance Settings']
settings['CheckBox3'].click()
settings['OK'].click()
window['Data TypeComboBox'].select(sys.argv[6])
window['Start'].click()
#myScreenshot = pyautogui.screenshot()
#myScreenshot.save(r'D:\\Jenkins\\DiskerCise\\DiskerCise_screenshot.png')
#run_time = os.getenv('Test_Timing')
#print('getenv run_time')
#print(run_time)
#runtime = sys.argv[6]
#time.sleep( 65*float(run_time) )
#window['Stop'].click()
#app.kill()
exit(0)
