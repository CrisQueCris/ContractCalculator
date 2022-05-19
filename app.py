from dash import Dash, dcc, html, dash_table, ctx
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import date, timedelta, datetime
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
from ModulScrapeWallstreet import scrape_futureprice, future_price_to_sql, extrapolate_data
import json
from modules_app import *
from plotly.subplots import make_subplots



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
                        html.Th('Date of contract'),
                        html.Th('Date of fullfillment')
                                            
                        ])
                    ]),
                html.Tbody([
                    html.Tr([html.H4('Add a contract')]),
                    html.Tr([
                        html.Td([dcc.Dropdown(id='commodity-dropdown-enter')]),
                        html.Td([dcc.Input(id='input-price-enter', type="number", value='0')]), 
                        html.Td([dcc.Input(id='input-amount-enter', type="number", value='300')]), 
                         html.Td([dcc.DatePickerSingle(
                                    id='input-date_contract-enter',
                                    #min_date_allowed=date.today(),
                                    #max_date_allowed=date.today() + timedelta(days=365*5),
                                    
                                    date=date.today() 
                                )]),
                        html.Td([dcc.DatePickerSingle(
                                    id='input-date_fullfillment-enter',
                                    #min_date_allowed=date.today(),
                                    #max_date_allowed=date.today() + timedelta(days=365*5),
                                    
                                    date=date.today() + timedelta(days=365/2)
                                )]),
                            
                       
                        html.Td([html.Button('enter contract', n_clicks=0, id='button-enter-contract-state'),
            html.Div(id='output_enter_button',
                 children='Press to add contract')
                            
                        ])
                        
                    ]),
                    
#Menu to delete a contract
                    html.Tr([html.H4('Delete a contract')]),
                    html.Tr([
                        
                        html.Td([dcc.Dropdown(id='commodity-dropdown-delete')]),
                        html.Td([dcc.Input(id='input-price-delete', type="number", value='0')]), 
                        html.Td([dcc.Input(id='input-amount-delete', type="number", value='300')]), 
                        
                            
                        html.Td([dcc.DatePickerSingle(
                                    id='input-date_contract-delete',
                                    #min_date_allowed=date.today(),
                                    #max_date_allowed=date.today() + timedelta(days=365*5),
                                    
                                    date=date.today() 
                                )]),
                        html.Td([dcc.DatePickerSingle(
                                    id='input-date_fullfillment-delete',
                                    #min_date_allowed=date.today(),
                                    #max_date_allowed=date.today() + timedelta(days=365*5),
                                    
                                    date=date.today() + timedelta(days=365/2)
                                )]),
                        html.Td([html.Button('delete contract', n_clicks=0, id='button-delete-contract-state')
            
                            
                        ])
                        
                    ]),
        html.Div(id='output_delete_button', children='Press to select contracts to delete')
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
             
              Output('output_enter_button', 'children'),
              Output('output_delete_button', 'children'),
              Output('commodity-dropdown-enter', 'options'),
              Output('commodity-dropdown-delete', 'options'),
              Output('price_df_store', 'data'),
              Output('commodities_df_store', 'data'),
              Output('contracts_df_store', 'data'),
              
               Output('output_hectar_wheat', 'children'),
                Output('output_to_per_hectar_wheat', "children"),
               
                Input('button-load_data', 'n_clicks'),
             Input('button-scrape_data', 'n_clicks'),
              Input('button_save_data', 'n_clicks'),
              Input('button-enter-contract-state', 'n_clicks'),
              Input('button-delete-contract-state', 'n_clicks'),
              
              
             Input('price_df_store', 'data'),
              Input('commodities_df_store', 'data'),
              Input('contracts_df_store', 'data'),
              
             State('commodity-dropdown-enter', 'value'),
              State('input-price-enter', 'value'),
              State('input-amount-enter', 'value'),
              State('input-date_fullfillment-enter', 'date'),
              State('input-date_contract-enter', 'date'), 
              
              State('commodity-dropdown-delete', 'value'),
              State('input-price-delete', 'value'),
              State('input-amount-delete', 'value'),
              State('input-date_fullfillment-delete', 'date'),
              State('input-date_contract-delete', 'date'),
              
              Input("input_hectar_wheat", "value"), 
              Input("input_harvest_per_ha_wheat", "value")
              
              
             )
def load_scrape_save_data(click_load, click_scrape, click_save, click_enter, click_delete, #Button clicks inputs
                          price_df_json, commodities_df_json, contracts_df_json, #stored Dataframe in json inputs
                         commodity_entered, price_entered, amount_entered, date_fullfillment_entered, date_contract_entered, #Enter contract inputs
                          commodity_del, price_del, amount_del, date_fullfillment_del, date_contract_del,
                         wheat_area, wheat_to_per_ha):
   
  
    
       
    button_id = ctx.triggered_id if not None else 'No clicks yet' #info about which button was triggered
    print(button_id)
    
    
    #load button
    if button_id == 'button-load_data':
        output_message, com_list, price_df_json, contracts_df_json, commodities_df_json = load_dfs()
      
            
    #scrape button    
    elif button_id == 'button-scrape_data':
        price_df = pd.read_json(price_df_json, orient = 'split')
        
        commodities_df = pd.read_json(commodities_df_json, orient = 'split')
        contracts_df = pd.read_json(contracts_df_json, orient = 'split')
        print("Attempt to scrape future price data.")
       
        try:
            future_df = scrape_futureprice()
            future_df_clean = future_df[['commodity_id', 'date_fullfillment', 'date_price', 'price', 'currency']]
            print('Scraped Wallstreet sucessfuly')
            print(price_df, future_df_clean)
        except:
            print("Failed to scrape Wallstreet")
        try:
            price_df['date_fullfillment']= pd.to_datetime(price_df['date_fullfillment'], format='%Y/%m/%d %H:%M:%S').dt.date
            price_df['date_price']= pd.to_datetime(price_df['date_price'], format='%Y/%m/%d %H:%M:%S').dt.date
            future_df_clean['date_fullfillment']=future_df_clean['date_fullfillment'].dt.date
            future_df_clean['date_price']=future_df_clean['date_price'].dt.date
            print(price_df, future_df_clean)
            price_df = pd.concat([price_df, future_df_clean], axis=0)
            print(price_df)
            price_df.drop_duplicates(keep= 'first', inplace=True)
            print(price_df)
            price_df_json = price_df.to_json(date_format='iso', orient='split')
            print(price_df, future_df_clean)
            print(f'Successfully added scraped data to price_df')
        except: 
            print('Error: Could not add scraped data to price_df')
    

    
    
    #save button
    elif button_id =='button_save_data':
        price_df = pd.read_json(price_df_json, orient = 'split')
        commodities_df = pd.read_json(commodities_df_json, orient = 'split')
        contracts_df = pd.read_json(contracts_df_json, orient = 'split')    
        try:
            print('Connecting to Database to save')
            con = sqlite3.connect('contrcalc.db')
            print('connected to db')
            print(contracts_df)
            contracts_df.to_sql('contracts', con, if_exists='replace', index=False, index_label='contract_id')
            print('contracts_df stored to db')
            price_df.to_sql('price_table', con, if_exists='replace', index_label='price_id')
            print('price_df stored to db')
            commodities_df.to_sql('commodities', con, if_exists='replace', index_label='commodity_id')
            print('commodities_df stored to db')
            output_message = 'Sucessfuly saved to db'
            print(output_message)
        except:
            output_message = 'Error: failed to save dataframes'
            print(output_message)
            
        
    
    # button enter contract
    elif button_id =='button-enter-contract-state':
        
        price_df = pd.read_json(price_df_json, orient = 'split')
        commodities_df = pd.read_json(commodities_df_json, orient = 'split')
        contracts_df = pd.read_json(contracts_df_json, orient = 'split')
        if not commodity_entered or not price_entered or not amount_entered or not date_fullfillment_entered or not date_contract_entered:
            output_message_enter = 'Define all features to add contract'
        else:     

            print('Attempt to add contract', commodity_entered)
            contract_commodity_id = commodities_df[commodities_df['name']==commodity_entered].index  #The id of the commodity that the is the subject of the contract  

            contract_id = len(contracts_df) +1
            contract = pd.DataFrame({'contract_id':contract_id, 'commodity_id': contract_commodity_id, 'price_per_to': price_entered, 'amount_to': amount_entered, 'date_fullfillment':date_fullfillment_entered, 'date_closure':date_contract_entered}, index=[0])
            contracts_df = pd.concat([contracts_df, contract], axis = 0)
            contracts_df_json = contracts_df.to_json(date_format='iso', orient='split')
            output_message_enter = 'Contract added. Click save to add to database'
            print(output_message_enter)

            
            
            
            
            
            
    #button delete contract
    elif button_id =='button-delete-contract-state':
        price_df = pd.read_json(price_df_json, orient = 'split')
        commodities_df = pd.read_json(commodities_df_json, orient = 'split')
        contracts_df = pd.read_json(contracts_df_json, orient = 'split')
        
        if not commodity_del or not price_del or not amount_del or not date_fullfillment_del or not date_contract_del:
            output_message_del = 'Define all features to delete contract'
        else:     
            print(commodity_del)
            if commodity_del == 'wheat':
                contract_commodity_id_del = 2
            amount_del = int(amount_del)
            print(contracts_df)
            print(f'check input: {contract_commodity_id_del}, {type(price_del), price_del}, {type(amount_del), amount_del}, {date_fullfillment_del}, {date_contract_del} ')
                      
            print(contracts_df['commodity_id']== contract_commodity_id_del)
            print(contracts_df['price_per_to']== price_del)
            print(contracts_df['amount_to']== amount_del)
            print(contracts_df['date_fullfillment']==date_fullfillment_del)
            print(contracts_df['date_closure']==date_contract_del)
            
            
            
            contract_to_del = contracts_df[contracts_df['date_fullfillment']==date_fullfillment_del] 
            print(contract_to_del)    
            contracts_df = contracts_df.drop(contract_to_del.index)
            contracts_df_json= contracts_df.to_json(date_format='iso', orient='split')
            print(contracts_df)
            output_message_del = f'Removed {contract_to_del}, click save to save changes on database'
            print(output_message_del)
    else:
        #updates from area planted and expected harvest in to/ha
        if 'wheat_to_per_ha' in locals() or 'wheat_area' in locals():
            try:
                commodities_df = pd.read_json(commodities_df_json, orient = 'split')
                print(commodities_df_json)
                print(commodities_df)
                commodities_df.loc[commodities_df.index==2,'estimate_harvest_to'] = wheat_to_per_ha
                commodities_df.loc[commodities_df.index==2, 'area_planted'] = wheat_area
                print(commodities_df)
                commodities_df_json = commodities_df.to_json(date_format='iso', orient='split')
                print('stored harvest data in commodities_df')
                output_hectar_wheat = f'{wheat_area}ha, press save'
                output_to_wheat = f'{wheat_to_per_ha}to/ha, press save'
#                 con = sqlite3.connect('contrcalc.db')
                
                
#                 print('Connecting to Database to save')
#                 con = sqlite3.connect('contrcalc.db')
                    
#                 commodities_df.to_sql('commodities', con, if_exists='replace', index_label='commodity_id')
#                 print('commodities_df stored to db')
                
                
                
            except:
                print("failed to store harvest data in commodities_df")
        else:
            output_hectar_wheat ='' 
            output_to_wheat = ''

            
    
    if 'output_message' not in locals():
        output_message = ''
    if 'com_list' not in locals(): 
        com_list =[]
    if 'output_message_enter' not in locals():
        output_message_enter = ''
    if 'output_message_del' not in locals():
        output_message_del = ''
    if 'output_hectar_wheat' not in locals():
        output_hectar_wheat = ''
    if 'output_to_wheat' not in locals():
        output_to_wheat = '' 
     
    #Updating Commodities_df to be stored in commodities_df_store
    
    
        
    
    
    
    return output_message, output_message_enter, output_message_del, com_list, com_list, price_df_json, commodities_df_json, contracts_df_json, output_hectar_wheat, output_to_wheat 
   
    



    
    









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









#toggle tropdown to select futures:
@app.callback(Output('date_fullfillment-dropdown', 'options'),
              Output('date_fullfillment-dropdown', 'value'),
             Input('price_df_store', 'data'),
             Input('commodities_df_store', 'data'))
def toggle_futures_dropdown(json_price_df, json_commodities_df):
    price_df = pd.read_json(json_price_df, orient = 'split')
    commodities_df = pd.read_json(json_commodities_df, orient = 'split')
    fullfillment_options = [datefull for datefull in price_df[price_df['commodity_id']==2]['date_fullfillment'].unique()]
    fullfillment_value = price_df[price_df['commodity_id']==2]['date_fullfillment'].unique()
    return fullfillment_options, fullfillment_value
  





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
    fig = make_subplots(specs=[[{"secondary_y": True}]])
       
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
            fig.add_trace(go.Scatter(x=day_of_price_of_selected_futures, y=price_of_selected_futures, name=future, mode='lines+markers'), secondary_y=False,)
            fig.update_traces(marker=dict(colorscale='Agsunset'))
            print('Added future to figure')
        except:
            print('Could not add future to figure')
    
    #Plot the prices per to of closed contracts on the y axis and the dates of closure on the x axis as points
    price_per_to_of_closed_contracts = contracts_df['price_per_to']
    dates_of_closed_contracts = contracts_df['date_closure']
    fullfillment_dates_of_contracts = contracts_df['date_fullfillment']
    
    try:    
        
        fig.add_trace(go.Scatter(name="date/price closed", x=dates_of_closed_contracts, y=price_per_to_of_closed_contracts, mode='markers'), secondary_y=False, )
        fig.update_yaxes(title_text="Future price and price of contracts in to", secondary_y=False)
        #fig.update_trace(marker=dict(colorscale='viridis'))
           
        print(f'Added to Contracts to Plot')
    except:
        print('Failed to add dates_of_closed_contract and price_per_to_of_closed_contractst to figure')
        
   
    
    
    
    
    #add column total harvest
    commodities_df['total_harvest']= commodities_df['estimate_harvest_to']*commodities_df['area_planted']
    
    #add next_harvest_date as daytetime 
    commodities_df['next_harvest_date'] = [datetime.strptime(f'2022/{month}/01', "%Y/%m/%d") for month in commodities_df['harvest_month']]
    
    
    #Add expected harvest barplot
    try:
        print(commodities_df.loc[commodities_df.index==2, 'next_harvest_date'])
        print(commodities_df['total_harvest'])
        fig.add_trace(go.Bar(x=commodities_df.loc[commodities_df.index==2, 'next_harvest_date'],
             y=commodities_df.loc[commodities_df.index==2, 'total_harvest'], name='expected harvest'), secondary_y=True, )
        fig.update_yaxes(title_text="contracted amount and expected harvest in to", secondary_y=True)
        print('added expected harvest plot')
    except:
        print("couldn't add expected harvest plot")
    
    #Add contracted amount in to as barplot
    try:
        fig.add_trace(go.Bar( name='contracted amount', x=contracts_df["date_fullfillment"],
             y=contracts_df["price_per_to"]), secondary_y=True)    
        print('added contracted amount in to')
    except:
        print("Error: couldn't add contracted amount in to")
    
    
    #Add marker styling 
    fig.update_traces(marker=dict(size=10,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
    
    #Add title
    fig.update_layout(title_text="Future prices, contracted amount in to and GBP and expected harvest")
    
    
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
    
    
    
                
            
            
            
    