# Proporciona las funciones para interactuar con la base de datos 

import sqlite3
import supabase
from dotenv import load_dotenv
import os

# Configuración de la conexión a la base de datos
load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_info(user_id):
    # Obtener información del usuario desde Supabase
    query = 'SELECT * FROM usuario WHERE celular = ###'
    params = (user_id,)
    response = supabase_client.query(query, params)
    if response['status'] == 200:
        user_info = response['data'][0]
    else:
        user_info = None
    return user_info

def update_local_file(user_id, file_path):
    # Actualizar archivo local con información del usuario
    user_info = get_user_info(user_id)
    if user_info:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
        cursor.execute('INSERT OR REPLACE INTO users (id, name, email) VALUES (?, ?, ?)', (user_info['id'], user_info['name'], user_info['email']))
        conn.commit()
        conn.close()
        return True
    else:
        return False
