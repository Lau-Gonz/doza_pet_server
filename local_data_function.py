import csv
import os
import json


def insert_data(payload):
    fieldnames = ["id_dispositivo", "comida_a_dispensar", "tiempo_dispensacion", "alimentado"]

    new_row = {
        "id_dispositivo": payload['record'].get('id_dispositivo'),
        "comida_a_dispensar": payload['record'].get('comida_a_dispensar'),
        "tiempo_dispensacion": payload['record'].get('tiempo_dispensacion'),
        "alimentado": 1
    }

    with open("cambios_comida.csv", "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(new_row)


def update_data(payload):
    temp_file = "temp.csv"
    fieldnames = ["id_dispositivo", "comida_a_dispensar", "tiempo_dispensacion", "alimentado"]

    with open("cambios_comida.csv", "r") as file, open(temp_file, "w", newline="") as temp:
        reader = csv.DictReader(file)
        writer = csv.DictWriter(temp, fieldnames=fieldnames)

        writer.writeheader()
        updated = False
        for row in reader:
            if row.get("id_dispositivo") and int(row["id_dispositivo"]) == payload['old_record'].get('id_dispositivo'):
                updated_row = {k: v for k, v in row.items() if k in fieldnames}
                updated_row["comida_a_dispensar"] = payload['record'].get('comida_a_dispensar')
                updated_row["tiempo_dispensacion"] = payload['record'].get('tiempo_dispensacion')
                updated_row["alimentado"] = payload['record'].get('alimentado')
                writer.writerow(updated_row)
                updated = True
            else:
                writer.writerow(row)

        if not updated:
            new_row = {
                "id_dispositivo": payload['record'].get('id_dispositivo'),
                "comida_a_dispensar": payload['record'].get('comida_a_dispensar'),
                "tiempo_dispensacion": payload['record'].get('tiempo_dispensacion'),
                "alimentado": 1
            }
            writer.writerow(new_row)

    os.replace(temp_file, "cambios_comida.csv")



def delete_data(payload):
    fieldnames = ["id_dispositivo", "comida_a_dispensar", "tiempo_dispensacion"]
    deleted_row_id = payload['old_record'].get('id_dispositivo')

    file_exists = os.path.isfile("cambios_comida.csv")
    if file_exists:
        rows = []
        with open("cambios_comida.csv", "r") as file:
            reader = csv.DictReader(file)
            existing_fieldnames = reader.fieldnames
            if all(fieldname in existing_fieldnames for fieldname in fieldnames):
                for row in reader:
                    if row["id_dispositivo"] != str(deleted_row_id):
                        rows.append(row)

        with open("cambios_comida.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
