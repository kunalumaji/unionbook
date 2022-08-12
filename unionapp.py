from re import template
from flask import Flask,render_template
from db_config import *
import psycopg2
# import json
# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

connection = psycopg2.connect(
        host = DB_HOST,
        user = DB_USER,
        dbname = DB_NAME,
        password = DB_PASS,
        port = DB_PORT
    )
cursor = connection.cursor()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<contact>')
def hello_world(contact):
    if not connection:
        return "Fail to connect to Database"
    else:
        pass
    pending_bill_query = '''SELECT * FROM pending_bills WHERE "Customer"='%s' AND "Bill amount" IS NOT NULL ''' % (contact)
    cursor.execute(pending_bill_query)
    pending_bill = cursor.fetchone()
    if pending_bill:
        fetch_transactions_query = '''SELECT * FROM bill_transactions WHERE "Bill no"=%s order by "Date" ''' % (pending_bill[0])
        cursor.execute(fetch_transactions_query)
        transactions = cursor.fetchall()
    else:
        pending_bill = None
        transactions = None
    result = {
        'invoice': pending_bill,
        'transactions': transactions
    }
    return render_template("invoice.html",data=result)

if __name__ == "__main__":
    app.run(debug=True)