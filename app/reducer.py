#!/usr/bin/env python3
import sys

current_key = None
current_total = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    try:
        categoria, mes, ingreso_str = line.split('\t')
        ingreso = float(ingreso_str)
        key = f"{categoria}\t{mes}"
    except ValueError:
        continue

    # Si la clave es la misma que la anterior, acumulamos
    if current_key == key:
        current_total += ingreso
    else:
        # Si la clave cambia y teníamos una anterior, emitimos el resultado
        if current_key:
            print(f"{current_key}\t{current_total:.2f}")
        current_key = key
        current_total = ingreso

# Emitir el último registro procesado
if current_key:
    print(f"{current_key}\t{current_total:.2f}")
