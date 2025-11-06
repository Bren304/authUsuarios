from connection import engine

try:
    with engine.connect() as conn:
        print("Conexión exitosa a la base de datos.")
except Exception as e:
    print("Error al conectar:", e)
