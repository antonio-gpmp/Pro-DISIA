import os
import subprocess

# Función para ejecutar scripts individuales
def ejecutar_script(script, input_file, output_file):
    try:
        subprocess.run(["python3", script, input_file, output_file], check=True)
        print(f"✅ Procesado {input_file} → {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error procesando {input_file}: {e}")

# Directorios de datos
directorios = {
    "cosecha": "./cosecha/",
    "meteo": "./meteo/",
    "precios": "./precios/"
}

# Scripts correspondientes
scripts = {
    "cosecha": "./cosecha/transform_cosecha.py",
    "meteo": "./meteo/transform_precipitation.py",
    "precios": "./precios/transform_precios.py"
}

# Procesamiento de archivos JSON
for categoria, ruta_dir in directorios.items():
    archivos = [f for f in os.listdir(ruta_dir) if f.endswith('.json') and not f.startswith('limpio_')]
    script = scripts[categoria]

    for archivo in archivos:
        input_path = os.path.join(ruta_dir, archivo)

        # Determinar el nombre del archivo limpio según la categoría
        if categoria == 'cosecha':
            output_name = f"limpio_{archivo}"
        elif categoria == "meteo":
            año = archivo.split('-')[1].split('.')[0]
            año_completo = f"20{año}"
            output_name = f"limpio_precipitaciones_{año_completo}.json"
        elif categoria == "precios":
            año_completo = archivo.split('_')[1].split('.')[0]
            output_name = f"limpio_precios_{año_completo}.json"

        output_path = os.path.join(ruta_dir, output_name)

        ejecutar_script(script, input_path, output_path)

# Finalmente ejecutar script para dataset completo
try:
    subprocess.run(["python3", "transform_final.py"], check=True)
    print("✅ Generado dataset completo con éxito.")
except subprocess.CalledProcessError as e:
    print(f"❌ Error al ejecutar transform_final.py: {e}")