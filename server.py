import json
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from bls_workflow import run_bls_workflow
import os

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            base_dir = os.path.dirname(os.path.abspath(__file__))
            index_path = os.path.join(base_dir, 'index.html')
            with open(index_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/verify':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                p = int(data['p'])
                a = int(data['a'])
                b = int(data['b'])
                priv_key = int(data['priv_key'])
                message = data['message']
                
                result = run_bls(p, a, b, priv_key, message)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
                
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e), "trace": traceback.format_exc()}).encode('utf-8'))

def run_bls(p, a, b, priv_key, message):
    return run_bls_workflow(p, a, b, priv_key, message)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting Matrix verification server...")
    print(f"Open your browser at -> http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
