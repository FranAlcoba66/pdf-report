from fastapi import FastAPI, Response
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import json
from pathlib import Path
import builtins

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates_dir = BASE_DIR / "templates"
data_file = BASE_DIR / "data" / "sample_data.json"

env = Environment(loader=FileSystemLoader(templates_dir))
# NECESARIO para que Jinja2 reconozca 'zip' y 'enumerate'
env.globals.update(zip=builtins.zip) 
env.globals.update(enumerate=builtins.enumerate) 

# FUNCIÓN CLAVE PARA CALCULAR LA POSICIÓN PORCENTUAL
def calculate_marker_position(value, min_val, max_val):
    """Calcula la posición porcentual de un valor dentro de un rango dado."""
    # Asegurar que el valor esté dentro de los límites del track visible
    clamped_value = max(min_val, min(max_val, value))
    
    range_span = max_val - min_val
    
    if range_span <= 0:
        return 50 # Retorna el centro si el rango es inválido o nulo

    adjusted_value = clamped_value - min_val
    position = (adjusted_value / range_span) * 100

    # Retorna la posición asegurando que esté entre 0 y 100
    return max(0, min(100, position))


@app.get("/")
def home():
    return {"message": "Bienvenido al generador de reportes PDF con FastAPI"}

@app.get("/report")
def generate_pdf():
    # 1️⃣ Cargar datos
    try:
        with open(data_file) as f:
            data = json.load(f)
    except Exception as e:
        return Response(content=f"Error al cargar o decodificar datos: {e}", status_code=500, media_type="text/plain")

    # 2️⃣ PROCESAMIENTO DE DATOS: Calcular la posición del marcador para CADA biomarcador
    for biomarker in data['biomarkers']:
        try:
            value = float(biomarker['value'])
            min_val = float(biomarker['min_range_value'])
            max_val = float(biomarker['max_range_value'])
            
            position = calculate_marker_position(value, min_val, max_val)
            # Guardamos la posición calculada en el diccionario de datos
            biomarker['position'] = round(position, 2) 
        except (ValueError, TypeError, KeyError) as e:
            # En caso de datos faltantes o incorrectos, establece una posición por defecto
            biomarker['position'] = 50 

    # 3️⃣ Renderizar HTML con Jinja2
    template = env.get_template("report2.html")
    # Es crucial usar base_url para que WeasyPrint encuentre el CSS y los archivos locales
    base_uri = str(BASE_DIR.as_uri()) + '/'
    html_content = template.render(data=data, base_url=base_uri)

    # 4️⃣ Convertir a PDF con WeasyPrint
    pdf = HTML(string=html_content, base_url=base_uri).write_pdf()

    # 5️⃣ Devolver como respuesta HTTP
    headers = {"Content-Disposition": "inline; filename=report.pdf"}
    return Response(content=pdf, media_type="application/pdf", headers=headers)