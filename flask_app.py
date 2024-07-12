from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import datetime

app = Flask(__name__)

# Conectar a la base de datos MySQL
try:
    conn = mysql.connector.connect(
        host="luckberonne.mysql.pythonanywhere-services.com",
        user="luckberonne",
        password="mysqlroot",
        database="luckberonne$default"
    )

    # Crear un cursor para ejecutar consultas
    mycursor = conn.cursor()

    # Crear la tabla si no existe
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Formulario (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            telefono VARCHAR(20),
            materia_interes VARCHAR(255),
            primaria BOOLEAN,
            secundaria BOOLEAN,
            terciario BOOLEAN,
            universidad BOOLEAN,
            mensaje TEXT,
            fecha_contacto_cliente DATETIME,
            fecha_solicitud_contacto DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

except mysql.connector.Error as e:
    print(f"Error de conexión a la base de datos: {e}")
    conn = None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        materia_interes = request.form.get('materia_interes')
        primaria = 'primaria' in request.form
        secundaria = 'secundaria' in request.form
        terciario = 'terciario' in request.form
        universidad = 'universidad' in request.form
        mensaje = request.form.get('mensaje')

        if conn is None:
            return "Error de conexión a la base de datos."

        # Preparar la consulta SQL para insertar datos
        sql = """
            INSERT INTO Formulario 
            (nombre, email, telefono, materia_interes, primaria, secundaria, terciario, universidad, mensaje,
            fecha_solicitud_contacto) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (nombre, email, telefono, materia_interes, primaria, secundaria, terciario, universidad, mensaje,
               datetime.datetime.now())

        try:
            mycursor.execute(sql, val)
            conn.commit()
            return redirect(url_for('success', nombre=nombre))
        except Exception as e:
            return f'Hubo un problema al procesar tu solicitud: {str(e)}'

    return render_template('index.html')

@app.route('/success')
def success():
    nombre = request.args.get('nombre')
    return f'Gracias, {nombre}! Vuelve pronto.'

@app.route('/admin')
def admin():
    if conn is None:
        return "Error de conexión a la base de datos."

    try:
        mycursor.execute("SELECT * FROM Formulario")
        data = mycursor.fetchall()
        return render_template('admin.html', data=data)
    except Exception as e:
        return f'Hubo un problema al obtener los datos: {str(e)}'

@app.route('/contactar/<int:id>', methods=['POST'])
def contactar(id):
    if conn is None:
        return "Error de conexión a la base de datos."

    try:
        # Actualizar la fecha de contacto cliente a la fecha y hora actual
        now = datetime.datetime.now()
        mycursor.execute("UPDATE Formulario SET fecha_contacto_cliente = %s WHERE id = %s", (now, id))
        conn.commit()
        return redirect(url_for('admin'))
    except Exception as e:
        return f'Hubo un problema al contactar al cliente: {str(e)}'

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    if conn is None:
        return "Error de conexión a la base de datos."

    try:
        # Eliminar el registro
        mycursor.execute("DELETE FROM Formulario WHERE id = %s", (id,))
        conn.commit()
        return redirect(url_for('admin'))
    except Exception as e:
        return f'Hubo un problema al eliminar el registro: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)