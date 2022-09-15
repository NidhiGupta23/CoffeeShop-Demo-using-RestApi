import pprint as pp
import pandas as pd
import datetime
import consumeCoffeeApi as consumer

class coffeeOrder:

    def __init__(self):
        self.cs = consumer.consumeCoffeeApi()
        self.coffee =  self.cs.getCoffeeDetails()
        self.customer = self.cs.getCustomerDetails()
        self.event = {}
  
    # Display the coffee menu
    def viewMenu(self):
        print(pd.DataFrame(self.coffee.get('coffee')))

    # Display specific coffee
    def viewSpecificCoffee(self, id):
        self.cs.getSpecificCoffeeDetail(id) 

    # select coffee type
    def selectCoffee(self):        
        try:
            coffeeType = int(input("Have you choosed your desired coffee? If yes, press the id number :   "))
            print("You selected coffee")
            self.event['cName'] = self.coffee.get('coffee')[coffeeType-1].get('cName')
            pp.pprint(self.event['cName'])
            return self.coffee.get('coffee')[coffeeType-1]
        except IndexError as ie:
            print("Sorry, wrong option choosed, try again...")
            exit

    # Get coffee price
    def coffeePrice(self):
        coffee = self.selectCoffee()
        self.event['cPrice'] = coffee.get('price')
        print("Its a great choice for a great day :) ")

############################################## CUSTOMER VERIFICATION ##################################################

    # For existing users to login
    def login(self):
        cemail = input("Enter email address :  ")
        self.getCustomerIndex(cemail)
        status=False
        if self.event['cusId'] == 0:
            print("Enter correct email ID")
            exit
        else:
            cpwd = input("Enter the password :  ")
            status = self.checkPwd(cpwd) 
            print("Status after checking pwd  ",status)
        print("Status after else  ",status)
        return status


    # Get the id of the customer using email provided
    def getCustomerIndex(self, cemail):
        try:
            for index in range(len(self.customer.get('Customers'))):
                if cemail == self.customer.get('Customers')[index].get('email'):
                    print("After getting the :  ", index) 
                    print( self.customer.get('Customers')[index])
                    self.event['cusIndex'] = index
                    self.event['cusId'] = self.customer.get('Customers')[index].get('id')
                    break            
        except:
            print("Not the correct Email ID entered")

    # Check for customer authentication using password 
    def checkPwd(self, cpwd):
        scustomer = self.cs.getSpecificCustomer(self.event['cusId'])
        print("After getting the pwd :  ", scustomer)
        status = False
        if cpwd == scustomer.get('pwd'):
            print("yes, pwd is correct")
            status = True
            self.event['email'] = scustomer.get('email')
            self.event['fname'] = scustomer.get('fname')
        else:
            print("Wrong password entered!!!")
            exit
        return status

    # Get credit check and return status
    def placeOrder(self):
        customerCredit = self.cs.getSpecificCustomer(self.event['cusId']).get('credit')
        #print(customerCredit)
        status = False
        if customerCredit > self.event['cPrice']:
            customerCredit = customerCredit - self.event['cPrice']
            status = True
            
        return [status, customerCredit]

    # Update user credits in database
    def updateCredits(self, leftAmount):
        print("leftAmount", leftAmount)
        status = self.cs.putCustomerDetail(self.event['cusId'], leftAmount, 1)
        if status == True:
             self.event['credit'] = self.cs.getSpecificCustomer(self.event['cusId']).get('credit')
             print("Remaining Amount in balance: ", self.event['credit'])
        else:
            print("Something went wrong....")
            exit
    

    # Check credits of user for placing order for coffee
    def checkCredits(self):
        orderStatus = False
        print("Checking the credit...Kindly wait...")
        [orderStatus, leftAmount] = self.placeOrder() 
        if orderStatus == True:       
            self.updateCredits(leftAmount)
        else:
            print("Not enough credits : ", leftAmount)
            exit
        
        return orderStatus 

    # Create new user
    def createAccount(self):
        print("Create your account : \n \n")
        customer = self.cs.postCustomerDetails()
        self.customer = self.cs.getCustomerDetails()
        print("Your id is : ", customer)

    # For users to login and check for credits
    def logIn(self):
        try:
            print("Kindly login into your account :) ")
            loginStatus = self.login()
            if loginStatus == False:
                print("Please check your user email/password and coffee Id")
                exit
            else:
                self.coffeePrice()
                orderStatus = self.checkCredits()
                return orderStatus
        except:
            print("Please check your user email/password and coffee Id")
            exit

    # Check status of user signUp
    def signUpStatus(self):
        orderStatus = False
        signUp = input("Have you created your account ? Press yes or no and enter  ")
        if signUp == 'no':
            self.createAccount()
        elif signUp == 'yes':
            orderStatus=self.logIn()
        else:
            print("Choose either yes or no !!!")
            exit
        return orderStatus

    # select coffee and authenticate user
    def order(self):   
        orderStatus = False     
        signUp = input("Do you have an account?  Press yes or no and enter  ")
        if signUp == 'no':
            self.createAccount()
            orderStatus=self.signUpStatus()
        elif signUp == 'yes':            
            orderStatus=self.logIn()
        else:
            print("Choose either yes or no !!!")
            exit  
        return orderStatus    

    # Take coffee order from user
    def take_order(self):
        #self.customer = self.cs.getCustomerDetails()
        status = self.order()
        if status == True:
            self.event['cOrder'] = 1
            self.manageEvents()
            print("Order placed !!! ")
        return status

################################################## UPDATION MENU ######################################################
    
    def updateMenu(self):
        print("Below are the options : ")
        print("1. Update credit \n")
        # 2. Update coffee price \n3. Update coffee description  (To implement)
        updateId = int(input("Choose option: "))
        if updateId == 1 : 
            print("Enter your login credentials and credit")
            [loginStatus, loginId] = self.login()
            if loginStatus == True:
                newCredit = float(input("Enter new credit : "))
                status = self.cs.putCustomerDetail(loginId, newCredit, 2)
            else:
                print("Please check your user email/password")
                exit
        elif updateId == 2 :
            # add admin authentication
            coffeeId = int(input("Enter the coffee Id : "))
            newPrice = float(input("Enter new price : "))
            status = self.updateCoffeeDetails(coffeeId, newPrice)
        elif updateId == 3 :
            coffeeId = int(input("Enter the coffee Id : "))
            newDesp =  input("Enter new description : ")
            status = self.updateCoffeeDetails(coffeeId, newDesp)
        else:
            print("Wrong option given...")
        
        if status == True:
            print("Details were sucessfully updated...")
        else:
            print("Something went  wrong with updations")
    
#######################################################################################################################

    def manageEvents(self):
        self.cs.postEventDetails(self.event)
        print(self.event)
       