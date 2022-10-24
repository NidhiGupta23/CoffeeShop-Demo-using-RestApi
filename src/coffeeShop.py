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
    useService = input('Press any key for Main Menu or * key to exit from our application  ')
    if useService != '*':
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
        try:
            c1 = order.coffeeOrder()
            service = c1.viewMainMenu()
            if service == '*':
                exit()
            else:
                completed = c1.actionToPerforme(service)
                if int(service) == 2 and completed == True:
                    print("\nOrder ID : ", count_order()) 
                elif completed == True:
                    print("Have a good day :) ")
                else:
                    print("\nLooks like services can not be fetched!!!\n")

            print("\n\nHi, welcome back!!! It is good to see you back :)")
            option=chooseOption()
            if option == False:
                del c1
        

        except ValueError:
            print("Choose from 1 to 10 only...")
            