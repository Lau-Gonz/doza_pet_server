import os
import csv
from datetime import datetime
import time
import serial
from supabase import create_client
from dotenv import load_dotenv


load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
disp = os.environ.get("DISPOSITIVO_ID")


archivo_csv = 'cambios_comida.csv'


ser = serial.Serial('/dev/ttyACM1',9600)
ser.flushInput()


supabase = create_client(url, key)


while True:
    
    hora_actual = time.localtime()
    minutos_actuales = hora_actual.tm_hour * 60 + hora_actual.tm_min
    print("\n \n Hora Actual", hora_actual.tm_hour, ":", hora_actual.tm_min, " , ", minutos_actuales )

    if minutos_actuales==0:
        with open(archivo_csv, 'r+') as archivo:
            lector_csv = csv.reader(archivo)
            next(lector_csv)
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
                
                mensaje = comida_a_dispensar.encode('latin-1')
                ser.write(mensaje)
                
                fila_modificada = fila[:3] + ["1"] + fila[4:]
                lineas_modificadas.append(fila_modificada)
                
                #if ser.in_waiting>0:
                    #line = ser.readline().decode('latin-1').strip()
                    #print("ERROR: ", line, "\n")
                    # Incluir el código para el cliente
                    #line = ser.readline().decode('latin-1').strip()
                    #line = "No_hay_comida"
                    #print("ERROR: ", line, "\n")
                    # Realiza la actualización en la tabla 'dispositivo'
                    #data = supabase.table('dispositivo').update({'error': 1}).eq('id', disp).execute()
                    #print(data)
                
                print("Todo termino ok")
            else:
                lineas_modificadas.append(fila)
    with open(archivo_csv, 'w', newline='') as archivo_modificado:
        escritor_csv = csv.writer(archivo_modificado)
        escritor_csv.writerows(lineas_modificadas)
    time.sleep(60)
