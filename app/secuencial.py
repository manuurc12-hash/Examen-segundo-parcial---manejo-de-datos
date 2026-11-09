#!/usr/bin/env python3
import csv
import time

def resolver_secuencial(path_csv):
    inicio = time.time()
    resultados = {}

    with open(path_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Omitir encabezado
        
        for row in reader:
            if len(row) < 8:
                continue
            try:
                fecha_hora = row[1].strip()
                categoria = row[3].strip()
                cantidad = float(row[5].strip())
                precio = float(row[6].strip())
                
                mes = fecha_hora[:7]
                clave = f"{categoria}\t{mes}"
                ingreso = cantidad * precio
                
                resultados[clave] = resultados.get(clave, 0.0) + ingreso
            except (ValueError, IndexError):
                continue

    fin = time.time()
    print(f"--- Proceso Secuencial Finalizado ---")
    print(f"Tiempo de ejecución: {fin - inicio:.2f} segundos")
    print(f"Total de registros procesados: {len(resultados)}")

if __name__ == "__main__":
    resolver_secuencial("/data/input/ventas_125051951.csv")
