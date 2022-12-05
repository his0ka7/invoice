from flask import Flask
from flask import render_template, request, redirect, session,url_for
from flask_sqlalchemy import SQLAlchemy

folder_name ="static"


app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///uwu.db"
app.config["SQLALCHEMY_TRACK_MODIFICAIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = '123456dlolyanegm'

class Invoice(db.Model):
    __tablename__="invoice_tbl"
    invoiceID = db.Column(db.Integer, primary_key=True)
    invoiceData = db.Column(db.DateTime(), nullable=False)
    totAmt = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    taxAmt = db.Column(db.Integer, nullable=True)
    netAmt = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.Integer, nullable=True)
    
class InvoiceDet(db.Model):
    __tablename__="invoiceDet_tbl"
    invoiceID = db.Column(db.Integer, primary_key=True)
    ItemID = db.Column(db.Integer, db.ForeignKey("Items_tbl.itemID"), primary_key=True)
    itemQty = db.Column(db.Integer, nullable=False)
    item_discount = db.Column(db.Integer, nullable=False)
    itemAmt = db.Column(db.Integer, nullable=True)
    item = db.relationship("Items", backref="item", lazy=True)
    
class Users(db.Model):
    __tablename__="usertbl"
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    

class Items(db.Model):
    __tablename__="Items_tbl"
    itemID = db.Column(db.Integer, primary_key=True)
    itemDesc = db.Column(db.String(), nullable=False)
    itemPrice = db.Column(db.Integer, nullable=False)
    
    


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard",methods=["POST"])
def dashboard():
    unam = request.form.get("username")
    pwd = request.form.get("password")
    session['username'] = unam
    ulist= Users.query.filter_by(username=unam).first()
    if ulist:
        uid=ulist.userid
        invList=Invoice.query.filter_by(userid=uid).all()
        return redirect(url_for("dashboard"), unam=unam,invList=invList, invDet=[], invsel=[])
    else:
        return render_template("index.html", msg='Wrnog Credentials!!')
    
@app.route("/showInvoice/<int:invID>")
def showInvoice(invID):
    unam=session['username']
    ulist=Users.query.filter_by(username=unam).first()
    invList=Invoice.query.filter_by(userid=ulist.userid).all()
    invDet=InvoiceDet.query.filter_by(invoiceID=invID).all()
    invSel =Invoice.query.filter_by(invoiceID=invID).first()
    return render_template("dashboard.html",unam=unam, invList=invList, invDet=invDet, invSel=invSel)

@app.route("")

@app.route("/logout")
def logout():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port= 3030)