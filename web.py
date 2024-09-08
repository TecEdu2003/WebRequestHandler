from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


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
        self.wfile.write(self.get_response(host, user_agent, path).encode("utf-8"))

    def get_response(self,host, user_agent, path):
        query = self.query_data()
        # Extraer la parte antes del '?'
        path_without_query = path.split('?')[0]
        
        # Extraer la parte después del último '/'
        if path_without_query.startswith("/proyecto/"):
            proyecto = path_without_query.split('/')[-1]
            # Obtener el parámetro 'autor' de la query string
            autor = query.get('autor', 'Desconocido')
            return f"<h1>Proyecto: {proyecto} Autor: {autor}</h1>"
        elif path == '/' and not None:
            try:
                with open('home.html', 'r') as file:
                    return file.read()
            except FileNotFoundError:
                return "<h1>Error 404: Página no encontrada</h1>"
        else:
            return f"<h1>Error 404: Página no encontrada</h1>"

            #return f"""
            #<h1> Hola Web </h1>
            #<p> URL Parse Result : {self.url()}         </p>
            #<p> Path Original: {self.path}         </p>
            #<p> Headers: {self.headers}      </p>
            #<p> Query: {self.query_data()}   </p>
            #<h1>Ruta Solicitada: {path}</h1>
            #<p>Host: {host}</p>
            #<p>User-Agent: {user_agent}</p>
         


if __name__ == "__main__":
    puerto = 8000
    print("Starting server on port {puerto}")
    server = HTTPServer(("localhost", puerto), WebRequestHandler)
    server.serve_forever()
