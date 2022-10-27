from distutils.log import error
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
        df = pd.DataFrame(columns=['COFFEE_ID', 'COFFEE_NAME', 'COFFEE_DESCRIPTION', 'COFFEE_PRICE'])
        for i in range(0, len(coffeeList)):
            df.loc[i] = [coffeeList[i]['COFFEE_ID'], coffeeList[i]['COFFEE_NAME'], coffeeList[i]['COFFEE_DESCRIPTION'], coffeeList[i]['COFFEE_PRICE']]
        print('\n\n',df.set_index('COFFEE_ID'))

    # Display specific coffee
    def viewSpecificCoffee(self, id):
        self.cs.getSpecificCoffeeDetail(id) 

    # select coffee type
    def selectCoffee(self):        
        try:
            coffeeType = int(input("\nChoose your desired coffee ID:   "))
            #print("You selected coffee")
            self.event['COFFEE_NAME'] = self.coffee.get('coffee')[coffeeType-1].get('COFFEE_NAME')
            print("\nYou selected coffee", self.event['COFFEE_NAME'])
            return self.coffee.get('coffee')[coffeeType-1]
        except IndexError:
            print("Sorry, wrong option choosed, try again...")
            exit

    # Get coffee price
    def coffeePrice(self):
        coffee = self.selectCoffee()
        self.event['COFFEE_PRICE'] = coffee.get('COFFEE_PRICE')
        print("Its a great choice for a great day :) ")

############################################## CUSTOMER VERIFICATION ##################################################

    # For existing users to login
    def login(self):
        cemail = input("Enter email address :  ")
        self.getCustomerIndex(cemail)
        status=False
        if self.event['CUSTOMER_ID'] == 0:
            print("Enter correct email ID")
            exit
        else:
            cpwd = input("Enter the password :  ")
            status = self.checkPwd(cpwd) 
            '''print("Status after checking pwd  ",status)  print("Status after else  ",status)'''
        return status


    # Get the id of the customer using email provided
    def getCustomerIndex(self, cemail):
        try:
            for index in range(len(self.customer.get('Customers'))):
                if cemail == self.customer.get('Customers')[index].get('CUSTOMER_EMAIL'):
                   # print("After getting the :  ", index)                     
                   # print( self.customer.get('Customers')[index])
                    self.event['cusIndex'] = index
                    self.event['CUSTOMER_ID'] = self.customer.get('Customers')[index].get('CUSTOMER_ID')
                    break            
        except:
            print("Not the correct Email ID entered")

    # Check for customer authentication using password 
    def checkPwd(self, cpwd):
        scustomer = self.cs.getSpecificCustomer(self.event['CUSTOMER_ID'])
        #print("After getting the pwd :  ", scustomer)
        status = False
        if cpwd == scustomer.get('PWD'):
            status = True
            self.event['CUSTOMER_EMAIL'] = scustomer.get('CUSTOMER_EMAIL')
            self.event['FIRST_NAME'] = scustomer.get('FIRST_NAME')
        else:
            print("Wrong password entered!!!")
            exit
        #print("After getting the pwd:  ", status) 
        return status

    # Get credit check and return status
    def placeOrder(self):
        customerCredit = self.cs.getSpecificCustomer(self.event['CUSTOMER_ID']).get('CREDIT')
        #print(customerCredit)
        status = False
        if customerCredit > self.event['COFFEE_PRICE']:
            customerCredit = customerCredit - self.event['COFFEE_PRICE']
            status = True
            
        return [status, customerCredit]

    # Update user credits in database
    def updateCredits(self, leftAmount):
        #print("leftAmount", leftAmount)
        status = self.cs.modifyCustomerDetails(self.event['CUSTOMER_ID'], 'CD', leftAmount, 1)
        if status == True:
             self.event['CREDIT'] = self.cs.getSpecificCustomer(self.event['CUSTOMER_ID']).get('CREDIT')
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
        print("Your id is ", customer['CUSTOMER_ID'])

    # For users to login and check for credits
    def logIn(self):
        try:
            print("Kindly login into your account :) ")
            loginStatus = self.login()
            #print("After email and pwd: ", loginStatus)
            if loginStatus == False:
                print("Please check your user email/password")
                exit
            else:   
                #print("We are inside the login")             
                onHouse = self.plotGraph.bonusCoffee('CUSTOMER_EMAIL', self.event['CUSTOMER_EMAIL'])
                #print("came back from the onHouse :  ", onHouse)
                self.coffeePrice()
                if onHouse == True:
                    self.event['CREDIT'] = self.cs.getSpecificCustomer(self.event['CUSTOMER_ID']).get('CREDIT')
                    orderStatus = self.cs.modifyCustomerDetails(self.event['CUSTOMER_ID'],'CD', self.event['CREDIT'], 3)
                else:
                    #print("Came back from bonus coffee")
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
        if signUp.lower() == 'no' or signUp.lower() == 'n':
            self.createAccount()
            orderStatus=self.signUpStatus()
        elif signUp.lower() == 'yes' or  signUp.lower() == 'y':            
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
        try:
            self.cs.postEventDetails(self.event)
            #print(self.event)
        except error:
            print(error)

    def viewCredits(self):
        view = input("Press 1 to see your remaining balance or  press any other number to exit from the system  ")
        if view == '1':
            if (self.plotGraph.bonusCoffee('CUSTOMER_EMAIL', self.event['CUSTOMER_EMAIL'])):
                self.event['COFFEE_PRICE'] = 0.0
                
            print("\nYour coffee bill was: ", self.event['COFFEE_PRICE'])
            print("Remaining balance: ", self.event['CREDIT'])
        
        
############################ DESIGN COFFEE SHOP #######################################################

    def viewMainMenu(self):
        print("\nMain Menu")
        print("1. Create account")
        print("2. Order a coffee")
        print("3. Add money to wallet")
        print("4. View account details")
        print("5. Modify account details")
        print("6. Delete account")
        print("7. View Coffee of the month")
        print("8. Give feedback and rating")
        print("9. Admin")
        print("10. Offers")
        option = input("\nEnter your choice or * to exit  ")        
        return option

    def actionToPerforme(self, option):
        if option == '1':
            print("\nAccount creation: \n")
            status = self.actionPerform1()
        elif option == '2':
            print("\nWe are ready to take you coffee order that will make your day extra special :) \n")
            status = self.actionPerform2() 
        elif option == '3':
            print("\nAdd amount in your wallet!!!\n")
            status = self.actionPerform3()
        elif option == '4':
            print("\nLogin to see your account details!!!\n")
            status = self.actionPerform4()
        elif option == '5':
            print("\nModify your details")
            status = self.actionPerform5()
        elif option == '6':
            print("\nLogin to delete your account\n")
            status = self.actionPerform6()
        elif option == '7':
            print("\nIt is wise to view coffee of the month ")
            self.plotGraph.viewPopularCoffee('COFFEE_NAME')   
            status = True          
        #TODO
        elif option == '8':
            print("Feature yet to be implemented")
            status = True    
        elif  option == '9':
            print("Login with your credentials")
            status = self.actionPerform9()   
        elif option == '10':
            print("Offers and discounts\n")
            self.actionPerform10()
            status = True   
        elif option == '*':
            print("\n\nWe are sad to see you go... Hope you will choose us again for a great cup of coffee")
            exit()
        else:
            print("Wrong option selected")
        return status
        

    def actionPerform1(self):
        customer = self.cs.postCustomerDetails()
        status = False
        if customer is not None:
            print("\nThank you for becoming our member!!!\n")
            print("Your customer ID is ", customer['CUSTOMER_ID'])
            status = True
        return status


    def actionPerform2(self):
        self.viewCoffeeMenu()
        status = self.take_order()
        return status

    def actionPerform3(self):
        print("\nAdditional Offers: ")
        print("Add 500kr and get additional 50kr in your wallet")
        print("Add 1000kr and get additional 100kr in your wallet")
        print("\nEnter your login credentials")
        status = False
        if self.event.get('CUSTOMER_ID') != None:
            loginStatus = True
        else:
            loginStatus = self.login()

        if loginStatus == True:
            try:
                newCredit = float(input("Amount to be added in credit : "))
                if newCredit >=500 and newCredit < 1000:
                    newCredit = newCredit + 50
                elif newCredit >= 1000:
                    newCredit = newCredit + 100
                print("Old balance in account is ", self.cs.getSpecificCustomer(self.event['CUSTOMER_ID']).get('CREDIT'))
                print("Amount to be added: ", newCredit)
                status = self.cs.modifyCustomerDetails(self.event['CUSTOMER_ID'],'CD', newCredit, 2)
                if status == True:
                    print("New balance in account is ", self.cs.getSpecificCustomer(self.event['CUSTOMER_ID']).get('CREDIT'))
                
            except ValueError:
                print("Amount can be only digits")
            finally:
                return status
        else:
            print("Please check your user email/password")
            exit


    def actionPerform4(self):
        loginStatus = self.login()
        if loginStatus == True:
            #customer = self.cs.getSpecificCustomer(823677)
            customer = self.cs.getSpecificCustomer(self.event['CUSTOMER_ID'])
            if customer is not None:
                print("-----------------------------------------------------")
                print( pd.DataFrame.from_dict(customer, orient='index'))
                print("-----------------------------------------------------")
                status = True
        else:
            print("Wrong email or password.")
            status = False
        return status

    def actionPerform5(self):        
        self.actionPerform4()
        print("Your details as of now")
        print("*** NOTE: CUSTOMER ID WILL NOT BE MODIFIED ***")
        change = input("Press 1 to continue changing details or any other key to go to main menu")
        if int(change) == 1:
            status = self.subActionPerform5()
            if status == True:
                self.actionPerform4()
        else:
            status = True

        
        return status

    def subActionPerform5(self):
        print("\n\nBelow are the field that can be modified")
        print("1. First Name")
        print("2. Last Name")
        print("3. Email ID")
        print("4. Password")
        print("5. Credit to add")
        option = input("Choose which field you want to modify ")
        status = False
        try:
            if int(option) == 1:
                updateValue = input("Enter new name")
                print("Old value is: ", self.cs.getSpecificCustomer(self.event['CUSTOMER_ID'].get('FIRST_NAME')))
                key = 'FN' 
            elif int(option) == 2:
                updateValue = input("Enter new name")
                print("Old value is: ", self.cs.getSpecificCustomer(self.event['CUSTOMER_ID'].get('LAST_NAME')))
                key = 'LN'
            elif int(option) == 3:
                updateValue = input("New email id... make sure its not the same as old one")
                print("Old value is: ", self.cs.getSpecificCustomer(self.event['CUSTOMER_ID'].get('CUSTOMER_EMAIL')))
                key = 'EL'
            elif int(option) == 4:
                updateValue = input("Enter new password")
                print("Old value is: ", self.cs.getSpecificCustomer(self.event['CUSTOMER_ID'].get('PWD')))
                key = 'PD'
            elif int(option) == 5:
                self.actionPerform3()
            else:
                key = 0 
                
            if key != 0:
                status = self.cs.modifyCustomerDetails(self.event['CUSTOMER_ID'], key, updateValue)
            else:
                print("Wrong option")
                
        except ValueError:
            print("Only integers are allowed")
        return status
    
    def actionPerform6(self):
        loginStatus = self.login()
        if loginStatus == True:
            msg = self.cs.deleteCustomerDetail(self.event['CUSTOMER_ID'])
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
            print('\nHello, Admin. \nChoose the services you want to perform ')
            self.subActionPerform9()
            status = True
        else:
            print("Invalid user name or password. Try again")
        return status


    def subActionPerform9(self):
        choice = True

        while choice==True:
            print("\nSub Menu")
            print("1. View customer vs credit graph")
            print("2. View customer vs coffee ordered graph")
            print("3. Modify coffee prices")
            print("4. Modify coffee description")
            print('5. Add new item in menu')
            print('6. Exit sub menu')
            adminOption = input('Enter your option ')
            if adminOption == '1':
                print("Graph of customers vs credit in their account")
                self.plotGraph.viewCustomer('Credit')
            elif adminOption == '2':
                print("Graph of customers vs no. of coffees ordered")
                self.plotGraph.viewCustomer('CoffeeOrder')
            elif adminOption == '3':
                print("Enter details to update coffee prices")
                coffeeId = int(input("Enter the coffee Id: "))
                newPrice = float(input("Enter new price: "))
                status = self.cs.updateCoffeeDetails(coffeeId, 'price', newPrice)
            elif adminOption == '4':
                print("Enter details to update coffee description")
                coffeeId = int(input("Enter the coffee Id: "))
                newDesp =  input("Enter new description: ")
                status = self.cs.updateCoffeeDetails(coffeeId, 'description', newDesp)
            elif adminOption == '5':
                print("Want to add something new ")
                newItem = self.cs.postCoffeeDetails()
                status = False
                if newItem is not None:
                    print("New Item ID is ", newItem['COFFEE_ID'])
                    status = True
                return status

            else:
                break
            choice = input('Do you still want to perform any operation(y/n) ')
            if choice.lower() == 'y' or choice.lower() == 'yes':
                choice = True


    def actionPerform10(self):
        print("1. Get every 7th coffee free in our shop \n     Condition applied: Valid per year")
        print("2. Additional Offers:   ")
        print("    Add 500kr and get additional 50kr in your wallet")
        print("    Add 1000kr and get additional 100kr in your wallet")

