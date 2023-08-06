#importar librerías y módulos
from win32gui import GetWindowText, GetForegroundWindow
import time
import threading
import sys
import matplotlib.pyplot as plt
from datetime import datetime
import datetime as dt
import operator


print('Ingrese "end" para finalizar el programa.')

#nombre ventana
def windowtext ():
    a = GetWindowText(GetForegroundWindow())
    return a

#inicio de variables para almacenar información
start_time = datetime.now()
process_time={}
timestamp = {}

#Limpiar nombres de ventanas y llenar el diccionario process_time con Ventana: Tiempo
def app_times():
    active_window = ''
    while True:
        #limpiar nombres de ventanas
        new_window = windowtext()
        new_window = (new_window.split('-'))[-1]
        new_window = new_window.strip()

        if active_window != new_window:
            #limpiar nombres de ventanas y reasignar ventan nueva a activa
            active_window = new_window
            active_window = (active_window.split('-'))[-1]
            active_window = active_window.strip()
        
        #registro de tiempo cada segundo
        timestamp[active_window] = int(time.time())
        time.sleep(1)

        #añadir ventanas nuevas únicamente
        if active_window not in process_time.keys():
            process_time[active_window] = 0
        process_time[active_window] = process_time[active_window]+int(time.time())-timestamp[active_window]
 
#funcion para introducir el resumen del trabajo
def finish():
    print('Ingresaste "end", el programa finalizará.')
    print('-'*50)

#funcion para descanso cada 20min
def rest_advice():
    while True:
        time.sleep(1200)
        print('Momento de descansar')

#paralelismos para esperar la entrada del usuario para finalizar el programa y para llevar el tiempo de descanso

threading1 = threading.Thread(target=app_times)
threading1.daemon = True
threading1.start()

threading2 = threading.Thread(target=rest_advice)
threading2.daemon= True
threading2.start()


#programa principal: resumen de trabajo, tiempos, gráfica.
while True:

    
    if input() == 'end':

        # tiempo total de trabajo
        end_time = datetime.now()
        time_spent = end_time-start_time
        finish()


        #resumen
        print('Resumen de trabajo')
        print('-'*50,'\nEl tiempo total de trabajo fue de', time_spent)

        #eliminar variables vacías del diccionario process_time
        if '' in process_time:
            process_time['Desktop'] = process_time.pop('')
        #ordenar diccionario en orden descendente según el tiempo
        process_time = dict(sorted(process_time.items(), key=operator.itemgetter(1),reverse=True))

        #separar llaves y valores en dos listas
        apps = list(process_time)
        seconds = list(process_time.values())

        #convertir time_spent en formato hh:mm:ss
        def time_format(n):
            n = int(n)
            time_format=str(dt.timedelta(seconds=n))
            return time_format

        #resumen de trabajo por actividades realizadas. actividad, tiempo.
        for i in range(len(apps)):
            print(apps[i], time_format(seconds[i]))

        #función diagrama circular
        def chart():
            labels1 = apps
            sizes = seconds

            #matriz de ceros para resaltar el primer elemento (elemento con mayor porcentaje) con el parametro {explode}
            def zeros(n):
                explode = [0.1]
                for i in range (n):
                    explode.append(0*i)
                return explode
            
            #parámetro explode para resaltar el elemento que primero se considera al graficar
            n = len(labels1)-1
            explode = zeros(n)
            
            fig1, ax1 = plt.subplots()
            porcent = []
            
            #pasar tiempo a porcentajes
            for i in sizes:
                porcent.append((i/sum(sizes))*100)
            
            #leyendas de la gráfica
            patches, texts = plt.pie(sizes, explode=explode, shadow=True, startangle=90)   
            labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels1, porcent)]

            #ordenar leyenda en orden descendente
            sort_legend = True
            if sort_legend:
                patches, labels, dummy =  zip(*sorted(zip(patches, labels, sizes),
                                                    key=lambda x: x[2],
                                                    reverse=True))
            #graficar leyenda
            plt.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.1, 1.),
                    fontsize=8)

        
            #eje equal para graficar de manera circular
            ax1.axis('equal')

            #tight_layout para corregir defectos de visualización
            plt.tight_layout()

            #mostrar gráfica
            plt.show()
        
        #llamar a la función chart para mostrar la gráfica
        chart()

        #terminar procesos paralelos.
        sys.exit()
        