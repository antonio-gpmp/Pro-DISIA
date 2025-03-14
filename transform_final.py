import json
import pandas as pd

mapeo_cultivos_productos = {
    "ARROZ": ["ARROZ CÁSCARA"],
    "CEBADA": ["CEBADA (2 carreras)"],
    "MAÍZ": ["MAÍZ GRANO"],
    "PATATA": ["PATATA EXTRATEMP Y TEMPRANA", "PATATA MED ESTAC Y TARDIA"],
    "CHUFA": ["CHUFA"],
    "ALFALFA": ["HENO DE ALFALFA"],
    "NARANJO DULCE": ["NAVELINA", "W. NAVEL", "NAVEL LANE LATE", "SALUSTIANA", "VALENCIA LATE"],
    "MANDARINO": ["CLAUSELLINA-OKITSU", "SATSUMA-OWARI", "CLEMENRUBI", "MARISOL",
                  "CLEMENTINA DE NULES", "CLEMENTINA HERNANDINA", "CLEMENVILLA O NOVA",
                  "ORTANIQUE", "NADORCOTT", "OTRAS MANDARINAS HÍBRIDAS"],
    "LIMONERO": ["LIMÓN VERNA", "LIMÓN FINO (Mesero)"],
    "MANZANA": ["MANZANA CONSUMO FRESCO"],
    "NÍSPERO": ["NISPERO"],
    "PERA": ["PERA CONSUMO EN FRESCO"],
    "ALBARICOQUE": ["ALBARICOQUE CONSUMO EN FRESCO"],
    "MELOCOTÓN (3)": ["MELOCOTÓN  CONSUMO EN FRESCO"],
    "NECTARINA": ["NECTARINA"],
    "CEREZA": ["CEREZA"],
    "CIRUELA": ["CIRUELA"],
    "HIGOS": ["HIGOS Y BREVAS"],
    "GRANADA": ["GRANADA"],
    "CAQUI": ["CAQUI"],
    "UVA DE MESA": ["UVA DE MESA"],
    "ALMENDRA": ["ALMENDRA CASCARA"],
    "LECHUGA": ["LECHUGA TOTAL"],
    "COLIFLOR": ["COLIFLOR"],
    "TOMATE": ["TOMATE CONSUMO EN FRESCO"],
    "CEBOLLA": ["CEBOLLA"],
    "PIMIENTO": ["PIMIENTO CONSUMO EN FRESCO"],
    "ALCACHOFA": ["ALCACHOFA consumo fresco", "ALCACHOFA industria"],
    "MELÓN": ["MELÓN"],
    "SANDÍA": ["SANDÍA"],
    "JUDÍAS VERDES": ["JUDÍA VERDE (Plana)"],
    "UVA DE VINIFICACIÓN": ["VINO BLANCO DOP+IGP  (R(CE) 479/2008)", "VINO BLANCO VARIETAL+OTROS (R(CE) 479/2008)",
             "VINO TINTO Y ROSADO DOP+IGP (R(CE) 479/2008)", "VINO TINTO Y ROSADO VARIETAL+OTROS (R(CE) 479/2008)"],
    "ACEITE DE OLIVA": ["Aceite de Oliva Virgen extra de < 0,8º (R(CE)1513/2001)",
                         "Aceite de Oliva Virgen de 0,8º a  2º (R(CE)1513/2001)",
                         "Aceite de Oliva Virgen de > 2º (R(CE)1513/2001)"],
    "FLORES (1)": ["FLOR CORTADA CLAVELES (euros/docena)", "FLOR CORTADA ROSAS (euros/docena)"]
}


# 🟢 Cargar los JSON limpios (cosechas, precios y meteorología)
años = list(range(2018, 2024))

cosechas = {año: json.load(open(f"./cosecha/limpio_cosecha{año}.json", "r", encoding="utf-8")) for año in años}
precios = {año: json.load(open(f"./precios/limpio_precios_{año}.json", "r", encoding="utf-8")) for año in años}
meteo = {año: json.load(open(f"./meteo/limpio_precipitaciones_{año}.json", "r", encoding="utf-8")) for año in años}

# 📊 Lista para el dataset final
dataset = []

# 🔄 Iterar sobre cada año
for año in años:
    for region, cultivos in cosechas[año].items():
        for cultivo in cultivos:
            nombre_cultivo = cultivo["CULTIVOS"]
            superficie = cultivo.get(f"{año}-superficie", 0)
            produccion = cultivo.get(f"{año}-produccion", 0)

            # 🔍 Buscar productos en el mapeo
            productos = mapeo_cultivos_productos.get(nombre_cultivo, [nombre_cultivo])

            # 📌 Generar una fila por cada producto asociado
            for producto in productos:
                precio_data = precios[año].get(producto, {
                    "COMUNITAT VALENCIANA": 0, "ALICANTE": 0, "CASTELLÓN": 0, "VALENCIA": 0
                })

                # 🌧 Obtener los datos meteorológicos de la región
                meteo_data = meteo[año].get(region, {mes: 0 for mes in ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN",
                                                                         "JUL", "AGO", "SEP", "OCT", "NOV", "DIC",
                                                                         "TOTAL", "MEDIA"]})

                dataset.append({
                    "Anio": año,
                    "Region": region,
                    "Cultivo": nombre_cultivo,
                    "Producto": producto,
                    "Superficie (ha)": superficie,
                    "Produccion (t)": produccion,
                    "Precio Comunitat Valenciana": precio_data["COMUNITAT VALENCIANA"],
                    "Precio Alicante": precio_data["ALICANTE"],
                    "Precio Castellon": precio_data["CASTELLÓN"],
                    "Precio Valencia": precio_data["VALENCIA"],
                    "Precipitacion Ene": meteo_data["ENE"],
                    "Precipitacion Feb": meteo_data["FEB"],
                    "Precipitacion Mar": meteo_data["MAR"],
                    "Precipitacion Abr": meteo_data["ABR"],
                    "Precipitacion May": meteo_data["MAY"],
                    "Precipitacion Jun": meteo_data["JUN"],
                    "Precipitacion Jul": meteo_data["JUL"],
                    "Precipitacion Ago": meteo_data["AGO"],
                    "Precipitacion Sep": meteo_data["SEP"],
                    "Precipitacion Oct": meteo_data["OCT"],
                    "Precipitacion Nov": meteo_data["NOV"],
                    "Precipitacion Dic": meteo_data["DIC"],
                    "Precipitacion Total": meteo_data["TOTAL"],
                    "Precipitacion Media": meteo_data["MEDIA"]
                })

# 📊 Convertir a DataFrame
df = pd.DataFrame(dataset)

# 📤 Guardar el dataset final
df.to_csv("dataset_final_completo.csv", index=False, encoding="utf-8")

print("✅ Dataset con cultivos, precios y meteorología guardado como 'dataset_final_completo.csv'")
