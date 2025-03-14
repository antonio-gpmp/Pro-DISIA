import json
import os
import argparse

def convertir_a_numeros(valor):
    """ Convierte una cadena en número si es posible, sino devuelve la misma cadena. """
    try:
        if isinstance(valor, str) and ("." in valor or "," in valor):  # Para detectar decimales
            return float(valor.replace(",", "."))  # Convertir a float y cambiar "," por "."
        return int(valor) if isinstance(valor, str) and valor.isdigit() else valor  # Convertir a entero si es posible
    except ValueError:
        return valor  # Devolver el mismo valor si no se puede convertir

def reestructurar_datos_precipitacion(data):
    """ Reestructura los datos para que los observatorios sean claves en el JSON. """
    datos_reestructurados = {}

    for observatorio in data:
        nombre_observatorio = observatorio.pop("OBSERVATORIO")  # Extraer el nombre
        datos_reestructurados[nombre_observatorio] = {clave: convertir_a_numeros(valor) for clave, valor in observatorio.items()}
        
        # Agregar la propiedad 'Unidad' si no está presente
        if "Unidad" not in datos_reestructurados[nombre_observatorio]:
            datos_reestructurados[nombre_observatorio]["Unidad"] = "l/m2"

    return datos_reestructurados

def procesar_archivo_precipitaciones(input_file, output_file):
    """ Carga, reestructura y guarda el archivo de precipitaciones """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Reestructurar los datos
    datos_reestructurados = reestructurar_datos_precipitacion(data)

    # Guardar el JSON limpio
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(datos_reestructurados, f, ensure_ascii=False, indent=4)

    print(f"✅ Archivo procesado y guardado como: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesa un archivo de precipitaciones y lo reestructura.")
    parser.add_argument("input_file", help="Ruta del archivo JSON de entrada")
    parser.add_argument("output_file", help="Ruta del archivo JSON de salida")
    
    args = parser.parse_args()
    procesar_archivo_precipitaciones(args.input_file, args.output_file)