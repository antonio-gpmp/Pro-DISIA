
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import matplotlib.pyplot as plt
import joblib

# Cargar y preparar los datos
df = pd.read_csv("dataset_final_completo.csv")

for col in ['Superficie (ha)', 'Produccion (t)']:
    df[col] = df[col].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)

df = df.dropna(subset=['Produccion (t)', 'Superficie (ha)'])
df = df[df['Produccion (t)'] > 0]

categorical_cols = ['Region', 'Cultivo', 'Producto']
precip_cols = [col for col in df.columns if "Precipitacion" in col]
numeric_cols = ['Superficie (ha)'] + precip_cols

X = df[categorical_cols + numeric_cols]
y = df['Produccion (t)']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown='ignore'), categorical_cols)
], remainder='passthrough')

from sklearn.linear_model import LinearRegression

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test, y_pred)

print("Regresión Lineal")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape * 100:.2f}%")

plt.figure(figsize=(6, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Producción real (t)")
plt.ylabel("Predicción (t)")
plt.title("Regresión Lineal - Real vs. Predicho")
plt.grid(True)
plt.tight_layout()
plt.show()

joblib.dump(pipeline, "modelo_regresion_lineal.pkl")
