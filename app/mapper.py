#!/usr/bin/env python3
import sys

# Ignorar el encabezado del CSV si viene presente
# Estructura del CSV: id,fecha_hora,tienda,categoria,producto,cantidad,precio_unitario,metodo_pago

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split(',')
    
    # Ignorar la línea de encabezado
    if parts[0] == "id" or len(parts) < 8:
        continue
        
    try:
        fecha_hora = parts[1].strip()
        categoria = parts[3].strip()
        cantidad = float(parts[5].strip())
        precio_unitario = float(parts[6].strip())
        
        # Extraer el año y mes (YYYY-MM) de 'YYYY-MM-DD HH:MM:SS'
        mes = fecha_hora[:7]
        
        # Calcular el ingreso de este registro
        ingreso = cantidad * precio_unitario
        
        # Emitir la clave (categoria\tmes) y el valor (ingreso)
        print(f"{categoria}\t{mes}\t{ingreso:.2f}")
    except (ValueError, IndexError):
        # Manejo de líneas mal formadas sin truncar el job
        continue
