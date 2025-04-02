import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import json
import joblib

# Cargar JSON
with open("dataset_final_completo.json", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)

# Filtrado de outliers obvios
df = df[(df['Produccion (t)'] > 100) & (df['Superficie (ha)'] > 0)]

# Agregar precipitación total
df['Precipitacion Total'] = df[[
    'Precipitacion Ene', 'Precipitacion Feb', 'Precipitacion Mar', 'Precipitacion Abr',
    'Precipitacion May', 'Precipitacion Jun', 'Precipitacion Jul', 'Precipitacion Ago',
    'Precipitacion Sep', 'Precipitacion Oct', 'Precipitacion Nov', 'Precipitacion Dic']].sum(axis=1)

# Variables
cat_cols = ["Region", "Cultivo", "Producto"]
num_cols = ['Superficie (ha)', 'Precipitacion Total']
target = 'Produccion (t)'

X = df[cat_cols + num_cols]
y = df[target]

# Preprocesamiento
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", StandardScaler(), num_cols)
    ]
)

# Pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])

# Hiperparámetros a explorar
param_grid = {
    'regressor__n_estimators': [100, 200, 300],
    'regressor__max_depth': [10, 20, 30, None],
    'regressor__min_samples_split': [2, 5],
    'regressor__min_samples_leaf': [1, 2]
}

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Grid search
grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='neg_mean_absolute_error', verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Mejor modelo
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# Métricas
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test[y_test > 0], y_pred[y_test > 0]) * 100

print("\nRandom Forest - Optimizado (JSON)")
print("Mejores hiperparámetros:", grid_search.best_params_)
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")

# Guardar modelo
joblib.dump(best_model, "random_forest_model.pkl")
print("\n✅ Modelo guardado en 'random_forest_model.pkl'")

# Gráfico Real vs Predicho
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6, edgecolors='k')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel("Valor Real")
plt.ylabel("Valor Predicho")
plt.title("Random Forest - Valor Real vs Predicho")
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_real_vs_predicho.png")
plt.show()
print("📊 Gráfico guardado como 'grafico_real_vs_predicho.png'")