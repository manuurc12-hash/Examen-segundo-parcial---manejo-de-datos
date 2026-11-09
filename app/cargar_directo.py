#!/usr/bin/env python3
import os
import psycopg2

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "midatabase")
DB_USER = os.getenv("POSTGRES_USER", "usuario_app")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password_seguro123")
DB_PORT = os.getenv("DB_PORT", "5432")

def cargar():
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
    )
    cur = conn.cursor()

    # Recrear la tabla limpia
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

    archivo = "/app/part-00000"
    registros = []
    
    with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.strip().split('\t')
            # Filtrar estrictamente solo las lineas del reducer (Categoria, Mes, Ingreso)
            if len(parts) == 3:
                try:
                    cat, mes, ingreso = parts[0].strip(), parts[1].strip(), float(parts[2].strip())
                    registros.append((cat, mes, ingreso))
                except ValueError:
                    continue

    cur.executemany("""
        INSERT INTO resultados_ventas (categoria, mes, ingreso_total)
        VALUES (%s, %s, %s);
    """, registros)

    conn.commit()
    print(f"¡Éxito instantáneo! Se cargaron {len(registros)} registros formateados en PostgreSQL.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    cargar()
