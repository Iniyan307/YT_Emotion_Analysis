from flask import Flask , render_template , request , url_for 
import mysql.connector
from flask_mysqldb import MySQL

import sentimentAnalysis
import yt_public

app=Flask(__name__,template_folder='templates', static_folder='static')    #referencing this file

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ytanalyser'

mysql=MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index' , methods=['GET','POST'])
def index():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']

        cur = mysql.connection.cursor()

        cur.execute('INSERT INTO user (name,email) VALUES(%s,%s)',(username,email))
        mysql.connection.commit()

        cur.close()
        return "Stored Successdully"

    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/login_validation', methods=['GET','POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT email,password FROM login WHERE email='{}' AND password='{}'".format(email,password))
    users=cur.fetchall()
    if len(users)>0:
        return render_template('dashboard.html')
    else:
        return render_template('login.html')


@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    return render_template('sign_up.html') 

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    name=request.form.get('name')
    PhoneNo=request.form.get('PhoneNo')
    email=request.form.get('email')
    password=request.form.get('password')

    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO login (Name,PhoneNo,email,password) VALUES('{}','{}','{}','{}')""".format(name,PhoneNo,email,password))
    mysql.connection.commit()
    cur.close()
    return render_template('dashboard.html') 



@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/vader', methods=['GET','POST'])
def vader():
    return render_template('vader.html')

@app.route('/vader_analyse', methods=['GET','POST'])
def vader_analyse():
    Ytlink=request.form.get('Ytlink')
    yt_public.main(Ytlink)
    y=sentimentAnalysis.sentimentAnalysisVader()
    score=y[0]
    data=y[1][0:]

    labels=[row[0] for row in data]
    values=[row[1] for row in data]

    return render_template('vader_analyse.html',score=score,labels=labels,values=values)

@app.route('/bert', methods=['GET','POST'])
def bert():
    return render_template('bert.html')

@app.route('/bert_analyse', methods=['GET','POST'])
def bert_analyse():
    Ytlink=request.form.get('Ytlink')
    yt_public.main(Ytlink)
    z=sentimentAnalysis.sentimentAnalysisBERT()

    data=z[0:]

    label=[row[0] for row in data]
    value=[row[1] for row in data]

    return render_template('bert_analyse.html',labels=label,values=value)



@app.route('/analyse',methods=['GET','POST'])
def analyse():
    Ytlink=request.form.get('Ytlink')
    option=request.form.get('option')
    x=yt_public.main(Ytlink)
    if option=="vader":
        return render_template('dashboard.html')
    if option=="bert":
        return render_template('dashboard.html',)

    # return render_template('dashboard.html',prediction1=y)
    
if __name__ == "__main__":
    app.run(debug=True)