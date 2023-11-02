# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

PAGE="""\
<html>
	<head>
		<title>Joy</title>
		<meta charset="utf-8">
		<meta name="description" content="Example page of use pure Javascript JoyStick">
		<link rel="stylesheet" type="text/css" href={{ url_for('static',filename='style.css') }}>
		<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
		
		<style>
*
{
	box-sizing: border-box;
}
body
{
	width:100%;
    	min-height: 100%;
	margin: 0px;
	padding: 0px;
}
.row
{
	width:100%;
	display: inline-flex;
	clear: both;
}

.columnCetral
{
  
  float: left;
  width: 100%;
}
.navbar {
  overflow: hidden;
  position: fixed;
  bottom: 0;
  width: 100%;
  margin: auto;
  background-color: black;
  opacity:0.6;
}

.navbar a {
  float: left;
  display: block;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
}

.navbar a:hover {

}

.navbar a.active {
  background-color: #4CAF50;
  color: white;
}

.main {
  padding: 16px;
  margin-bottom: 30px;
}


.camera-movement{
  float: none;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.lights-button{
	float: right;
}
.camera-bg {
  position: fixed;
  top: 0;
  left: 5%;

  /* Preserve aspet ratio */
  max-width: 90%;
  min-height: 100%;

    /* Full height */
  height: 100%;


  /* Center and scale the image nicely */
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;

}
i.fa {
  display: inline-block;
  border-radius: 60px;
  box-shadow: 0px 0px 2px #888;
  padding: 0.5em 0.6em;


}

img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 35%
}

button {
    background-color: Transparent;
    background-repeat:no-repeat;
    border: none;
    cursor:pointer;
    overflow: hidden;
    outline:none;
}

h2 {
  text-align: center;
}
div.fixed {
  position: fixed;
  bottom: 0;
  right: 0;
  width: 200px;
  border: 3px solid blue;
  color: #cc0010;
  background-color: white;
}
.content {
  padding: 20px;
}
.card {
  background-color: white;
  box-shadow: 2px 2px 12px 1px rgba(140,140,140,.5);
}
.card-title {
  color:#003366;
  font-weight: bold;
}
.cards {
  max-width: 800px;
  margin: 0 auto;
  display: grid; grid-gap: 2rem;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}
.reading {
  font-size: 1.2rem;
}
.cube-content{
  width: 100%;
  background-color: white;
  height: 300px; 
  margin: auto;
}
		</style>
		
	</head><script src="{{ url_for('static',filename='three.min.js') }}"></script>
	<body>
		<div class="container"> <!----bar-->
			<header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
			  <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
				<img class="d-block" src="sym.png" alt="" style="width: 50px;">
				<span class="fs-4 fw-bold">PCSHS PL</span>
			  </a>
		
			  <ul class="nav nav-pills">
				<li class="nav-item"><a href="#" class="nav-link active" aria-current="page">Home</a></li>
				<li class="nav-item"><a href="Gallery.html" class="nav-link">Gallery</a></li>
				<li class="nav-item"><a href="#" class="nav-link">About</a></li>
			  </ul>
			</header>
		  </div>
		<div class="px-4 py-5 mb-5 text-center">
			<div class="container">
				
			</div>
			<h3 class=" fw-bold">Underwater Resource </h3>
			<h1 class="display-5 fw-bold">Exploration Drone</h1>
			
			<div class="col-lg-6 mx-auto">
			  <div class="w-80">
				<div class="pd-2">
					<center><img src="stream.mjpg" width="640" height="480"></center>
				</div>
			 </div>
			</div> 
		  </div>
		
		 
		<div class="d-flex row justify-content-center mx-auto">
			<div class="col-3">
				<div class="h-100 p-3 text-white bg-primary rounded-3">
				  <h2>TDS Sensor</h2>
				  <div class="fw-bold"><p>Value :  <span id='v1'>0</span></p></div>
				</div>
			</div>
			<div class="col-3">
				<div class="h-100 p-3 text-white bg-success rounded-3">
				  <h2>Position</h2>
				  <div class="fw-bold"><p>X :  <span id='v2'>0</span></p></div>
				  <div class="fw-bold"><p>Y :  <span id='v3'>0</span></p></div>
				  <div class="fw-bold"><p>Z :  <span id='v4'>0</span></p></div>
				</div>
			</div>
			<div class="col-3">
				<div class="h-100 p-3 text-dark bg-warning rounded-3">
				  <h2>....</h2>
				  <p> component themes and more.</p>
				</div>

			</div>
		</div>	
		
	</body>
</html>
"""

print("Server Start")
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)
    

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='1280x960', framerate=30) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 180
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
