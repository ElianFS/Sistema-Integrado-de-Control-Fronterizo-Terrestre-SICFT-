import sqlite3
from datetime import datetime, timedelta
import uuid
from init_db import crear_base_de_datos, DB_NAME

def generar_operacion():
    return "SICFT-" + str(uuid.uuid4())[:8].upper()

def validar_patente_formato(patente):
    return len(patente) >= 6

def es_vehiculo_bloqueado(patente):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM vehiculos_bloqueados WHERE patente = ?", (patente,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def consultar_sag_db(documento):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM conductores_restringidos WHERE documento = ?", (documento,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is None

def registrar_log_db(operacion, patente, documento, estado):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cursor.execute(
        "INSERT INTO log_operaciones VALUES (?, ?, ?, ?, ?)",
        (operacion, fecha, patente, documento, estado)
    )
    conn.commit()
    conn.close()

def guardar_permiso_activo_db(id_permiso, patente, documento, f_emision, f_vencimiento):
    """Guarda el permiso aprobado de forma oficial en la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    qr_simulado = f"QR-{id_permiso}-{patente}"
    cursor.execute(
        "INSERT INTO permisos_emitidos VALUES (?, ?, ?, ?, ?, ?)",
        (id_permiso, patente, documento, f_emision, f_vencimiento, qr_simulado)
    )
    conn.commit()
    conn.close()

def registrar_salida_temporal():
    print("\n===== REGISTRO DE SALIDA TEMPORAL =====")
    patente = input("Ingrese patente del vehículo: ").upper().strip()
    documento = input("Ingrese RUT/Pasaporte conductor: ").strip()

    print("\nValidando información en Base de Datos...")

    if not validar_patente_formato(patente):
        print("\nERROR: Patente inválida (mínimo 6 caracteres).")
        return

    # Filtro Bloqueo
    if es_vehiculo_bloqueado(patente):
        operacion = generar_operacion()
        print("\n===================================")
        print("ALERTA ROJA: Vehículo bloqueado.")
        print("===================================")
        registrar_log_db(operacion, patente, documento, "RECHAZADO")
        return

    # Filtro SAG
    if not consultar_sag_db(documento):
        operacion = generar_operacion()
        print("\n===================================")
        print("ALERTA SAG: Conductor restringido.")
        print("===================================")
        registrar_log_db(operacion, patente, documento, "RECHAZADO")
        return

    # Operación Aprobada
    fecha_emision = datetime.now()
    fecha_vencimiento = fecha_emision + timedelta(days=180)
    operacion = generar_operacion()

    f_emision_str = fecha_emision.strftime("%d/%m/%Y")
    f_vencimiento_str = fecha_vencimiento.strftime("%d/%m/%Y")

    print("\n===================================")
    print("OPERACIÓN APROBADA")
    print("===================================")
    print(f"N° Permiso: {operacion}")
    print(f"Fecha Vencimiento: {f_vencimiento_str}")

    # Guardamos en AMBAS tablas
    registrar_log_db(operacion, patente, documento, "APROBADO")
    guardar_permiso_activo_db(operacion, patente, documento, f_emision_str, f_vencimiento_str)


def menu_historial():
    """Submenú para decidir qué datos de la base de datos queremos revisar."""
    print("\n--- CONSULTA DE BASE DE DATOS ---")
    print("1. Ver Permisos Oficiales Emitidos (Solo Aprobados)")
    print("2. Ver Historial Completo de Auditoría (Logs)")
    opc = input("Seleccione: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if opc == "1":
        cursor.execute("SELECT id_permiso, patente, documento_conductor, fecha_vencimiento FROM permisos_emitidos")
        registros = cursor.fetchall()
        print("\n===== PERMISOS DE SALIDA ACTIVOS =====")
        for reg in registros:
            print(f"Permiso: {reg[0]} | Patente: {reg[1]} | Conductor: {reg[2]} | Vence: {reg[3]}")
            
    elif opc == "2":
        cursor.execute("SELECT operacion, fecha, patente, estado FROM log_operaciones ORDER BY fecha DESC")
        registros = cursor.fetchall()
        print("\n===== LOGS DE AUDITORÍA CENTRAL =====")
        for reg in registros:
            print(f"[{reg[1]}] Op: {reg[0]} | Patente: {reg[1]} | Estado: {reg[3]}")
    else:
        print("Opción inválida.")
        
    conn.close()

def modo_offline():
    print("\n===== MODO OFFLINE =====")
    print("Operación local habilitada utilizando la base de datos SQLite.")

def menu():
    crear_base_de_datos()
    while True:
        print("\n===================================")
        print(" SICFT - Control Fronterizo Terrestre")
        print("===================================")
        print("1. Registrar salida temporal")
        print("2. Ver base de datos / Historial")
        print("3. Modo offline")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_salida_temporal()
        elif opcion == "2":
            menu_historial()
        elif opcion == "3":
            modo_offline()
        elif opcion == "4":
            print("\nSistema finalizado.")
            break

if __name__ == "__main__":
    menu()