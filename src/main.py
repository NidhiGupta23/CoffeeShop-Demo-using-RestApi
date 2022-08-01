from time import time
import coffeeOrder as order


if __name__ == "__main__":
    c1 = order.coffeeOrder()
    #customer = c1.getCustomerDetails()
    c1.welcome_page()
    # Add timer to sleep for 5 mseconds
    print("\n \n")
    c1.viewMenu()
    # Add timer to sleep for 5 mseconds
    drink = input("Do you want to order coffee ? Press yes or no :   ")
    if drink == "yes":
        c1.placeOrder()
    else:
        print("Have a great day!!!")


    #admin = input("Are you admin ? ")
    #if admin == "True":
    #    pp.pprint(customer)
    #else:
    #    print("you are not authorised....")