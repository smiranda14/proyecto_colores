import os
import re
import math
import pandas as pd
from PIL import Image
from google.cloud import vision

# === CONFIGURACIÓN GOOGLE VISION ===
client = vision.ImageAnnotatorClient()

# === PALETA DE COLORES ESTÁNDAR ===
PALETA_COLORES = {
    "negro": "#000000", "blanco": "#FFFFFF", "rojo": "#E10600", "azul": "#0057FF",
    "verde": "#0BB34C", "amarillo": "#FFC300", "celeste": "#7FDBFF", "gris": "#9E9E9E",
    "chocolate": "#5C3317", "naranja": "#FF6A00", "rosado": "#FF6FA5",
    "morado": "#7A3E9D", "crema": "#F5E8C7", "multicolor": "#808080"
}

# === FUNCIONES DE COLOR ===
def hex_a_rgb(h):
    return tuple(int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def distancia(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

def color_cercano(rgb):
    return min(PALETA_COLORES, key=lambda k: distancia(rgb, hex_a_rgb(PALETA_COLORES[k])))

def rgb_a_hex(rgb):
    return '#%02x%02x%02x' % rgb

# === DETECCIÓN DE COLOR CON IA GOOGLE VISION ===
def obtener_color_principal_vision(ruta):
    """Usa Google Vision API para obtener el color dominante."""
    with open(ruta, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.image_properties(image=image)
    colors = response.image_properties_annotation.dominant_colors.colors

    if not colors:
        return (128, 128, 128)  # gris neutro

    color = colors[0].color
    rgb = (int(color.red), int(color.green), int(color.blue))
    return rgb

# === LIMPIEZA DE NOMBRES ===
def aplicar_patron(base, patron):
    if patron == "limpieza_nike":
        if base.upper().startswith("AURORA_"):
            base = base[8:]
        base = base.replace(" ", "")
        base = re.sub(r"-{2,}", "-", base).strip("-")

    elif patron == "limpieza_adidas":
        if "_" in base:
            ref, resto = base.split("_", 1)
        else:
            ref, resto = base, ""
        resto = re.sub(r'_[0-9]+_', '_', resto)
        resto = re.sub(r'_[0-9]+', '', resto)
        resto = re.sub(r'(?i)Photography', '', resto)
        resto = re.sub(r'(?i)_?white', '', resto)
        resto = resto.replace(" ", "-").replace("_", "-")
        resto = re.sub(r"-{2,}", "-", resto).strip("-")
        base = f"{ref}_{resto}" if resto else ref

    else:
        base = base.strip().replace(" ", "-").replace("_", "-")
        base = re.sub(r"-{2,}", "-", base).strip("-")

    return base.strip().upper()

# === LIMPIEZA FINAL ===
def limpiar_nombre(filename, marca, reglas_df):
    base, _ = os.path.splitext(filename)
    base = base.strip()
    regla = reglas_df[reglas_df["MARCA"].str.upper() == marca.upper()]
    if regla.empty:
        regla = reglas_df[reglas_df["MARCA"].str.upper() == "GENERICO"]
    if regla.empty:
        return base + ".jpg"

    patron = str(regla.iloc[0].get("PATRON_CLEAN", "") or "")
    mayus = str(regla.iloc[0].get("MAYUSCULA", "")).upper() == "TRUE"
    formato_final = str(regla.iloc[0].get("FORMATO_FINAL", "{filename}.jpg") or "{filename}.jpg")

    base = aplicar_patron(base, patron)
    if mayus:
        base = base.upper()

    nuevo_nombre = formato_final.replace("{filename}", base)
    if not nuevo_nombre.lower().endswith(".jpg"):
        nuevo_nombre += ".jpg"
    return nuevo_nombre

# === PROCESAMIENTO PRINCIPAL ===
def procesar(input_dir, output_dir, output_imgs, reglas_path):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_imgs, exist_ok=True)

    reglas_df = pd.read_excel(reglas_path)
    registros = []

    for marca in os.listdir(input_dir):
        marca_path = os.path.join(input_dir, marca)
        if not os.path.isdir(marca_path):
            continue

        print(f"🔹 Procesando {marca}...")

        # Crear subcarpeta para la marca dentro de output_formateadas
        out_marca = os.path.join(output_imgs, marca)
        os.makedirs(out_marca, exist_ok=True)

        for file in os.listdir(marca_path):
            if not file.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            ruta = os.path.join(marca_path, file)
            try:
                nombre_final = limpiar_nombre(file, marca, reglas_df)
                ruta_guardado = os.path.join(out_marca, nombre_final)

                # Convertir a JPG (RGB)
                img = Image.open(ruta)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(ruta_guardado, "JPEG", quality=90)

                # Color con Google Vision
                rgb = obtener_color_principal_vision(ruta_guardado)
                hex_dom = rgb_a_hex(rgb)
                col_std = color_cercano(rgb)

                registros.append({
                    "marca": marca,
                    "archivo_original": file,
                    "archivo_final": nombre_final,
                    "color_dominante": hex_dom,
                    "color_estandar": col_std,
                    "ruta_guardado": ruta_guardado,
                    "estado": "OK"
                })

            except Exception as e:
                registros.append({
                    "marca": marca,
                    "archivo_original": file,
                    "estado": f"Error: {str(e)}"
                })

    df = pd.DataFrame(registros)
    df.to_excel(os.path.join(output_dir, "reporte_colores_final.xlsx"), index=False)
    print("\n✅ Proceso completado y reporte exportado con éxito.")
    print("📁 Imágenes formateadas guardadas en subcarpetas dentro de:", output_imgs)

# === EJECUCIÓN ===
if __name__ == "__main__":
    procesar(
        "G:/Mi unidad/proyecto_colores/input_imagenes",
        "G:/Mi unidad/proyecto_colores/output_reportes",
        "G:/Mi unidad/proyecto_colores/output_formateadas",
        "G:/Mi unidad/proyecto_colores/reglas_imagenes.xlsx"
    )
