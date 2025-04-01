# Guía de Uso - Transformación de Datos de Cosechas desde CSV a JSON

Este script permite transformar archivos CSV con datos agrícolas en formato español (coma decimal y punto para miles) a un archivo JSON estructurado, listo para análisis o integración con otras herramientas.

## Requisitos

- Python 3 instalado.
- Archivo CSV con datos de cosechas, con columnas como `2020-superficie`, `2020-produccion`, etc.

## Uso

Puedes ejecutar el script desde la terminal con los siguientes comandos:

### En sistemas con `python`:

```bash
python transformar_csv.py -i cosecha2020.csv -o limpio2020.json
```

### En sistemas con `python3`:

```bash
python3 transformar_csv.py -i cosecha2020.csv -o limpio2020.json
```

## Parámetros

- `-i`, `--input` → Ruta del archivo CSV de entrada (obligatorio).
- `-o`, `--output` → Ruta del archivo JSON de salida (obligatorio).
- `-y`, `--year` → Año a procesar (opcional). Si no se especifica, se intenta extraer automáticamente del nombre del archivo de entrada.

### Ejemplos

```bash
python transformar_csv.py -i cosecha2019.csv -o limpio2019.json
```

```bash
python3 transformar_csv.py -i datos_cosecha.csv -o salida.json -y 2021
```

## Funcionamiento

1. **Lee archivos CSV con formato español** (coma decimal, punto como separador de miles).
2. **Detecta o usa el año especificado** para seleccionar las columnas correspondientes (`{año}-superficie`, `{año}-produccion`).
3. **Elimina filas vacías o no válidas** (por ejemplo, encabezados intermedios como "CEREALES PARA GRANO").
4. **Limpia los nombres de cultivo**, eliminando espacios extra.
5. **Estructura los datos** bajo una clave `"COMUNIDAD VALENCIANA"` y guarda el resultado en formato JSON.

## Salida

El JSON generado tendrá una estructura como la siguiente:

```json
{
  "COMUNIDAD VALENCIANA": [
    {
      "CULTIVOS": "ARROZ",
      "2020-superficie": 15000.0,
      "2020-produccion": 90000.0
    },
    {
      "CULTIVOS": "TRIGO",
      "2020-superficie": 4300.0,
      "2020-produccion": 14000.0
    }
  ]
}
```

## Notas

- Asegúrate de que el archivo CSV tenga las columnas del año correspondiente.
- El script es útil para limpieza de datos previos a análisis o uso en modelos de Machine Learning.
- Si tienes problemas al ejecutarlo, verifica que Python esté correctamente instalado y accesible desde tu terminal.