# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 10:26:48 2021

@author: DOYLE_RYAN
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 19:59:48 2021

@author: DOYLE_RYAN
"""

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import base64


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# pandas dataframe to html table

df = pd.read_csv("C:/Users/DOYLE_RYAN/Documents/hall_of_fame_stats.csv", header=0)
df['BA']=df['BA'].map("{:,.3f}".format)
df['SLG']=df['SLG'].map("{:,.3f}".format)
df['OBP']=df['OBP'].map("{:,.3f}".format)
df['OPS']=df['OPS'].map("{:,.3f}".format)
df=df.drop(columns=['GDP', 'SF', 'IBB','SH'])

app = dash.Dash(__name__, external_stylesheets=stylesheet)

stats_labels = [{'label' : stat, 'value' : stat} for stat in df.columns[7:]]



app.layout = html.Div([
    html.Div([
    
    html.H1('MLB Hall of Fame Batting Stats',
            style={'textAlign' : 'center', 'font-family': 'gotham bold'}),
    html.A('Baseball Reference (Source)',
           href='https://www.baseball-reference.com/',
           style={'textAlign' : 'center'},
           target='_blank'),
    ]),
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 10,
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            virtualization=True,
            
            style_cell_conditional=[
                {'if': {'column_id': 'RK'},
                 'width': '5%', 'textAlign': 'left'},
                {'if': {'column_id': 'Name'},
                 'width': '10%', 'textAlign': 'left'},
                {'if': {'column_id': 'WAR/pos'},
                 'width': '5%', 'textAlign': 'left'},
                {'if': {'column_id': 'G'},
                 'width': '5%', 'textAlign': 'left'},
                {'if': {'column_id': 'PA'},
                 'width': '5%', 'textAlign': 'left'},
                {'if': {'column_id': 'AB'},
                 'width': '5%', 'textAlign': 'left'},
                {'if': {'column_id': 'R'},
                 'width': '4%', 'textAlign': 'left'},
                {'if': {'column_id': 'H'},
                 'width': '4%', 'textAlign': 'left'},
                {'if': {'column_id': '2B'},
                 'width': '4%', 'textAlign': 'left'},
                {'if': {'column_id': '3B'},
                 'width': '4%', 'textAlign': 'left'},
                {'if': {'column_id': 'HR'},
                 'width': '3%', 'textAlign': 'left'},
                {'if': {'column_id': 'RBI'},
                 'width': '4%', 'textAlign': 'left'},
                {'if': {'column_id': 'BB'},
                 'width': '3%', 'textAlign': 'left'},
                {'if': {'column_id': 'SO'},
                 'width': '3%', 'textAlign': 'left'},
                {'if': {'column_id': 'BA'},
                 'width': '4%', 'textAlign': 'left'},
                {'if': {'column_id': 'OBP'},
                 'width': '4%', 'textAlign': 'left'},
                {'if': {'column_id': 'SLG'},
                 'width': '4%', 'textAlign': 'left'},
                {'if': {'column_id': 'OPS'},
                 'width': '4%', 'textAlign': 'left'},
                ],
            ),    
        ],
        className='row'),
    html.Div([
        html.H4('Stat to Display:'),
        dcc.Dropdown(
            id='statsdropdown',
            options=stats_labels,
            value='WAR/pos'
            )
        ]),
    html.Div([
        html.Div([
            dcc.Graph(id='barchart',
            style={'width': '220vh', 'height': '100vh'})
            ],
            className='six columns')
    ]),
    html.Div([
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
    html.H4("ABOUT",
            style={'textAlign' : 'left', 'font-family': 'gotham bold'}),
    html.H4("-This Dashboard allows the user to compare the batting statistics of any MLB player inducted into the Hall of Fame",
            style={'textAlign' : 'left', 'font-family': 'gotham bold'}),
    html.H4("-In order to use the Dashboard please selct the players you would like to compare and pick a statistical catagory from the dropdown list",
            style={'textAlign' : 'left', 'font-family': 'gotham bold'}),
    html.H4("The source for this data is ",
            style={'textAlign' : 'left', 'font-family': 'gotham bold'}),
    html.A('www.baseballreference.com',
           href='https://www.baseball-reference.com/',
           style={'textAlign' : 'left', 'font-family': 'gotham bold'})
    ])
 ])
   

@app.callback(
    Output('barchart', 'figure'),
    [Input('datatable_id', 'selected_rows'),
     Input('statsdropdown', 'value')]
    )
def update_data(chosen_rows,statsdropval):
    
    df_filtered = df.copy()
    
    if chosen_rows:
        df_filtered = df.iloc[chosen_rows,]

    bar_chart = px.bar(df_filtered,
                       x='Name',
                       y=statsdropval,
                       color='Name',
                       labels={'Player Name' : 'Chosen Stat'})
    
    return bar_chart
             
server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)