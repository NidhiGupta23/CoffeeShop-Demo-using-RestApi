import json
import time
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


################################################## CUSTOMER VERIFICATION ######################################################

    # For existing users to login
    def login(self):
        cemail = input("Enter email address :  ")
        loginId =  self.getCustomerID(cemail)
        if loginId == 0:
            print("Enter correct email ID")
            exit
        else:
            cpwd = input("Enter the password :  ")
            print("Print the login ID : ", loginId)
            status = self.checkPwd(loginId, cpwd) 
        return [status, loginId]


    # Get the id of the customer using email provided
    def getCustomerID(self, cemail):
        cid = 0
        for i in range(len(self.customer.get('Customers'))):
            if cemail == self.customer.get('Customers')[i+1].get('email'):
                cid = i+1
                print("All details : ", self.customer.get('Customers')[cid])
                print("Customer ID :  ", i, cid)
                time.sleep(5)
                break
            
        return cid


    # Check for customer authentication using password 
    def checkPwd(self, cid, cpwd):
        scustomer = self.cs.getSpecificCustomer(cid)
        status = False
        if cpwd == scustomer.get('pwd'):
               status = True
               print("Getting all details checkPwd :    ", cid, scustomer)

        return status

    # Get credit check and return status
    def placeOrder(self, loginId, coffeePrice):
        customerCredit = self.customer.get('Customers')[loginId].get('credit')
        status = False
        if customerCredit > coffeePrice:
            customerCredit = customerCredit - coffeePrice
            status = True
            
        return [status, customerCredit]


    

    

    # Check credits of user for placing order for coffee
    def checkCredits(self, loginStatus, loginId, coffeePrice):
        if loginStatus == True:
            print("Checking the credit...Kindly wait...")
            [orderStatus, leftAmount] = self.placeOrder(loginId, coffeePrice) 
            if orderStatus == True:          
                print("We got id from coffeeOrder :  ", loginId)         
                self.updateCredits(loginId, leftAmount)
            else:
                print("Not enough credits : ", leftAmount)
                exit
        else:
            print("Wrong password : ")
            exit
        return orderStatus 
    
    # select coffee and authenticate user
    def order(self):
        coffee = self.selectCoffee()
        coffeePrice = coffee.get('price')
        print("Its a great choice for a great day :) ")
        signUp = input("Do you have an account?  Press yes or no and enter  ")
        if signUp == 'no':
            self.createAccount()
        print("Kindly login into your account :) ")
        [loginStatus, loginId] = self.login()
        orderStatus = self.checkCredits(loginStatus, loginId, coffeePrice)
            
        return orderStatus    

    # Take coffee order from user
    def take_order(self):
        status = self.order()
        if status == True:
            print("Order placed !!! ")
        return status
    
    # Create new user
    def createAccount(self):
        customer = self.cs.postCustomerDetails()
        print("Your id is : ", customer)
           
    # Update user credits in database
    def updateCredits(self, loginId, leftAmount):
        updated = self.cs.putCustomerDetail(loginId, leftAmount)
        print("User info updated: ", updated)
        customerCredit = self.customer.get('Customers')[loginId].get('credit')
        print("Remaining Amount in balance: ", customerCredit)
        
