import requests  as req
import json


class consumeCoffeeApi:
    def __init__(self):
        self.customerApi = "http://127.0.0.1:5000/customerDetails"
        self.coffeeAp = "http://127.0.0.1:5000/coffeeDetails"
        
        
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
            coffeeDetail =  req.delete(self.coffeeAp + "/" + str(id))
            return (coffeeDetail)
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

    def putCustomerDetail(self, id, newCredit):
        customerDetails = self.getSpecificCustomer(id)        
        # credit = customerDetails.credit - bill
        # 'id': customerDetails.id,
        print("We got following details : ", customerDetails)
        response = req.put(self.customerApi, json={'fname': customerDetails['fname'], 'lname': customerDetails['lname'], 'email': customerDetails['email'], 'pwd': customerDetails['pwd'], 'credit': newCredit})
        
        print("Checking if succeess...")       
        
        return response.text