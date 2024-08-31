from livereload import Server, shell

server = Server()

ruta_absoluta = r'C:\Users\Patricio\Documents\Clases Video\Directos\personalizacion\SubsTwitch2'
# Observa los archivos HTML, CSS y JS
server.watch(ruta_absoluta+'\index.html')
server.watch(ruta_absoluta+'\script.js')
server.watch(ruta_absoluta+'\style.css')
server.watch(ruta_absoluta+'\bits.json')
server.watch(ruta_absoluta+'\suscriptores.json')

# Ejecuta el servidor en el puerto 8765
server.serve(root=ruta_absoluta, port=8765)
