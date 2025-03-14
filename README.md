# Pro-DISIA
Trabajo de la asignatura DISIA del MUII de la UCLM


# Guía de Uso - Generación del Dataset Final

Este script permite consolidar los datos de **cosechas, precios y meteorología** en un único dataset estructurado en formato CSV, listo para ser utilizado en entrenamientos de modelos de Machine Learning o análisis de datos.

## Requisitos
- **Python 3** instalado en el sistema.
- Archivos JSON limpios de:
  - **Cosechas** (`./cosecha/limpio_cosechaYYYY.json`)
  - **Precios** (`./precios/limpio_precios_YYYY.json`)
  - **Meteorología** (`./meteo/limpio_precipitaciones_YYYY.json`)

## Uso
Para ejecutar el script y generar el dataset final, utiliza el siguiente comando:


### En sistemas con `python`:
```bash
python transform_final.py
```

### En sistemas con `python3`:
```bash
python3 transform_final.py
```

## Funcionamiento
1. **Carga los datos de cosechas, precios y meteorología** desde archivos JSON para los años 2018-2023.
2. **Relaciona los cultivos con los productos de mercado** mediante un mapeo predefinido.
3. **Une la información por región y año**, combinando:
   - **Superficie cultivada**
   - **Producción agrícola**
   - **Precios del mercado** (por provincia)
   - **Precipitaciones mensuales y anuales**
4. **Genera un archivo CSV estructurado** con todos los datos fusionados.

## Salida
El script generará un archivo **`dataset_final_completo.csv`** que contiene la información consolidada y lista para su uso en análisis o entrenamiento de modelos.

## Notas
- Asegúrate de que los archivos JSON de entrada están en las carpetas correspondientes (`./cosecha/`, `./precios/`, `./meteo/`).
- Si el script no se ejecuta, verifica que Python 3 está correctamente instalado y agregado al `PATH`.
- Puedes modificar el script para incluir nuevos años si es necesario.
