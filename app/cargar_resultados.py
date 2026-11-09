#!/usr/bin/env python3
import os
import psycopg2

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "midatabase")
DB_USER = os.getenv("POSTGRES_USER", "usuario_app")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password_seguro123")
DB_PORT = os.getenv("DB_PORT", "5432")

def cargar_datos():
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
    )
    cur = conn.cursor()

    # Crear tabla de resultados si no existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resultados_ventas (
            id SERIAL PRIMARY KEY,
            categoria VARCHAR(100),
            mes VARCHAR(7),
            ingreso_total NUMERIC(15, 2)
        );
    """)
    conn.commit()

    # Limpiar tabla para evitar duplicados
    cur.execute("TRUNCATE TABLE resultados_ventas;")
    conn.commit()

    archivo_resultado = "/data/output/resultado/part-00000"
    if not os.path.exists(archivo_resultado):
        # Intentar ruta local de app por si se corre fuera de Hadoop
        archivo_resultado = "/app/part-00000"

    registros = []
    with open(archivo_resultado, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) == 3:
                cat, mes, ingreso = parts
                registros.append((cat, mes, float(ingreso)))

    cur.executemany("""
        INSERT INTO resultados_ventas (categoria, mes, ingreso_total)
        VALUES (%s, %s, %s);
    """, registros)

    conn.commit()
    print(f"Éxito: Se cargaron {len(registros)} registros en PostgreSQL.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    cargar_datos()
