from flask import Flask, render_template, request, redirect, flash, jsonify, url_for

import numpy as np
from keras.models import model_from_json
import os
from PIL import Image
import cv2

ruta = 'static/uploads'

# img file
file_path = os.path.join(ruta, 'tmp.png')

# File Upload
APP_ROOT = os.path.abspath(os.path.dirname(__file__))
label = ["Marimba", "Montuna Santeña", "Ocarina"]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = ruta

model = None

model_path = os.path.join(APP_ROOT, 'models', 'model.json')
weights_path = os.path.join(APP_ROOT, 'models', 'modelW.h5')

# Load Model
def load_model():
    with open(model_path, 'r') as json_file:
        model_json = json_file.read()

    global model
    model = model_from_json(model_json)
    model.load_weights(weights_path)
    print('Modelo cargado correctamente.')

@app.route('/')
def index():
    if model is None:
        load_model()
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/guardar-imagen', methods=['POST'])
def guardar_imagen():
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen.filename != '':
            # Guardar la imagen en la carpeta de uploads
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], 'tmp.png'))

    # Devolver la URL de la imagen cargada
    url = url_for('static', filename='uploads/tmp.png')
    return jsonify({'url': url})

@app.route('/procesar-imagen', methods=['POST'])
def procesar_imagen():
    if model is not None:
        # Predicción
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'tmp.png')
        x = cv2.imread(image_path)
        x = cv2.resize(x, (240, 240))
        x = x.astype('float32') / 255.0
        x = np.expand_dims(x, axis=0)

        arreglo = model.predict(x)
        resultado = arreglo[0].round()
        max_resultado = np.argmax(resultado)

        dressID = np.argmax(resultado)
        print(dressID)
        dressName = label[dressID]

        return jsonify({'dressName': dressName})

    return jsonify({'dressName': 'Desconocido'})

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
