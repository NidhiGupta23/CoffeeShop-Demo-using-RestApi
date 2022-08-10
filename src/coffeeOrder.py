import json as js
import pprint as pp
import pandas as pd
import consumeCoffeeApi as consumer

class coffeeOrder:

    def __init__(self):
        self.cs = consumer.consumeCoffeeApi()
        self.coffee =  self.cs.getCoffeeDetails()
        self.customer = self.cs.getCustomerDetails()

    # Display the coffee shop logo
    def welcome_page(self):
        print("########################################################################################################################")
        print("########################################################################################################################")
        print("                     ####  ####  #####  #####  #####  #####       ####  #  #  ####  ####  ")
        print("                     #     #  #  #      #      #      #           #     #  #  #  #  #  #  ")
        print("                     #     #  #  ###    ###    ###    ####        ####  ####  #  #  ####  ")
        print("                     #     #  #  #      #      #      #              #  #  #  #  #  #     ")
        print("                     ####  ####  #      #      #####  #####       ####  #  #  ####  #     ")
        print("########################################################################################################################")
        print("########################################################################################################################")

   
    # Display the coffee menu
    def viewMenu(self):
        print(pd.DataFrame(self.coffee.get('coffee')))

    # Display specific coffee
    def viewSpecificCoffee(self, id):
        self.cs.getSpecificCoffeeDetail(id) 

    # select coffee type
    def selectCoffee(self):
        coffeeType = int(input("Have you choosed your desired coffee? If yes, press the id number :   "))
        try:
            print("You selected coffee")
            pp.pprint(self.coffee.get('coffee')[coffeeType-1].get('cName'))
            return self.coffee.get('coffee')[coffeeType-1]
        except IndexError as ie:
            print("Sorry, wrong option choosed, try again...")
            exit

    # Check for customer authentication using password 
    def checkPwd(self, cid, cpwd):
        scustomer = self.cs.getSpecificCustomer(cid)
        status = False
        if cpwd == scustomer.get('pwd'):
               status = True

        return status

    # Get credit check and return status
    def placeOrder(self, loginId, coffeePrice):
        customerCredit = self.customer.get('Customers')[loginId].get('credit')
        status = False
        if customerCredit > coffeePrice:
            customerCredit = customerCredit - coffeePrice
            status = True
            
        return [status, customerCredit]


    # Get the id of the customer using email provided
    def getCustomerID(self, cemail):
        cid = 0
        for i in range(len(self.customer.get('Customers'))):
            if cemail == self.customer.get('Customers')[i+1].get('email'):
                cid = i+1
                break
            
        return cid


    def order(self):
        orderId = 1
        coffee = self.selectCoffee()
        coffeePrice = coffee.get('price')
        print("Its a great choice for a great day :) ")
        cemail = input("Enter email address :  ")
        loginId =  self.getCustomerID(cemail)
        if loginId == 0:
            print("Enter correct email ID")
            exit
        else:
            cpwd = input("Enter the password :  ")
            status = self.checkPwd(loginId, cpwd) 
            if status == False:
                print("Wrong password : ")
                exit
            else:
                print("Checking the credit...Kindly wait...")
                [orderStatus, leftAmount] = self.placeOrder(loginId, coffeePrice) 
                if orderStatus == True:                    
                    print("Remaining credits : ", leftAmount)
                    orderId = orderId + 1
                else:
                    print("Not enough credits : ", leftAmount)
                    exit
        return orderStatus    


    def take_order(self):
        status = self.order()
        if status == True:
            print("Order placed !!! ")
        return status