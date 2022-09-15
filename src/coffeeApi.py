# File focuses on get, post, update and delete coffee details with rest-apis using flask
# create and activate virtual environment 
# { python -m venv .venv
#   set FLASK_APP=coffeeApi.py
#   flask run
#  }
# use postman for post and delete methods


from datetime import datetime
from email.policy import default
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/CoffeeData.db'
app.config['SQLALCHEMY_BINDS'] = {'customer' : 'sqlite:///../database/CustomersData.db' , 
                                  'shop' : 'sqlite:///../database/ShopData.db' }

db = SQLAlchemy(app)

# For handling database
class CoffeeDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cName = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(150))
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'{self.cName} - {self.description} - {self.price}'
        

class CustomersData(db.Model):
    __bind_key__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True)
    pwd = db.Column(db.String(50))
    credit = db.Column(db.Float)
    
    def __repr__(self):
        return f'{self.fname}  {self.lname}'


class ShopData(db.Model):
    __bind_key__ = 'shop'
    bill = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(150))    
    credit = db.Column(db.Float)
    cName = db.Column(db.String(50))    
    fname = db.Column(db.String(50))
    cOrder = db.Column(db.Integer, nullable=False)
    timeStamp = db.Column(db.String, nullable=False)
    #DateTime, default=datetime.now().strftime('%Y-%m-%d'))
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'{self.fname}  {self.credit}  {self.timeStamp}'

# Starting page of the server
@app.route('/')
def index():
    return ('Welcome here to our coffee shop')

#######################################################################################################################
                     ########## IMPLEMENTING REST API FOR PRODUCT CUSTOMER ##########

# Get all customers details - GET METHOD
@app.route('/customerDetails', methods=['GET'])
def get_customerDetails():
    customers = CustomersData.query.all()
    output = []
    for customer in customers:
        details = {'id': customer.id, 'fname': customer.fname, 'lname': customer.lname, 'email': customer.email, 'credit': customer.credit}
        output.append(details)    
    return {"Customers" : output}

# Add new customer into the database - POST METHOD
@app.route('/customerDetails', methods=['POST'])
def add_customerDetails():
    customer = CustomersData(fname=request.json['fname'], lname=request.json['lname'], email=request.json['email'], pwd=request.json['pwd'], credit=request.json['credit'])
    db.session.add(customer)
    db.session.commit()
    return {'id': customer.id}

# since put method is not supported in html so we will convert it into POST method
# update particular customer details - PUT METHOD
@app.route('/customerDetails/update', methods=['POST'])
def update_customerDetails():
    customer = CustomersData(id=request.json['id'], fname=request.json['fname'], lname=request.json['lname'], email=request.json['email'], pwd=request.json['pwd'], credit=request.json['credit'])
    db.session.add(customer)
    db.session.commit()
    return {'id': customer.id}


# update particular customer details - PUT METHOD
@app.route('/customerDetails/<id>', methods=['PUT'])
def update_customerDetail(id):
    customer = CustomersData.query.get(id)
    customer['fname'] = request.json['fname']
    customer['lname'] = request.json['lname']
    customer['email'] = request.json['email']
    customer['pwd'] = request.json['pwd']
    customer['credit'] = request.json['credit']
    db.session.commit()
    return {'id': customer['id'], 'fname': customer['fname'], 'lname': customer['lname'], 'email': customer['email'], 'credit': customer['credit']}

# delete a particular customer - DELETE METHOD
@app.route('/customerDetails/<id>', methods=['DELETE'])
def delete_customerDetail(id):
    customer = CustomersData.query.get(id)    
    if customer is None:
        return {'error': 'customer does not exists'}
    db.session.delete(customer)
    db.session.commit()
    return {'message': 'deletion successful'}

# display details of specific customer
@app.route('/customerDetails/<id>')
def get_customDetail(id):
    customer = CustomersData.query.get_or_404(id)
    return {'id': customer.id, 'fname': customer.fname, 'lname': customer.lname, 'email': customer.email, 'pwd': customer.pwd, 'credit': customer.credit}

#######################################################################################################################
                       ########## IMPLEMENTING REST API FOR PRODUCT COFFEE ##########

# get all coffee details from the database - GET METHOD
@app.route('/coffeeDetails', methods=['GET'])
def get_coffeeDetails():
    coffeeD = CoffeeDetails.query.all()
    output = []
    for coffee in coffeeD:
        details = {'id': coffee.id, 'cName': coffee.cName, 'description': coffee.description, 'price': coffee.price}
        output.append(details)    
    return {"coffee" : output}

# add coffee details into the database - POST METHOD
@app.route('/coffeeDetails', methods=['POST'])
def add_coffeeDetails():
    coffeeD = CoffeeDetails(cName=request.json['cName'], description=request.json['description'], price=request.json['price'])
    db.session.add(coffeeD)
    db.session.commit()
    return {'id': coffeeD.id}

# update the details of particular coffee - PUT METHOD
@app.route('/coffeeDetails/<id>', methods=['PUT'])
def update_coffeeDetail(id):
    coffeeD = CoffeeDetails.query.get(id)
    coffeeD.cName = request.json['cName']
    coffeeD.description = request.json['description']
    coffeeD.price = request.json['price']
    db.session.commit()
    return {'id': coffeeD.id, 'cName': coffeeD.cName, 'description': coffeeD.description, 'price': coffeeD.price}

# delete a particular coffee - DELETE METHOD
@app.route('/coffeeDetails/<id>', methods=['DELETE'])
def delete_coffeeDetail(id):
    coffeeD = CoffeeDetails.query.get(id)    
    if coffeeD is None:
        return {'error': 'coffee does not exists'}
    db.session.delete(coffeeD)
    db.session.commit()
    return {'message': 'deletion successful'}

# display details of specific coffee
@app.route('/coffeeDetails/<id>')
def get_coffeeDetail(id):
    coffeeD = CoffeeDetails.query.get_or_404(id)
    return {'id': coffeeD.id, 'cName': coffeeD.cName, 'description': coffeeD.description, 'price': coffeeD.price}


#######################################################################################################################
            ########## IMPLEMENTING REST API FOR SETTING AND GETTING CUSTOMERS DETAILS IN SHOP ##########

# Get all events - GET METHOD
@app.route('/shopDetails', methods=['GET'])
def get_shopEvents():
    shopData = ShopData.query.all()
    output = []
    for event in shopData:
        details = {'id': event.id, 'timeStamp': event.timeStamp, 'fname': event.fname, 'email': event.email, 'credit': event.credit, 'bill': event.bill, 'cName': event.cName, 'cOrder': event.cOrder}
        output.append(details)    
    return {"ShopEvents" : output}

# Add new event into the database - POST METHOD
@app.route('/shopDetails', methods=['POST'])
def add_shopEvent():
    event = ShopData(fname=request.json['fname'], email=request.json['email'], credit=request.json['credit'], bill=request.json['bill'], cName=request.json['cName'], cOrder=request.json['cOrder'], timeStamp=str(datetime.now().strftime('%Y-%m-%d')))
    db.session.add(event)
    db.session.commit()
    return {'id': event.id}

# display specific event
@app.route('/shopDetails/<id>')
def get_specificEvent(id):
    event = ShopData.query.get_or_404(id)
    return {'id': event.id, 'timeStamp': event.timeStamp, 'fname': event.fname,  'credit': event.credit, 'bill': event.bill, 'cName': event.cName}

# delete a particular event - DELETE METHOD
@app.route('/shopDetails/<id>', methods=['DELETE'])
def delete_specificEvent(id):
    event = ShopData.query.get(id)    
    if event is None:
        return {'error': 'customer does not exists'}
    db.session.delete(event)
    db.session.commit()
    return {'message': 'deletion successful'}


# Testing Api - GET METHOD
@app.route('/shopDetail', methods=['GET'])
def get_shopEvent():
    shopData = ShopData.query.all()
    output = []
    for event in shopData:
        details = {'id': event.id, 'email': event.email, 'credit': event.credit, 'cOrder': event.cOrder}
        output.append(details)    
    return {"ShopEvents" : output}