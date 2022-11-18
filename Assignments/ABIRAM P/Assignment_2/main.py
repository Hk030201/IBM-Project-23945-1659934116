from flask import Flask,render_template #package or module importing
from flask import Flask
from flask import request, redirect, url_for, render_template
import ibm_db
app = Flask(__name__) #flask running procedure
db_connection = ibm_db.connect("DATABASE=bludb;QUERYTIMEOUT=1;CONNECTTIMEOUT=10;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=./DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=gxm80926;PWD=trAQThC2HeR1Vyqk", "", "")
#routing concept using render template---
@app.route('/')
def home():
    return render_template("index.html")
@app.route('/blog')
def blog():
    return render_template("blog.html")
@app.route('/login',methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        sql_query = "SELECT password from Users WHERE EMAILID = '{}'".format(data["user"])
        result = ibm_db.exec_immediate(db_connection,sql_query)
        print(result)
        value = ibm_db.fetch_tuple(result)
        if value == data["password"]:
            return redirect(url_for("blog.html"))
        else:
            return "<p style=color:red;>Invalid Credentials</p>"
    if request.method == "GET":
        return render_template("login.html")

@app.route('/register',methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        sql_query = "INSERT INTO USERS (NAME,EMAILID,PASSWORD,MOBILENUMBER) VALUES('{}','{}','{}','{}')".format(data["username"], data["email"], data["password"], data["mobilenumber"])
        ibm_db.exec_immediate(db_connection,sql_query)
        return redirect(url_for("login"))
    if request.method == "GET":
        return render_template("register.html")

#end of routing 
if __name__ == "__main__":
    app.run(debug=True)