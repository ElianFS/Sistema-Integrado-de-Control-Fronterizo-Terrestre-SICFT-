from datetime import datetime, timedelta
import random
import uuid

# =====================================
# SICFT
# Sistema Integrado de Control Fronterizo Terrestre
# =====================================

vehiculos_bloqueados = [
    "XYZ999",
    "AA111AA",
    "BB222BB"
]

conductores_restringidos = [
    "11111111-1",
    "22222222-2"
]

log_operaciones = []


def generar_operacion():
    return "SICFT-" + str(uuid.uuid4())[:8].upper()


def validar_patente(patente):
    if len(patente) < 6:
        return False
    return True


def consultar_sag(documento):
    if documento in conductores_restringidos:
        return False
    return True


def registrar_log(operacion, estado):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    registro = {
        "fecha": fecha,
        "operacion": operacion,
        "estado": estado
    }

    log_operaciones.append(registro)


def registrar_salida_temporal():

    print("\n===== REGISTRO DE SALIDA TEMPORAL =====")

    patente = input("Ingrese patente del vehículo: ").upper()
    documento = input("Ingrese RUT/Pasaporte conductor: ")

    print("\nValidando información...")

    # Validación patente
    if not validar_patente(patente):
        print("\nERROR: Patente inválida.")
        return

    # Vehículo bloqueado
    if patente in vehiculos_bloqueados:

        operacion = generar_operacion()

        print("\n===================================")
        print("ALERTA ROJA")
        print("Vehículo con salida pendiente.")
        print("Operación cancelada.")
        print("===================================")

        registrar_log(operacion, "RECHAZADO")
        return

    # Validación SAG
    if not consultar_sag(documento):

        operacion = generar_operacion()

        print("\n===================================")
        print("ALERTA SAG")
        print("Conductor con restricción activa.")
        print("Operación cancelada.")
        print("===================================")

        registrar_log(operacion, "RECHAZADO")
        return

    # Aprobación
    fecha_emision = datetime.now()
    fecha_vencimiento = fecha_emision + timedelta(days=180)

    operacion = generar_operacion()

    print("\n===================================")
    print("OPERACIÓN APROBADA")
    print("===================================")

    print(f"N° Operación: {operacion}")
    print(f"Patente: {patente}")
    print(f"Documento: {documento}")

    print(
        "Fecha emisión:",
        fecha_emision.strftime("%d/%m/%Y")
    )

    print(
        "Fecha vencimiento:",
        fecha_vencimiento.strftime("%d/%m/%Y")
    )

    print("Vigencia: 180 días")
    print("Código QR: [SIMULADO]")

    registrar_log(operacion, "APROBADO")


def ver_logs():

    print("\n===== HISTORIAL DE OPERACIONES =====")

    if len(log_operaciones) == 0:
        print("No existen registros.")
        return

    for registro in log_operaciones:
        print("--------------------------------")
        print("Fecha:", registro["fecha"])
        print("Operación:", registro["operacion"])
        print("Estado:", registro["estado"])


def modo_offline():

    print("\n===== MODO OFFLINE =====")
    print("Sin conexión al servidor central.")
    print("Operación local habilitada.")
    print("Sincronización pendiente: 3 registros.")
    print("Los datos serán enviados cuando")
    print("la conexión sea restablecida.")


def menu():

    while True:

        print("\n")
        print("===================================")
        print(" SICFT")
        print(" Sistema Integrado de Control")
        print(" Fronterizo Terrestre")
        print("===================================")

        print("1. Registrar salida temporal")
        print("2. Ver historial")
        print("3. Modo offline")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_salida_temporal()

        elif opcion == "2":
            ver_logs()

        elif opcion == "3":
            modo_offline()

        elif opcion == "4":
            print("\nSistema finalizado.")
            break

        else:
            print("\nOpción inválida.")


# Inicio del sistema
menu()