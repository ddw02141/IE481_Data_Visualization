import random

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import flask
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
import os
from math import *
import pandas as pd
import plotly.express as px
# import dash_dangerously_set_inner_html

INTERVAL = 3000
prev_graph = None
prev_html = None
prev_time = None
prev_dayofweek = 0
prev_hour = 0


app = Flask(__name__, template_folder = './')
app.secret_key = "ie481-programming code"

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app_dash = dash.Dash(__name__, server=app, external_stylesheets=external_stylesheets, url_base_pathname='/activity/')

# @app.route('/activity/map')
# def map():
#     return render_template('Map_Viz.html')

@app.route('/')
def activity():
    return flask.redirect('/activity')
df = pd.read_csv("grouped_dataset.csv")

remove_columns = ['day_of_week', 'time_sort', 'new_time_group', 'Unnamed: 0', 'Unnamed: 0.1','longitude', 'latitude']
acts = [col for col in list(df.columns) if col not in remove_columns]
print(acts)
# ['On_the_Move', 'Sleep', 'Study', 'Hard_Exercise', 'Facebook', 'Kakaotalk', 'Instagram', 'Video', 'Not Classified', 'Web_surfing']
x = [cos(radians((x-1)*360/len(acts)+90)) for x in range(len(acts))]
y = [sin(radians((x-1)*360/len(acts)+90)) for x in range(len(acts))]
# rgbs = [(random.randint(0,255), random.randint(0,255), random.randint(0,255)) for _ in range(len(acts))]
rgbs = [(0,0,153), (0,51,25), (102,204,0), (255,102,255), (153,204,255), (255,255,0),(204,0,204),(255,0,0),(128,128,128),(250,250,250)]
colors = [f'rgb({a}, {b}, {c})' for a,b,c in rgbs] 
color_discrete_map = dict()
for i, act in enumerate(acts):
    color_discrete_map[act] = colors[i]
# marker_size = [random.randint(0,200) for _ in range(5)]
day_of_week = {0:"Mon", 1:"Tue", 2:"Wed", 3:"Thr", 4:"Fri", 5:"Sat", 6:"Sun"}


idx = 0


# ts = pd.to_datetime(1557273676330, unit='ms')
now = df.loc[idx, "new_time_group"] + ", " + day_of_week[df.loc[idx, "day_of_week"]]


marker_size = [df.loc[idx, act] for act in acts]
acts_with_number = []
for i in range(len(marker_size)):
	acts_with_number.append(acts[i] + "\n" + str(int(marker_size[i])))

marker_size = [ms*4 + 10 for ms in marker_size]
options = []
for i,t in enumerate(df.loc[0:23, "new_time_group"]):
    newt = t[:5] + t[-3:]
    d = {'label':newt, 'value':i}
    options.append(d)

app_dash.layout = html.Div(className="wrapper",
    children=[

        html.H1(className="title",
                children= ['The   ',           
                html.Img(className="img", src=app_dash.get_asset_url("daily_life.jpg")),
                ' of KAIST people',
                ]
        ),

        
        
        html.Div(className = "dropdown_wrapper", 
            children=[
            
            html.Div(className="time", 
                children=[
                    dcc.Interval(id='time_timer', interval=INTERVAL),
                    html.H2(id="time", children='')
                ],
            ),


            html.Div(className="left", 
            children = [
                dcc.Dropdown(
                    id='hour_dropdown',
                    className='dropdown',
                    options = options,
                    value=0,
                ),
            ]),

            html.Div(className='right',
            children = [
                
                dcc.Dropdown(
                    id='dayofweek_dropdown',
                    className='dropdown2',
                    options = [
                        {'label':'Mon', 'value': 0},
                        {'label':'Tue', 'value': 1},
                        {'label':'Wed', 'value': 2},
                        {'label':'Thr', 'value': 3},
                        {'label':'Fri', 'value': 4},
                        {'label':'Sat', 'value': 5},
                        {'label':'Sun', 'value': 6},
                    ],
                    value=0,
                ),
                ]
            ),

            html.Div(
                children=[
                    html.Button(className="gobut", children=['Go'], id='go'),
                ]
            ),

            html.Div(
                children=[
                    html.Button(className="but", children=['Start Simulation'], id='start_timer'),
                ],
            ),
            html.Div(className="hidden", children='', id="hidden-div", ),
            html.Div(className="hidden", children='', id="hidden-div2", ),
            html.Div(className="hidden", children='', id="hidden-div3", ),

            ]
        ),

        

        
        
    
    	html.Div(
        className="box",
        children=[
            dcc.Interval(id='timer', interval=INTERVAL),
            dcc.Graph(
                id='example-graph',
                figure={'data' : [
                 go.Pie(
                    values = marker_size,
                    labels = acts,
                    textinfo='label+percent',
                    insidetextorientation='radial',
                    textfont=dict(size=30),
                    marker=dict(colors=colors),
                    # color_discrete_map=color_discrete_map,
                ),
            ],
            
            'layout' : go.Layout(
                showlegend = True,
                title = "Activity",
                titlefont=dict(
                    family="Courier New, monospace",
                    size=40,
                    color="#7f7f7f"
                ),
                width = inf,
                height = 1000,
                legend=dict(
                    font=dict(
                        size=20
                    )
                ),

            )
        }
                
            ),
        ]),




        html.Div(
            # style={'border': 'none', 'width': '50%', 'height': 600,'white-space': 'pre-wrap'},
            # style={'position':'relative', 'border': 'none', 'width': '50%', 'height': '100%','white-space': 'pre-wrap'},
            className="box2",
            children=[
                # html.H1(children='Map', id='second', style={'text-align':'center'}),
                dcc.Interval(id='html_timer', interval=INTERVAL),
                # html.Embed(id="htmlFile", src=app_dash.get_asset_url("map.html"), style={'text-align':'center', 'width':'100%', 'height': 1000})
                html.Iframe(id="htmlFile", src=app_dash.get_asset_url("map.html"), style={'text-align':'center', 'width':'100%', 'height': 1000})

            ]

        ),
    # html.A(html.Button('Location Cluster', className='three columns'),
    # href='map'),
	
	# ])
	# ])

    ]
)

# htmls = os.listdir('map_viz')
html_idx = 0
Timer_on = False
idx_changed = [False, False, False]

@app_dash.callback(output=Output('time', 'children'),
              inputs=[Input('time_timer', 'n_intervals')])
# @app_dash.callback(output=[Output('hour_dropdown', 'value'),
#                         Output('dayofweek_dropdown', 'value')],
#               inputs=[Input('time_timer', 'n_intervals')])
def update_time(n_clicks):
    print("update_time")
    global idx
    global prev_time
    global prev_dayofweek
    if Timer_on:
        idx += 1
        idx %= 168

    now = df.loc[idx, "new_time_group"] + ", " + day_of_week[df.loc[idx, "day_of_week"]]
    if prev_time==None or Timer_on or idx_changed[0]:
        prev_time = now
        idx_changed[0] = False
    #     prev_time = df.loc[idx, "new_time_group"][:5] + df.loc[idx, "new_time_group"][-3:]
    #     prev_dayofweek = day_of_week[df.loc[idx, "day_of_week"]]
    # print(prev_time, " ", prev_dayofweek)
    return prev_time

@app_dash.callback(output=Output('htmlFile', 'src'),
              inputs=[Input('html_timer', 'n_intervals')])
def update_html(n_clicks):
    print("update_html")
    global prev_html

    if prev_html==None or Timer_on or idx_changed[1]:
        idx_changed[1] = False
        prev_html = f"map_viz/map{idx}.html"
        

    
    return app_dash.get_asset_url(prev_html)

@app_dash.callback(output=Output('example-graph', 'figure'),
              inputs=[Input('timer', 'n_intervals')])
def update_graph(n_clicks):
    print("update_graph")
    
    global idx
    global x
    global y
    global now
    global prev_graph
    global color

    # x = [cos(radians((x-1)*360/len(acts)+18)) for x in range(len(acts))]
    # y = [sin(radians((x-1)*360/len(acts)+90)) for x in range(len(acts))]
    # print("*******************************")
    # print(f"idx : {idx}")
    # print("*******************************")
    marker_size = [df.loc[idx, act] for act in acts]
    acts_with_number = []
    for i in range(len(marker_size)):
        acts_with_number.append(acts[i] + "\n" + str(int(marker_size[i])))
    # marker_size = [ms*4 + 10 for ms in marker_size]
    if prev_graph==None or Timer_on or idx_changed[2]:
        idx_changed[2] = False
        prev_graph = {'data' : [
                 go.Pie(
                    values = marker_size,
                    labels = acts,
                    textinfo='label+percent',
                    insidetextorientation='radial',
                    textfont=dict(size=30),
                    marker=dict(colors=colors),
                    # color_discrete_map=color_discrete_map,
                ),
            ],
            
            'layout' : go.Layout(
                showlegend = True,
                title = "Activity",
                titlefont=dict(
                    family="Courier New, monospace",
                    size=40,
                    color="#7f7f7f"
                ),
                width = inf,
                height = 1000,
                legend=dict(
                    font=dict(
                        size=20
                    )
                ),

            )
        }
    return prev_graph
@app_dash.callback(output=Output('start_timer', 'children'),
              inputs=[Input('start_timer', 'n_clicks')],
              state=[State('start_timer', 'children')])
def click_button(n_clicks, input_value):
    print("button clicked!")
    print(input_value)
    global Timer_on
    if input_value=="Start Simulation":
        Timer_on = True
        return " Stop Simulation"
    else:
        Timer_on = False
        return "Start Simulation"
@app_dash.callback(output=Output('hidden-div', 'children'),
              inputs=[Input('hour_dropdown', 'value')])

def hour_dropdown(value):
    print("hour_dropdown!")
    global prev_hour
    prev_hour = value
    return ""

@app_dash.callback(output=Output('hidden-div2', 'children'),
              inputs=[Input('dayofweek_dropdown', 'value')])
def dayofweek_dropdown(value):
    print("dayofweek_dropdown!")
    global prev_dayofweek
    prev_dayofweek = value
    return ""

@app_dash.callback(output=Output('hidden-div3', 'children'),
              inputs=[Input('go', 'n_clicks')])
def click_go_button(n_clicks):
    print("Go clicked!")
# def click_go_button(n_clicks):

# def click_go_button(*args):
    global idx
    global idx_changed
    now = df.loc[idx, "new_time_group"] + ", " + day_of_week[df.loc[idx, "day_of_week"]]

    # print(hour, ", ", dayofweek)
    
    idx = prev_dayofweek * 24 + prev_hour
    idx_changed = [True, True, True]
    print(f"idx_changed : {idx_changed}")
    return ''

if __name__ == '__main__':
    app.run(debug=True)