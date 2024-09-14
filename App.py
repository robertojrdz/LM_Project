import mysql.connector
from flask import Flask, render_template, request, redirect


app = Flask(__name__)
app.debug = True

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1a.2b.3c,',
    database='crudb'
)

@app.route('/')
def index():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM  empleados")
    contacts = cursor.fetchall()
    cursor.close()
    return render_template("index.html", contacts=contacts) 

@app.route('/submit', methods = ["POST", "GET"])
def submit():
    try:
        if request.method == "POST":
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            cellphone = request.form['cellphone']
            email = request.form['email']
            cursor = mydb.cursor()
            sql = 'INSERT INTO empleados (firstName, lastName, cellphone, email) VALUES (%s, %s, %s, %s);'
            values = ( firstName, lastName, cellphone, email)
            cursor.execute(sql, values)
            mydb.commit()

            cursor.execute("SELECT * FROM empleados")
            contacts = cursor.fetchall()

            return render_template('index.html', contacts=contacts)
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/update/<thisID>', methods = ["POST", "GET"])
def update(thisID):
    try:
        if request.method == "POST":
            id = thisID
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            cellphone = request.form['cellphone']
            email = request.form['email']
            cursor = mydb.cursor()
            sql = 'UPDATE empleados SET firstName = %s, lastName = %s, cellphone = %s, email = %s WHERE id = %s;'
            values = ( firstName, lastName, cellphone, email, id)
            cursor.execute(sql, values)
            mydb.commit()
            cursor.execute("SELECT * FROM empleados")
            contacts = cursor.fetchall()
            return render_template('index.html', contacts = contacts)
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/delete/<thisID>', methods = ["POST", "GET"])
def delete(thisID):
    try:
        if request.method == "POST":
            id = thisID
            cursor = mydb.cursor()
            sql = "DELETE FROM empleados where id = %s"
            values = (id, )
            cursor.execute(sql, values)
            mydb.commit()
            
            cursor.execute("SELECT * FROM empleados")
            contacts = cursor.fetchall()
            return render_template('index.html', contacts = contacts)
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/search', methods = ["GET", "POST"])
def search():
    try:
        if request.method == "POST":
            firstName = request.form['firstName']
            fn = '%'+firstName+'%'
            lastName = request.form['lastName']
            ln = '%'+lastName+'%'
            cellphone = request.form['cellphone']
            cph = '%'+cellphone+'%'
            email = request.form['email']
            em = '%'+email+'%'
            search = ((firstName, lastName, cellphone, email), )
            sql = ''
            cursor = mydb.cursor()
            if firstName != '' and sql == '':
                if lastName != '' and sql == '':
                    if cellphone != '' and sql == '':
                        if email != '' and sql == '':
                            sql = "SELECT * FROM empleados WHERE firstName LIKE %s, lastName LIKE %s, cellphone LIKE %s, email LIKE %s;"
                            values = (fn, ln, cph, em)
                        else:
                            sql = "SELECT * FROM empleados WHERE firstName LIKE %s, lastName LIKE %s, cellphone LIKE %s;"
                            values = (fn, ln, cph)
                    else:
                        if email != '' and sql == '':
                            sql = "SELECT * FROM empleados WHERE firstName LIKE %s, lastName LIKE %s, email LIKE %s;"
                            values = (fn, ln, em)
                        else:
                            sql = "SELECT * FROM empleados WHERE firstName LIKE %s OR lastName LIKE %s;"
                            values = (fn, ln)
                if cellphone != '' and sql == '':
                    if email != '' and sql == '':
                        sql = "SELECT * FROM empleados WHERE firstName LIKE %s, cellphone LIKE %s, email LIKE %s;"
                        values = (fn, cph, em)
                    else:
                        sql = "SELECT * FROM empleados WHERE firstName LIKE %s, cellphone LIKE %s;"
                        values = (fn, cph)
                else:
                    if email != '' and sql == '':
                        sql = "SELECT * FROM empleados WHERE firstName LIKE %s, email LIKE %s;"
                        values = (fn, ln, em)
                    else:
                        sql = "SELECT * FROM empleados WHERE firstName LIKE %s;"
                        values = (fn, )
            else:
                if lastName != '' and sql == '':
                    if cellphone != '' and sql == '':
                        if email != '' and sql == '':
                            sql = "SELECT * FROM empleados WHERE lastName LIKE %s, cellphone LIKE %s, email LIKE %s;"
                            values = (ln, cph, em)
                        else:
                            sql = "SELECT * FROM empleados WHERE lastName LIKE %s, cellphone LIKE %s;"
                            values = (ln, cph)
                    else:
                        if email != '' and sql == '':
                            sql = "SELECT * FROM empleados WHERE lastName LIKE %s, email LIKE %s;"
                            values = (ln, em)
                        else:
                            sql = "SELECT * FROM empleados WHERE lastName LIKE %s;"
                            values = (ln, )
                else:
                    if cellphone != '' and sql == '':
                        if email != '' and sql == '':
                            sql = "SELECT * FROM empleados WHERE cellphone LIKE %s, email LIKE %s;"
                            values = (cph, em)
                        else:
                            sql = "SELECT * FROM empleados WHERE cellphone LIKE %s;"
                            values = (cph, )
                    else:
                        if email != '' and sql == '':
                            sql = "SELECT * FROM empleados WHERE email LIKE %s"
                            values = (em, )
            if sql != '':
                cursor.execute(sql, values)
                searchResult = cursor.fetchall()
                return render_template("search.html", contacts = searchResult, searchs = search) 
            else:
                return render_template("search.html")
    except Exception as e:
       print(e)
    finally:
       cursor.close()

@app.route('/searchPage', methods = ["GET"])
def rsearch():
    try:
        if request.method == "GET":
            return render_template('search.html')
    except Exception as e:
        print(e)
    finally:
        return render_template('search.html')

@app.route('/indexPage', methods = ["GET"])
def rindex():
    try:
        if request.method == "GET":
            return render_template('index.html')
    except Exception as e:
        print(e)
    finally:
        return render_template('index.html')

@app.route('/updatePage/<id>', methods = ["GET"])
def rupdate(id):
    try:
        if request.method == "GET":
            cursor = mydb.cursor()
            sql = 'SELECT * FROM  empleados WHERE id ='
            sql2 = sql + str(id)
            cursor.execute(sql2)
            contacts = cursor.fetchall()

            return render_template('update.html', contacts = contacts)
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/submitPage', methods = ["GET"])
def rsubmit():
    try:
        if request.method == "GET":
            return render_template('submit.html')
    except Exception as e:
        print(e)
    finally:
        return render_template('submit.html')
    
@app.route('/deletePage/<id>', methods = ["GET"])
def rdelete(id):
    try:
        if request.method == "GET":
            cursor = mydb.cursor()
            sql = 'SELECT * FROM  empleados WHERE id = '
            sql2 = sql + str(id)
            cursor.execute(sql2)
            contacts = cursor.fetchall()

            return render_template('delete.html', contacts = contacts)
    except Exception as e:
        print(e)
    finally:
        cursor.close()


if __name__ == "__main__":
    app.run()