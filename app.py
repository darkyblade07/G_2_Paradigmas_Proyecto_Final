import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Función para verificar si la extensión es permitida
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}  # Agregar extensiones permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        # Extrae la categoría del nombre del archivo
        file_name, extension = os.path.splitext(file.filename)
        categories = file_name.split('.')

        # Maneja casos especiales
        if len(categories) == 1:
            # Categoría simple
            category = categories[0]
        elif len(categories) > 1:
            # Múltiples categorías
            # Selecciona la primera categoría que coincida con las permitidas
            for category in categories:
                if category in ALLOWED_EXTENSIONS:
                    break
            else:
                # No hay categoría coincidente, usa la primera por defecto
                category = categories[0]

        # Crea la carpeta para la categoría si no existe
        category_folder = os.path.join(app.config['UPLOAD_FOLDER'], category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        # Construye la ruta completa del archivo
        file_path = os.path.join(category_folder, file.filename)

        # Guarda el archivo en la ruta completa del archivo
        file.save(file_path)

        confirmation_message = f'Successfully uploaded. File location: {file_path}.'

    else:
        confirmation_message = 'Invalid file type. Allowed extensions: {ALLOWED_EXTENSIONS}'

    return render_template('index.html', confirmation=confirmation_message)


if __name__ == '__main__':
    app.run(debug=True)




