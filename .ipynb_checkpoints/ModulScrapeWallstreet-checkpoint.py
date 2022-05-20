import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import pandas as pd
from datetime import datetime, date, timedelta
import re
import sqlite3



def scrape_futureprice():
    '''Scrapes wallstreet-online for current day future prices'''
    try: 
        url = 'https://www.wallstreet-online.de/rohstoffe/hu0002045586-weizen-1-tonne-1000-kg-europe-preis'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, features="lxml")
        print(f'Server respsonse: {page}')
    except:
        print('Could not retrieve data from Wallstreet online')
    
    
    ## Table to Dateframe
    future_price_today = pd.DataFrame(columns=['Kontrakt', 'letzer_kurs', 'absolut', 'perf_perc', 'Fälligkeit', 'Vergleich', 'date_scraped'])
    print(soup)
    try:
        for i in soup.select('div:nth-child(11) > table > tbody >tr'): #extrakt tablerows
            row = []
            for j in i.select('td'): # extract table data of rows
                row.append(j.get_text())
                print(f'row: {row}')
            row.append(date.today() - timedelta(days=1))
            ser = pd.Series(row, index=['Kontrakt', 'letzer_kurs', 'absolut', 'perf_perc', 'Fälligkeit', 'Vergleich', 'date_scraped'])
            
            future_price_today = pd.concat([future_price_today, pd.DataFrame(ser).transpose()], ignore_index=True)
        print("Managed to load data into dataframe 'future_price_today'")
        #print(future_price_today)
    except:
        print("Error loading data into dataframe 'future_price_today'")
    try:
        # Data cleaning
        future_price_today['currency']=[re.split('(\d+,\d+)', string)[2] for string in future_price_today['absolut']] #splits currency from price
        future_price_today['absolut']=[re.split('(\d+,\d+)', string)[1] for string in future_price_today['absolut']]
        future_price_today['letzer_kurs']=[re.split('(\d+,\d+)', string)[1] for string in future_price_today['letzer_kurs']]
        future_price_today.drop(['Vergleich'], inplace=True, axis=1)
        future_price_today.columns =['kontrakt', 'price', 'absolut_inc', 'perc_inc', 'date_fullfillment', 'date_price', 'currency'] # rename column names

        #change datatype from string to date
        future_price_today['date_fullfillment'] = pd.to_datetime(future_price_today['date_fullfillment'], format='%d.%m.%Y') 
        future_price_today['date_price'] = pd.to_datetime(future_price_today['date_price'], format='%Y-%m-%d')

        #change coma seperation of decimals to point
        future_price_today['price'] = [string.replace(',','.') for string in future_price_today['price']]
        future_price_today['price'] = pd.to_numeric(future_price_today['price'])
        future_price_today['commodity_id'] = 2 # commodity-id 2 = wheat
        print(f"Data loaded from wallstreet online:/n {future_price_today}")
    except: 
        print("Data cleaning was not succesful")
    return future_price_today



def future_price_to_sql(future_price_today):
    ''' Adds future_price today to the sql database price_table'''
    print('Attempt to parse future_price_today to sql database')
    #print(future_price_today.columns)
    tosql_df = future_price_today[['commodity_id', 'date_fullfillment', 'date_price', 'price', 'currency']]
    #print(tosql_df)
    try:
        con = sqlite3.connect('contrcalc.db') 
        tosql_df.to_sql('price_table', con, if_exists='append', index=False)
        print('Added price data to price table.')
    except:
        print('Error, failed to add data to price_table')
    return


#Simulate random wheat price in the future
def extrapolate_data(future_df):
    '''Produce fake future price data'''
    for i in range(1,9): #Takes the first 8 futures and add random variation for the next 40 days in the future
        for day in range(40):
            ts = future_df.iloc[i]["date_price"] + timedelta(days=day) #Adds one day to date of the price
            price = future_df.iloc[i]['price'] + randint(-10, 10) #Adds randomnes to the price
            series = future_df.iloc[i].copy()
            series["date_price"] = ts    
            series["price"] = price
            future_df = pd.concat([future_df, pd.DataFrame(series).transpose()], axis=0)
    return future_df


    