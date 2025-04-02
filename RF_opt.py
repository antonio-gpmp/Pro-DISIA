import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error,
    mean_absolute_percentage_error, r2_score
)

# 📥 Cargar datos JSON
with open("dataset_final_completo.json", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)

# 🧹 Filtrar outliers extremos
df = df[df["Produccion (t)"] > 100]

# 📊 Variables
cat_cols = ["Region", "Cultivo", "Producto"]
num_cols = ["Superficie (ha)", "Precipitacion Total"]
target = "Produccion (t)"
X = df[cat_cols + num_cols]
y = df[target]

# ⚙️ Preprocesamiento
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ("num", StandardScaler(), num_cols)
])

# 🔁 Pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])

# 🧪 División del dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔍 Búsqueda de hiperparámetros
param_grid = {
    "regressor__n_estimators": [100, 200, 300],
    "regressor__max_depth": [10, 15, 20],
    "regressor__min_samples_split": [2, 5],
    "regressor__min_samples_leaf": [1, 2]
}

grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring="neg_mean_absolute_error", verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)

# 🏆 Mejor modelo
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# 📈 Métricas
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test, y_pred) * 100
r2 = r2_score(y_test, y_pred)

print("\nRandom Forest - Optimizado (JSON)")
print("Mejores hiperparámetros:", grid_search.best_params_)
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")
print(f"R²: {r2:.4f}")

# 💾 Guardar modelo
joblib.dump(best_model, "random_forest_model.pkl")
print("✅ Modelo guardado en 'random_forest_model.pkl'")

# 📊 Gráfico Real vs Predicho
plt.figure(figsize=(8, 8))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
plt.xlabel("Producción Real (t)")
plt.ylabel("Producción Predicha (t)")
plt.title("🎯 Real vs Predicho")
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_real_vs_predicho.png")
print("📊 Gráfico guardado como 'grafico_real_vs_predicho.png'")
plt.close()

# 📉 Histograma de errores
residuals = y_test - y_pred
plt.figure(figsize=(8, 5))
plt.hist(residuals, bins=30, edgecolor="black")
plt.title("📉 Histograma de errores (residuos)")
plt.xlabel("Error (Real - Predicho)")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("histograma_residuos.png")
print("📉 Histograma guardado como 'histograma_residuos.png'")
plt.close()

# 🧠 Importancia de características
importances = best_model.named_steps["regressor"].feature_importances_
feature_names = best_model.named_steps["preprocessor"].get_feature_names_out()
feat_imp_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
feat_imp_df = feat_imp_df.sort_values("Importance", ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(feat_imp_df["Feature"][:15][::-1], feat_imp_df["Importance"][:15][::-1])
plt.xlabel("Importancia")
plt.title("💡 Top 15 Características más importantes")
plt.tight_layout()
plt.savefig("importancia_caracteristicas.png")
print("📌 Gráfico de importancia guardado como 'importancia_caracteristicas.png'")
plt.close()
