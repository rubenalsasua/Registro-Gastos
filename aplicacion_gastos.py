import json
import os
from datetime import datetime

# Archivo donde se almacenarán los datos
FILE_NAME = "gastos.json"
CATEGORIAS = ["Hogar", "Comida", "Ocio", "Transporte", "Salud", "Otros"]
LIMITE_GASTO_MENSUAL = 2000
LIMITE_GASTO_INDIVIDUAL = 500

def cargar_gastos():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def guardar_gastos(gastos):
    with open(FILE_NAME, "w") as file:
        json.dump(gastos, file, indent=4)

def calcular_gasto_mensual(gastos):
    mes_actual = datetime.now().strftime("%Y-%m")
    return sum(g["importe"] for g in gastos if g["fecha"].startswith(mes_actual))

def agregar_gasto():
    descripcion = input("Descripción del gasto: ")
    importe = float(input("Importe: "))

    if importe > LIMITE_GASTO_INDIVIDUAL:
        print("Lo siento, pero no tienes permitido gastar más de 500€ en un solo gasto.")
        return

    print("Categorías disponibles:")
    for i, cat in enumerate(CATEGORIAS, 1):
        print(f"{i}. {cat}")
    categoria = int(input("Seleccione una categoría (número): "))
    categoria = CATEGORIAS[categoria - 1]
    fecha = datetime.now().strftime("%Y-%m-%d")
    
    gastos = cargar_gastos()
    gasto_mensual_actual = calcular_gasto_mensual(gastos)

    if gasto_mensual_actual + importe > LIMITE_GASTO_MENSUAL:
        print("Atención, has gastado más de 2000€ este mes.")
    
    gastos.append({"descripcion": descripcion, "importe": importe, "categoria": categoria, "fecha": fecha})
    guardar_gastos(gastos)
    print("Gasto agregado exitosamente.")

def mostrar_gastos():
    gastos = cargar_gastos()
    if not gastos:
        print("No hay gastos registrados.")
        return
    
    print("\nListado de Gastos:")
    for i, gasto in enumerate(gastos, 1):
        print(f"{i}. {gasto['fecha']} - {gasto['descripcion']} ({gasto['categoria']}): {gasto['importe']}€")

def editar_gasto():
    gastos = cargar_gastos()
    mostrar_gastos()
    if not gastos:
        return
    
    idx = int(input("Seleccione el número del gasto a editar: ")) - 1
    if 0 <= idx < len(gastos):
        nuevo_importe = float(input("Nuevo importe: ") or gastos[idx]['importe'])

        if nuevo_importe > LIMITE_GASTO_INDIVIDUAL:
            print("Lo siento, pero no tienes permitido gastar más de 500€ en un solo gasto.")
            return

        gastos[idx]['descripcion'] = input("Nueva descripción: ") or gastos[idx]['descripcion']
        gastos[idx]['importe'] = nuevo_importe
        print("Categorías disponibles:")
        for i, cat in enumerate(CATEGORIAS, 1):
            print(f"{i}. {cat}")
        cat_idx = input("Nueva categoría (número o Enter para mantener): ")
        if cat_idx:
            gastos[idx]['categoria'] = CATEGORIAS[int(cat_idx) - 1]

        guardar_gastos(gastos)
        print("Gasto actualizado correctamente.")
    else:
        print("Selección inválida.")

def eliminar_gasto():
    gastos = cargar_gastos()
    mostrar_gastos()
    if not gastos:
        return
    
    idx = int(input("Seleccione el número del gasto a eliminar: ")) - 1
    if 0 <= idx < len(gastos):
        del gastos[idx]
        guardar_gastos(gastos)
        print("Gasto eliminado correctamente.")
    else:
        print("Selección inválida.")

def menu():
    while True:
        print("\nGestión de Gastos")
        print("1. Agregar Gasto")
        print("2. Mostrar Gastos")
        print("3. Editar Gasto")
        print("4. Eliminar Gasto")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_gasto()
        elif opcion == "2":
            mostrar_gastos()
        elif opcion == "3":
            editar_gasto()
        elif opcion == "4":
            eliminar_gasto()
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    menu()
