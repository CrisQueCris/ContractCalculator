from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import date, timedelta, datetime
import sqlite3
import plotly.graph_objects as go



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#load table with price data

con = sqlite3.connect('contrcalc.db') 
price_df = pd.read_sql('Select * FROM price_table', con, index_col='price_id')



#load table with contracts



#load table with commodities

commodities_df = pd.read_sql("Select * from commodities", con, index_col='commodity_id')
contracts_df = pd.read_sql('Select * FROM contracts', con, index_col='contract_id',  parse_dates=['date_closure', 'date_fullfillment'])



app = Dash(__name__, external_stylesheets=external_stylesheets)

start_date=str(date.today())
end_date=str(date.today() + timedelta(days=60))

app.layout = html.Div([
    
    #Title
    html.H1('Contract Simulator'),
    #Load Button
    html.Button('Load Data', n_clicks=0, id='button-load_data'),
        
    html.Div([
    
    #Tabs that display the different contracts and commodities
    dcc.Tabs(id="commodities-tab", value='wheat_tab_val', children=[ 
        dcc.Tab(label='wheat'),
        dcc.Tab(label='barley'),
        dcc.Tab(label='corn', value='corn-tab-val'),
        dcc.Tab(label='rapeseed', value='rapeseed-tab-val'),
        ]),
    html.Div(id='tabs-content', children=[]),
    #Dropdown to select the respective Futuresprice
        dcc.Dropdown([datefull for datefull in price_df[price_df['commodity_id']==2]['date_fullfillment'].unique()], price_df[price_df['commodity_id']==2]['date_fullfillment'].unique(), id='date_fulllfillment-dropdown',
        multi=True
        ),              
    #Graph showing contracted amount
        dcc.Graph(id='price_dev'),            
    #Graph showing commodity price        
    
    
    
    #Slider to adapt time
    
#        dcc.RangeSlider((date.today() - timedelta(days=30)).date(), date.today() + timedelta(days=180), #7, count=1, value=[datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(end_date, '%Y-%m-%d')], #id='rangeslider_time'),
    
    #DatePickerRange to adapt RangSlider
        dcc.DatePickerRange(
        id='date-picker-range',
        start_date=date.today(),
        end_date_placeholder_text=date.today()
        ),
    
    
    #Table showing contracts
 
    dash_table.DataTable(
    contracts_df.to_dict('records'),
    [{"name": i, "id": i} for i in contracts_df.columns]
    ),
        
        
        
        
    #Menu to add a contract
    html.Div(id = 'contracts-menu',
        children = [
            html.Table([
                html.Caption(title='Enter a new cotract'),
                html.Thead([
                    html.Tr([
                        html.Th('Commodity'),
                        html.Th('Price per to'),
                        html.Th('Amount in to'),
                        html.Th('Date of fullfillment'),
                        html.Th('Date of contract')                    
                        ])
                    ]),
                html.Tbody([
                    html.Tr([
                        html.Td([dcc.Dropdown([com for com in commodities_df['name']], commodities_df['name'][2], id='commodity-dropdown')]),
                        html.Td([dcc.Input(id='input-price', type="number", value=250)]), #Try to set the value to the current price of the future with the respective fullfillment date
                        html.Td([dcc.Input(id='input-amount', type="number", value='300')]), 
                        html.Td([dcc.DatePickerSingle(
                                    id='input-date_fullfillment',
                                    min_date_allowed=date.today(),
                                    max_date_allowed=date.today() + timedelta(days=365*5),
                                    
                                    date=date.today() + timedelta(days=365/2)
                                )]),
                            
                        html.Td([dcc.DatePickerSingle(
                                    id='input-date_contract',
                                    min_date_allowed=date.today(),
                                    max_date_allowed=date.today() + timedelta(days=365*5),
                                    
                                    date=date.today() 
                                )])
                        
                    ])     
        
                ]),
            #Button to enter a contract 
            html.Button('enter-contract', n_clicks=0, id='button-enter-contract-state'),
            html.Div(id='output-container-button',
                 children='Press to add contract')
            ]),
    
    #Menu to enter prospected harvest
        dash_table.DataTable(
        commodities_df.to_dict('records'),
        [{"name": i, "id": i} for i in commodities_df.columns]
        )
   
    ])
        ], id='main_div'),
], id='app')














#Callbacks

#load data

@app.callback(Output('main_div', 'children'),
    Input('button-load_data', 'n_clicks'))
def load_data(n_clicks):
    global commodities_df, contracts_df, price_df
     
    try:
        con = sqlite3.connect('contrcalc.db')
        commodities_df = pd.read_sql("Select * from commodities", con, index_col='commodity_id')
        contracts_df = pd.read_sql('Select * FROM contracts', con, index_col='contract_id',  parse_dates=['date_closure', 'date_fullfillment'])
        price_df = pd.read_sql('Select * FROM price_table', con, index_col='price_id')
        print('reloaded data: commodities_df, contracts_df, price_df')
    except:
        print("Error: couldn't reload data from database")
    return commodities_df, contracts_df, price_df


# Changing tab:

#@app.callback(Output('tabs-content', 'children'),
#             Input('commodities-tab', 'value'))
#def render_commodity(tab):
#    return tab


# Changing date range:
@app.callback(Output('rangeslider_time', 'value'[1]),
              Input('date-picker-range', 'start_date'),
             Input('date-picker-range', 'end_date'))
def date_to_slider(start_date, end_date):
    #print(start_date, end_date)
    #start_data =int(start_date)
    #end_date = datetime.strptime(end_date, '%Y-%m-%d')
    return start_date, end_date


#Adding Contract
           
@app.callback(Output('output-container-button', 'children'),
            Input('button-enter-contract-state', 'n_clicks'),
              State('commodity-dropdown', 'value'),
              State('input-price', 'value'),
              State('input-amount', 'value'),
              State('input-date_fullfillment', 'date'),
              State('input-date_contract', 'date')
             )
def add_contract(n_clicks, commodity, price, amount, date_fullfillment, date_contract):
    global contracts_df
    contract_commodity_id = commodities_df[commodities_df['name']==commodity].index  #The id of the commodity that the is the subject of the contract  
    contract = pd.DataFrame({'commodity_id': contract_commodity_id, 'price_per_to': price, 'amount_to': amount, 'date_fullfillment':date_fullfillment, 'date_closure':date_contract}, index=[0])
    contracts_df = pd.concat([contracts_df, contract], axis = 0)
    
    #sends the new contract to sql:
    try:
        con = sqlite3.connect('contrcalc.db')
        contract.to_sql('contracts', con, if_exists='append', index=False)
        print(f'Contract saved: n_clicks:{n_clicks}, commodity:{commodity}, price:{price}, amount:{amount}, date_fullfillment:{date_fullfillment}, date_contract:{date_contract}')
    except:
        print('Failed to send the dataframe to the database')
    
    return

#Display only price data that was selected in Dropdown
@app.callback(Output('price_dev', 'figure'),
             Input('date_fulllfillment-dropdown', 'value'))
def display_price(dates_ff):
    #print(dates_ff)
    #print(price_df['price'])
    print(price_df['date_fullfillment'])
    fig = go.Figure()
       
    # Plot the prices of the selected Futures on the y axis and the date of these prices on the y axis   
    dff = dates_ff  #all available closing dates of Futures
    for future in enumerate(dff):
        print(future)
        fullfill_series = price_df['date_fullfillment'] #
        selected_futures = fullfill_series.isin(future) # series of the values that where selected in 'date_fulllfillment-dropdown' (fullfillment dates of Futures)
        day_of_price_of_selected_futures = price_df[selected_futures]['date_price']
        price_of_selected_futures= price_df['price']
        fig.add_trace(go.Scatter(x=day_of_price_of_selected_futures, y=price_of_selected_futures))
    
    
    #Plot the prices per to of closed contracts on the y axis and the dates of closure on the x axis as points
    price_per_to_of_closed_contracts = contracts_df['price_per_to']
    dates_of_closed_contracts = contracts_df['date_closure']
    for index_of_closed_contract, closed_contract in enumerate(dates_of_closed_contracts):
        print(index_of_closed_contract, closed_contract)
        date_of_closed_contract = dates_of_closed_contracts[index_of_closed_contract]
        price_of_closed_contract = price_per_to_of_closed_contracts[index_of_closed_contract]
        print(f'date_of_closed_contract:{date_of_closed_contract}, price_of_closed_contract: {price_of_closed_contract}.')
        fig.add_trace(go.Scatter(x=[date_of_closed_contract], y=[price_of_closed_contract]))
        
        
        
        
        
    fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
    fig.update_layout(title_text="Wheat Future prices")
    fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="todate"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="todate"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
    return fig





if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
                
            
            
            
    