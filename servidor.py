import os

# Ruta absoluta donde se encuentra el archivo index.html
ruta_absoluta = r'C:\Users\Patricio\Documents\Clases Video\Directos\personalizacion\SubsTwitch2'

# Cambiar al directorio donde está el index.html
os.chdir(ruta_absoluta)

# Iniciar un servidor HTTP en el puerto 8765
os.system('python -m http.server 8765')