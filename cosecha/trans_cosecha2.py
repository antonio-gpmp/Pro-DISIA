import pandas as pd
import json
import argparse
import re
import sys

def extraer_anio_desde_nombre(nombre_archivo):
    """Extrae un año de 4 cifras desde el nombre del archivo."""
    coincidencias = re.findall(r'20\d{2}', nombre_archivo)
    return coincidencias[0] if coincidencias else None

def transformar_csv_multi_a_json(archivo_entrada, archivo_salida, anio):
    # Leer el CSV completo
    df = pd.read_csv(archivo_entrada, sep=';', encoding='utf-8', decimal=',', thousands='.')

    # Nombres de columnas a usar
    col_superficie = f"{anio}-superficie"
    col_produccion = f"{anio}-produccion"

    if col_superficie not in df.columns or col_produccion not in df.columns:
        print(f"❌ Error: El archivo no contiene '{col_superficie}' y/o '{col_produccion}'.")
        sys.exit(1)

    # Identificar índices de los bloques
    indices_cabecera = df.index[df.iloc[:, 0].str.contains("CEREALES PARA GRANO", na=False)].tolist()

    if len(indices_cabecera) != 4:
        print("❌ Error: No se han encontrado exactamente 4 bloques regionales en el archivo.")
        sys.exit(1)

    nombres_provincias = ["COMUNIDAD VALENCIANA", "ALICANTE", "CASTELLON", "VALENCIA"]
    resultado = {}

    for i, nombre in enumerate(nombres_provincias):
        inicio = indices_cabecera[i] + 1
        fin = indices_cabecera[i + 1] if i + 1 < len(indices_cabecera) else len(df)
        bloque = df.iloc[inicio:fin].copy()

        bloque.columns = df.columns  # Asegura nombres de columnas correctos
        bloque = bloque[[df.columns[0], col_superficie, col_produccion]]
        bloque.columns = ["CULTIVOS", col_superficie, col_produccion]

        # Limpieza de datos
        bloque["CULTIVOS"] = bloque["CULTIVOS"].astype(str).str.strip()
        bloque[col_superficie] = pd.to_numeric(bloque[col_superficie], errors='coerce')
        bloque[col_produccion] = pd.to_numeric(bloque[col_produccion], errors='coerce')
        bloque = bloque.dropna(subset=[col_superficie, col_produccion])

        resultado[nombre] = bloque.to_dict(orient="records")

    # Guardar como JSON
    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transformar CSV de cosechas con múltiples regiones al formato JSON limpio.")
    parser.add_argument('-i', '--input', required=True, help='Ruta del archivo CSV de entrada')
    parser.add_argument('-o', '--output', required=True, help='Ruta del archivo JSON de salida')
    parser.add_argument('-y', '--year', help='Año (ej: 2020). Si no se indica, se intenta extraer del nombre del archivo.')

    args = parser.parse_args()

    anio = args.year or extraer_anio_desde_nombre(args.input)
    if not anio:
        print("❌ No se pudo determinar el año. Usa -y para especificarlo.")
        sys.exit(1)

    transformar_csv_multi_a_json(args.input, args.output, anio)
