import http.server
import socketserver

_PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", _PORT), Handler) as httpd:
    print('Waiting...')
    httpd.serve_forever()
