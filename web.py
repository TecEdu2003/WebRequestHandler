from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

# Abre el archivo HTML y lee su contenido
with open('home.html', 'r', encoding='utf-8') as file:
    html_home = file.read()
with open('1.html', 'r', encoding='utf-8') as file:
    html_1 = file.read()

# Crea el diccionario y almacena el contenido del HTML en una clave
diccionario = {
    #Página Home, lee el contenido del archivo home.html
    '/': html_home ,
    #Página 1, lee el contenido del archivo 1.html
    '/proyecto/1': html_1,
    #Página 2, contiene hipervínculos para acceder las demás páginas
    '/proyecto/2': f"""<html><h3><a href="/"> Home </a></h3>
    <h3><a href="/proyecto/1"> Proyecto 1 </a></h3>
    <h3><a href="/proyecto/3"> Proyecto 3</a></h3></html>""",
    #Página 3, contiene hipervínculos para acceder las demás páginas
    '/proyecto/3':f"""<html><h3><a href="/"> Home </a></h3>
    <h3><a href="/proyecto/1"> Proyecto 1 </a></h3>
    <h3><a href="/proyecto/2"> Proyecto 2</a></h3></html>""",
}

class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        host = self.headers.get('Host')
        user_agent = self.headers.get('User-Agent')
        path = self.path
        
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Server", "CustomPythonServer/1.0")
        self.send_header("Date", self.date_time_string())
        self.end_headers()
        
        #Ahora usamos el diccionario para reflejar el contenido de las direcciones, en caso de que no exista muestra  el Error 404
        response_content = diccionario.get(self.path, "<html><h1>404 Not Found</h1></html>")
        self.wfile.write(response_content.encode("utf-8")) 

        
 
            
if __name__ == "__main__":
    puerto = 8000
    print("Starting server on port {puerto}")
    server = HTTPServer(("localhost", puerto), WebRequestHandler)
    server.serve_forever()
