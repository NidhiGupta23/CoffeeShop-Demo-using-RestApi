# File focuses on get, post, update and delete coffee details with rest-apis using flask
# create and activate virtual environment 
# { python -m venv .venv
#   set FLASK_APP=coffeeApi.py
#   flask run
#  }
# use postman for post and delete methods


from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/CofeeData.db'
app.config['SQLALCHEMY_BINDS'] = {'customer' : 'sqlite:///../database/CustomerData.db' , 
                                  'shop' : 'sqlite:///../database/ShopData.db' }

db = SQLAlchemy(app)

# For handling database
class CoffeeDetails(db.Model):
    COFFEE_ID = db.Column(db.Integer, primary_key=True)
    COFFEE_NAME = db.Column(db.String(50), unique=True)
    COFFEE_DESCRIPTION = db.Column(db.String(150))
    COFFEE_PRICE = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'{self.COFFEE_NAME} - {self.COFFEE_DESCRIPTION} - {self.COFFEE_PRICE}'
        

class CustomersData(db.Model):
    __bind_key__ = 'customer'
    CUSTOMER_ID = db.Column(db.Integer, primary_key=True)
    FIRST_NAME = db.Column(db.String(50))
    LAST_NAME = db.Column(db.String(50))
    CUSTOMER_EMAIL = db.Column(db.String(150), unique=True)
    PWD = db.Column(db.String(50))
    CREDIT = db.Column(db.Float)
    
    def __repr__(self):
        return f'{self.FIRST_NAME}  {self.LAST_NAME}'


class ShopData(db.Model):
    __bind_key__ = 'shop'
    BILL = db.Column(db.Float, nullable=False)
    CUSTOMER_EMAIL = db.Column(db.String(150))    
    CREDIT = db.Column(db.Float)
    CUSTOMER_ID = db.Column(db.Integer, nullable=False)
    FIRST_NAME = db.Column(db.String(50))    
    COFFEE_NAME = db.Column(db.String(50))
    DATE = db.Column(db.String, nullable=False)
    #DateTime, default=datetime.now().strftime('%Y-%m-%d'))
    EVENT_ID = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'{self.FIRST_NAME}  {self.CREDIT}  {self.DATE}'

# Starting page of the server
@app.route('/')
def index():
    db.create_all()
    return ('Welcome here to our coffee shop')

#######################################################################################################################
                     ########## IMPLEMENTING REST API FOR PRODUCT CUSTOMER ##########

# Get all customers details - GET METHOD
@app.route('/customerDetails', methods=['GET'])
def get_customerDetails():
    customers = CustomersData.query.all()
    output = []
    for customer in customers:
        details = {'CUSTOMER_ID': customer.CUSTOMER_ID, 'FIRST_NAME': customer.FIRST_NAME, 'LAST_NAME': customer.LAST_NAME, 'CUSTOMER_EMAIL': customer.CUSTOMER_EMAIL, 'PWD': customer.PWD, 'CREDIT': customer.CREDIT}
        output.append(details)    
    return {"Customers" : output}

# Add new customer into the database - POST METHOD
@app.route('/customerDetails', methods=['POST'])
def add_customerDetails():    
    customer = CustomersData(CUSTOMER_ID=request.json['CUSTOMER_ID'], FIRST_NAME=request.json['FIRST_NAME'], LAST_NAME=request.json['LAST_NAME'], CUSTOMER_EMAIL=request.json['CUSTOMER_EMAIL'], PWD=request.json['PWD'], CREDIT=request.json['CREDIT'])
    db.session.add(customer)
    db.session.commit()
    return {'CUSTOMER_ID': customer.CUSTOMER_ID}

# since put method is not supported in html so we will convert it into POST method
# update particular customer details - PUT METHOD
@app.route('/customerDetails/update', methods=['POST'])
def update_customerDetails():
    customer = CustomersData(CUSTOMER_ID=request.json['CUSTOMER_ID'], FIRST_NAME=request.json['FIRST_NAME'], LAST_NAME=request.json['LAST_NAME'], CUSTOMER_EMAIL=request.json['CUSTOMER_EMAIL'], PWD=request.json['PWD'], CREDIT=request.json['CREDIT'])
    
    db.session.add(customer)
    db.session.commit()
    return {'CUSTOMER_ID': customer.CUSTOMER_ID}


# update particular customer details - PUT METHOD
@app.route('/customerDetails/<id>', methods=['PUT'])
def update_customerDetail(id):
    customer = CustomersData.query.get(id)
    customer['FIRST_NAME'] = request.json['FIRST_NAME']
    customer['LAST_NAME'] = request.json['LAST_NAME']
    customer['CUSTOMER_EMAIL'] = request.json['CUSTOMER_EMAIL']
    customer['PWD'] = request.json['PWD']
    customer['CREDIT'] = request.json['CREDIT']
    db.session.commit()
    return {'CUSTOMER_ID': customer['CUSTOMER_ID'], 'FIRST_NAME': customer['FIRST_NAME'], 'LAST_NAME': customer['LAST_NAME'], 'CUSTOMER_EMAIL': customer['CUSTOMER_EMAIL'], 'CREDIT': customer['CREDIT']}

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
    return {'CUSTOMER_ID': customer.CUSTOMER_ID, 'FIRST_NAME': customer.FIRST_NAME, 'LAST_NAME': customer.LAST_NAME, 'CUSTOMER_EMAIL': customer.CUSTOMER_EMAIL, 'PWD': customer.PWD, 'CREDIT': customer.CREDIT}

#######################################################################################################################
                       ########## IMPLEMENTING REST API FOR PRODUCT COFFEE ##########

# get all coffee details from the database - GET METHOD
@app.route('/coffeeDetails', methods=['GET'])
def get_coffeeDetails():
    coffeeD = CoffeeDetails.query.all()
    output = []
    for coffee in coffeeD:
        details = {'COFFEE_ID': coffee.COFFEE_ID, 'COFFEE_NAME': coffee.COFFEE_NAME, 'COFFEE_DESCRIPTION': coffee.COFFEE_DESCRIPTION, 'COFFEE_PRICE': coffee.COFFEE_PRICE}
        output.append(details)    
    return {"coffee" : output}

# add coffee details into the database - POST METHOD
@app.route('/coffeeDetails', methods=['POST'])
def add_coffeeDetails():
    coffeeD = CoffeeDetails(COFFEE_NAME=request.json['COFFEE_NAME'], COFFEE_DESCRIPTION=request.json['COFFEE_DESCRIPTION'], COFFEE_PRICE=request.json['COFFEE_PRICE'])
    db.session.add(coffeeD)
    db.session.commit()
    return {'COFFEE_ID': coffeeD.COFFEE_ID}

# update the details of particular coffee - PUT METHOD
@app.route('/coffeeDetails/update', methods=['POST'])
def update_coffeeDetail():
    coffee = CoffeeDetails(COFFEE_ID=request.json['COFFEE_ID'], COFFEE_NAME=request.json['COFFEE_NAME'], COFFEE_DESCRIPTION=request.json['COFFEE_DESCRIPTION'], COFFEE_PRICE=request.json['COFFEE_PRICE'])
    db.session.add(coffee)
    db.session.commit()
    return {'COFFEE_ID': coffee.COFFEE_ID}

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
    return {'COFFEE_ID': coffeeD.COFFEE_ID, 'COFFEE_NAME': coffeeD.COFFEE_NAME, 'COFFEE_DESCRIPTION': coffeeD.COFFEE_DESCRIPTION, 'COFFEE_PRICE': coffeeD.COFFEE_PRICE}


#######################################################################################################################
            ########## IMPLEMENTING REST API FOR SETTING AND GETTING CUSTOMERS DETAILS IN SHOP ##########

# Get all events - GET METHOD
@app.route('/shopDetails', methods=['GET'])
def get_shopEvents():
    shopData = ShopData.query.all()
    output = []
    for event in shopData:
        details = {'EVENT_ID': event.EVENT_ID, 'DATE': event.DATE, 'FIRST_NAME': event.FIRST_NAME, 'CUSTOMER_EMAIL': event.CUSTOMER_EMAIL, 'CREDIT': event.CREDIT, 'BILL': event.BILL, 'COFFEE_NAME': event.COFFEE_NAME, 'CUSTOMER_ID': event.CUSTOMER_ID}
        output.append(details)    
    return {"ShopEvents" : output}

# Add new event into the database - POST METHOD
@app.route('/shopDetails', methods=['POST'])
def add_shopEvent():
    event = ShopData(FIRST_NAME=request.json['FIRST_NAME'], CUSTOMER_EMAIL=request.json['CUSTOMER_EMAIL'], CREDIT=request.json['CREDIT'], BILL=request.json['BILL'], COFFEE_NAME=request.json['COFFEE_NAME'], CUSTOMER_ID=request.json['CUSTOMER_ID'], DATE=str(datetime.now().strftime('%Y-%m-%d')))
    db.session.add(event)
    db.session.commit()
    return {'EVENT_ID': event.EVENT_ID}

# display specific event
@app.route('/shopDetails/<id>')
def get_specificEvent(id):
    event = ShopData.query.get_or_404(id)
    return {'EVENT_ID': event.EVENT_ID, 'DATE': event.DATE, 'FIRST_NAME': event.FIRST_NAME,  'CREDIT': event.CREDIT, 'BILL': event.BILL, 'COFFEE_NAME': event.COFFEE_NAME}

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
        details = {'EVENT_ID': event.EVENT_ID, 'CUSTOMER_EMAIL': event.CUSTOMER_EMAIL, 'CREDIT': event.CREDIT, 'CUSTOMER_ID': event.CUSTOMER_ID}
        output.append(details)    
    return {"ShopEvents" : output}