import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import matplotlib.pyplot as plt
import joblib

# 📥 Cargar JSON
with open("dataset_final_completo.json", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)

# 🔢 Columnas categóricas y numéricas
cat_cols = ["Region", "Cultivo", "Producto"]
num_cols = [
    'Superficie (ha)',
    'Precipitacion Ene', 'Precipitacion Feb', 'Precipitacion Mar', 'Precipitacion Abr',
    'Precipitacion May', 'Precipitacion Jun', 'Precipitacion Jul', 'Precipitacion Ago',
    'Precipitacion Sep', 'Precipitacion Oct', 'Precipitacion Nov', 'Precipitacion Dic'
]

# 🎯 Variable objetivo
target = 'Produccion (t)'

X = df[cat_cols + num_cols]
y = df[target]

# 🔄 Preprocesamiento
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", "passthrough", num_cols)
    ]
)

# 🔧 Pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])

# 🔍 Grid de hiperparámetros
param_grid = {
    'regressor__n_estimators': [100, 200, 300],
    'regressor__max_depth': [10, 20, 30, None],
    'regressor__min_samples_split': [2, 5, 10],
    'regressor__min_samples_leaf': [1, 2, 4]
}

# ✂️ División del dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔍 Búsqueda de hiperparámetros
grid_search = GridSearchCV(model, param_grid, cv=3, scoring='neg_mean_absolute_error', verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)

# ✅ Modelo final
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# 📊 Métricas
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# ⚠️ Evitar divisiones por cero en MAPE
non_zero_idx = y_test != 0
mape = mean_absolute_percentage_error(y_test[non_zero_idx], y_pred[non_zero_idx]) * 100

print("\nRandom Forest Optimizado (JSON)")
print("Mejores hiperparámetros:", grid_search.best_params_)
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")

# 📈 Visualización
plt.figure(figsize=(10,6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r')
plt.xlabel("Producción Real (t)")
plt.ylabel("Producción Predicha (t)")
plt.title("Random Forest - Real vs Predicho")
plt.grid(True)
plt.tight_layout()
plt.show()

# 💾 Guardar modelo
joblib.dump(best_model, "modelo_random_forest_opt.pkl")
print("✅ Modelo guardado como modelo_random_forest_opt.pkl")
