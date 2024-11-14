#import for html website
import threading
from io import BytesIO
import cv2
from logging import warning
from traceback import print_exc
from threading import Condition
from PIL import Image
from http.server import BaseHTTPRequestHandler, HTTPServer
import numpy as np
import sys

#importing required OpenCV modules
from cv2 import COLOR_RGB2BGR, cvtColor

#html website
PAGE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pi-Car-Turbo Stream</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        header {
            background-color: #333;
            padding: 10px;
            text-align: center;
            color: white;
        }
        nav {
            background-color: #eee;
            padding: 10px;
        }
        nav a {
            margin-right: 15px;
            text-decoration: none;
            color: #333;
            font-weight: bold;
        }
        section {
            padding: 20px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Pi-Car-Turbo Stream</h1>
    </header>
    <nav>
        <a href="/normal.py">Normal</a>
    </nav>
    <section>
        <h2>Welcome to Pi-Car-Turbo Stream!</h2>
        <p>This is a simple website with Python backend.</p>
    </section>
</body>
</html>
"""


#class to manage streaming output
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = BytesIO()
        self.condition = Condition()

    def write(self, buf, camera_id=1):
        if buf.startswith(b'\xff\xd8'):
            if camera_id == 1:
                #clear buffer for camera 1
                self.buffer.truncate()
                with self.condition:
                    self.frame = self.buffer.getvalue()
                    self.condition.notify_all()
                self.buffer.seek(0)
            elif camera_id == 2:
                #clear buffer for camera 2
                self.buffer2.truncate()
                with self.condition:
                    self.frame2 = self.buffer2.getvalue()
                    self.condition.notify_all()
                self.buffer2.seek(0)
        if camera_id == 1:
            #write buffer for camera 1
            return self.buffer.write(buf)
        elif camera_id == 2:
            #write buffer for camera 2
            return self.buffer2.write(buf)

#create StreamingOutput instance
output = StreamingOutput()

#class to handle HTTP requests
class StreamingHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        if self.path == '/':
            #redirect root path to index.html
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            #serve the HTML page
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path.startswith('/normal.py'):
            
            self.sendHeader()

            try:
                static_image = Image.open("image.jpg")
                while True:
                    self.send_frame(static_image)
            except Exception as e:
                print_exc()
                warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            #handle 404 error
            self.send_error(404)
            self.end_headers()


    def sendHeader(self):

        #MJPEG streaming path
        self.send_response(200)
        self.send_header('Age', 0)
        self.send_header('Cache-Control', 'no-cache, private')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
        self.end_headers()


    def send_frame(self, static_image):
        with BytesIO() as output:
            static_image.save(output, "JPEG")
            frame_data = output.getvalue()

        self.wfile.write(b'--FRAME\r\n')
        self.send_header('Content-Type', 'image/jpeg')
        self.send_header('Content-Length', len(frame_data))
        self.end_headers()
        self.wfile.write(frame_data)
        self.wfile.write(b'\r\n')


#class to handle StreamingServer
class StreamingServer(HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def run_server():
    address = ('', 8443)
    server = StreamingServer(address, StreamingHandler)
    print("Server started on port 8443. Type 'exit' to stop.")
    server.serve_forever()
    
def init():
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    while True:
        user_input = input("Type 'exit' to stop the server: ")
        if user_input.strip().lower() == 'exit':
            break

    print("Shutting down the server...")
    server.shutdown()
    server_thread.join()
    print("Server stopped.")

if __name__ == "__main__":
    init()
