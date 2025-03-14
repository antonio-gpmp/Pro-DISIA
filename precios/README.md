# Guía de Uso - Limpieza de Datos de Precios de Productos

Este script permite limpiar y reestructurar los datos de precios de productos, eliminando valores innecesarios, convirtiendo precios en formato numérico y organizando la información de manera estructurada.

## Requisitos
- Python 3 instalado en el sistema.
- Archivo JSON con datos de precios en el formato adecuado.

## Uso
Para ejecutar el script, utiliza el siguiente comando en la terminal:

```bash
python procesar_precios_json.py precios_2023.json limpio_precios_2023.json
```

## Parámetros
- `precios_2023.json` → Archivo de entrada con los datos sin procesar.
- `limpio_precios_2023.json` → Archivo de salida con los datos transformados.

## Funcionamiento
1. **Elimina filas vacías** del archivo original.
2. **Limpia y renombra las claves** para mayor claridad.
3. **Convierte precios a valores numéricos (float)** y reemplaza valores vacíos o guiones `-` con `0`.
4. **Guarda los datos en un formato estructurado** para su posterior análisis o uso en modelos de Machine Learning.

## Salida
El script generará un nuevo archivo JSON con los datos limpios y listos para su uso en análisis o integración con modelos predictivos.

## Notas
- Asegúrate de tener permisos adecuados para ejecutar el script y escribir archivos en el directorio de salida.
- Si el script no se ejecuta, verifica que tienes Python correctamente instalado y agregado al `PATH`.

---

¡Ahora puedes limpiar los datos de precios de productos de manera eficiente y automatizada! 🚀