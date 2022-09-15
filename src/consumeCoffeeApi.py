from asyncio.windows_events import NULL
from sqlite3 import Timestamp
from tkinter import E
import requests  as req


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
        coffeeDetail = req.post(self.coffeeAp, json = {'cName' : cName, 'description': description, 'price': price})
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
        customerDetails = req.post(self.customerApi, json = {'fname': fname, 'lname': lname, 'email': email, 'pwd':pwd, 'credit': credit})
        return customerDetails.text


    def putCustomerDetail(self, id, newCredit, activity):
        customerDetails = self.getSpecificCustomer(id)
        #print(customerDetails)
        deletedcustomer = self.deleteCustomerDetail(id)
        #print(deletedcustomer)
        if deletedcustomer:
            if activity == 1:
                response = req.post(self.updatecustomerApi, json={'id': customerDetails['id'], 'fname': customerDetails['fname'], 'lname': customerDetails['lname'], 'email': customerDetails['email'], 'pwd': customerDetails['pwd'], 'credit': newCredit})
                if response is not NULL:
                    return True
                else:
                    return False
            elif activity == 2:
                response = req.post(self.updatecustomerApi, json={'id': customerDetails['id'], 'fname': customerDetails['fname'], 'lname': customerDetails['lname'], 'email': customerDetails['email'], 'pwd': customerDetails['pwd'], 'credit': customerDetails['credit'] + newCredit})
                if response is not NULL:
                    return True
                else:
                    return False
            else:
                response = req.post(self.updatecustomerApi, json={'id': customerDetails['id'], 'fname': customerDetails['fname'], 'lname': customerDetails['lname'], 'email': customerDetails['email'], 'pwd': customerDetails['pwd'], 'credit': customerDetails['credit']})
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
        eventDetails = req.post(self.shopApi, json = {'fname': details['fname'], 'email': details['email'], 'credit': details['credit'], 'bill': details['cPrice'], 'cName': details['cName'], 'cOrder': details['cOrder'] })
        print(eventDetails.text)
        return eventDetails.text

    # delete specific event
    def deleteEventDetail(self, id):
        try:
            req.delete(self.shopApi + "/" + str(id))
            return True
        except:
            return ("Error : Not Found")