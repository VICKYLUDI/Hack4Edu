from flask import Flask, render_template, request, redirect, flash, jsonify

import numpy as np
from keras.models import model_from_json
import os
from PIL import Image

ruta = 'static/uploads'

#audio file
file_path = os.path.join(ruta, 'tmp.png')

#File Upload
APP_ROOT = os.path.abspath(os.path.dirname(__file__))
label = ["Pollera panameña"]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = ruta

@app.route('/')
def index():
    #if model is None:
        #load_model()
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/save', methods=['POST'])
def save():
    if request.method == "POST":
        file = request.files['audio_data']
        if file.filename == '' or file is None:
            flash('No selected file')
            return redirect(request.url)
        else:
            file.save(os.path.join(APP_ROOT,app.config['UPLOAD_FOLDER'],"tmp.png"))
        return render_template('index.html', request="POST")
    else:
         return render_template("index.html")

@app.route('/guardar-archivo', methods=['POST'])
def guardar_archivo():
    lastfile = os.path.join(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], 'tmp.png'))
    if os.path.exists(lastfile):
        os.remove(lastfile)

    file = request.files['archivo']
    file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], 'tmp.png'))

    # Devolver la URL del archivo cargado
    url = request.host_url + 'static/uploads/tmp.png'
    print(url)
    return jsonify({'url': url})

model = None
#model_path = os.path.join(APP_ROOT, 'models', 'model.json')
#weights_path = os.path.join(APP_ROOT, 'models', 'modelW.h5')
#Load Model
def load_model():
    with open(model_path, 'r') as json_file:
        model_json = json_file.read()

    global model
    model = model_from_json(model_json)
    model.load_weights(weights_path)
    print('Modelo cargado correctamente.')

if __name__ == '__main__':
    #load_model()
    app.run(debug=True, port=os.getenv("PORT", default=5000))
    #app.run(port=os.getenv("PORT", default=5000))