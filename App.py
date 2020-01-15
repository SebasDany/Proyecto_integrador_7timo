from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'access'
mysql = MySQL(app)
app.secret_key = "mysecretkey"
# routes
@app.route('/')
def Index():

    return render_template('login.html')

@app.route('/docente')
def docente():

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM docente')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    ms=' '
    if request.method == 'POST':


        nombre = request.form['nombre']
        cedula = request.form['cedula']
        sexo = request.form['sexo']
        username = request.form['username']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM docente where  cedula=" + cedula)
        sp = cur.fetchone()
        cur.execute("SELECT * FROM docente where  username='" +username+"'")
        sp1 = cur.fetchone()
        if sp1:
            var=username

            msg = "Ya existe  el docente con " + var
            cur.execute('SELECT * FROM docente')
            data = cur.fetchall()
            cur.close()
            return render_template('index.html', contacts=data, msg=msg)

        if sp:
            var=cedula
            msg="Ya existe  el docente con  "+var
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM docente')
            data = cur.fetchall()
            cur.close()
            return render_template('index.html', contacts=data,msg=msg)

        else:
            cur.execute("INSERT INTO docente (id_docente, nombre_docente, cedula, sexo,username) VALUES ( null" + ",'" + nombre + "'," + cedula +",'"+sexo+ "','"+username+"')")

            mysql.connection.commit()

            return redirect(url_for('docente'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    print("estoy editando")
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM docente WHERE id_docente = '+id)
    data = cur.fetchall()
    print(data)
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        sexo = request.form['sexo']
        cur = mysql.connection.cursor()

        cur.execute("UPDATE docente SET nombre_docente = '" + nombre + "', cedula = " + cedula + ", sexo = '" + sexo + "' WHERE docente.id_docente= " + id + ";")
        print("UPDATE docente SET nombre_docente = '" + nombre + "', cedula = " + cedula + ", sexo = '" + sexo + "' WHERE docente.id_docente= " + id + ";")

        #flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('docente'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM docente WHERE id_docente = {0}'.format(id))
    mysql.connection.commit()

    return redirect(url_for('docente'))


@app.route('/horario')
def horario1():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM docente')
    data = cur.fetchall()
    cur.execute('SELECT * FROM materia')
    data1 = cur.fetchall()
    cur.execute('SELECT aulas.numero_de_aula FROM bloques,aulas WHERE bloques.id_bloque=aulas.id_bloque')
    au=cur.fetchall()
    cur.execute('SELECT laboratorios.numero_lab FROM laboratorios,bloques WHERE bloques.id_bloque=laboratorios.id_bloque')
    lab=cur.fetchall()
    cur.execute('SELECT horario.id_horario, docente.nombre_docente,materia.nombre_materia,hora_entrada,hora_salida,dia,grupo, aulab FROM horario,docente,materia WHERE docente.id_docente=horario.id_docente AND materia.id_materia=horario.id_materia')
    horarios=cur.fetchall()
    cur.close()
    return render_template("horario.html",contacts=data,contact=data1,au=au,lab=lab,horarios=horarios)




@app.route('/bloque')
def bloque1():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM bloques')

    data = cur.fetchall()
    cur.execute('SELECT aulas.id,bloques.nombre_bloque ,aulas.numero_de_aula FROM aulas,bloques WHERE bloques.id_bloque=aulas.id_bloque ')
    data1=cur.fetchall()

    cur.execute('SELECT laboratorios.id,bloques.nombre_bloque,laboratorios.numero_lab FROM laboratorios,bloques WHERE bloques.id_bloque=laboratorios.id_bloque')
    data2 = cur.fetchall()
    cur.close()

    return render_template("registro_bloque.html",contacts=data,aulas=data1,laboratorios=data2)

@app.route('/materia')
def materia1():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materia')

    data = cur.fetchall()
    return render_template("materia.html",contacts=data)

@app.route('/insert_materia', methods=['POST'])
def insert_materia():
    nbloque = request.form['nbloque']
    print(nbloque)
    s="INSERT INTO materia (id_materia, nombre_materia) VALUES (NULL, '"+nbloque+"');"
    print(s)
    cur = mysql.connection.cursor()
    cur.execute(s)

    mysql.connection.commit()

    return redirect(url_for('materia1'))

@app.route('/deleteC/<string:idb>', methods = ['POST','GET'])
def deleteC(idb):
    cur = mysql.connection.cursor()
    q='DELETE FROM materia WHERE id_materia = {0}'.format(idb)
    cur.execute(q)
    print(q)
    mysql.connection.commit()
    return redirect(url_for('materia1'))








@app.route('/insert_bloque', methods=['POST'])

def insert_bloque():
    msg = ''
    nbloque = request.form['nbloque']
    print(nbloque)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bloques WHERE nombre_bloque = '" + nbloque + "'")
    bloque = cur.fetchone()
    if bloque:

        msg = 'Ya existe ese bloque!'
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM bloques')

        data = cur.fetchall()
        cur.execute(
            'SELECT aulas.id,bloques.nombre_bloque ,aulas.numero_de_aula FROM aulas,bloques WHERE bloques.id_bloque=aulas.id_bloque ')
        data1 = cur.fetchall()

        cur.execute(
            'SELECT laboratorios.id,bloques.nombre_bloque,laboratorios.numero_lab FROM laboratorios,bloques WHERE bloques.id_bloque=laboratorios.id_bloque')
        data2 = cur.fetchall()
        cur.close()

        return render_template("registro_bloque.html", contacts=data, aulas=data1, laboratorios=data2,msg=msg)


    else:

        s="INSERT INTO bloques (id_bloque, nombre_bloque) VALUES (NULL, '"+nbloque+"');"
        print(s)

        cur.execute(s)

        mysql.connection.commit()
        return redirect(url_for('bloque1'))

@app.route('/deleteB/<string:idb>', methods = ['POST','GET'])
def deleteB(idb):
    cur = mysql.connection.cursor()
    q='DELETE FROM bloques WHERE id_bloque = {0}'.format(idb)
    cur.execute(q)
    print(q)
    mysql.connection.commit()
    return redirect(url_for('bloque1'))

@app.route('/insert_horario', methods=['POST'])
def insert_horario():
    print("··························")
    iddocente = request.form['iddocente']
    idmateria = request.form['idmateria']
    print(iddocente)
    print(idmateria)
    nday = request.form['nday']
    inicio= request.form['inicio']
    print(inicio)
    salida = request.form['salida']
    grupo = request.form['idgrupo']
    aulab = request.form['aulab']
    print(salida)
    print("aulab",aulab)
    cur = mysql.connection.cursor()
    query1="INSERT INTO horario (id_horario, id_materia, id_docente, hora_entrada, hora_salida, dia, grupo, aulab) VALUES (NULL, "+idmateria+", "+iddocente+", "+inicio+","+salida+",'"+nday+"', '"+grupo+"', '"+aulab+"');"
    print(query1)
    cur.execute(query1)
    mysql.connection.commit()

    return redirect(url_for('horario1'))





@app.route('/insert_bloque_aulas', methods=['POST'])
def insert_bloque_aulas():
    print("··························")
    idBoque = request.form['idBloque']
    print(idBoque)
    nlab = request.form['nlab']
    print(nlab)
    naula = request.form['naulas']
    print(naula)

    cur = mysql.connection.cursor()
    '''
    cur.execute("SELECT * FROM laboratorios, bloques where bloques.id_bloque="+idBoque +" AND laboratorios.numero_lab="+nlab)
    print("SELECT * FROM laboratorios, bloques where bloques.id_bloque=" + idBoque + " AND laboratorios.numero_lab=" + nlab)
    sla=cur.fetchone()
    cur.execute("SELECT * FROM aulas, bloques where bloques.id_bloque=" + idBoque + " AND aulas.numero_de_aula=" + naula)
    print("SELECT * FROM aulas, bloques where bloques.id_bloque=" + idBoque + " AND aulas.numero_de_aula=" + naula)
    sau = cur.fetchone()
    if sla and sau:
        msg1="ya existe el laboratorio "+nlab
        msg2="ya existe el aula "+ naula
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM bloques')

        data = cur.fetchall()
        cur.execute(
            'SELECT aulas.id,bloques.nombre_bloque ,aulas.numero_de_aula FROM aulas,bloques WHERE bloques.id_bloque=aulas.id_bloque ')
        data1 = cur.fetchall()

        cur.execute(
            'SELECT laboratorios.id,bloques.nombre_bloque,laboratorios.numero_lab FROM laboratorios,bloques WHERE bloques.id_bloque=laboratorios.id_bloque')
        data2 = cur.fetchall()
        cur.close()

        #return render_template("registro_bloque.html", contacts=data, aulas=data1, laboratorios=data2,msg1=msg1,msg2=msg2)
    #else:
       '''''
    if (int(nlab)>0):
        s1 = "INSERT INTO laboratorios (id, id_bloque, numero_lab) VALUES (NULL," + idBoque + "," + nlab + ");"
        cur.execute(s1)
        mysql.connection.commit()
    if (int(naula)>0):
        s = "INSERT INTO aulas (id, id_bloque, numero_de_aula) VALUES (NULL, " + idBoque + "," + naula + ");"
        cur.execute(s)
        mysql.connection.commit()
        print(s)
        return redirect(url_for('bloque1'))
# starting the app
@app.route('/deleteL/<string:idL>', methods = ['POST','GET'])
def deleteL(idL):
    cur = mysql.connection.cursor()
    q='DELETE FROM laboratorios WHERE id = {0}'.format(idL)
    cur.execute(q)
    print(q)
    mysql.connection.commit()
    return redirect(url_for('bloque1'))
@app.route('/deleteA/<string:idA>', methods = ['POST','GET'])
def deleteA(idA):
    cur = mysql.connection.cursor()
    q='DELETE FROM aulas WHERE id = {0}'.format(idA)
    cur.execute(q)
    print(q)
    mysql.connection.commit()
    return redirect(url_for('bloque1'))

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)
        # Check if account exists using MySQL
        cursor =mysql.connection.cursor()

        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        print("vcshdvchvdhcvhsd")
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
        # If account exists in accounts table in out database
        if account:
            print(session)
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            print("estoy dentro del iff")

            # Create session data, we can access this data in other routes
            return redirect(url_for('docente'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        print(username)
        print(password)
        print(email)
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        print("SELECT * FROM accounts WHERE username = '"+username+"'")
        cursor.execute("SELECT * FROM accounts WHERE username = '"+username+"'")

        account = cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            print(1)
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            print(2)
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            print(3)
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
            print(4)
        else:
            print(5)
            cursor = mysql.connection.cursor()
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        print(6)
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor()
        query='SELECT * FROM accounts WHERE id ='+ str(session['id'])
        print(query)
        cursor.execute(query)
        print("estoy dentro de la sesion")
        print('SELECT * FROM accounts WHERE id =', session['id'])
        account = cursor.fetchone()
        print(account)
        # Show the profile page with account info
        return render_template('profile.html', accounts=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
app.run()
