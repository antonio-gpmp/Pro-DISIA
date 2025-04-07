import pandas as pd
import joblib

# Datos del olivo (puedes ajustar valores)
datos_nuevos = pd.DataFrame([{
    'Region': 'CASTELLON',
    'Cultivo': 'MANZANA',
    'Producto': 'MANZANA CONSUMO FRESCO',
    'Superficie (ha)': 100.0,
    'Precipitacion Ene': 30.0,
    'Precipitacion Feb': 30.0,
    'Precipitacion Mar': 30.0,
    'Precipitacion Abr': 30.0,
    'Precipitacion May': 30.0,
    'Precipitacion Jun': 30.0,
    'Precipitacion Jul': 0.0,
    'Precipitacion Ago': 0.0,
    'Precipitacion Sep': 30.0,
    'Precipitacion Oct': 30.0,
    'Precipitacion Nov': 30.0,
    'Precipitacion Dic': 30.0,
    'Precipitacion Media': 400.0,
    'Precipitacion Total': 300.0
}])

# Cargar el modelo previamente entrenado
modelo = joblib.load("modelo_random_forest.pkl")

# Predecir
prediccion = modelo.predict(datos_nuevos)

# Mostrar resultado
print(f"Producción estimada de aceite: {prediccion[0]:,.2f} toneladas")
