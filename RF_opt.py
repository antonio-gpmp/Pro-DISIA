import pandas as pd
import numpy as np
import json
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# Cargar JSON
with open("dataset_final_completo.json", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)

# Filtrado de outliers (opcional y ajustable)
df = df[(df['Superficie (ha)'] > 0) & (df['Produccion (t)'] > 100)]

# Columnas categóricas y numéricas
cat_cols = ["Region", "Cultivo", "Producto"]
num_cols = ['Superficie (ha)',
            'Precipitacion Ene', 'Precipitacion Feb', 'Precipitacion Mar', 'Precipitacion Abr',
            'Precipitacion May', 'Precipitacion Jun', 'Precipitacion Jul', 'Precipitacion Ago',
            'Precipitacion Sep', 'Precipitacion Oct', 'Precipitacion Nov', 'Precipitacion Dic']

# Añadir columna de precipitaciones totales
df['Precipitacion Total'] = df[[col for col in num_cols if 'Precipitacion' in col]].sum(axis=1)
num_cols = ['Superficie (ha)', 'Precipitacion Total']

# Target
target = 'Produccion (t)'
X = df[cat_cols + num_cols]
y = df[target]

# Preprocesamiento
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ("num", StandardScaler(), num_cols)
])

# Pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])

# Hiperparámetros optimizados previamente o ajustables
param_grid = {
    'regressor__n_estimators': [200],
    'regressor__max_depth': [30],
    'regressor__min_samples_split': [2],
    'regressor__min_samples_leaf': [1]
}

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Grid Search
grid_search = GridSearchCV(model, param_grid, cv=3, scoring='neg_mean_absolute_error', verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Mejor modelo
best_model = grid_search.best_estimator_
joblib.dump(best_model, "random_forest_model.pkl")

# Predicción
y_pred = best_model.predict(X_test)

# Métricas
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test, y_pred[y_test != 0]) * 100  # evita división por 0

print("\nRandom Forest - Solo superficie + precipitacion")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")

# Importancia de características
feature_names = (
    best_model.named_steps['preprocessor']
    .transformers_[0][1]
    .get_feature_names_out(cat_cols)
    .tolist() + num_cols
)
importances = best_model.named_steps['regressor'].feature_importances_
sorted_indices = np.argsort(importances)[::-1]

plt.figure(figsize=(12, 6))
plt.title("Importancia de características")
plt.bar(range(len(importances)), importances[sorted_indices], align="center")
plt.xticks(range(len(importances)), [feature_names[i] for i in sorted_indices], rotation=90)
plt.tight_layout()
plt.show()
