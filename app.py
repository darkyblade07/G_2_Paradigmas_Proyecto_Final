import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar la carga de archivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']

    if file.filename == '':
        return redirect('/')
    
    # Verifica y crea la carpeta 'uploads'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    # Guarda el archivo en la carpeta 'uploads'
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Determinar la extensión del archivo
    file_extension = filename.rsplit('.', 1)[1].lower()

    # Determinar la carpeta de destino según la extensión
    destination_folder = os.path.join(app.config['UPLOAD_FOLDER'], file_extension)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Mover el archivo a la carpeta de destino
    result_file_path = os.path.join(destination_folder, filename)
    os.rename(file_path, result_file_path)

    return f'File uploaded successfully. Result saved as {result_file_path}.'

if __name__ == '__main__':
    app.run(debug=True)
