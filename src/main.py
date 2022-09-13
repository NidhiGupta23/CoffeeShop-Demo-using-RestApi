import time
import coffeeOrder as order

  # Display the coffee shop logo
def welcome_page():
    print("########################################################################################################################")
    print("########################################################################################################################")
    print("                     ####  ####  #####  #####  #####  #####       ####  #  #  ####  ####  ")
    print("                     #     #  #  #      #      #      #           #     #  #  #  #  #  #  ")
    print("                     #     #  #  ###    ###    ###    ####        ####  ####  #  #  ####  ")
    print("                     #     #  #  #      #      #      #              #  #  #  #  #  #     ")
    print("                     ####  ####  #      #      #####  #####       ####  #  #  ####  #     ")
    print("########################################################################################################################")
    print("########################################################################################################################")


def count_order():
        count_order.counter += 1
        return count_order.counter

count_order.counter = 0

if __name__ == "__main__":
    welcome_page()
    time.sleep(5)
    print("\n \n")    
    drink = input("Do you want to order coffee ? Press yes or no :   ")
    while(drink == 'yes'):
        c1 = order.coffeeOrder()
        c1.viewMenu()
        time.sleep(5)
        status = c1.take_order()
        if status == True:
            if drink == "yes":
                print("Order ID : ", count_order())        
        else:
            print("Try again !!!")
        drink = input("Do you want to order coffee ? Press yes or no :   ")
        del c1

    updateDetails = input("Do you want to update your details ? Press yes or no :   ")
    if updateDetails == "yes":
        c1 = order.coffeeOrder()
        c1.updateMenu()
    
    print("Have a good day :) ")
        

    #admin = input("Are you admin ? ")
    #if admin == "True":
    #    pp.pprint(customer)
    #else:
    #    print("you are not authorised....")