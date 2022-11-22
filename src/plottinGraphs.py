from numpy import rollaxis
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import consumeCoffeeApi as consumer


class plottinGraphs:
   def __init__(self):
      self.cs = consumer.consumeCoffeeApi()
      self.event =  self.cs.getEventsDetails()
      self.eventAll = self.event.get('ShopEvents')
      self.df = pd.DataFrame(columns=['EVENT_ID', 'FIRST_NAME', 'CUSTOMER_EMAIL', 'COFFEE_NAME', 'BILL', 'CUSTOMER_ID', 'CREDIT', 'DATE'] )
      for i in range(0, len(self.eventAll)): 
         self.df.loc[i] = [self.eventAll[i]['EVENT_ID'], self.eventAll[i]['FIRST_NAME'], self.eventAll[i]['CUSTOMER_EMAIL'], self.eventAll[i]['COFFEE_NAME'], self.eventAll[i]['BILL'], self.eventAll[i]['CUSTOMER_ID'], self.eventAll[i]['CREDIT'], self.eventAll[i]['DATE']]
      self.df['NewDATE'] = pd.to_datetime(self.df['DATE'])        
      self.df['YEAR'] = pd.DatetimeIndex(self.df['NewDATE']).year 
      self.df['MONTH'] = pd.DatetimeIndex(self.df['NewDATE']).month 

   # To view the logs of shop
   def viewEvents(self):
      print('\n', self.df.set_index('EVENT_ID'))


   def viewPopularCoffee(self, column1):       
      sns.set(style="whitegrid")
      sns.countplot(x=column1, data=self.df.loc[(self.df['MONTH']==dt.datetime.now().month) & (self.df['YEAR']==dt.datetime.now().year)]) 
      plt.xticks(rotation=45)
      plt.ylabel('COFFEE_COUNT')
      plt.title('Popular coffees of the MONTH')
      plt.show()


   def viewCustomer(self, column2):
      # use customr ID here to display
      sns.set(style="whitegrid")
      if column2 == 'CoffeeOrder':
         plot1 =  sns.countplot(x=self.df['CUSTOMER_ID'],data=self.df['YEAR']==dt.datetime.now().year)
         plt.xticks(rotation=45)
         plt.title('Customers vs Coffee ordered')
         plt.tight_layout()
         plt.show() 
      elif column2 == 'Credit':
         self.customerCredit()
      else:
         print("Not supported currently...")       


   def bonusCoffee(self, column1, user):
      trimData = self.df.loc[(self.df[column1]==user) & (self.df['YEAR']==dt.datetime.now().year)]
      '''print("trim Data")       print(trimData)'''
      setBonus = False
      try:
         if (len(trimData.value_counts())+1) % 7 == 0 :
            setBonus = True
            print("-----------------------------------------------------")
            print("|             Your coffee is on the house           |")         
            print("-----------------------------------------------------")
         else:
            setBonus = False
            print("\nOrder ", 7-((len(trimData.value_counts())+1) % 7), " more for bonus coffee")
      except:
         print("Facing issue with fetching data")
      
      return setBonus

   
   def customerCredit(self):
      self.customer =  self.cs.getCustomerDetails()
      self.customerAll = self.customer.get('Customers')
      self.customerdf = pd.DataFrame(columns=['CUSTOMER_ID', 'FIRST_NAME', 'LAST_NAME', 'CUSTOMER_EMAIL', 'PWD', 'CREDIT'] )
      for i in range(0, len(self.customerAll)): 
         self.customerdf.loc[i] = [self.customerAll[i]['CUSTOMER_ID'], self.customerAll[i]['FIRST_NAME'], self.customerAll[i]['LAST_NAME'],  self.customerAll[i]['CUSTOMER_EMAIL'], self.customerAll[i]['PWD'], self.customerAll[i]['CREDIT']]
 
      plot1 =  sns.barplot(x=self.customerdf['CUSTOMER_ID'], y=self.customerdf['CREDIT'] , data=self.customerdf)
      plt.xticks(rotation=45)
      plt.title('Customers vs Credit')
      plt.show()



'''p1 = plottinGraphs()
#p1.viewEvents()
p1.viewPopularCoffee('COFFEE_NAME')
p1.viewCustomer('CoffeeOrder')
p1.viewCustomer('Credit')
#p1.bonusCoffee('MailID', 'jan@coffee.com')'''
