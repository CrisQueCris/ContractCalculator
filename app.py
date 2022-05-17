from dash import Dash, dcc, html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div([
    
    
    #Title
    html.H1('Contract Simulator'), 
    
    
    
    #Tabs that display the different contracts and commodities
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[ 
        dcc.Tab(label='Wheat', value='tab-1-example-graph'),
        dcc.Tab(label='Barley', value='tab-2-example-graph'),
        dcc.Tab(label='Corn', value='tab-3-example-graph'),
        dcc.Tab(label='Rapeseed', value='tab-4-example-graph'),
        ]),
    html.Div(id='tabs-content-example-graph'),
                
            
            
            
            
            
            #Graph showing contracted amount
            
            
            #Graph showing commodity price
            dcc.Graph(
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [3, 1, 2],
                        'type': 'bar'
                    }]
                }
            ),
    
    
    dcc.Dropdown(
    ['Spotprice', 'May 2022', 'June 2022', 'July 2022', 'August 2022', 'September 2022'],
    ['Spotprice', 'September 2022'],
    multi=True
    )    
    ])




@app.callback(Output('tabs-content-example-graph', "out-all-types",'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
            
            #Heading Commodity
            html.H3('Wheat price'),
                        
        ])
    elif tab == 'tab-2-example-graph':
        return html.Div([
            html.H3('Tab content 2'),
        ])
    


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
                
            
            
            
    