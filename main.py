# Importar las funciones y clases necesarias de los diferentes archivos
from cronjob import send_info_to_arduino
from dataset import get_user_info, update_local_file
from realtime import on_change

# Configurar el cronjob
scheduler = BlockingScheduler()
scheduler.add_job(send_info_to_arduino, 'interval', minutes=5)
scheduler.start()

# Obtener la información del usuario y actualizar el archivo local
user_id = 'el_id_del_usuario'
info = get_user_info(user_id)
update_local_file(info)

# Escuchar los cambios en la base de datos
realtime = client.realtime()
realtime.on('usuarios:info', lambda payload: on_change(payload, user_id))

# Enviar mensajes cortos al usuario
print('El servidor está en línea')

while True:
    send_info_to_arduino()
    time.sleep(300)  # Esperar 5 minutos antes de enviar la siguiente información