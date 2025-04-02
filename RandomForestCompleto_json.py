
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import joblib

# Cargar datos desde el JSON
df = pd.read_json("dataset_final_completo.json")

# Limpieza de columnas numéricas
def limpiar_valores_numericos(valor):
    if isinstance(valor, str):
        valor = valor.strip().replace(".", "").replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            return None
    return valor

for col in ['Superficie (ha)', 'Produccion (t)']:
    df[col] = df[col].apply(limpiar_valores_numericos)

df = df.dropna(subset=['Produccion (t)', 'Superficie (ha)'])
df = df[df['Produccion (t)'] > 0]

# Selección de variables
categorical_cols = ['Region', 'Cultivo', 'Producto']
precip_cols = [col for col in df.columns if "Precipitacion" in col and col not in ['Precipitacion Total', 'Precipitacion Media']]
numeric_cols = ['Superficie (ha)'] + precip_cols

X = df[categorical_cols + numeric_cols]
y = df['Produccion (t)']

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Preprocesador y modelo
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown='ignore'), categorical_cols)
], remainder='passthrough')

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

# Métricas
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test, y_pred)

print("Random Forest")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape * 100:.2f}%")

# Gráfico
plt.figure(figsize=(6, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Producción real (t)")
plt.ylabel("Predicción (t)")
plt.title("Random Forest - Real vs. Predicho")
plt.grid(True)
plt.tight_layout()
plt.show()

# Guardar modelo
joblib.dump(pipeline, "modelo_random_forest.pkl")
