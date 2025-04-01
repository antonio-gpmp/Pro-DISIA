import pandas as pd
import json
import argparse
import re
import sys

def extraer_anio_desde_nombre(nombre_archivo):
    """Extrae un año de 4 cifras desde el nombre del archivo."""
    coincidencias = re.findall(r'20\d{2}', nombre_archivo)
    return coincidencias[0] if coincidencias else None

def transformar_csv_a_json(archivo_entrada, archivo_salida, anio):
    # Cargar el CSV con formato español
    df = pd.read_csv(archivo_entrada, sep=';', encoding='utf-8', decimal=',', thousands='.')

    # Nombres de columna esperados para el año
    col_superficie = f"{anio}-superficie"
    col_produccion = f"{anio}-produccion"

    # Verificar existencia de columnas necesarias
    if col_superficie not in df.columns or col_produccion not in df.columns:
        print(f"❌ Error: El archivo no contiene '{col_superficie}' y/o '{col_produccion}'.")
        sys.exit(1)

    # Limpiar valores: solo filas donde haya valores numéricos en superficie y producción
    df = df[df[col_superficie].apply(lambda x: pd.notna(x) and isinstance(x, (int, float, str)))]
    df = df[df[col_produccion].apply(lambda x: pd.notna(x) and isinstance(x, (int, float, str)))]

    # Convertir a numérico (por si quedaron strings)
    df[col_superficie] = pd.to_numeric(df[col_superficie], errors='coerce')
    df[col_produccion] = pd.to_numeric(df[col_produccion], errors='coerce')

    # Eliminar filas donde ambas columnas sean nulas
    df = df.dropna(subset=[col_superficie, col_produccion])

    # Limpiar espacios en nombres de cultivo
    df['CULTIVOS'] = df['CULTIVOS'].astype(str).str.strip()

    # Seleccionar y renombrar columnas
    df = df[['CULTIVOS', col_superficie, col_produccion]]
    df = df.rename(columns={
        col_superficie: f"{anio}-superficie",
        col_produccion: f"{anio}-produccion"
    })

    # Construir estructura final
    resultado = {
        "COMUNIDAD VALENCIANA": df.to_dict(orient='records')
    }

    # Guardar como JSON
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transformar CSV de cosechas al formato JSON limpio.")
    parser.add_argument('-i', '--input', required=True, help='Ruta del archivo CSV de entrada')
    parser.add_argument('-o', '--output', required=True, help='Ruta del archivo JSON de salida')
    parser.add_argument('-y', '--year', help='Año (ej: 2020). Si no se indica, se intenta extraer del nombre del archivo.')

    args = parser.parse_args()

    anio = args.year or extraer_anio_desde_nombre(args.input)
    if not anio:
        print("❌ No se pudo determinar el año. Usa -y para especificarlo.")
        sys.exit(1)

    transformar_csv_a_json(args.input, args.output, anio)