import json
import os
import argparse

def limpiar_datos(data):
    datos_limpiados = {}

    # Si el JSON es una lista, convertirlo en un diccionario
    if isinstance(data, list):
        nuevo_data = {}
        for elemento in data:
            if isinstance(elemento, dict):  # Asegurar que es un diccionario
                nuevo_data.update(elemento)  # Unir los diccionarios dentro de la lista
        data = nuevo_data  # Ahora `data` será un diccionario

    for region, cultivos in data.items():
        nuevos_cultivos = []
        
        for cultivo in cultivos:
            # Extraer todos los años disponibles, ignorando claves como "MEDIA"
            años_disponibles = [key.split('-')[0] for key in cultivo.keys()
                                if key.endswith("-superficie") and cultivo[key] != "" and key.split('-')[0].isdigit()]

            if años_disponibles:
                # Obtener el año más reciente
                año_mayor = max(map(int, años_disponibles))
                
                # Crear un nuevo diccionario con solo el cultivo y los datos del año mayor
                nuevo_cultivo = {
                    "CULTIVOS": cultivo["CULTIVOS"],
                    f"{año_mayor}-superficie": cultivo.get(f"{año_mayor}-superficie", ""),
                    f"{año_mayor}-produccion": cultivo.get(f"{año_mayor}-produccion", "")
                }
                nuevos_cultivos.append(nuevo_cultivo)
        
        if nuevos_cultivos:
            datos_limpiados[region] = nuevos_cultivos

    return datos_limpiados

def procesar_archivo(input_file, output_file):
    """ Carga, limpia y guarda el archivo de cosechas """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Limpiar los datos
    datos_limpiados = limpiar_datos(data)

    # Guardar el JSON limpio en el archivo de salida
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(datos_limpiados, f, ensure_ascii=False, indent=4)

    print(f"✅ Archivo procesado y guardado como: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesa un archivo JSON de cosechas y lo limpia.")
    parser.add_argument("input_file", help="Ruta del archivo JSON de entrada")
    parser.add_argument("output_file", help="Ruta del archivo JSON de salida")
    
    args = parser.parse_args()
    procesar_archivo(args.input_file, args.output_file)
