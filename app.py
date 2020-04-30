from flask import Flask, render_template, request, redirect, url_for, flash, session, request, logging
from flask_mysqldb import MySQL
import MySQLdb.cursors
from wtforms import form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt



app = Flask(__name__)
app.debug=True
# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin1234'
app.config['MYSQL_DB'] = 'flaskcrud'
mysql = MySQL(app)
# settings
app.secret_key = "mysecretkey"


@app.route('/')
def index():
    return render_template('index.html')
# login--------------------------------------------

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id_ac']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

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
    elif request.method == 'POST':
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
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
            
            # http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id_ac = %s', (session['id_ac'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
            
    

#----------------------login----------------------------------------------
 
@app.route('/conductores')
def conductores():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('conductores.html', contacts = data)
def conductores():
 return render_template('conductores.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('conductores'))
    #editar datos


@app.route('/vehiculos')
def vehiculos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM vehiculo')
    data = cur.fetchall()
    cur.close()
    return render_template('vehiculos.html', vehiculo = data)

@app.route('/add_auto', methods=['POST'])
def add_auto():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        kilom = request.form['kilom']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO vehiculo (marca, modelo, kilom) VALUES (%s,%s,%s)", (marca, modelo, kilom))
        mysql.connection.commit()
        flash('autos Added successfully')
        return redirect(url_for('vehiculos'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('home'))

@app.route('/asignaciones')
def asignaciones():
 return render_template('asignaciones.html')

 #modulo vehiculo--------------------------------------------
# editat datos coductor
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])
# subir datos editados conductor
@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('conductores'))
# vehiculo edit
@app.route('/editv/<id_v>', methods = ['POST', 'GET'])
def get_vehiculo(id_v):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM vehiculo WHERE id_v = %s', (id_v))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-vehiculo.html', vehiculo = data[0])
# subir datos editados vehiculo
@app.route('/updatevehi/<id_v>', methods=['POST'])
def update_vehiculo(id_v):
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        kilom = request.form['kilom']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE vehiculo
            SET marca = %s,
                modelo = %s,
                kilom = %s
            WHERE id_v = %s
        """, (marca, modelo, kilom, id_v))
        flash('vehicu Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('vehiculos'))
#fin modulo vehiculo------------------------------------------------------



if __name__ =='__main__':
    app.run()

