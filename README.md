# 🧠 Automatización de imágenes con Python y Google Vision AI 🐍

Este proyecto automatiza el proceso de **limpieza, renombrado y detección de color** en imágenes e-commerce.  
Fue desarrollado como parte de una iniciativa para optimizar la gestión de activos digitales y reducir tareas repetitivas en el flujo de carga de productos.

---

## 🚀 Objetivo del proyecto
Transformar un proceso manual y propenso a errores en un flujo **automatizado, escalable y conectado a la nube**, integrando:
- **Python** como motor principal de automatización.
- **Google Drive API** como sistema de almacenamiento y gestión de archivos.
- **Google Cloud Vision AI** para la detección inteligente de color y análisis visual.

---

## ⚙️ Flujo general
1️⃣ Carpeta origen en Google Drive
↓
2️⃣ Conexión con la API de Drive (descarga automatizada)
↓
3️⃣ Limpieza de nombres y estandarización (regex por marca)
↓
4️⃣ Análisis visual con Vision AI (color y etiquetas)
↓
5️⃣ Clasificación automática por marca/categoría
↓
6️⃣ Subida de archivos procesados a Drive
↓
7️⃣ Generación de reporte en CSV / Excel

## 🧰 Requisitos
- Python 3.9+
- Instalar dependencias:
```bash
pip install -r requirements.txt

requirements.txt:
pandas
pillow
colorthief
google-api-python-client
google-auth
google-auth-oauthlib
google-auth-httplib2
google-cloud-vision
qrcode

▶️ Ejecución

Configura las credenciales de Google Cloud (Drive + Vision).
Ejecuta: python main_color_detector_v2.py

💡 Tecnologías

Python · Google Drive API · Google Vision AI · Pandas · Pillow

📊 Ejemplo

| Original                                                         | Resultado                                    |
| ---------------------------------------------------------------- | -------------------------------------------- |
| JR8598_1_FOOTWEAR_Photography_Side Lateral Center View_white.jpg | JR8598_FOOTWEAR-SIDE-LATERAL-CENTER-VIEW.jpg |

Desarrollado por: Stefanía M.
Python e IA al servicio de la automatización en e-commerce.






