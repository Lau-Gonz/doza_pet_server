import csv
from datetime import datetime
import time

# Ruta del archivo CSV
archivo_csv = 'cambios_comida.csv'

while True:
    # Obtén la hora actual
    hora_actual = time.localtime()
    segundos_actuales = hora_actual.tm_hour * 3600 + hora_actual.tm_min * 60

    if segundos_actuales==0:
        with open(archivo_csv, 'r+') as archivo:
            lector_csv = csv.reader(archivo)
            lineas_csv = list(lector_csv)
            archivo.seek(0)  # Vuelve al inicio del archivo

            for linea in lineas_csv:
                linea[3] = "1"  # Actualiza la columna "dar_comer" a 0
                archivo.write(','.join(linea) + '\n')

    # Lee el archivo CSV en cada iteración para obtener la información actualizada
    with open(archivo_csv, 'r') as archivo:
        lector_csv = csv.reader(archivo)
        lineas_csv = list(lector_csv)
        # Salta la primera línea si contiene encabezados
        encabezados = lineas_csv[0]

        # Itera sobre las filas del archivo CSV
        for i, fila in enumerate(lineas_csv[1:], start=1):
            tiempo_dispensacion = int(fila[2])
            dar_comer = int(fila[3])
            # Comprueba si la hora actual coincide con el tiempo de dispensación
            if segundos_actuales == tiempo_dispensacion & dar_comer==1:
                id_dispositivo = fila[0]
                comida_a_dispensar = fila[1]
                alimentado = fila[3]
                # Imprime la información de la fila
                print(f"ID del dispositivo: {id_dispositivo}")
                print(f"Comida a dispensar: {comida_a_dispensar}")
                print(f"Tiempo de dispensación: {tiempo_dispensacion}")
                print(f"Se debe dar de comer: {bool(alimentado)}")

                lineas_csv[i][3] = "0"

    # Espera 1 hora antes de verificar nuevamente
    time.sleep(60)
    print("Ya paso un minuto xd")