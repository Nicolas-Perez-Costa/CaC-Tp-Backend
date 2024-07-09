from datetime import date
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2Ventiladores*@localhost:5432/postgres'
app.config['SECRET_KEY'] = 'supersecreto'
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Asegura que las plantillas se recarguen automáticamente
app.config['JSON_AS_ASCII'] = False  # Desactiva la conversión automática de caracteres especiales a ASCII
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Para una representación más clara de JSON

db = SQLAlchemy(app)

# Modelo de datos
class DatosUsuarioContactos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    materia_interes = db.Column(db.String(30), nullable=False)
    primaria = db.Column(db.Boolean, nullable=False, default=False)
    secundaria = db.Column(db.Boolean, nullable=False, default=False)
    terciario = db.Column(db.Boolean, nullable=False, default=False)
    universidad = db.Column(db.Boolean, nullable=False, default=False)
    mensaje = db.Column(db.String(150))
    fecha_solicitud_contacto = db.Column(db.Date, default=db.func.current_date())
    fecha_contacto_cliente = db.Column(db.Date)

# Formulario WTForms
class DatosUsuarioContactoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    materia_interes = SelectField('Materia de Interés', choices=[
        ('', 'Seleccione una materia'), 
        ('Matemáticas', 'Matemáticas'), 
        ('Ciencias', 'Ciencias'), 
        ('Inglés', 'Inglés'), 
        ('Historia', 'Historia')], validators=[DataRequired()])
    primaria = BooleanField('Primaria')
    secundaria = BooleanField('Secundaria')
    terciario = BooleanField('Terciario')
    universidad = BooleanField('Universidad')
    mensaje = TextAreaField('Mensaje')
    submit = SubmitField('Enviar')


@app.route('/data.json')
def get_data():
    with open('static/data/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Rutas
@app.route('/', methods=['GET', 'POST'])
def index():
    form = DatosUsuarioContactoForm()
    if form.validate_on_submit():
        contacto = DatosUsuarioContactos(
            nombre=form.nombre.data,
            email=form.email.data,
            telefono=form.telefono.data,
            materia_interes=form.materia_interes.data,
            primaria=form.primaria.data,
            secundaria=form.secundaria.data,
            terciario=form.terciario.data,
            universidad=form.universidad.data,
            mensaje=form.mensaje.data
        )
        db.session.add(contacto)
        db.session.commit()
        return redirect(url_for('index'))
    
    # Cargar datos estáticos desde data.json
    with open('static/data/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    contactos = DatosUsuarioContactos.query.all()
    return render_template('index.html', data=data, contactos=contactos, form=form)

@app.route('/admin')
def admin():
    # Consultar todos los contactos de la base de datos
    contactos = DatosUsuarioContactos.query.all()
    # Renderizar la plantilla admin.html y pasar los contactos como contexto
    return render_template('admin.html', contactos=contactos)

@app.route('/editar/<int:contacto_id>', methods=['POST', 'GET'])
def editar_contacto(contacto_id):
    contacto = DatosUsuarioContactos.query.get_or_404(contacto_id)
    contacto.fecha_contacto_cliente = date.today()  # Insertar fecha actual
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/eliminar/<int:contacto_id>', methods=['POST', 'GET'])
def eliminar_contacto(contacto_id):
    contacto = DatosUsuarioContactos.query.get_or_404(contacto_id)
    db.session.delete(contacto)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
