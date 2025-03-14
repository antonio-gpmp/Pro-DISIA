# Guía de Uso - Limpieza de Datos de Cosechas

Este script permite limpiar y reestructurar los datos de cosechas, extrayendo la información más reciente disponible y organizándola en un formato adecuado para su análisis.

## Requisitos
- Python 3 instalado en el sistema.
- Archivo JSON con datos de cosechas en el formato adecuado.

## Uso
Para ejecutar el script, utiliza el siguiente comando en la terminal:

```bash
python transform_cosecha.py cosecha2023.json limpio_cosecha2023.json
```

```bash
python3 transform_cosecha.py cosecha2023.json limpio_cosecha2023.json
```

## Parámetros
- `cosecha2023.json` → Archivo de entrada con los datos sin procesar.
- `limpio_cosecha2023.json` → Archivo de salida con los datos transformados.

## Funcionamiento
1. **Convierte el JSON de lista a diccionario** si es necesario.
2. **Elimina valores innecesarios** y extrae solo los datos del año más reciente disponible.
3. **Mantiene solo las claves esenciales**: 
   - Nombre del cultivo.
   - Superficie cultivada.
   - Producción registrada.
4. **Guarda los datos en un formato estructurado** para su posterior análisis o uso en modelos predictivos.

## Salida
El script generará un nuevo archivo JSON con los datos de cosechas limpios y listos para ser utilizados en análisis o integración con modelos de Machine Learning.

## Notas
- Asegúrate de tener permisos adecuados para ejecutar el script y escribir archivos en el directorio de salida.
- Si el script no se ejecuta, verifica que tienes Python correctamente instalado y agregado al `PATH`.