from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import date, timedelta
import sqlite3



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#load table with price data
future_df = pd.read_csv('Data/future_df.csv')

#load table with contracts
contracts_df = pd.read_csv('Data/contracts_df.csv') 


#load table with commodities
con = sqlite3.connect('contrcalc.db')
commodities_df = pd.read_sql("Select * from commodities", con, index_col='commodity_id')

app = Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div([
    
    
    #Title
    html.H1('Contract Simulator'), 
    
    
    
    #Tabs that display the different contracts and commodities
    dcc.Tabs(id="commodities-tab", value='wheat_tab_val', children=[ 
        dcc.Tab(label='wheat', value='wheat-tab-val'),
        dcc.Tab(label='barley', value='barley-tab-val'),
        dcc.Tab(label='corn', value='corn-tab-val'),
        dcc.Tab(label='rapeseed', value='rapeseed-tab-val'),
        ]),
    html.Div(id='tabs-content', children=[
    #Dropdown to select the respective Futuresprice
    dcc.Dropdown(
    ['Spotprice', 'May 2022', 'June 2022', 'July 2022', 'August 2022', 'September 2022'],
    ['Spotprice', 'September 2022'],
    multi=True
    ),    
    #Graph showing contracted amount
    dcc.Graph(
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [3, 1, 2],
                        'type': 'bar'
                    }]
                }
            ),            
    #Graph showing commodity price        
    
    
    
    #Slider to adapt time
    dcc.RangeSlider(-5, 10, 1, count=1, value=[-3, 7]),
    
    #DatePickerRange to adapt RangSlider
    dcc.DatePickerRange(
    id='date-picker-range',
    start_date=date(1997, 5, 3),
    end_date_placeholder_text='Select a date!'
    ),
    
    ]),
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
                        html.Td([dcc.Input(id='input-price', type="number", value='80')]),
                        html.Td([dcc.Input(id='input-amount', type="number", value='300')]),
                        html.Td([dcc.DatePickerSingle(
                                    id='input-date_fullfillment',
                                    min_date_allowed=date.today(),
                                    max_date_allowed=date.today() + timedelta(days=365*5),
                                    
                                    date=date.today()
                                )]),
                            
                        html.Td([dcc.DatePickerSingle(
                                    id='input-date_contract',
                                    min_date_allowed=date.today(),
                                    max_date_allowed=date.today() + timedelta(days=365*5),
                                    
                                    date=date.today() + timedelta(days=365/2)
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
])
            
#Callbacks

# Changing tab:

@app.callback(Output('tabs-content', 'children'),
             Input('commodities-tab', 'value'))
def render_commodity(tab):
    return tab


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
    output_text = f'Contracts saved: {n_clicks}'
    
    commodity_id = commodities_df[commodities_df['name']==commodity].index
    contract = pd.DataFrame({'commodity_id': commodity_id, 'price_per_to': price, 'amount_to': amount, 'date_fullfillment':date_fullfillment, 'date_closure':date_contract}, index=[0])
    contracts_df = pd.concat([contracts_df, contract], axis = 0)
    contract.to_csv('Data/contracts_df.csv')
    con = sqlite3.connect('contrcalc.db')
    contract.to_sql('contracts', con, if_exists='append', index=False)
    return output_text
    


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
                
            
            
            
    