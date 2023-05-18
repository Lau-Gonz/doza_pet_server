import os
import csv

fieldnames = ["id_porcion", "comida_a_dispensar", "tiempo_dispensacion", "alimentado"]
with open("cambios_comida.csv", "a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    print(os.stat("cambios_comida.csv").st_size <= 0)
    if os.stat("cambios_comida.csv").st_size <= 0:
        writer.writeheader()