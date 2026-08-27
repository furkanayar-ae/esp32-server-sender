import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from server.interface_adapters.http_controller import SensorController

controller = SensorController()

class CleanHTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Controller'a yönlendir
        response_dict = controller.handle_post_request(post_data)
        
        # HTTP yanıtını dön
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_dict).encode('utf-8'))

if __name__ == "__main__":
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, CleanHTTPHandler)
    print("Clean Architecture Python Sunucusu Port 3000'de başlatıldı...")
    httpd.serve_forever()