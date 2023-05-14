import os
import csv
from dotenv import load_dotenv
from realtime.connection import Socket
from local_data_function import insert_data, update_data, delete_data
import json

load_dotenv()

ID = os.environ.get("SUPABASE_ID", "")
KEY = os.environ.get("SUPABASE_KEY", "")
URL = f"wss://{ID}.supabase.co/realtime/v1/websocket?apikey={KEY}&vsn=1.0.0"
ID_DISPOSITVO = os.environ.get("DISPOSITIVO_ID", "")


def callback1(payload):
    # Cuando la tabla funcione, es necesario agregar una condición para que solo busque el id del dispositivo
    print(f"Cambio en la tabla ", payload.get("table"), " : ", payload.get("type"), payload)
    if payload.get("type") == "INSERT":
        insert_data(payload)
    elif payload.get("type") == "UPDATE":
        update_data(payload)
    elif payload.get("type") == "DELETE":
        delete_data(payload)


def main():
    s = Socket(URL)
    s.connect()
    channel_1 = s.set_channel("realtime:public:porcion")
    channel_1.join().on("*", callback1)
    s.listen()


if __name__ == "__main__":
    main()