import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import numpy as np

# === Cargar JSON ===
with open("dataset_final_completo.json", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)

# === Ingeniería de características ===
# Crear columna de precipitacion total anual
df['Precipitacion Total'] = df[[
    'Precipitacion Ene', 'Precipitacion Feb', 'Precipitacion Mar', 'Precipitacion Abr',
    'Precipitacion May', 'Precipitacion Jun', 'Precipitacion Jul', 'Precipitacion Ago',
    'Precipitacion Sep', 'Precipitacion Oct', 'Precipitacion Nov', 'Precipitacion Dic']].sum(axis=1)

# === Visualización ===
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Precipitacion Total', y='Produccion (t)', hue='Cultivo')
plt.title('Relación entre precipitación total y producción')
plt.xlabel('Precipitación Total (mm)')
plt.ylabel('Producción (t)')
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# === Modelo simplificado ===
cat_cols = ["Region", "Cultivo", "Producto"]
num_cols = ["Superficie (ha)", "Precipitacion Total"]
target = "Produccion (t)"

X = df[cat_cols + num_cols]
y = df[target]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", "passthrough", num_cols)
    ]
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=200, max_depth=30, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test, y_pred) * 100

print("\nRandom Forest - Solo superficie + precipitacion")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")

# === Importancia de características ===
importances = model.named_steps["regressor"].feature_importances_
features = model.named_steps["preprocessor"].get_feature_names_out()

sorted_importances = sorted(zip(importances, features), reverse=True)
print("\nImportancia de características:")
for score, name in sorted_importances[:10]:
    print(f"{name}: {score:.4f}")
