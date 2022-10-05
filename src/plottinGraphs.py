import pandas as pd
import matplotlib.pyplot as plt
from pyparsing import col
import seaborn as sns
import datetime as dt

import consumeCoffeeApi as consumer

'''Layout of this class
1. get all events from shop data
2. transfer it to pandas dataframe
3. get a dicitonary or list to count the no. of coffees that were ordered
4. plot a graph through the data

3. get a list of people and no. of times they ordered coffee
4. 
'''

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
      plt.title('Populare coffees of the MONTH')
      plt.show()


   def viewCustomer(self, column1, column2):
      # use customr ID here to display
      trimData = self.df.groupby(column1).sum().reset_index()
      print(trimData)
      '''trimData1 = self.df.groupby('Name').sum().reset_index()
      print(trimData1)
      print(trimData1.merge(trimData))'''
      sns.set(style="whitegrid")
      if column2 == 'CoffeeOrder':
         plot1 = sns.barplot(x='Name', y=column2, data=trimData)
         plt.title('Customers vs Coffee ordered')
      elif column2 == 'Credit':
         plot1 = sns.barplot(x='Name', y=column2, data=trimData)
         plt.title('Customers vs Credit')
      

      plt.show()      


   def bonusCoffee(self, column1, CUSTOMER_EMAIL):
      trimData = self.df[self.df[column1]==CUSTOMER_EMAIL]
      thisYear = dt.datetime.now().year

      

      '''1. sought date
           a. get year and MONTH
           b. get data of same year
         2. count the coffee order
         3. add 1 coffee check if sum is a multiple of 7
           a. yes: send a signal to make that order free
           b. no: send a signal to deduct amount from CREDIT
           '''
      
      


   

p1 = plottinGraphs()
p1.viewEvents()
p1.viewPopularCoffee('COFFEE_NAME')
p1.viewCustomer('MailID', 'CoffeeOrder')
p1.viewCustomer('MailID', 'Credit')
p1.bonusCoffee('MailID', 'jan@coffee.com')
