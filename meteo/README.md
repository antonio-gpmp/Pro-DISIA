# Guía de Uso - Limpieza de Datos Meteorológicos

Este script permite limpiar y reestructurar los datos meteorológicos de precipitaciones, convirtiendo valores de texto en números y organizando la información en un formato más manejable.

## Requisitos
- Python 3 instalado en el sistema.
- Archivo JSON con datos de precipitaciones en el formato adecuado.

## Uso
Para ejecutar el script, utiliza uno de los siguientes comandos según la versión de Python instalada en tu sistema:

### En sistemas con `python3`:
```bash
python3 convert_precipitation.py precipitaciones-22.json limpio_precipitaciones-22.json
```

### En sistemas con `python`:
```bash
python convert_precipitation.py precipitaciones-22.json limpio_precipitaciones-22.json
```

## Parámetros
- `precipitaciones-22.json` → Archivo de entrada con los datos sin procesar.
- `limpio_precipitaciones-22.json` → Archivo de salida con los datos transformados.

## Funcionamiento
1. Convierte valores de texto a formato numérico (float/int).
2. Reestructura los datos agrupando por observatorio.
3. Agrega la unidad de medida (`"Unidad": "l/m2"`) si no está presente.
4. Guarda el archivo transformado con el nombre especificado.

## Salida
El script generará un nuevo archivo JSON con los datos limpios y estructurados, listo para ser utilizado en análisis o modelos de Machine Learning.

## Notas
- Asegúrate de tener los permisos adecuados para ejecutar el script.
- Si el script no se ejecuta, verifica que tienes Python correctamente instalado y agregado al `PATH`.

