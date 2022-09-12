from flask import Flask, render_template, request,redirect, session, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime
import pyttsx3
import speech_recognition as sr

app = Flask(__name__)
app.secret_key = '231ad3242e231b2132b214034bbca3'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aishu$1606'
app.config['MYSQL_DB'] = 'project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/video2')
def video2():
    return render_template('demo_2.html')


@app.route('/video2', methods=['POST'])
def index():

    text_speech = pyttsx3.init()
    answer = request.form['answer']
    text_speech.say(answer)
    text_speech.runAndWait()
    return render_template('demo_2.html')

@app.route("/video2 ", methods=["GET", "POST"])
def index_1():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)

    return render_template('demo_2.html', transcript=transcript)


@app.route('/book', methods=['GET', 'POST'])
def book():
    return render_template("book.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor() 
    
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = MD5(%s)", (username, password)
        )
        account = cursor.fetchone()

        if account:
            last_login = datetime.now() 
            session['loggedin'] = True
            session['username'] = account['username']
            session['password'] = account['password']
            cursor.execute(
                "UPDATE users SET last_login = %s where username=%s",
                (last_login, session['username']),
            )
            mysql.connection.commit() 
            cursor.close()
            return render_template(
                'eve.html',
                session=session['loggedin'],
                name=session['username'],
                msg="Login Successful!",
            )
        else:
            return render_template("log.html", msg="Invalid Username or Password!")
    return render_template('log.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    rmsg = ""
    if request.method == "POST":
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        email = userDetails['email']
        repass = userDetails['reenterPassword'] 
        if password != repass:
            rmsg = "Password does not match!"
            return render_template("reg.html", rmsg=rmsg)
        else:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", [username])
            account = cursor.fetchone()

            if account:
                rmsg = "Username already exists!"
                return render_template("register.html", rmsg=rmsg)
            else:
                cursor.execute(
                    "INSERT INTO users(username,password,email) VALUES(%s,MD5(%s),%s)",
                    (username, password, email),
                )
                mysql.connection.commit()
                cursor.close()
            return redirect(url_for('login'))
    return render_template('reg.html')


if __name__ == "__main__":
    app.run(port='8000')

