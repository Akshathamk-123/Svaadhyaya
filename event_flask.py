from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)
app.secret_key = '231ad3242e231b2132b214034bbca3'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aishu$1606'
app.config['MYSQL_DB'] = 'project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

events_available = ['birthday', 'anniversary', 'other']

pricing = {
    'birthday': {
        'tier1': {'base': 7500, 'person': 750},
        'tier2': {'base': 10000, 'person': 1000},
        'tier3': {'base': 12500, 'person': 1250},
        'tier4': {'base': 17000, 'person': 1550},
    },
    'anniversary': {
        'tier1': {'base': 9000, 'person': 1000},
        'tier2': {'base': 12000, 'person': 1300},
        'tier3': {'base': 15000, 'person': 1600},
        'tier4': {'base': 20000, 'person': 1900},
    },
    'other': {
        'tier1': {'base': 8000, 'person': 875},
        'tier2': {'base': 11000, 'person': 1150},
        'tier3': {'base': 14000, 'person': 1400},
        'tier4': {'base': 18500, 'person': 1700},
    },
}


@app.route('/')
@app.route('/home')
def index():
    if 'loggedin' in session:
        return render_template('index.html', session=session['loggedin'], name=session['username'])
    else:
        return render_template('index.html', session=False)


@app.route('/users/<username>', methods=['GET', 'POST'])
def dashboard(username):
    if 'loggedin' in session and username == session['username']:
        cursor = mysql.connection.cursor() 
        #cursor.execute('''INSERT INTO example VALUES(1,'name1')''')
        #cursor.execute('''INSERT INTO example VALUES(1,'name2')''')
        cursor.execute(
            '''
            SELECT p.*, TIMESTAMPDIFF(YEAR, dob, CURDATE()) AS age, c.*
            from personal p NATURAL JOIN contact c WHERE pid =
            (SELECT pid from has WHERE uid =
            ( SELECT uid from users WHERE username = %s)) 
            ''',
            [session['username']],

            
        )
        personal_details = cursor.fetchone()
        cursor.execute(
            '''
            SELECT COUNT(eid) as count FROM books WHERE uid = 
            (SELECT uid FROM users WHERE username = %s)
            ''',
            [session['username']],

            
        )
        count_event = cursor.fetchone()
        cursor.execute(
            '''
            SELECT e.*, b.* FROM event e NATURAL JOIN books b WHERE e.eid IN
            (SELECT eid FROM books WHERE uid = 
            (SELECT uid FROM users WHERE username = %s ))
            ''',
            [session['username']],
        )
        event_details = cursor.fetchall()
        return render_template(
            'dashboard.html',
            name=username,
            pdata=personal_details,
            cn=count_event,
            events=event_details,
        )
    return render_template('login.html')


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
                'index.html',
                session=session['loggedin'],
                name=session['username'],
                msg="Login Successful!",
            )
        else:
            return render_template("login.html", msg="Invalid Username or Password!")
    return render_template('login.html')


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
            return render_template("register.html", rmsg=rmsg)
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
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/<eventname>', methods=['GET', 'POST'])
def book_event(eventname: str):
    if request.method == 'POST':
        ev = request.form
        person1 = person2 = None
        if eventname == 'birthday':
            person1 = ev['person1']
            etype = 'Birthday'
        elif eventname == 'anniversary':
            person1 = ev['person1']
            person2 = ev['person2']
            etype = 'Anniversary'
        else:
            etype = ev['etype']
        venue = ev['venue']
        tier = ev['tier']
        max_people = ev['max']
        date = ev['edate']
        requests = ev['requests']
        cost = (
            int(max_people) * pricing[eventname][tier]['person'] + pricing[eventname][tier]['base']
        )
        if tier == 'tier1':
            tier = 1
        elif tier == 'tier2':
            tier = 2
        elif tier == 'tier3':
            tier = 3
        elif tier == 'tier4':
            tier = 4
        cursor = mysql.connection.cursor()
        cursor.execute(
            '''
            INSERT INTO event(etype, edate, etier, ecost, evenue, emax_people, especial)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
            ''',
            (etype, date, tier, cost, venue, max_people, requests),
        )
        cursor.execute(
            '''
            INSERT INTO books VALUES(
                (SELECT uid FROM users WHERE username=%s),
                (SELECT LAST_INSERT_ID()),
                %s,%s)
            ''',
            (session['username'], person1, person2),
        )
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('dashboard', username=session['username']))

    if eventname in events_available:
        if 'loggedin' in session:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "SELECT pid FROM has WHERE uid = (SELECT uid from users where username = %s)",
                [session['username']],
            )
            per_details = cursor.fetchone()
            if not per_details:
                return redirect(url_for('personal'))
            return render_template(
                'booking.html',
                session=session['loggedin'],
                name=session['username'],
                event=eventname.capitalize(),
                t1_base=pricing[eventname]['tier1']['base'],
                t2_base=pricing[eventname]['tier2']['base'],
                t3_base=pricing[eventname]['tier3']['base'],
                t4_base=pricing[eventname]['tier4']['base'],
                t1_per=pricing[eventname]['tier1']['person'],
                t2_per=pricing[eventname]['tier2']['person'],
                t3_per=pricing[eventname]['tier3']['person'],
                t4_per=pricing[eventname]['tier4']['person'],
            )
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))


@app.route('/personal', methods=['GET', 'POST'])
def personal():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute(
        '''
        SELECT p.* ,c.*  FROM personal p NATURAL JOIN contact c WHERE pid = (SELECT pid from has where uid = (SELECT uid from users where username=%s))
        ''',
        [session['username']],
        )
        details = cursor.fetchone()
        cursor.close()
        if request.method == "POST":
            firstname = request.form['fname']
            middlename = request.form['mname']
            lastname = request.form['lname']
            DOB = request.form['dob']
            contact1 = request.form['contact1']
            contact2 = request.form['contact2']
            contact3 = request.form['contact3']
            gender = request.form['gender']
            address = request.form['address']
            cursor = mysql.connection.cursor()
            cursor.execute(
                '''
                    SELECT * FROM has WHERE uid = 
                    (SELECT uid FROM users WHERE username = %s)
                ''',
                [session['username']],
            )
            personal_exists = cursor.fetchone()
            if personal_exists:
                cursor.execute(
                    '''
                    UPDATE personal SET
                    fname=%s,
                    mname=%s,
                    lname=%s,
                    dob=%s,
                    gender=%s,
                    address=%s WHERE pid =
                    (SELECT pid FROM has WHERE uid = 
                    (SELECT uid FROM users WHERE username=%s))
                    ''',
                    (
                        firstname,
                        middlename,
                        lastname,
                        DOB,
                        gender.capitalize(),
                        address,
                        session['username'],
                    ),
                )
                cursor.execute(
                    '''
                    UPDATE contact SET
                    contact1=%s,
                    contact2=%s,
                    contact3=%s
                    WHERE pid=
                    (SELECT pid FROM has WHERE uid = 
                    (SELECT uid FROM users WHERE username=%s))
                    ''',
                    (contact1, contact2, contact3, session['username']),
                )
            else:
                cursor.execute(
                    '''
                    INSERT INTO
                    personal(fname,mname,lname,dob,gender,address) 
                    VALUES(%s,%s,%s,%s,%s,%s)
                    ''',
                    (firstname, middlename, lastname, DOB, gender.capitalize(), address),
                )
                cursor.execute(
                    '''
                    INSERT INTO contact VALUES(
                        (SELECT LAST_INSERT_ID()),
                        %s, %s, %s
                    )
                    ''',
                    (contact1, contact2, contact3),
                )
               
                cursor.execute(
                    '''
                    INSERT INTO has VALUES(
                        (SELECT uid FROM users WHERE username=%s),
                        (SELECT LAST_INSERT_ID())
                    )
                    ''',
                    [session['username']],
                )
            mysql.connection.commit()
            cursor.close()
            
            return redirect(url_for('dashboard', username=session['username']))
        return render_template(
            'personal.html', session=session['loggedin'], name=session['username'],details = details
        )
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)