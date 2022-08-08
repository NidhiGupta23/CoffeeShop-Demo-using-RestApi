import time
import coffeeOrder as order


if __name__ == "__main__":
    c1 = order.coffeeOrder()
    c1.welcome_page()
    time.sleep(5)
    print("\n \n")
    c1.viewMenu()
    time.sleep(5)
    drink = input("Do you want to order coffee ? Press yes or no :   ")
    if drink == "yes":
        c1.order()
    else:
        print("Have a great day!!!")


    #admin = input("Are you admin ? ")
    #if admin == "True":
    #    pp.pprint(customer)
    #else:
    #    print("you are not authorised....")