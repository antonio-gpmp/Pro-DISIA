
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

from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", XGBRegressor(random_state=42))
])

param_grid = {
    'regressor__n_estimators': [100, 150],
    'regressor__learning_rate': [0.05, 0.1],
    'regressor__max_depth': [4, 6]
}

grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='neg_root_mean_squared_error', verbose=1)
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test, y_pred)

print("XGBoost optimizado")
print(grid_search.best_params_)
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape * 100:.2f}%")

plt.figure(figsize=(6, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Producción real (t)")
plt.ylabel("Predicción (t)")
plt.title("XGBoost optimizado - Real vs. Predicho")
plt.grid(True)
plt.tight_layout()
plt.show()

joblib.dump(best_model, "modelo_xgboost_optimizado.pkl")
