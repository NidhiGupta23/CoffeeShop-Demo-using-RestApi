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
        fname = input("Enter First Name and press enter : ")
        lname = input("Enter Last Name and press enter : ")
        email = input("Enter EMail and press enter : ")
        pwd = input("Enter 8 digit Password and press enter : ")
        credit = float(input("Enter Credit and press enter : "))
        customer_id = randrange(000000, 999999)
        customerDetails = req.post(self.customerApi, json = {'CUSTOMER_ID':customer_id,'FIRST_NAME': fname, 'LAST_NAME': lname, 'CUSTOMER_EMAIL': email, 'PWD':pwd, 'CREDIT': credit})
        return customerDetails.json()


    def putCustomerDetail(self, id, newCredit, activity):
        customerDetails = self.getSpecificCustomer(id)
        #print(customerDetails)
        deletedcustomer = self.deleteCustomerDetail(id)
        #print(deletedcustomer)
        if deletedcustomer:
            if activity == 1:
                response = req.post(self.updatecustomerApi, json={'CUSTOMER_ID': customerDetails['CUSTOMER_ID'], 'FIRST_NAME': customerDetails['FIRST_NAME'], 'LAST_NAME': customerDetails['LAST_NAME'], 'CUSTOMER_EMAIL': customerDetails['CUSTOMER_EMAIL'], 'PWD': customerDetails['PWD'], 'CREDIT': newCredit})
                if response is not NULL:
                    return True
                else:
                    return False
            elif activity == 2:
                response = req.post(self.updatecustomerApi, json={'CUSTOMER_ID': customerDetails['CUSTOMER_ID'], 'FIRST_NAME': customerDetails['FIRST_NAME'], 'LAST_NAME': customerDetails['LAST_NAME'], 'CUSTOMER_EMAIL': customerDetails['CUSTOMER_EMAIL'], 'PWD': customerDetails['PWD'], 'CREDIT': customerDetails['CREDIT'] + newCredit})
                if response is not NULL:
                    return True
                else:
                    return False
            else:
                response = req.post(self.updatecustomerApi, json={'CUSTOMER_ID': customerDetails['CUSTOMER_ID'], 'FIRST_NAME': customerDetails['FIRST_NAME'], 'LAST_NAME': customerDetails['LAST_NAME'], 'CUSTOMER_EMAIL': customerDetails['CUSTOMER_EMAIL'], 'PWD': customerDetails['PWD'], 'CREDIT': customerDetails['CREDIT']})
                if response is not NULL:
                    return True
                else:
                    return False
        else:
            return False
       

    def modifyCustomerDetails(self, id, field, newValue):
        customerDetails = self.getSpecificCustomer(id)
        deletedcustomer = self.deleteCustomerDetail(id)
        if deletedcustomer:
            if field == 'FN':
                pass
            elif field == 'LN':
                pass
            elif field == 'EMail':
                pass
            elif field == 'PWD':
                pass
            elif field == 'CREDIT':
                pass

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