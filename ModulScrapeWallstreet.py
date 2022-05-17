import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import pandas as pd
from datetime import datetime, date, timedelta
import re
import sqlite3



def scrape_futureprice():
    url = 'https://www.wallstreet-online.de/rohstoffe/hu0002045586-weizen-1-tonne-1000-kg-europe-preis'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html')
    ## Table to Dateframe
    future_price_today = pd.DataFrame(columns=['Kontrakt', 'letzer_kurs', 'absolut', 'perf_perc', 'Fälligkeit', 'Vergleich', 'date_scraped'])
    for i in soup.select('div:nth-child(11) > table > tbody >tr'):
        row = []
        for j in i.select('td'):
            row.append(j.get_text())
        row.append(date.today() - timedelta(days=1))
        ser = pd.Series(row, index=['Kontrakt', 'letzer_kurs', 'absolut', 'perf_perc', 'Fälligkeit', 'Vergleich', 'date_scraped'])
        future_price_today = future_price_today.append(ser, ignore_index=True)
       
    # Split currency
    future_price_today['currency']=[re.split('(\d+,\d+)', string)[2] for string in future_price_today['absolut']]
    future_price_today['absolut']=[re.split('(\d+,\d+)', string)[1] for string in future_price_today['absolut']]
    future_price_today['letzer_kurs']=[re.split('(\d+,\d+)', string)[1] for string in future_price_today['letzer_kurs']]
    future_price_today.drop(['Vergleich'], inplace=True, axis=1)
    future_price_today.columns =['kontrakt', 'price', 'absolut_inc', 'perc_inc', 'date_fullfillment', 'date_price', 'currency']
        
    future_price_today['date_fullfillment'] = pd.to_datetime(future_price_today['date_fullfillment'], format='%d.%m.%Y')
    future_price_today['date_price'] = pd.to_datetime(future_price_today['date_price'], format='%Y-%m-%d')
      
    
    future_price_today['price'] = [string.replace(',','.') for string in future_price_today['price']]
    future_price_today['price'] = pd.to_numeric(future_price_today['price'])
    future_price_today['commodity_id'] = 2
    return future_price_today



def future_price_to_sql(future_price_today):
    con = sqlite3.connect('contrcalc.db')
    cur = con.cursor()
    for i in range(0, len(future_price_today)):
        cur.execute("""
        INSERT INTO price_table (
        commodity_id, date_fullfillment, date_price, price, currency) 
        VALUES (?,?,?,?,?)   
        """,
                   (future_price_today.iloc[i, 7],\
                    future_price_today.iloc[i, 4],\
                    future_price_today.iloc[i, 5],\
                    future_price_today.iloc[i, 1],\
                    future_price_today.iloc[i, 6])
                   )
    con.commit()
    return

    