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
DISPOSITIVO_ID = os.environ.get("DISPOSITIVO_ID")


def callback1(payload):

    if payload.get("type") == "INSERT":

        if payload['record'].get("id_dispositivo") == int(DISPOSITIVO_ID):

            print("New Payload: \n",payload, "\n")
            insert_data(payload)

    if payload.get("type") == "UPDATE":

        if payload['record'].get("id_dispositivo") == int(DISPOSITIVO_ID):

            print("New Payload: \n",payload, "\n")
            update_data(payload)

    if payload.get("type") == "DELETE":

        if payload['old_record'].get("id_dispositivo") == int(DISPOSITIVO_ID):

            delete_data(payload)
            print("New Payload: \n",payload, "\n")


def main():
    
    s = Socket(URL)
    s.connect()
    channel_1 = s.set_channel("realtime:public:porcion")
    channel_1.join().on("*", callback1)
    s.listen()


if __name__ == "__main__":
    main()