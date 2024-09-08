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
        contenido = {
            '/': f"""<html>
            <h1> Hola Web </h1>
            <p> URL Parse Result : {self.url()}         </p>
            <p> Path Original: {self.path}         </p>
            <p> Headers: {self.headers}      </p>
            <p> Query: {self.query_data()}   </p>
            <h1>Ruta Solicitada: {path}</h1>
            <p>Host: {host}</p>
            <p>User-Agent: {user_agent}</p>
            </html>""",
            '/proyecto/web-uno': "<html><h1>Proyecto: web-uno :]</h1></html>",
            '/proyecto/web-dos': "<html><h1>Proyecto: web-dos :)</h1></html>",
            '/proyecto/web-tres': "<html><h1>Proyecto: web-tres :/</h1></html>",
        }
        
        return contenido.get(path, "<h1>Error 404: Página no encontrada</h1>")

        
 
            
         


if __name__ == "__main__":
    puerto = 8000
    print("Starting server on port {puerto}")
    server = HTTPServer(("localhost", puerto), WebRequestHandler)
    server.serve_forever()
