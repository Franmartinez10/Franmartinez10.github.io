import os
import unicodedata

def crear_slug(texto):
    """Crea una cadena de texto amigable para URLs a partir de un texto."""
    # Normaliza a NFD para separar letras y tildes
    texto = unicodedata.normalize('NFD', texto)
    # Codifica a ASCII ignorando los caracteres que no se pueden convertir (tildes)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    # Convierte a minúsculas
    texto = texto.lower()
    # Reemplaza espacios y otros caracteres no alfanuméricos por guiones
    texto = ''.join(c if c.isalnum() else '-' for c in texto)
    # Elimina guiones múltiples
    while '--' in texto:
        texto = texto.replace('--', '-')
    # Elimina guiones al principio y al final
    texto = texto.strip('-')
    return texto

def generar_paginas():
    """Función principal que lee las frases y genera los archivos HTML."""
    # 1. Crear la carpeta de salida si no existe
    if not os.path.exists('frases'):
        os.makedirs('frases')

    # 2. Leer todas las frases del archivo
    try:
        with open('frases.txt', 'r', encoding='utf-8') as f:
            frases = [line.strip() for line in f if line.strip()]
        if not frases:
            print("❌ ERROR: El archivo 'frases.txt' está vacío. Añade algunas frases.")
            return
    except FileNotFoundError:
        print("❌ ERROR: No se encontró el archivo 'frases.txt'. Asegúrate de que existe en la misma carpeta.")
        return

    # 3. Leer la plantilla HTML
    try:
        with open('plantilla.html', 'r', encoding='utf-8') as f:
            plantilla = f.read()
    except FileNotFoundError:
        print("❌ ERROR: No se encontró el archivo 'plantilla.html'.")
        return

    # 4. Generar una página para cada frase
    total_frases = len(frases)
    for i, frase_actual in enumerate(frases):
        
        # Crear un nombre de archivo amigable para SEO (slug)
        slug = crear_slug(frase_actual)
        nombre_archivo = f"{i+1}-{slug[:60]}.html"

        # Determinar el link anterior y siguiente
        if i > 0:
            slug_anterior = crear_slug(frases[i-1])
            link_anterior = f"{i}-{slug_anterior[:60]}.html"
        else:
            link_anterior = "../index.html"  # Vuelve al inicio si es la primera

        if i < total_frases - 1:
            slug_siguiente = crear_slug(frases[i+1])
            link_siguiente = f"{i+2}-{slug_siguiente[:60]}.html"
        else:
            link_siguiente = "../index.html"  # Vuelve al inicio si es la última

        # Reemplazar los marcadores en la plantilla
        contenido_final = plantilla.replace('{{TITULO_FRASE}}', f'Yo Nunca Nunca: {frase_actual}')
        contenido_final = contenido_final.replace('{{FRASE_CONTENIDO}}', frase_actual)
        contenido_final = contenido_final.replace('{{LINK_ANTERIOR}}', link_anterior)
        contenido_final = contenido_final.replace('{{LINK_SIGUIENTE}}', link_siguiente)

        # Escribir el nuevo archivo HTML en la carpeta 'frases'
        with open(os.path.join('frases', nombre_archivo), 'w', encoding='utf-8') as f:
            f.write(contenido_final)

        print(f"✅ Página creada: {nombre_archivo}")

    print(f"\n🚀 ¡Proceso completado! Se han generado {total_frases} páginas en la carpeta /frases.")

# Ejecución del script
if __name__ == '__main__':
    generar_paginas()