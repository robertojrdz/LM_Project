import mysql.connector
from flask import Flask, render_template, request


app = Flask(__name__)
#app.debug = True

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1a.2b.3c,',
    database='crudb'
)

@app.route('/')
def helloworld():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM  empleados")
    contacts = cursor.fetchall()
    cursor.close()
    return render_template("index.html", contacts=contacts) 

@app.route('/show', methods = ["POST","GET"])
def show():
    try:
        if request.method == "POST":
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            cellphone = request.form['cellphone']
            email = request.form['email']
            cursor = mydb.cursor()
            sql = 'INSERT INTO empleados VALUES (%s, %s, %s, %s)'
            values = ( firstName, lastName, cellphone, email)
            cursor.execute(sql, values)
            mydb.commit()

            cursor.execute("SELECT * FROM  empleados")
            contacts = cursor.fetchall()

            return render_template('index.html', contacts=contacts)
    except Exception as e:
       print(e)
    finally:
       cursor.close()       

if __name__ == "__main__":
    app.run()