from asyncio.windows_events import NULL
import requests  as req
from random import randrange


class consumeCoffeeApi:
    def __init__(self):
        self.customerApi = "http://127.0.0.1:5000/customerDetails"
        self.coffeeAp = "http://127.0.0.1:5000/coffeeDetails"
        self.updatecustomerApi = "http://127.0.0.1:5000/customerDetails/update"
        self.shopApi = "http://127.0.0.1:5000/shopDetails"
        
    ######################################################################################################################
                       ########## IMPLEMENTING FUNCTIONS TO CONSUME REST API FOR PRODUCT COFFEE ##########

    def getCoffeeDetails(self):
        coffeeDetail = req.get(self.coffeeAp)
        return coffeeDetail.json()

    def postCoffeeDetails(self):
        cName = input('Coffee name : ')
        description = input('Descripton of the coffee : ') 
        price = input("Price of the coffee : ")
        coffeeDetail = req.post(self.coffeeAp, json = {'COFFEE_NAME' : cName, 'COFFEE_DESCRIPTION': description, 'COFFEE_PRICE': price})
        return coffeeDetail.json()

    def updateCoffeeDetails(self, id, field, value):
        coffeeDetails = self.getSpecificCoffeeDetail(id)
        deletedcoffee = self.deleteCoffeeDetail(id)
        if deletedcoffee:
            if field == 'price':
                response =  req.post(self.coffeeAp, json={'COFFEE_ID': coffeeDetails['COFFEE_ID'], 'COFFEE_NAME':coffeeDetails['COFFEE_NAME'] , 'COFFEE_DESCRIPTION': coffeeDetails['COFFEE_DESCRIPTION'], 'COFFEE_PRICE': value})
            elif field == 'description':
                response =  req.post(self.coffeeAp, json={'COFFEE_ID': coffeeDetails['COFFEE_ID'], 'COFFEE_NAME':coffeeDetails['COFFEE_NAME'] , 'COFFEE_DESCRIPTION': value, 'COFFEE_PRICE': coffeeDetails['COFFEE_PRICE']})
            else:
                response =  req.post(self.coffeeAp, json={'COFFEE_ID': coffeeDetails['COFFEE_ID'], 'COFFEE_NAME':coffeeDetails['COFFEE_NAME'] , 'COFFEE_DESCRIPTION': coffeeDetails['COFFEE_DESCRIPTION'], 'COFFEE_PRICE': coffeeDetails['COFFEE_PRICE']})
        
            if response is not NULL:
                return True
            else:
                return False
        else:
            return False

    def getSpecificCoffeeDetail(self, id):
        coffeeDetail = req.get(self.coffeeAp + "/" + str(id))
        return coffeeDetail.json()

    def deleteCoffeeDetail(self, id):
        try:
            req.delete(self.coffeeAp + "/" + str(id))
            return True
        except:
            return ("Error : Not Found")



    ######################################################################################################################
                       ########## IMPLEMENTING FUNCTIONS TO CONSUME REST API FOR PRODUCT CUSTOMER ##########


    def getCustomerDetails(self):
        customerDetails = req.get(self.customerApi)
        return customerDetails.json()

    def getSpecificCustomer(self, id):
        customerDetails = req.get(self.customerApi + "/" + str(id))
        return customerDetails.json()

    def postCustomerDetails(self):
            
        fname = input("Enter First Name and press enter  ")
        print("First Name: ", fname)
        lname = input("Enter Last Name and press enter : ")
        print("Last Name: ", lname)
        email = input("Enter EMail and press enter : ")
        print("EMail: ", email)
        pwd = input("Enter 8 digit Password and press enter : ")
        print("Password: ", pwd)
        credit = float(input("Enter Credit and press enter : "))
        print("Credit: ", credit)      

        customer_id = randrange(000000, 999999)
        customerDetails = req.post(self.customerApi, json = {'CUSTOMER_ID':customer_id,'FIRST_NAME': fname, 'LAST_NAME': lname, 'CUSTOMER_EMAIL': email, 'PWD':pwd, 'CREDIT': credit})
        return customerDetails.json()
        

    def modifyCustomerDetails(self, id, field, newValue, activity=None):
        customerDetails = self.getSpecificCustomer(id)
        deletedcustomer = self.deleteCustomerDetail(id)
        if deletedcustomer:
            if field == 'FN':
                response = req.post(self.updatecustomerApi, json={'CUSTOMER_ID': customerDetails['CUSTOMER_ID'], 'FIRST_NAME': newValue, 'LAST_NAME': customerDetails['LAST_NAME'], 'CUSTOMER_EMAIL': customerDetails['CUSTOMER_EMAIL'], 'PWD': customerDetails['PWD'], 'CREDIT': customerDetails['CREDIT']})
            elif field == 'LN':
                response = req.post(self.updatecustomerApi, json={'CUSTOMER_ID': customerDetails['CUSTOMER_ID'], 'FIRST_NAME': customerDetails['FIRST_NAME'], 'LAST_NAME': newValue, 'CUSTOMER_EMAIL': customerDetails['CUSTOMER_EMAIL'], 'PWD': customerDetails['PWD'], 'CREDIT': customerDetails['CREDIT']})
            elif field == 'EL':
                response = req.post(self.updatecustomerApi, json={'CUSTOMER_ID': customerDetails['CUSTOMER_ID'], 'FIRST_NAME': customerDetails['FIRST_NAME'], 'LAST_NAME': customerDetails['LAST_NAME'], 'CUSTOMER_EMAIL': newValue, 'PWD': customerDetails['PWD'], 'CREDIT': customerDetails['CREDIT']})
            elif field == 'PD':
                response = req.post(self.updatecustomerApi, json={'CUSTOMER_ID': customerDetails['CUSTOMER_ID'], 'FIRST_NAME': customerDetails['FIRST_NAME'], 'LAST_NAME': customerDetails['LAST_NAME'], 'CUSTOMER_EMAIL': customerDetails['CUSTOMER_EMAIL'], 'PWD': newValue, 'CREDIT': customerDetails['CREDIT']})
            elif field == 'CD':
                if activity == 1:
                    response = req.post(self.updatecustomerApi, json={'CUSTOMER_ID': customerDetails['CUSTOMER_ID'], 'FIRST_NAME': customerDetails['FIRST_NAME'], 'LAST_NAME': customerDetails['LAST_NAME'], 'CUSTOMER_EMAIL': customerDetails['CUSTOMER_EMAIL'], 'PWD': customerDetails['PWD'], 'CREDIT': newValue})
                elif activity == 2:
                    response = req.post(self.updatecustomerApi, json={'CUSTOMER_ID': customerDetails['CUSTOMER_ID'], 'FIRST_NAME': customerDetails['FIRST_NAME'], 'LAST_NAME': customerDetails['LAST_NAME'], 'CUSTOMER_EMAIL': customerDetails['CUSTOMER_EMAIL'], 'PWD': customerDetails['PWD'], 'CREDIT': customerDetails['CREDIT'] + newValue})
                else:
                    response = req.post(self.updatecustomerApi, json={'CUSTOMER_ID': customerDetails['CUSTOMER_ID'], 'FIRST_NAME': customerDetails['FIRST_NAME'], 'LAST_NAME': customerDetails['LAST_NAME'], 'CUSTOMER_EMAIL': customerDetails['CUSTOMER_EMAIL'], 'PWD': customerDetails['PWD'], 'CREDIT': customerDetails['CREDIT']})
            else:
                response = req.post(self.updatecustomerApi, json={'CUSTOMER_ID': customerDetails['CUSTOMER_ID'], 'FIRST_NAME': customerDetails['FIRST_NAME'], 'LAST_NAME': customerDetails['LAST_NAME'], 'CUSTOMER_EMAIL': customerDetails['CUSTOMER_EMAIL'], 'PWD': customerDetails['PWD'], 'CREDIT': customerDetails['CREDIT']})

            if response is not NULL:
                return True
            else:
                return False
        else:
            return False
       
       
    # delete specific customer
    def deleteCustomerDetail(self, id):
        try:
            req.delete(self.customerApi + "/" + str(id))
            return True
        except:
            return ("Error : Not Found")


######################################################################################################################
  ########## IMPLEMENTING FUNCTIONS TO CONSUME REST API FOR SETTING AND GETTING CUSTOMERS DETAILS IN SHOP ##########

    def getEventsDetails(self):
        eventDetails = req.get(self.shopApi)
        return eventDetails.json()

    def getSpecificEvent(self, id):
        eventDetails = req.get(self.shopApi + "/" + str(id+1))
        return eventDetails.json()

    def postEventDetails(self, details):
        eventDetails = req.post(self.shopApi, json = {'FIRST_NAME': details['FIRST_NAME'], 'CUSTOMER_EMAIL': details['CUSTOMER_EMAIL'], 'CREDIT': details['CREDIT'], 'BILL': details['COFFEE_PRICE'], 'COFFEE_NAME': details['COFFEE_NAME'], 'CUSTOMER_ID': details['CUSTOMER_ID'] })
        #print(eventDetails.text)
        return eventDetails.text

    # delete specific event
    def deleteEventDetail(self, id):
        try:
            req.delete(self.shopApi + "/" + str(id))
            return True
        except:
            return ("Error : Not Found")