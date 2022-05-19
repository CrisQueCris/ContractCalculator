from dash import Dash, dcc, html, dash_table, ctx
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import date, timedelta, datetime
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
from ModulScrapeWallstreet import scrape_futureprice, future_price_to_sql, extrapolate_data
import json



def load_dfs():
    """loads commodities_df, contracts_df, price_df from contrcalc.db""" 
    try:
        print('Attempt to load commodites_df, contracts_df and price_df from sql database')
        con = sqlite3.connect('contrcalc.db')
        print('conntected to db')
        commodities_df = pd.read_sql("Select * from commodities", con, index_col='commodity_id')
        commodities_df_json = commodities_df.to_json(date_format='iso', orient='split')
        print('loaded commodities')


        contracts_df = pd.read_sql('Select * FROM contracts', con, index_col='contracts_id')
        print(contracts_df)
        contracts_df_json= contracts_df.to_json(date_format='iso', orient='split')
        print('loaded contracts')


        price_df = pd.read_sql('Select * FROM price_table', con, index_col='price_id')
        price_df_json = price_df.to_json(date_format='iso', orient='split')
        print('loaded prices')
        output_message = f'reloaded data: {commodities_df.columns}, {contracts_df.columns}, {price_df.columns}'
        com_list = [com for com in commodities_df['name']]
    except:
        output_message = "Error: couldn't reload data from database"
        print(output_message)
    return output_message, com_list, price_df_json, contracts_df_json, commodities_df_json 