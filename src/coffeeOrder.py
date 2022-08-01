import json as js
import pprint as pp
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
        print("####  ####  #####  #####  #####  #####       ####  #  #  ####  ####  ")
        print("#     #  #  #      #      #      #           #     #  #  #  #  #  #  ")
        print("#     #  #  ###    ###    ###    ####        ####  ####  #  #  ####  ")
        print("#     #  #  #      #      #      #              #  #  #  #  #  #     ")
        print("####  ####  #      #      #####  #####       ####  #  #  ####  #     ")
        print("########################################################################################################################")
        print("########################################################################################################################")

   
    # Display the coffee menu
    def viewMenu(self):
        pp.pprint(self.coffee.get('coffee'))


    def viewSpecificCoffee(self, id):
        self.cs.getSpecificCoffeeDetail(id)


    def placeOrder(self):
        coffeeType = input("Have you choosed your desired coffee? If yes, press the id number")
        if self.coffee.get('coffee').index(coffeeType):
            print("You selected coffee")
            pp.pprint(self.viewSpecificCoffee(coffeeType))
        else:
            print("Try again")