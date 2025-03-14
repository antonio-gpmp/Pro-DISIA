import json
import os
import argparse

def limpiar_datos_productos(data):
    datos_limpiados = {}
    
    # Encontrar el índice del último producto vacío
    ultimo_vacio = None
    for i, item in enumerate(data):
        if item["PRODUCTOS"].strip() == "":
            ultimo_vacio = i

    # Si hay un producto vacío, solo mantenemos hasta ahí
    if ultimo_vacio is not None:
        data = data[:ultimo_vacio]

    for item in data:
        producto = item.get("PRODUCTOS", "").strip()

        # Saltar filas con PRODUCTOS vacío
        if not producto:
            continue

        # Limpiar el nombre de "COMUNITAT VALENCIANA"
        precios = {
            "COMUNITAT VALENCIANA": item.get("COMUNITAT\nVALENCIANA", "").replace("\n", " ").strip(),
            "ALICANTE": item.get("ALICANTE", "").strip(),
            "CASTELLÓN": item.get("CASTELLÓN", "").strip(),
            "VALENCIA": item.get("VALENCIA", "").strip()
        }

        # Convertir números de string a float y reemplazar "-" con 0
        for key in precios:
            precios[key] = 0 if precios[key] == "-" else float(precios[key].replace(",", ".")) if precios[key] else 0

        # Guardar en el diccionario con el producto como clave
        datos_limpiados[producto] = precios

    return datos_limpiados

def procesar_archivo(input_file, output_file):
    """ Carga, limpia y guarda el archivo de precios """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Limpiar los datos
    datos_limpiados = limpiar_datos_productos(data)

    # Guardar el JSON limpio en el archivo de salida
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(datos_limpiados, f, ensure_ascii=False, indent=4)

    print(f"✅ Archivo procesado y guardado como: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesa un archivo JSON de precios de productos y lo limpia.")
    parser.add_argument("input_file", help="Ruta del archivo JSON de entrada")
    parser.add_argument("output_file", help="Ruta del archivo JSON de salida")
    
    args = parser.parse_args()
    procesar_archivo(args.input_file, args.output_file)
