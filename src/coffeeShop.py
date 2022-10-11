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

def chooseOption():
    useService = input('Press 1 to use our services or any other number to exit from our application  ')
    if useService == '1':
        option = True
    else:
        option = False
    return option


if __name__ == "__main__":
    welcome_page()
    time.sleep(2)
    print("\n \n")
    print('                     Welcome to our Coffee shop where you’ll find every kind of coffee that you want!')
    print('                                  Your presence is our motivation to do better!\n\n') 
    option=chooseOption()
    while(option == True):
        c1 = order.coffeeOrder()
        service = c1.viewMainMenu()
        if int(service) >= 1  and int(service) <= 10:
            completed = c1.actionToPerforme(service)
            if int(service) == 2 and completed == True:
                print("\nOrder ID : ", count_order()) 
            elif completed == True:
                print("Have a good day :) ")
            else:
                print("\nSomething went wrong... TRY AGAIN...")
        else:
            print("\nLooks like you choosed wrong option!!!\n")

        print("\n\nHi, welcome back!!! It is good to see you back :)")
        option=chooseOption()
        del c1


    #admin = input("Are you admin ? ")
    #if admin == "True":
    #    pp.pprint(customer)
    #else:
    #    print("you are not authorised....")
    '''status = c1.take_order()
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
    '''