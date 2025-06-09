import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Ruta a la carpeta con imágenes
ruta_carpeta = r'img\frames'

# Recorre todos los archivos en la carpeta
for nombre_archivo in os.listdir(ruta_carpeta):
    ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)

    # Verifica si el archivo es una imagen
    if nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        try:
            imagen = mpimg.imread(ruta_completa)
            print(f"{nombre_archivo}: shape = {imagen.shape}")
        except Exception as e:
            print(f"{nombre_archivo}: Error al leer la imagen ({e})")
