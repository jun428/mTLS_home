
from flask import Flask, render_template, request
from serial import Serial
import struct
import ssl

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pongers'
    
port = '/dev/ttyUSB0'  
baud = 9600  

ctrl_Ardu = Serial(port, baud)
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/light", methods=['POST', 'GET'])
def light():
    mod = 0b0
    if request.method == 'POST':
        if request.form['Red'] == "on":
            mod = mod | 0b100
        if request.form['Green'] == "on":
            mod = mod | 0b10
        if request.form['Blue'] == "on":
            mod = mod | 0b1
        color = struct.pack('i', mod)
        print(color)
        ctrl_Ardu.write(color)
        c = ctrl_Ardu.read()
        print(c)
    return render_template('light.html')



if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    print(context)
    print("test")
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/home/cslab2/Desktop/fwknop/certs/ca.crt')
    context.load_cert_chain(certifile='/home/cslab2/Desktop/fwknop/certs/client.crt', keyfile='/home/cslab2/Desktop/fwknop/certs/client.key')
    app.run('0.0.0.0', 8000, ssl_context=context)
