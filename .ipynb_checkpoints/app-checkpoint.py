from dash import Dash, dcc, html, dash_table, ctx
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import date, timedelta, datetime
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
from ModulScrapeWallstreet import scrape_futureprice, future_price_to_sql, extrapolate_data
import json



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colorscales = px.colors.named_colorscales()

#load table with price data

#con = sqlite3.connect('contrcalc.db') 
#price_df = pd.read_sql('Select * FROM price_table', con, index_col='price_id')



#load table with contracts
#contracts_df = pd.read_sql('Select * FROM contracts', con, index_col='contract_id',  parse_dates=['date_closure', 'date_fullfillment'])


#load table with commodities

#commodities_df = pd.read_sql("Select * from commodities", con, index_col='commodity_id')




app = Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=True)

start_date=str(date.today())
end_date=str(date.today() + timedelta(days=60))

app.layout = html.Div([
    
    #Title
    html.H1('Contract Simulator'),
    #Load Button
    html.Button('Load Data', n_clicks=0, id='button-load_data'),
    html.Div(id='output-load_data'),
    html.Button('Load todays prices', n_clicks=0, id='button-scrape_data'),
    html.Div(id='output-scraped_data'),
    html.Button('Save Data to DB', n_clicks=0, id='button_save_data'),
    html.Div(id='output_save_data'),
        
    html.Div([
    
    #Tabs that display the different contracts and commodities
    dcc.Tabs(id="commodities-tab", value='wheat_tab_val', children=[ 
        dcc.Tab(label='wheat'),
        dcc.Tab(label='barley'),
        dcc.Tab(label='corn', value='corn-tab-val'),
        dcc.Tab(label='rapeseed', value='rapeseed-tab-val'),
        ]),
    
        # Div with all content of one grain, so far only placeholder
        html.Div(id='tabs-content', children=[]),
        html.Div(
    [#input for area planted
        html.Div( 
                 ["Area planted in ha", 
                  dcc.Input(
                    id="input_hectar_wheat",
                    type='number',
                    placeholder='Area planted (ha)'
                    ),
                  html.Div(id='output_hectar_wheat')]),
      #input for amount harvested
         html.Div(       
                ["Expected harvest in to/ha", 
                 dcc.Input(
                    id="input_harvest_per_ha_wheat",
                    type='number',
                    placeholder='Expected harvest (to/ha)'
                ),
                html.Div(id='output_to_per_hectar_wheat')])
    ]
    ),
    #Dropdown to select the respective Futuresprice
        html.Div([dcc.Dropdown(id='date_fullfillment-dropdown',
            multi=True
            )],
                 id="select_future_dropdown"),
                      
    #Graph showing contracted amount
        dcc.Graph(id='price_dev'),            
    #Graph showing commodity price        
    
    
    
    #Slider to adapt time
    
#        dcc.RangeSlider((date.today() - timedelta(days=30)).date(), date.today() + timedelta(days=180), #7, count=1, value=[datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(end_date, '%Y-%m-%d')], #id='rangeslider_time'),
    
#    #DatePickerRange to adapt RangSlider
#        dcc.DatePickerRange(
#        id='date-picker-range',
#        start_date=date.today(),
#        end_date_placeholder_text=date.today()
#        ),
    
    
   
        
        
        
        
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
                    html.Tr([html.H4('Add a contract')]),
                    html.Tr([
                        html.Td([dcc.Dropdown(id='commodity-dropdown')]),
                        html.Td([dcc.Input(id='input-price', type="number", value='')]), 
                        html.Td([dcc.Input(id='input-amount', type="number", value='300')]), 
                        html.Td([dcc.DatePickerSingle(
                                    id='input-date_fullfillment',
                                    #min_date_allowed=date.today(),
                                    #max_date_allowed=date.today() + timedelta(days=365*5),
                                    
                                    date=date.today() + timedelta(days=365/2)
                                )]),
                            
                        html.Td([dcc.DatePickerSingle(
                                    id='input-date_contract',
                                    #min_date_allowed=date.today(),
                                    #max_date_allowed=date.today() + timedelta(days=365*5),
                                    
                                    date=date.today() 
                                )]),
                        html.Td([html.Button('enter contract', n_clicks=0, id='button-enter-contract-state'),
            html.Div(id='output-container-button',
                 children='Press to add contract')
                            
                        ])
                        
                    ]),
                    
#Menu to delete a contract
                    html.Tr([html.H4('Delete a contract')]),
                    html.Tr([
                        
                        html.Td([dcc.Dropdown(id='commodity-dropdown-delete')]),
                        html.Td([dcc.Input(id='input-price-delete', type="number", value='')]), 
                        html.Td([dcc.Input(id='input-amount-delete', type="number", value='300')]), 
                        html.Td([dcc.DatePickerSingle(
                                    id='input-date_fullfillment-delete',
                                    #min_date_allowed=date.today(),
                                    #max_date_allowed=date.today() + timedelta(days=365*5),
                                    
                                    date=date.today() + timedelta(days=365/2)
                                )]),
                            
                        html.Td([dcc.DatePickerSingle(
                                    id='input-date_contract-delete',
                                    #min_date_allowed=date.today(),
                                    #max_date_allowed=date.today() + timedelta(days=365*5),
                                    
                                    date=date.today() 
                                )]),
                        html.Td([html.Button('delete contract', n_clicks=0, id='button-delete-contract-state')
            
                            
                        ])
                        
                    ]),
        html.Div(id='delete-button', children='Press to select contracts to delete')
                ])
            #Button to enter a contract 
            
            ]),
    
            
             #Table showing contracts
 
    # '''dash_table.DataTable(
    # contracts_df.to_dict('records'),
    # [{"name": i, "id": i} for i in contracts_df.columns]
    # ),'''
            
            
            
    #Menu to enter prospected harvest
        # dash_table.DataTable(
        # commodities_df.to_dict('records'),
        # [{"name": i, "id": i} for i in commodities_df.columns]
        # ),
        #      dash_table.DataTable(
        # price_df.to_dict('records'),
        # [{"name": i, "id": i} for i in commodities_df.columns]
        # )
   
    ]),
        
        #Containers that store date when it is pushed from one function to the next:
        dcc.Store(id='price_df_store'), #price_df
        dcc.Store(id='commodities_df_store'), # commodities_df
        dcc.Store(id='contracts_df_store'),
        dcc.Store(id='future_price_today_store')
        
        
        
        ], id='main_div'),
], id='app')














#Callbacks

#Callback that managed the load button and the scrape button behaviour

@app.callback(Output('output-load_data', 'children'),
              Output('output-scraped_data', 'children'),
              Output('commodity-dropdown', 'options'),
              Output('commodity-dropdown-delete', 'options'),
              Output('price_df_store', 'data'),
              Output('commodities_df_store', 'data'),
              Output('contracts_df_store', 'data'),
               
                Input('button-load_data', 'n_clicks'),
             Input('button-scrape_data', 'n_clicks'),
             Input('price_df_store', 'data'),
              Input('commodities_df_store', 'data'),
              Input('contracts_df_store', 'data'))
def load_scrape_data(click_load, click_scrape, price_df_json, commodities_df_json, contracts_df_json):
    
    
    
       
    button_id = ctx.triggered_id if not None else 'No clicks yet'
    print(button_id)
    if button_id == 'button-load_data':
        print('Attempt to load commodites_df, contracts_df and price_df from sql database') 
        try:
            con = sqlite3.connect('contrcalc.db')
            commodities_df = pd.read_sql("Select * from commodities", con, index_col='commodity_id')
            commodities_df_json = commodities_df.to_json(date_format='iso', orient='split')
            print('loaded commodities')


            contracts_df = pd.read_sql('Select * FROM contracts', con, index_col='contract_id',  parse_dates=['date_closure', 'date_fullfillment'])
            contracts_df_json= contracts_df.to_json(date_format='iso', orient='split')
            print('loaded contracts')


            price_df = pd.read_sql('Select * FROM price_table', con, index_col='price_id')
            price_df_json = price_df.to_json(date_format='iso', orient='split')
            print('loaded prices')
            output_message_load = 'reloaded data: commodities_df, contracts_df, price_df'
            com_list = [com for com in commodities_df['name']]
        except:
            output_message_load = "Error: couldn't reload data from database"
            print(output_message_load)
            
        
    elif button_id == 'button-scrape_data':
        print("Attempt to scrape future price data.")
        price_df = pd.read_json(price_df_json, orient = 'split')
        try:
            future_df = scrape_futureprice()
            future_df_clean = future_df[['commodity_id', 'date_fullfillment', 'date_price', 'price', 'currency']]
            print('Scraped Wallstreet sucessfuly')
            print(price_df, future_df_clean)
        except:
            print("Failed to scrape Wallstreet")
        try:
            price_df = pd.concat([price_df, future_df_clean], axis=0)
            price_df.drop_duplicates(keep= 'first', inplace=True)
            print(price_df, future_df_clean)
            print(f'Successfully added scraped data to price_df.')
        except: 
            print('Error: Could not add scraped data to price_df')
        
    else:
        output_message_load = ''
        output_message_scrape = ''
        com_list = []
    
    if 'output_message_scrape' not in locals():
        output_message_scrape = ''
    if 'output_message_load' not in locals(): 
        output_message_load =''
    if 'com_list' not in locals(): 
        com_list =[]
    if 'price_df_json' not in locals():
        price_df = pd.read_json(price_df_json, orient = 'split')
    if  'commodities_df_json' not in locals():
        commodities_df = pd.read_json(commodities_df_json, orient = 'split')
    if 'contracts_df_json' not in locals():
        contracts_df = pd.read_json(contracts_df_json, orient = 'split')
        
    return output_message_load, output_message_scrape, com_list, com_list, price_df_json, commodities_df_json, contracts_df_json    




#Button save data to database
@app.callback(Output('output_save_data', 'children'),
             Input('price_df_store', 'data'),
             Input('contracts_df_store', 'data'),
              Input('commodities_df_store', 'data'),
             Input('future_price_today_store', 'data'))
def save_to_db(price_df_json, contracts_df_json, commodities_df_json, future_price_today_store):
    output_message = 'this button does nothing'
    return output_message
    
    









#Button load todays prices:




# Changing tab:

#@app.callback(Output('tabs-content', 'children'),
#             Input('commodities-tab', 'value'))
#def render_commodity(tab):
#    return tab


# Changing date range:
#@app.callback(Output('rangeslider_time', 'value'[1]),
#              Input('date-picker-range', 'start_date'),
#             Input('date-picker-range', 'end_date'))
#def date_to_slider(start_date, end_date):
#    #print(start_date, end_date)
#    #start_data =int(start_date)
#    #end_date = datetime.strptime(end_date, '%Y-%m-%d')
#    return start_date, end_date



# save expected harvest 
@app.callback(
              Output('output_hectar_wheat', 'children'),
                Output('output_to_per_hectar_wheat', "children"),
             Input("input_hectar_wheat", "value"), 
              Input("input_harvest_per_ha_wheat", "value")
             )
def save_expected_harvest(harvest_area, harvest_tph):
    harvest_list=(harvest_tph, harvest_area,)
    querry=("""
    UPDATE commodities
    SET 
        estimate_harvest_to = ?,
        area_planted = ?
    WHERE
        commodity_id = 2;
    """) 
    try:
        con = sqlite3.connect('contrcalc.db')
        print("Connected to SQLite")
        cur = con.cursor()
        cur.execute(querry, harvest_list)
        con.commit()
        print("Total", cur.rowcount, "Records inserted successfully into SqliteDb_developers table")
        con.commit()
        cur.close()
        output_hectar_wheat = f'Saved to database: {harvest_area} ha'
        output_to_wheat = f'Saved to database: {harvest_tph} to/ha'
    except sqlite3.Error as error:
            print("Failed to insert multiple records into sqlite table", error)
            output_hectar_wheat = "not saved"
            output_to_wheat = "not saved"
    finally:
        if (con):
            con.close()
            print("The SQLite connection is closed")
    return output_hectar_wheat, output_to_wheat





#toggle tropdown to select futures:
@app.callback(Output('date_fullfillment-dropdown', 'options'),
              Output('date_fullfillment-dropdown', 'value'),
             Input('price_df_store', 'data'),
             Input('commodities_df_store', 'data'))
def toggle_futures_dropdown(json_price_df, json_commodities_df):
    price_df = pd.read_json(json_price_df, orient = 'split')
    commodities_df = pd.read_json(json_commodities_df, orient = 'split')
    fullfillment_options = [datefull for datefull in price_df[price_df['commodity_id']==2]['date_fullfillment'].unique()]
    fullfillment_value = price_df[price_df['commodity_id']==2]['date_fullfillment'].unique().max()
    return fullfillment_options, fullfillment_value









#Delete Contract
@app.callback(Output('delete-button', 'children'),
              Input('button-delete-contract-state', 'n_clicks'),
              Input('contracts_df_store', 'data'),
            
              Input('commodities_df_store', 'data'),
              State('commodity-dropdown-delete', 'value'),
              State('input-price-delete', 'value'),
              State('input-amount-delete', 'value'),
              State('input-date_fullfillment-delete', 'date'),
              State('input-date_contract-delete', 'date')
             )           
def delete_contract(n_clicks, contracts_df_json, commodities_df_json, commodity, price, amount, date_fullfillment, date_contract):
    contracts_df = pd.read_json(contracts_df_json, orient='split')
    commodities_df = pd.read_json(commodities_df_json, orient='split')
    
    if not commodity or not price or not amount or not date_fullfillment or not date:
        output = 'Define all features to delete contract'
    else:     
        contract_commodity_id = commodities_df[commodities_df['name']==commodity].index  #The id of the commodity that is the subject of the contract  

        print(contract_commodity_id)
        contract = pd.DataFrame({'commodity_id': contract_commodity_id, 'price_per_to': price, 'amount_to': amount, 'date_fullfillment':date_fullfillment, 'date_closure':date_contract}, index=[0])
        contracts_df = pd.concat([contracts_df, contract], axis = 0)

        print(f'Attempt to delete contract: {contract_commodity_id, price, amount, date_fullfillment, date_contract}')
        querry = """
        SELECT * FROM contracts
            WHERE (price_per_to = :price)"""
        #sends the new contract to sql:
        output = 'Select features of contract to delete.'
        try:
            if price:
                print(f'Connecting to db to collect contract')
                con = sqlite3.connect('contrcalc.db')
                to_delete = pd.read_sql(querry, con, params = {'price':price})
                output = f'Do you want to delete this contract? {to_delete}'

                #print(f'Contract saved: n_clicks:{n_clicks}, commodity:{commodity}, price:{price}, amount:{amount}, date_fullfillment:{date_fullfillment}, date_contract:{date_contract}')
            else:
                print('No contract selected, some input is not clear.')
                pass
        except:
            print('Failed to select a contract from database')

        try:
            print('Deleting contracts')
            con = sqlite3.connect('contrcalc.db')
            cur = con.cursor()
            cur.execute(""" DELETE FROM contracts
                                    WHERE ( 
                                    price_per_to = :price
                                    AND amount_to = :amount
                                    AND date_fullfillment = :date_ff
                                    AND date_closure = :date_c
                                    )
                """, {"contract_commodity_id": contract_commodity_id, 'price': price, 'amount': amount, 'date_ff': date_fullfillment, 'date_c':date_contract})
            con.close()
            output += 'Contract deleted'
        except: 
            print('Something went wrong while trying to delte contract')
    return output


#Add Contract
           
@app.callback(Output('output-container-button', 'children'),
              Input('commodities_df_store', 'data'),
              Input('contracts_df_store', 'data'),
            Input('button-enter-contract-state', 'n_clicks'),
              State('commodity-dropdown', 'value'),
              State('input-price', 'value'),
              State('input-amount', 'value'),
              State('input-date_fullfillment', 'date'),
              State('input-date_contract', 'date')
             )
def add_contract(commodities_df_json, contracts_df_json, n_clicks, commodity, price, amount, date_fullfillment, date_contract):
    commodities_df = pd.read_json(commodities_df_json, orient='split')
    contracts_df = pd.read_json(contracts_df_json, orient='split')
    
    if not commodity or not price or not amount or not date_fullfillment or not date:
        output_message = 'Define all features to add contract'
    else:     
    
        print('Attempt to add contract', commodity)
        contract_commodity_id = commodities_df[commodities_df['name']==commodity].index  #The id of the commodity that the is the subject of the contract  

        print(contract_commodity_id)
        contract = pd.DataFrame({'commodity_id': contract_commodity_id, 'price_per_to': price, 'amount_to': amount, 'date_fullfillment':date_fullfillment, 'date_closure':date_contract}, index=[0])
        contracts_df = pd.concat([contracts_df, contract], axis = 0)

        #sends the new contract to sql:
        try:
            if price:
                con = sqlite3.connect('contrcalc.db')
                contract.to_sql('contracts', con, if_exists='append', index=False)
                output_message = f'Contract saved: n_clicks:{n_clicks}, commodity:{commodity}, price:{price}, amount:{amount}, date_fullfillment:{date_fullfillment}, date_contract:{date_contract}'
            else:
                output_message = 'No contract added because, price is empty.'
                pass
        except:
            output_message = 'Failed to send the dataframe to the database'

    return output_message






#Display only price data that was selected in Dropdown
@app.callback(Output('price_dev', 'figure'),
             Input('date_fullfillment-dropdown', 'value'),
             Input("input_hectar_wheat", "value"), 
              Input("input_harvest_per_ha_wheat", "value"),
             Input("price_df_store", "data"),
             Input("contracts_df_store", "data"),
             Input("commodities_df_store", "data"))
def display_price(dates_ff, harvest_area, harvest_tph, price_df_json, contracts_df_json, commodities_df_json):
    commodities_df = pd.read_json(commodities_df_json, orient='split')
    contracts_df = pd.read_json(contracts_df_json, orient='split')
    price_df = pd.read_json(price_df_json, orient='split')
    #print('Adding Data to Figure')
    #print(price_df['price'])
    #print(price_df['date_fullfillment'])
    fig = go.Figure()
       
    # Plot the prices of the selected Futures on the y axis and the date of these prices on the y axis   
    dff = dates_ff  #all available closing dates of Futures
    #print(f'Available closing dates: {dff}')
    for index, future in enumerate(dff):
        #print(f'Future to add to figure: {index, future}')
        try:
            fullfill_series = price_df['date_fullfillment'] #
            #print(f'All fullfillment dates in price_df: {fullfill_series}')
            #print(fullfill_series.isin(future))
            #selected_futures = fullfill_series[future] # series of the values that where selected in 'date_fullfillment-dropdown' (fullfillment dates of Futures)
            #print(f'selected futures: {selected_futures}')
            day_of_price_of_selected_futures = price_df[price_df['date_fullfillment']==future]['date_price']
            price_of_selected_futures= price_df['price']
            fig.add_trace(go.Scatter(x=day_of_price_of_selected_futures, y=price_of_selected_futures, name=future, mode='lines+markers'))
            fig.update_traces(marker=dict(colorscale='Agsunset'))
            print('Added future to figure')
        except:
            print('Could not add future to figure')
    
    #Plot the prices per to of closed contracts on the y axis and the dates of closure on the x axis as points
    price_per_to_of_closed_contracts = contracts_df['price_per_to']
    dates_of_closed_contracts = contracts_df['date_closure']
    fullfillment_dates_of_contracts = contracts_df['date_fullfillment']
    
    try:    
        
        fig.add_trace(go.Scatter(name="date/price closed", x=dates_of_closed_contracts, y=price_per_to_of_closed_contracts, mode='markers'))
        #fig.update_trace(marker=dict(colorscale='viridis'))
           
        print(f'Added to Scatterplot: date_of_closed_contract:{dates_of_closed_contracts}, price_of_closed_contract: {price_per_to_of_closed_contracts}.')
    except:
        print('Failed to add dates_of_closed_contract and price_per_to_of_closed_contractst to figure')
        
   
    
    
    
    
    #add column total harvest
    commodities_df['total_harvest']= commodities_df['estimate_harvest_to']*commodities_df['area_planted']
    
    #add next_harvest_date as daytetime 
    commodities_df['next_harvest_date'] = [datetime.strptime(f'2022/{month}/01', "%Y/%m/%d") for month in commodities_df['harvest_month']]
    print(commodities_df)
    
    
    #Add contracted amount in to as barplot
    fig.add_trace(go.Bar( name='contracted amount', x=contracts_df["date_fullfillment"],
             y=contracts_df["price_per_to"], width=100))    
    
    
    #Add expected harvest barplot
    fig.add_trace(go.Bar(x=commodities_df[commodities_df.index==2]['next_harvest_date'],
             y=commodities_df['total_harvest'], name='expected harvest', width=200))
    
    
    
    
    
    
    
    #Add marker styling 
    fig.update_traces(marker=dict(size=10,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
    
    #Add title
    fig.update_layout(title_text="Wheat Future prices")
    
    
    #Add boxes to select time frame
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
        #Ad rangeslider to filter timeframe
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
    return fig



# #Manage dataflow to price_df_store, commodities_df_store and contracts_df_store
# @app.callback(Output('price_df_store', 'data'),
#              Output('commodities_df_store', 'data'),
#              Output('contracts_df_store'),
#              Input(),
#              Input(),
#              Input(),)
# def manage_data_store():
#     return




if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
                
            
            
            
    