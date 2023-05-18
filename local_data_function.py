import csv
import os
import json
from datetime import datetime

def insert_data(payload):
    fieldnames = ["id_porcion", "comida_a_dispensar", "tiempo_dispensacion", "alimentado"]
    tiempo_str = payload['record'].get('tiempo_dispensacion')
    tiempo_normal = datetime.strptime(tiempo_str, '%H:%M:%S').time()
    new_row = {
        "id_porcion": payload['record'].get('id_porcion'),
        "comida_a_dispensar": payload['record'].get('comida_a_dispensar'),
        "tiempo_dispensacion": tiempo_normal.hour * 60 + tiempo_normal.minute,
        "alimentado": 0
    }
    with open("cambios_comida.csv", "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if os.stat("cambios_comida.csv").st_size <= 0:
            writer.writeheader()
        writer.writerow(new_row)


def update_data(payload):
    temp_file = "temp.csv"
    fieldnames = ["id_porcion", "comida_a_dispensar", "tiempo_dispensacion", "alimentado"]
    with open("cambios_comida.csv", "r") as file, open(temp_file, "w", newline="") as temp:
        reader = csv.DictReader(file)
        writer = csv.DictWriter(temp, fieldnames=fieldnames)
        writer.writeheader()
        updated = False
        for row in reader:
            if row.get("id_porcion") and int(row["id_porcion"]) == payload['old_record'].get('id_porcion'):
                updated_row = {k: v for k, v in row.items() if k in fieldnames}
                updated_row["comida_a_dispensar"] = payload['record'].get('comida_a_dispensar')
                tiempo_str = payload['record'].get('tiempo_dispensacion')
                tiempo_normal = datetime.strptime(tiempo_str, '%H:%M:%S').time()
                updated_row["tiempo_dispensacion"] = tiempo_normal.hour * 60 + tiempo_normal.minute
                updated_row["alimentado"] = row.get("alimentado")
                writer.writerow(updated_row)
                updated = True
            else:
                writer.writerow(row)
        if not updated:
            tiempo_str = payload['record'].get('tiempo_dispensacion')
            tiempo_normal = datetime.strptime(tiempo_str, '%H:%M:%S').time()
            new_row = {
                "id_porcion": payload['record'].get('id_porcion'),
                "comida_a_dispensar": payload['record'].get('comida_a_dispensar'),
                "tiempo_dispensacion": tiempo_normal.hour * 60 + tiempo_normal.minute,
                "alimentado": 0
            }
            writer.writerow(new_row)
    os.replace(temp_file, "cambios_comida.csv")


def delete_data(payload):
    fieldnames = ["id_porcion", "comida_a_dispensar", "tiempo_dispensacion", "alimentado"]
    deleted_row_id = payload['old_record'].get('id_porcion')
    file_exists = os.path.isfile("cambios_comida.csv")
    if file_exists:
        rows = []
        with open("cambios_comida.csv", "r") as file:
            reader = csv.DictReader(file)
            existing_fieldnames = reader.fieldnames
            if all(fieldname in existing_fieldnames for fieldname in fieldnames):
                for row in reader:
                    if row["id_porcion"] != str(deleted_row_id):
                        new_row = {fieldname: row[fieldname] for fieldname in fieldnames}
                        rows.append(new_row)
        with open("cambios_comida.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
