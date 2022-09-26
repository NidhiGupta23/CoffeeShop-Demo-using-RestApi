import time
import pandas as pd
import consumeCoffeeApi as consumer
import plottinGraphs as pg

class coffeeOrder:

    def __init__(self):
        self.cs = consumer.consumeCoffeeApi()
        self.coffee =  self.cs.getCoffeeDetails()
        self.customer = self.cs.getCustomerDetails()
        self.plotGraph = pg.plottinGraphs()
        self.event = {}
  
    # Display the coffee menu
    def viewCoffeeMenu(self):
        coffeeList = self.coffee.get('coffee')
        df = pd.DataFrame(columns=['id', 'cName', 'description', 'price'])
        for i in range(0, len(coffeeList)):
            df.loc[i] = [coffeeList[i]['id'], coffeeList[i]['cName'], coffeeList[i]['description'], coffeeList[i]['price']]
        df.rename(columns = {'cName':'CoffeeName', 'description':'Description', 'id':'ID', 'price':'Price'}, inplace = True)
        print('\n\n',df.set_index('ID'))

    # Display specific coffee
    def viewSpecificCoffee(self, id):
        self.cs.getSpecificCoffeeDetail(id) 

    # select coffee type
    def selectCoffee(self):        
        try:
            coffeeType = int(input("\nHave you choosed your desired coffee? If yes, press the id number :   "))
            #print("You selected coffee")
            self.event['cName'] = self.coffee.get('coffee')[coffeeType-1].get('cName')
            print("\nYou selected coffee", self.event['cName'])
            return self.coffee.get('coffee')[coffeeType-1]
        except IndexError:
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
            #print("Status after checking pwd  ",status)print("Status after else  ",status)
        return status


    # Get the id of the customer using email provided
    def getCustomerIndex(self, cemail):
        try:
            for index in range(len(self.customer.get('Customers'))):
                if cemail == self.customer.get('Customers')[index].get('email'):
                    '''print("After getting the :  ", index) 
                    print( self.customer.get('Customers')[index])'''
                    self.event['cusIndex'] = index
                    self.event['cusId'] = self.customer.get('Customers')[index].get('id')
                    break            
        except:
            print("Not the correct Email ID entered")

    # Check for customer authentication using password 
    def checkPwd(self, cpwd):
        scustomer = self.cs.getSpecificCustomer(self.event['cusId'])
        #print("After getting the pwd :  ", scustomer)
        status = False
        if cpwd == scustomer.get('pwd'):
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
        #print("leftAmount", leftAmount)
        status = self.cs.putCustomerDetail(self.event['cusId'], leftAmount, 1)
        if status == True:
             self.event['credit'] = self.cs.getSpecificCustomer(self.event['cusId']).get('credit')
        else:
            print("Something went wrong....")
            exit
    

    # Check credits of user for placing order for coffee
    def checkCredits(self):
        orderStatus = False
        #print("Checking the credit...Kindly wait...")
        [orderStatus, leftAmount] = self.placeOrder() 
        if orderStatus == True:       
            self.updateCredits(leftAmount)
        else:
            print("Not enough credits : ", leftAmount)
            exit
        
        return orderStatus 

    # Create new user
    def createAccount(self):
        customer = self.cs.postCustomerDetails()
        self.customer = self.cs.getCustomerDetails()
        print("Your id is ", customer['id'])

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
            print("Please check your user email/password or coffee Id")
            exit

    # Check status of user signUp
    def signUpStatus(self):
        orderStatus = False
        signUp = input("\nHave you created your account ? Press yes or no and enter  ")
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
        signUp = input("\n\nDo you have an account?  Press yes or no and enter  ")
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
            print("\n\nOrder placed !!!\n\n ")
            self.viewCredits()
        return status

      
    #######################################################################################################################

    def manageEvents(self):
        self.cs.postEventDetails(self.event)
        #print(self.event)
       
    def viewCredits(self):
        try:
            view = int(input("Press 1 to see your remaining balance or  press any other number to exit from the system  "))
            if view == 1:
                print("\nYour coffee bill was: ", self.event['cPrice'])
                print("Remaining balance: ", self.event['credit'])
            
        except ValueError:
            print("Systems only take numbers... press number 1 to view or any other number to exit")
        

############################ DESIGN COFFEE SHOP #######################################################

    def viewMainMenu(self):
        print("\nFollowing are the services that we provide:")
        print("1. Create account")
        print("2. Order a coffee")
        print("3. Add money to wallet")
        print("4. View account details")
        print("5. Modify account details")
        print("6. Delete account")
        print("7. View Coffee of the month")
        print("8. Give feedback and rating")
        print("9. Admin")
        try:
            option = input("\nKindly choose one of the options from above and press Enter to continue  ")
        except ValueError:
            print("Kinly insert only integers")
            try:
                option = int(input("Kindly choose one of the options from above and press Enter to continue  "))
            except ValueError:
                print('Only accepts integers!!!')
        finally:
            if option is None:
                option = 0
            return option

    def actionToPerforme(self, option):
        if option == '1':
            print("\nKindly enter following details to create your account: \n")
            status = self.actionPerform1()
        elif option == '2':
            print("\nWe are ready to take you coffee order that will make your day extra special :) \n")
            status = self.actionPerform2() 
        elif option == '3':
            print("\nWelcome back to add amount in your wallet!!!\n")
            status = self.actionPerform3()
        elif option == '4':
            print("\nLogin to see your account details!!!\n")
            status = self.actionPerform4()
        elif option == '5':
            pass
        elif option == '6':
            print("\nLogin to delete your account\n")
            status = self.actionPerform6()
        elif option == '7':
            print("\nIt is wise to view and coffee of the month ")
            self.plotGraph.viewPopularCoffee('CoffeeName', 'CoffeeOrder')            
        #TODO
        elif option == '8':
            print("Feature yet to be implemented")
            status = True    
        elif  option == '9':
            print("Login with your credentials")
            status = self.actionPerform9()      
        else:
            print("\n\nWe are sad to see you go... Hope you will choose us again for a great cup of coffee")
            exit()
        return status
        

    def actionPerform1(self):
        customer = self.cs.postCustomerDetails()
        status = False
        if customer is not None:
            print("\nThank you for becoming our memeber!!!\n")
            print("Your customer ID is ", customer['id'])
            status = True
        return status


    def actionPerform2(self):
        self.viewCoffeeMenu()
        time.sleep(2)
        status = self.take_order()
        return status

    def actionPerform3(self):
        print("\nHello, are you aware of our offer? If not, then let me tell you.")
        print("\nAdd 500kr and get additional 50kr in your wallet")
        print("\nAdd 1000kr and get additional 100kr in your wallet")
        print("\n\nEnter your login credentials")
        loginStatus = self.login()
        if loginStatus == True:
            try:
                newCredit = float(input("Amount to be added in credit : "))
                if newCredit >=500 and newCredit < 1000:
                    newCredit = newCredit + 50
                elif newCredit >= 1000:
                    newCredit = newCredit + 100
                status = self.cs.putCustomerDetail(self.event['cusId'], newCredit, 2)
                if status == True:
                    print("New balance in account is ", self.cs.getSpecificCustomer(self.event['cusId']).get('credit'))
            except ValueError:
                print("Amount can be only digits")
        else:
            print("Please check your user email/password")
            exit


    def actionPerform4(self):
        loginStatus = self.login()
        if loginStatus == True:
            customer = self.cs.getSpecificCustomer(self.event['cusId'])
            if customer is not None:
                print(customer)
                status = True
        else:
            print("Wrong email or password.")
            status = False
        return status

    def actionPerform6(self):
        loginStatus = self.login()
        if loginStatus == True:
            msg = self.cs.deleteCustomerDetail(self.event['cusId'])
            if msg is not None:
                print(msg)
                status = True
        else:
            print("Wrong email or password.")
            status = False
        return status

    def actionPerform9(self):
        status = False
        adminUser = input("Enter Admin user name: ")
        adminPwd = input("Enter Admin password: ")
        if adminUser == 'AdminUser123' and adminPwd == 'AdminPwd123':
            print('\nHello, Admin. \nChoose the services you want to perform')
            self.subActionPerform9()
        else:
            print("Invalid user name or password. Try again")

   
    def subActionPerform9(self):
        choice = True
        while choice==True:
            print("\nFollowing are the services that you can see")
            print("1. View customer vs credit graph")
            print("2. View customer vs coffee ordered graph")
            print("3. Modify coffee prices")
            print("4. Modify coffee description")
            print('5. Add new item in menu')
            print('6. Exit sub menu')
            adminOption = input('Choose an option from top')
            if adminOption == '1':
                print("Graph of customers vs credit in their account")
                self.plotGraph.viewCustomer('MailID', 'Credit')
            elif adminOption == '2':
                print("Graph of customers vs no. of coffees ordered")
                self.plotGraph.viewCustomer('MailID', 'CoffeeOrder')
            elif adminOption == '3':
                print("Enter details to update coffee prices")
                coffeeId = int(input("Enter the coffee Id : "))
                newPrice = float(input("Enter new price : "))
                status = self.updateCoffeeDetails(coffeeId, newPrice)
            elif adminOption == '4':
                print("Enter details to update coffee description")
                coffeeId = int(input("Enter the coffee Id : "))
                newDesp =  input("Enter new description : ")
                status = self.updateCoffeeDetails(coffeeId, newDesp)
            elif adminOption == '5':
                print("Want to add something new ")
            else:
                break
            choice = input('Do you still want to perform any operation')
