import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="API Resultados Ventas - MapReduce")

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "midatabase")
DB_USER = os.getenv("POSTGRES_USER", "usuario_app")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password_seguro123")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT,
        cursor_factory=RealDictCursor
    )

class ResultadoSchema(BaseModel):
    categoria: str
    mes: str
    ingreso_total: float

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API conectada a PostgreSQL"}

# GET /resultados -> Todos los registros (Parte D)
@app.get("/resultados")
def get_resultados():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM resultados_ventas ORDER BY categoria, mes;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# GET /resultados/<categoria> -> Filtro por clave (Parte D)
@app.get("/resultados/{categoria}")
def get_resultados_by_categoria(categoria: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM resultados_ventas WHERE LOWER(categoria) = LOWER(%s) ORDER BY mes;", (categoria,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return rows

# POST /resultados -> Operación de escritura CRUD (Parte D)
@app.post("/resultados", status_code=201)
def create_resultado(item: ResultadoSchema):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO resultados_ventas (categoria, mes, ingreso_total) VALUES (%s, %s, %s) RETURNING *;",
        (item.categoria, item.mes, item.ingreso_total)
    )
    nuevo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return nuevo
