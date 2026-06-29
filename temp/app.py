from flask import Flask, jsonify, request
import os
import redis
import psycopg2

app = Flask(__name__)

# Conexión a Redis — OJO: el host es el NOMBRE del contenedor, no una IP
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),   # "redis" = nombre del contenedor
    port=6379,
    decode_responses=True
)

# Función para conectar a Postgres
def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),     # "postgres" = nombre del contenedor
        dbname=os.getenv("DB_NAME", "miapp"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "secret")
    )

# Crear la tabla al arrancar (si no existe)
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id SERIAL PRIMARY KEY,
            texto TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    # Incrementar contador de visitas en Redis
    visitas = redis_client.incr("visitas")
    return jsonify({
        "mensaje": "Hola desde Flask + Docker!",
        "visitas": visitas
    })

@app.route("/mensajes", methods=["GET"])
def listar_mensajes():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, texto FROM mensajes")
    mensajes = [{"id": row[0], "texto": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(mensajes)

@app.route("/mensajes", methods=["POST"])
def crear_mensaje():
    texto = request.json.get("texto")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO mensajes (texto) VALUES (%s)", (texto,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "creado", "texto": texto}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)