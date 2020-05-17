import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas
import plotly.graph_objs as go
import dash_table
from data_combine_process import data
import urllib 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__) #external_stylesheets=external_stylesheets)

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

#df = pd.read_csv(
#    'https://gist.githubusercontent.com/chriddyp/' +
#    '5d1ea79569ed194d432e56108a04d188/raw/' +
#    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
#    'gdp-life-exp-2007.csv')



app.layout = html.Div(children=[
    # dcc.Graph(
    #     id='life-exp-vs-gdp',
    #     figure={
    #         'data': [
    #             go.Scatter(
    #                 x=data[data.groupby('Fulladdress_processed').transform('count') > 1].finalscore_FA,
    #                 y=data[data.groupby('Fulladdress_processed').transform('count') > 1].finalscore_LN,
    #                 text=data[data.groupby('Fulladdress_processed').transform('count') >1]['Legal_Name'],
    #                 mode='markers',
    #                 opacity=0.7,
    #                 marker={
    #                     'size': 15,
    #                     'line': {'width': 0.5, 'color': 'white'}
    #                 },
    #                 name='new'
    #             )
    #         ],
    #         'layout': go.Layout(
    #             xaxis={ 'title': 'Full Address Final Score'},
    #             yaxis={'title': 'Legal Name Final Score'},
    #             margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
    #             legend={'x': 0, 'y': 1},
    #             hovermode='closest'
    #         )
    #     }
    # ),

    # html.H4(children='US Agriculture Exports (2011)'),
    # dash_table.DataTable(
    #     data= data.to_dict('rows'),
    #     columns = [{'id': c, 'name': c} for c in data.columns],
    #     n_fixed_rows=1,
    #     style_table={'overflowX': 'scroll','maxHeight': '300',
    #                     'overflowY': 'scroll' },
    # ),

    html.Div(id='output-a'),
    html.Div(id='Shape'),

    html.Label('Final group score: Address'),
    dcc.RangeSlider(
        id='address-group-score',
        min=0,
        max=data.finalscore_FA_means.astype('float').max(),
        marks={i: 'Score {}'.format(i) if i == 1 else str(i) 
                for i in range(0, int(data.finalscore_FA_means.max()), 10)},
            value=[0, 100],
    ),
    html.Label('Final group score: Name'),
    dcc.RangeSlider(
        id='name-group-score',
        min=0,
        max=data.finalscore_LN_means_scaled.astype('float').max(),
        marks={i: 'Score {}'.format(i) if i == 1 else str(i) 
                for i in range(0, int(data.finalscore_LN_means_scaled.max()), 10)},
            value=[0, 100],
    ),
  #  html.Button('Reset', id='reset-sliders', n_clicks=0)
    html.Div(id='none',children=[],style={'display': 'none', 'margin-top': 30}),

    html.A(
        'Download Data',
        id='download-link',
        download="rawdata.csv",
        href="",
        target="_blank"
    )
    
])

@app.callback(
    dash.dependencies.Output('output-a', 'children'),
    [dash.dependencies.Input('address-group-score', 'value'), 
    dash.dependencies.Input('name-group-score', 'value')]    
    )
def updatetable(addressscore, namescore):
    return dash_table.DataTable(
        data= data[(data.finalscore_LN_means_scaled <= namescore[1]) & (data.finalscore_LN_means_scaled >= namescore[0]) & (data.finalscore_FA_means >= addressscore[0]) & (data.finalscore_FA_means <= addressscore[1])].sort_values(by='Legal_Name').to_dict('rows'),
        columns = [{'id': c, 'name': c} for c in data.columns],
       # n_fixed_rows=1,
        n_fixed_columns=2,
         style_table={'overflowX': 'scroll','maxHeight': '900',
                        'overflowY': 'scroll', 'minWidth': '1800' },
         style_cell={
         'minWidth': '180px', 'width': '180px',
         'height':'10px', 'minHeight': '10px'},       
    #     css=[{
    #     'selector': '.dash-cell div.dash-cell-value',
    #     'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
    # }],         
        editable=True,
        filtering=True,
        sorting=True,
        sorting_type='multi',
        pagination_mode="fe",
            pagination_settings={
                "displayed_pages": 1,
                "current_page": 0,
                "page_size": 35,
            }
    )

@app.callback(
    dash.dependencies.Output('Shape', 'children'),
    [dash.dependencies.Input('address-group-score', 'value'), 
    dash.dependencies.Input('name-group-score', 'value')]    
    )
def updatenrows(addressscore, namescore):
    return "Number of rows: ", str(data[(data.finalscore_LN_means_scaled <= namescore[1]) & (data.finalscore_LN_means_scaled >= namescore[0]) & (data.finalscore_FA_means >= addressscore[0]) & (data.finalscore_FA_means <= addressscore[1])].shape[0])


@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [dash.dependencies.Input('none', 'children')])
def savetofile(none):
    csv_string = data.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string

# for out in ['address-group-score', 'name-group-score']:
#     @app.callback(dash.dependencies.Output(out, 'value'), [dash.dependencies.Input('reset-sliders', 'n_clicks')])
#     def resetcounter(n_clicks):
#         if n_clicks > 0:
#             return {'value':[40,80]}
#         else:
#             pass

if __name__ == '__main__':
    app.run_server(debug=True)