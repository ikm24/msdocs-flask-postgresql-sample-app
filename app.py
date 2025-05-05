import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# The import must be done after db initialization due to circular import issue
from models import ImagenCloud

@app.route('/', methods=['GET'])
def index():
    print('Solicitud para la página principal')
    imagenes = ImagenCloud.query.all()
    return render_template('index.html', imagenes=imagenes)

@app.route('/create', methods=['GET'])
def crear_imagen():
    print('Solicitud para crear nueva ImagenCloud')
    return render_template('crear_imagen.html')

@app.route('/add', methods=['POST'])
@csrf.exempt
def add_imagen():
    try:
        usuario = request.values.get('usuario')
        imagen = request.values.get('imagen')
        tipo = request.values.get('tipo')
        pixelesR = request.values.get('pixelesR')
        pixelesG = request.values.get('pixelesG')
        pixelesB = request.values.get('pixelesB')
    except (KeyError):

        return redirect('crear_imagen', {
            'error_message': "Todos los campos son obligatorios",
        })
    else:
        imagenCloud = ImagenCloud()
        imagenCloud.usuario = usuario
        imagenCloud.imagen = imagen
        imagenCloud.tipo = tipo
        imagenCloud.pixelesR = int(pixelesR)
        imagenCloud.pixelesG = int(pixelesG)
        imagenCloud.pixelesB = int(pixelesB)
        imagenCloud.fecha = datetime.now()
        db.session.add(imagenCloud)
        db.session.commit()

        return redirect(url_for('index'))
    
@app.route('/remove/<int:id>', methods=['POST'])
@csrf.exempt
def remove_imagen(id):
    
    imagen_a_eliminar = ImagenCloud.query.get_or_404(id)
    
    db.session.delete(imagen_a_eliminar)
    db.session.commit()
    print('Imagen de id {} eliminada'.format(id))

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
