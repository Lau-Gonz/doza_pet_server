# Archivo encargado de modificar el arduino o la base de datos según las actualizaciones presentes
# en la base de datos cada minuto

import time
import serial
import sqlite3
from supabase import create_client
from dataset import get_user_info
from dotenv import load_dotenv
import os

# Configuración del puerto serial
SERIAL_PORT = '/dev/ttyUSB0'  # El puerto serial que estás utilizando
SERIAL_RATE = 9600  # La velocidad de comunicación serial (en baudios)

# Configuración de Supabase
load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Función para actualizar el archivo SQLite3 con los cambios de la base de datos
def update_sqlite3_file(table_name):
    # Obtener los cambios de la base de datos utilizando los protocolos de mensaje de Supabase
    subscription = client.realtime.from(table_name).on('UPDATE', lambda payload: None)
    while True:
        # Esperar a que haya un cambio en la base de datos
        change = subscription.any()
        
        # Actualizar el archivo SQLite3 con los nuevos datos
        user_id = 'el_id_del_usuario'
        info = get_user_info(user_id)
        conn = sqlite3.connect(f'ruta_del_archivo_sqlite3_{table_name}')
        cursor = conn.cursor()
        cursor.execute(f'UPDATE tabla SET alimento = "{info["alimento"]}", cantidad = {info["cantidad"]} WHERE id = {user_id}')
        conn.commit()
        cursor.close()
        conn.close()

# Función para enviar la información al Arduino
def send_info_to_arduino(table_name):
    # Obtener la información del usuario desde el archivo SQLite3
    user_id = 'el_id_del_usuario'
    conn = sqlite3.connect(f'ruta_del_archivo_sqlite3_{table_name}')
    cursor = conn.cursor()
    cursor.execute(f'SELECT alimento, cantidad FROM tabla WHERE id = {user_id}')
    info = cursor.fetchone()
    cursor.close()
    conn.close()

    # Crear la cadena de caracteres a enviar al Arduino
    message = f'{info[0]},{info[1]}\n'

    # Configurar y abrir el puerto serial
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, timeout=1)

    # Esperar un segundo para que el Arduino se inicie
    time.sleep(1)

    # Enviar la cadena de caracteres al Arduino
    ser.write(message.encode())

    # Cerrar el puerto serial
    ser.close()

tables=['dispositivo','mascota','porcion','usuario']
# Función principal que ejecuta el cronjob
def main():
    # Actualizar el archivo SQLite3 con los cambios de la base de datos en segundo plano
    for table_name in tables:
        update_sqlite3_file(table_name)

    # Configurar el cronjob para enviar la información al Arduino cada X tiempo
    while True:
        for table_name in tables:
            send_info_to_arduino(table_name)
        time.sleep(60)  # Esperar 60 segundos antes de enviar la siguiente información

if __name__ == '__main__':
    main()
