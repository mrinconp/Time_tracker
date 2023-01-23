from win32gui import GetWindowText, GetForegroundWindow
from datetime import datetime
import threading
import time
import sys

print('Ingrese "end" para finalizar el programa.')

entrada = ''
start_time = datetime.now()
active_window = 0
wnd_names = []

def get_name(list):
    names=[]
    app_windows=[]
    for i in range (0, len(list)):
        app_windows.append(list[i].split('-'))
    for j in range (0,len(app_windows)):
        aux = app_windows[j]
        names.append(aux[-1].strip())
    while ('' in names):
        names.remove('')
    return names

#Programs list
def active_windows():
    active_window = 0
    while True:
        new_window = GetWindowText(GetForegroundWindow())
        if active_window != new_window:
            active_window = new_window
            if active_window not in (wnd_names):
                wnd_names.append(active_window)
                #convert names into dictionary to avoid duplicate entries:
                names = list(dict.fromkeys(get_name(wnd_names))) 
                print(names)
        time.sleep(1)

def finish():
    print('Ingresaste "end", el programa finalizará.')

# now threading1 runs regardless of user input
threading1 = threading.Thread(target=active_windows)
threading1.daemon = True
threading1.start()

while True:
    if input() == 'end':
        finish()
        end_time = datetime.now()
        time_spent = end_time-start_time
        print('El tiempo total de trabajo fue de', time_spent)
        sys.exit()