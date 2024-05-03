from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import os
from dotenv import load_dotenv, dotenv_values

app = Flask(__name__)

load_dotenv()

connString = os.getenv('AZ_CONN_STRING')

sqlDBConn = pyodbc.connect(
    connString
)

@app.route('/')
def index():
    print(connString)
    cursor = sqlDBConn.cursor()
    customers = cursor.execute("select * from TblCustomers order by CustomerID Desc").fetchall()
    return render_template('index.html', customers = customers)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create/', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        name = request.form['customerName']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        comments = request.form['comments']
        cursor = sqlDBConn.cursor()
        cursor.execute("Insert Into TblCustomers(CustomerName,Address,City,Comments,State) values(?,?,?,?,?)",
                (name,address, city,comments,state))
        sqlDBConn.commit()
        return redirect(url_for('index'))
    else:
        return render_template('create.html')

@app.route('/update/<int:id>/')
def update(id):
    if id == 0:
        return redirect(url_for('index'))
    else:
        cursor = sqlDBConn.cursor()
        customer = cursor.execute("select * from TblCustomers where customerid = ?",id).fetchall()
        return render_template('update.html', customer = customer)
    
@app.route('/updateData/', methods=['POST'])
def updateData():
    if request.method == 'POST':
        id = request.form['customerID']
        name = request.form['customerName']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        comments = request.form['comments']
        cursor = sqlDBConn.cursor()
        cursor.execute("Update TblCustomers Set CustomerName = ?,Address = ?,City = ?,Comments = ?,State = ? where customerid = ?",
                (name,address, city,comments,state,id))
        sqlDBConn.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
if __name__ == "__main__":
    app.run()