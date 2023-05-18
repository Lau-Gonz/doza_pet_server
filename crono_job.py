import csv
from datetime import datetime
import time

archivo_csv = 'cambios_comida.csv'

while True:
    hora_actual = time.localtime()
    minutos_actuales = hora_actual.tm_hour * 60 + hora_actual.tm_min
    print("Hora Actual", hora_actual.tm_hour, ":", hora_actual.tm_min, " , ", minutos_actuales )
    if minutos_actuales==0:
        with open(archivo_csv, 'r+') as archivo:
            lector_csv = csv.reader(archivo)
            lineas_csv = list(lector_csv)
            archivo.seek(0)
            for linea in lineas_csv:
                linea[3] = "0"
                archivo.write(','.join(linea) + '\n')
    with open(archivo_csv, 'r') as archivo:
        lector_csv = csv.reader(archivo)
        lineas_csv = list(lector_csv)
        encabezados = lineas_csv[0]
        lineas_modificadas = [encabezados] 
        for i, fila in enumerate(lineas_csv[1:], start=1):
            tiempo_dispensacion = int(fila[2])
            dar_comer = int(fila[3])
            if (minutos_actuales == tiempo_dispensacion) and (dar_comer==0):
                id_porcion = fila[0]
                comida_a_dispensar = fila[1]
                print(f"ID de la porcion: {id_porcion}")
                print(f"Comida a dispensar: {comida_a_dispensar}")
                print(f"Tiempo de dispensación: {tiempo_dispensacion}")
                print(f"Se debe dar de comer: {not dar_comer}")
                fila_modificada = fila[:3] + ["1"] + fila[4:]
                lineas_modificadas.append(fila_modificada)
            else:
                lineas_modificadas.append(fila)
    with open(archivo_csv, 'w', newline='') as archivo_modificado:
        escritor_csv = csv.writer(archivo_modificado)
        escritor_csv.writerows(lineas_modificadas)
    time.sleep(60)
    print("Ya paso un minuto xd ", hora_actual.tm_hour, ":", hora_actual.tm_min, " , ", minutos_actuales )