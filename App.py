from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from time import time

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix,roc_auc_score,roc_curve, classification_report
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    tiempo_inicial = time()
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
            tiempo_final = time()

            tiempo_ejecucion = tiempo_final - tiempo_inicial
            print('TIEMPO DE EJECUCION INGRESO DOCENTE : ', tiempo_ejecucion)


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
    tiempo_inicial = time()


    if request.method == 'POST':
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        sexo = request.form['sexo']
        cur = mysql.connection.cursor()

        cur.execute("UPDATE docente SET nombre_docente = '" + nombre + "', cedula = " + cedula + ", sexo = '" + sexo + "' WHERE docente.id_docente= " + id + ";")
        print("UPDATE docente SET nombre_docente = '" + nombre + "', cedula = " + cedula + ", sexo = '" + sexo + "' WHERE docente.id_docente= " + id + ";")

        #flash('Contact Updated Successfully')
        mysql.connection.commit()
        tiempo_final = time()

        tiempo_ejecucion = tiempo_final - tiempo_inicial
        print('TIEMPO DE EJECUCION ACTUALIZACION DEL CONTACTO : ', tiempo_ejecucion)
        return redirect(url_for('docente'))


@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    tiempo_inicial = time()
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM docente WHERE id_docente = {0}'.format(id))
    mysql.connection.commit()
    tiempo_final = time()

    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('TIEMPO DE EJECUCION ELIMINACION DEL CONTACTO: ', tiempo_ejecucion)

    return redirect(url_for('docente'))



@app.route('/horario')
def horario1():
    tiempo_inicial = time()
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
    tiempo_final = time()

    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('TIEMPO DE EJECUCION CONSULAT DOCENTE, LAB,HORARIOS: ', tiempo_ejecucion)

    return render_template("horario.html",contacts=data,contact=data1,au=au,lab=lab,horarios=horarios)



@app.route('/bloque')
def bloque1():
    tiempo_inicial = time()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM bloques')

    data = cur.fetchall()
    cur.execute('SELECT aulas.id,bloques.nombre_bloque ,aulas.numero_de_aula FROM aulas,bloques WHERE bloques.id_bloque=aulas.id_bloque ')
    data1=cur.fetchall()

    cur.execute('SELECT laboratorios.id,bloques.nombre_bloque,laboratorios.numero_lab FROM laboratorios,bloques WHERE bloques.id_bloque=laboratorios.id_bloque')
    data2 = cur.fetchall()
    cur.close()
    tiempo_final = time()

    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('TIEMPO DE EJECUCION CONSULTA BLOQUES: ', tiempo_ejecucion)

    return render_template("registro_bloque.html",contacts=data,aulas=data1,laboratorios=data2)


@app.route('/materia')
def materia1():

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materia')

    data = cur.fetchall()
    return render_template("materia.html",contacts=data)

@app.route('/insert_materia', methods=['POST'])
def insert_materia():
    tiempo_inicial = time()
    nbloque = request.form['nbloque']
    print(nbloque)
    s="INSERT INTO materia (id_materia, nombre_materia) VALUES (NULL, '"+nbloque+"');"
    print(s)
    cur = mysql.connection.cursor()
    cur.execute(s)

    mysql.connection.commit()
    tiempo_final = time()

    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('TIEMPO DE EJECUCION INSERTAR MATERIAS: ', tiempo_ejecucion)

    return redirect(url_for('materia1'))


@app.route('/deleteC/<string:idb>', methods = ['POST','GET'])
def deleteC(idb):
    tiempo_inicial = time()
    cur = mysql.connection.cursor()
    q='DELETE FROM materia WHERE id_materia = {0}'.format(idb)
    cur.execute(q)
    print(q)
    mysql.connection.commit()
    tiempo_final = time()

    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('TIEMPO DE EJECUCION ELIMAR MATERIAS: ', tiempo_ejecucion)


    return redirect(url_for('materia1'))







@app.route('/insert_bloque', methods=['POST'])

def insert_bloque():
    tiempo_inicial = time()
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
        tiempo_final = time()

        tiempo_ejecucion = tiempo_final - tiempo_inicial
        print('TIEMPO DE EJECUCION INSERTAR BLOQUES: ', tiempo_ejecucion)

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
    tiempo_inicial = time()
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

    tiempo_final = time()

    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('TIEMPO DE EJECUCION INSERTAR HORARIOS: ', tiempo_ejecucion)

    return redirect(url_for('horario1'))






@app.route('/insert_bloque_aulas', methods=['POST'])
def insert_bloque_aulas():
    tiempo_inicial = time()
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
        tiempo_final = time()

        tiempo_ejecucion = tiempo_final - tiempo_inicial
        print('TIEMPO DE EJECUCION INSERTAR BLOQUES Y AULAS: ', tiempo_ejecucion)

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
    tiempo_inicial = time()
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
            tiempo_final = time()

            tiempo_ejecucion = tiempo_final - tiempo_inicial
            print('TIEMPO DE EJECUCION LOGIN: ', tiempo_ejecucion)
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
   tiempo_inicial = time()
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   tiempo_final = time()
   tiempo_ejecucion = tiempo_final - tiempo_inicial
   print('TIEMPO DE EJECUCION CIERRE DE SESION: ', tiempo_ejecucion)
   return redirect(url_for('login'))




# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    tiempo_inicial = time()
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
            tiempo_final = time()

            tiempo_ejecucion = tiempo_final - tiempo_inicial
            print('TIEMPO DE EJECUCION REGISTRO DE USUARIOS: ', tiempo_ejecucion)
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
    tiempo_inicial = time()
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
        tiempo_final = time()

        tiempo_ejecucion = tiempo_final - tiempo_inicial
        print('TIEMPO DE EJECUCION VISAUALIZACION D PERFILES: ', tiempo_ejecucion)
        return render_template('profile.html', accounts=account)
    # User is not loggedin redirect to login page

    return redirect(url_for('login'))

@app.route('/machine')
def machine():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM docente')
    data = cur.fetchall()
    contact = data


    return render_template("machine.html",contact=data)

@app.route('/predecir', methods=['POST'])
def predecir():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM docente')
    data = cur.fetchall()

    hen = request.form['horaentrada']
    hsa = request.form['horasalida']
    dn = request.form['dianumero']
    print(hen,hsa,dn)


    reader = pd.read_csv('dataset.csv', encoding='utf8', delimiter=";")

    reader = reader.drop('Nombre', axis=1)
    # reader = reader.values

    reader["hora_salida"] = reader["hora_salida"].str.split(":", n=1, expand=True)
    reader["hora_enterada"] = reader["hora_enterada"].str.split(":", n=1, expand=True)
    reader['hora_timbre'] = reader["hora_timbre"].str.split(":", n=1, expand=True)
    reader['delay_time'] = reader["delay_time"].str.split(":", n=2, expand=True)
    reader['date'] = pd.to_datetime(reader['date'])
    date = []
    for i in reader.date:
        date.append(i.weekday())

    reader['date'] = date

    reader = reader.drop(reader.columns[[4, 6]], axis='columns')

    x = reader.drop(['atraso', 'hora_timbre'], axis=1).values
    y = reader.atraso.values

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    escalar = StandardScaler()

    # x_train = escalar.fit_transform(x_train)
    # x_test = escalar.fit_transform(x_test)

    algoritmo = LogisticRegression()

    # x_train = np.reshape(1,-1)
    # print(algoritmo)

    algoritmo.fit(x_train, y_train)

    H1=np.array([int(hen),int(hsa),int(dn)])
    h1=H1.reshape(1,-1)
    '''
    d1 = {"hora_enterada":16,
        "hora_salida":20,
       "date": 3}

    #df2 = pd.DataFrame(H1, index=[1])
    '''
    y_pred2 = algoritmo.predict(h1)
    print(y_pred2)
    if(y_pred2==0):
        respredict= str(y_pred2) + " Llegara puntual"

    else :
        respredict =str(y_pred2)+ "Se atrasara por algun motivo"

    y_pred = algoritmo.predict(x_test)

    accuracy = accuracy_score(y_test, y_pred)
    matrix_confusion = confusion_matrix(y_test, y_pred)
    ################
    print(accuracy)
    matriz=matrix_confusion
    PJ = []
    for x in range(len(matriz)):
        sumaColumna = 0
        for y in range(len(matriz)):
            sumaColumna = sumaColumna + matriz[y][x]
        PJ.append(sumaColumna)

    print(matriz)
    print(PJ)
    precision = []
    for x1 in range(len(matriz)):
        Pr = matriz[x1][x1] / PJ[x1]
        print("Precision ", x1 + 1, " =", Pr)
        precision.append(Pr)

    # Recall
    CI = []
    for x2 in range(len(matriz)):
        sumfilas = 0
        for y2 in range(len(matriz)):
            sumfilas = sumfilas + matriz[x2][y2]
        CI.append(sumfilas)

    print(CI)
    Recall = []
    for x3 in range(len(matriz)):
        Re = matriz[x3][x3] / CI[x3]
        print("Recall ", x3 + 1, " =", Re)
        Recall.append(Re)

    # Accuracy
    sumafila = 0
    for x4 in range(len(matriz)):
        sumafila = sumafila + PJ[x4]
    suma = 0
    for x5 in range(len(matriz)):
        suma = suma + matriz[x5][x5]

    print('')

    Ac = suma / sumafila
    print("Accuracy: ", Ac)

    # F1 SCORE
    print(' ')
    print("Precicion", precision)
    print("Recall", Recall)
    fscore=[]
    for i in range(len(matriz)):
        f1 = (2 * (precision[i] * Recall[i])) / (precision[i] + Recall[i])
        fscore.append(f1)
        print("F Score ", i + 1, " =", f1)
    print("Precicion", precision)
    print("Recall", Recall)
    print("")
    ##############
    repor=classification_report(y_test, y_pred)
    report1=repor.split('\n')
    print(repor.split('\n'))


    print("", classification_report(y_test, y_pred))
    Log_roc_auc = roc_auc_score(y_test, algoritmo.predict(x_test))
    fpr, tpr, thresholds = roc_curve(y_test, algoritmo.predict_proba(x_test)[:, 1])

    plt.figure()

    plt.plot(fpr, tpr, label=" Curva Roc Logistic Regression area = %0.2f" % Log_roc_auc)
    plt.legend(loc="lower right")
    #plt.show()
    plt.savefig("static/image/image2.png", depi=100)
    g2 = 'static/image/image2.png'
##contacts=data,precision=precision,recall=Recall

    return render_template ('machine.html',recall=Recall,fscore=fscore,presicion=precision, pred1=respredict,contact=data,results=repor,recomend=y_test,pred=y_pred,speech=report1,contacts=data,acc=accuracy,coseno=matrix_confusion,im2=g2)

@app.route('/buscar', methods=['POST'])
def buscar()->'html' :
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM docente')
    data = cur.fetchall()


    prof = request.form['profesor']
    print(prof)
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM horario where id_docente = '+prof)
    data1 = cur.fetchall()

    return render_template('machine.html',datos=data1,contact = data)

app.run()
