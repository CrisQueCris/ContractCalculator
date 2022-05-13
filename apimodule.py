from config_gitignore import api_key #imports api key to access commodities API
import pandas as pd
import requests #library to querry APIs
import seaborn as sns
from matplotlib import pyplot as plt
import sqlite3
from datetime import date, timedelta, datetime

def get_historical_data(start_date, end_date, api_key):
    '''querries commodities_api and returns historical wheat price data in Euro as a JSON'''
    base = 'EUR'
    symbols = 'WHEAT'
    url = 'https://www.commodities-api.com/api/timeseries'
    querry = url+'?access_key=' + api_key +  '&start_date='+start_date+'&end_date='+end_date+'&base='+base+'&symbols='+symbols
    response = requests.get(querry)
    return response

def json_to_sql(response):
    ''' json from get_hostorical_data() and parses sql into wheat_spotprice table'''
    con = sqlite3.connect('contrcalc.db',timeout=10)
    cur = con.cursor()
    for date, price in response.json()['data']['rates'].items():
        price = 1/list(price.values())[0]        
        date_time = datetime.strptime(date, '%Y-%m-%d')
        date = date_time.date()
        cur.execute('''
        INSERT INTO wheat_spotprice VALUES(?,?)
        ''', (date, price))
        con.commit() 
     
    con.close()
    return 

def get_price_since_last_querry():    
    con = sqlite3.connect('contrcalc.db')
    cur = con.cursor()
    for i in  con.execute('''
    Select MAX(date_price) FROM price_table
        JOIN 
        WHERE commodity_id = 
    ''''):
        last_date = i[0]
    con.commit()  
    con.close()
    yesterday = str(date.today() - timedelta(days=1))
    day_after_last_date = str(datetime.strptime(last_date, '%Y-%m-%d').date() + timedelta(days=1))
    response = get_historical_data(day_after_last_date, yesterday, api_key)
    return response