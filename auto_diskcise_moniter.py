import wmi
from pywinauto import Application,mouse , keyboard
from pywinauto.win32functions import SetForegroundWindow
from time import sleep
from os import listdir
from os.path import join
from shutil import copyfile

LogOutputPaht='C:\\Jenkins\\Diskercise\\Report'

def printStatus(mainWindow):
    content = mainWindow.list_control_identifiers()[0]
    transcations = content['child'][17]["text"]
    transpersecond = content['child'][15]["text"]
    mbstransferred = content['child'][24]["text"]
    kbsreadpersecond = content['child'][25]["text"]
    kbswritepersecond = content['child'][26]["text"]
    runningTime = content['child'][20]["text"]
    print(transcations, transpersecond, mbstransferred, kbsreadpersecond, kbswritepersecond, runningTime)

def fetchError(mainWindow):
    mainWindow = application.top_window()
    SetForegroundWindow(mainWindow.wrapper_object())
    print("> Error Window appear")
    print("> window title: ")
    title = mainWindow.list_control_identifiers()[0]["text"]
    print("> " + title)
    print("> window content")
    content = mainWindow.list_control_identifiers()[0]["child"][2]["text"]
    print("> " + content)

    logfilePath = join(LogOutputPaht,"diskercise.txt")
    print("save log file to "+logfilePath)
    logfile = open(logfilePath, 'w')
    logfile.write("Window Title:\n")
    logfile.write(title)
    logfile.write("\n\n")
    logfile.write("Window Content:\n")
    logfile.write(content.replace("\\n","\n"))
    logfile.close()
    
def moniterApp(applicationArray):
    allEnd = True
    total = len(applicationArray)
    for index, application in enumerate(applicationArray, start=1):
        try:
            mainWindow = application.top_window()
            content = mainWindow.list_control_identifiers()[0]
        except:
            print('process %d end' % (index))
            if total == index and allEnd:
                print("all process end")
                return None
            else:
                continue
        
        allEnd = False
        try:
            printStatus(mainWindow)
        except:
            try:
                fetchError(mainWindow)
            except:
                print("Unknown Error Windows")
            return False

    return True

def writeStatus(status):
    statusFilePath = join(LogOutputPaht,"Diskercise_status.txt")
    statusFile = open(statusFilePath, 'w')
    statusFile.write(status)
    statusFile.close()
    
def killProgram(name):
    from subprocess import call
    call(["taskkill","/f","/im",name])

c = wmi.WMI ()
processIdArray = []

print("wait diskcise READY")
sleep(60)

for process in c.Win32_Process ():
    print (process.ProcessId, process.Name)
    if (process.Name == u'Diskercise.exe'):
        print("find diskercise")
        print(process.ProcessId)
        processIdArray.append(process.ProcessId)

print("All Diskercise process: ")
print(processIdArray)
if len(processIdArray) == 0:
    print("Unable to find any diskercise process")
    writeStatus("FAIL")
    exit(0)

applicationArray = []

for pid in processIdArray:
    application = Application().connect(process=pid)
    applicationArray.append(application)

while True:
    sleep(10)
    programStatus = moniterApp(applicationArray)
    if (programStatus==True):
        print("Diskercise Running")
    elif (programStatus==None):
        print("All Diskercise End")
        writeStatus("PASS")
        break
    else:
        print("some message box appear")
        writeStatus("FAIL")
        break

