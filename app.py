import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'Files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set()
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

# Función para verificar si la extensión es permitida
def allowed_file(filename):
    return True

# Página principal
@app.route('/')
def index():
    return render_template('index.html', confirmation=None)


# Ruta para manejar la carga de archivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']

    if file.filename == '':
        return redirect('/')

    if file and allowed_file(file.filename):
        # Verifica y crea la carpeta 'uploads'
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        # Guarda el archivo en la carpeta 'uploads'
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Mover el archivo a la carpeta principal si no tiene extensión
        if '.' not in filename:
            result_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            # Determinar la extensión del archivo
            file_extension = filename.rsplit('.', 1)[1].lower()

            # Determinar la carpeta de destino según la extensión
            destination_folder = os.path.join(app.config['UPLOAD_FOLDER'], file_extension)
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            # Mover el archivo a la carpeta de destino
            result_file_path = os.path.join(destination_folder, filename)

        os.rename(file_path, result_file_path)

        # Ordenar los archivos alfabéticamente en la carpeta de destino
        if os.path.isdir(destination_folder):
            files_in_folder = os.listdir(destination_folder)
            sorted_files = sorted(files_in_folder)
            for i, file_name in enumerate(sorted_files):
                old_file_path = os.path.join(destination_folder, file_name)
                new_file_path = os.path.join(destination_folder, file_name)  # Modificación aquí
                os.rename(old_file_path, new_file_path)

        confirmation_message = f'Successfully uploaded. File location: {result_file_path}.'
    
        return render_template('index.html', confirmation=confirmation_message)
    else:
        return render_template('index.html', confirmation='Invalid file extension. Only txt, pdf, png, jpg, jpeg, gif, csv, json, sql are allowed.')


if __name__ == '__main__':
    app.run(debug=True)
