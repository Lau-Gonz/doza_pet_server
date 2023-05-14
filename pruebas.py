from datetime import datetime
import time
hora_actual = datetime.now()
print(hora_actual)

## Dia siguiente a las 00:00:00
hora_actual = time.localtime()
segundos = hora_actual.tm_hour * 3600 + hora_actual.tm_min * 60 + hora_actual.tm_sec

print(bool(0))

print(segundos)