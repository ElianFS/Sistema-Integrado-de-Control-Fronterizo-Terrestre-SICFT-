import sqlite3

DB_NAME = "sicft.db"

def crear_base_de_datos():
    print("Iniciando creación de la Base de Datos SICFT...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Tabla de Vehículos Bloqueados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehiculos_bloqueados (
            patente TEXT PRIMARY KEY
        )
    """)

    # 2. Tabla de Conductores Restringidos (SAG)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conductores_restringidos (
            documento TEXT PRIMARY KEY
        )
    """)

    # 3. Tabla de Auditoría (Guarda TODO: Aprobados y Rechazados)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log_operaciones (
            operacion TEXT PRIMARY KEY,
            fecha TEXT,
            patente TEXT,
            documento TEXT,
            estado TEXT
        )
    """)

    # 4. NUEVA TABLA: Permisos Emitidos Activos (Solo guarda los aprobados con sus fechas)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS permisos_emitidos (
            id_permiso TEXT PRIMARY KEY,
            patente TEXT,
            documento_conductor TEXT,
            fecha_emision TEXT,
            fecha_vencimiento TEXT,
            codigo_qr TEXT
        )
    """)

    # Precarga de datos de prueba
    cursor.execute("SELECT COUNT(*) FROM vehiculos_bloqueados")
    if cursor.fetchone()[0] == 0:
        patentes_mock = [("XYZ999",), ("AA111AA",), ("BB222BB",)]
        cursor.executemany("INSERT INTO vehiculos_bloqueados VALUES (?)", patentes_mock)

    cursor.execute("SELECT COUNT(*) FROM conductores_restringidos")
    if cursor.fetchone()[0] == 0:
        conductores_mock = [("11111111-1",), ("22222222-2",)]
        cursor.executemany("INSERT INTO conductores_restringidos VALUES (?)", conductores_mock)

    conn.commit()
    conn.close()
    print("¡Base de datos 'sicft.db' actualizada con éxito!\n")

if __name__ == "__main__":
    crear_base_de_datos()