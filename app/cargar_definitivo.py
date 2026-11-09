#!/usr/bin/env python3
import os
import subprocess
import psycopg2

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "midatabase")
DB_USER = os.getenv("POSTGRES_USER", "usuario_app")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password_seguro123")
DB_PORT = os.getenv("DB_PORT", "5432")

def cargar():
    print("1. Conectando a PostgreSQL...")
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
    )
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS resultados_ventas;")
    cur.execute("""
        CREATE TABLE resultados_ventas (
            id SERIAL PRIMARY KEY,
            categoria VARCHAR(100),
            mes VARCHAR(7),
            ingreso_total NUMERIC(15, 2)
        );
    """)
    conn.commit()

    print("2. Obteniendo datos procesados directamente de Hadoop...")
    # Extraer únicamente la salida de MapReduce ignorando el CSV original
    cmd = ["docker", "exec", "hadoop_standalone", "cat", "/data/output/resultado/part-00000"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    registros = []
    for line in result.stdout.splitlines():
        parts = line.strip().split('\t')
        if len(parts) == 3:
            try:
                cat, mes, ingreso = parts[0].strip(), parts[1].strip(), float(parts[2].strip())
                registros.append((cat, mes, ingreso))
            except ValueError:
                continue

    print(f"3. Insertando {len(registros)} registros formateados...")
    cur.executemany("""
        INSERT INTO resultados_ventas (categoria, mes, ingreso_total)
        VALUES (%s, %s, %s);
    """, registros)

    conn.commit()
    print(f"¡ÉXITO TOTAL! Se insertaron {len(registros)} registros en menos de 1 segundo.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    cargar()
