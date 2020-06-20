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
# import dash_dangerously_set_inner_html

INTERVAL = 1000
prev_graph = None
prev_html = None
prev_time = None

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
acts = ["Not Classified", "SNS", "Video", "Exercise", "Sleep"]
x = [cos(radians((x-1)*360/len(acts)+90)) for x in range(len(acts))]
y = [sin(radians((x-1)*360/len(acts)+90)) for x in range(len(acts))]

day_of_week = {0:"Mon", 1:"Tue", 2:"Wed", 3:"Thr", 4:"Fri", 5:"Sat", 6:"Sun"}

df = pd.read_csv("grouped_dataset.csv")
idx = 0


# ts = pd.to_datetime(1557273676330, unit='ms')
now = df.loc[idx, "new_time_group"] + ", " + day_of_week[df.loc[idx, "day_of_week"]]

# marker_size = [random.randint(0,200) for _ in range(5)]

marker_size = [df.loc[idx, act] for act in acts]
acts_with_number = []
for i in range(len(marker_size)):
	acts_with_number.append(acts[i] + "\n" + str(int(marker_size[i])))

marker_size = [ms*4 + 10 for ms in marker_size]



app_dash.layout = html.Div(className="wrapper",
    children=[
        html.H1(children=[
                'Daily life of KAIST people'
            ],
            style={'text-align':'center'}
        ),

        html.Div(id="time", 
            children=[
                dcc.Interval(id='time_timer', interval=INTERVAL),
                html.H2(id='main_time', children=''),
            ],
            style={'text-align':'center'}
        ),

        html.Div(
            children=[
                html.Button(className="but", children=['Start Simulation'], id='start_timer'),
            ],
        ),
        
    
	html.Div(
    className="box",
    children=[
        dcc.Interval(id='timer', interval=INTERVAL),
        dcc.Graph(
            id='example-graph',
            figure={'data' : [
                 go.Scatter(
                    x = x,
                    y = y,
                    mode = 'markers+text',
                    marker = dict(
                    	color=['rgb(93, 164, 214)', 'rgb(255, 144, 14)', 'rgb(44, 160, 101)', 
                    			'rgb(255, 65, 54)', 'rgb(64, 255, 255)', 'rgb(0, 255, 0)']
           					),
                    marker_size = marker_size,
                 	text = acts_with_number,
                 	textfont=dict(
				        # family="sans serif",
				        size=30,
				        # color="crimson"
			    	)

            	),
            ],
            
            'layout' : go.Layout(
            	showlegend = False,
                title = "Activity Cluser",
                titlefont=dict(
			        family="Courier New, monospace",
			        size=40,
			        color="#7f7f7f"
			    ),
                width = inf,
                height = 1000,
                xaxis = dict(
                	range = [-2, 2],
                	showgrid = False,
                	visible = False,
                	zeroline = False
                ),
                yaxis = dict(
                	range = [-2, 2],
                	showgrid = False,
                	visible = False,
                	zeroline = False
                )
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

])

htmls = ["map.html", "easy_html.html"]
html_idx = 0
Timer_on = False


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



@app_dash.callback(output=Output('htmlFile', 'src'),
              inputs=[Input('html_timer', 'n_intervals')])
def update_graph(n_clicks):
    # print("html_timer")
    global html_idx
    global prev_html
    html_idx += 1
    html_idx %= 2
    print(htmls[html_idx])
    if prev_html==None or Timer_on:
        prev_html = htmls[html_idx]
    return app_dash.get_asset_url(prev_html)

@app_dash.callback(output=Output('main_time', 'children'),
              inputs=[Input('time_timer', 'n_intervals')])
def update_graph(n_clicks):
    # print("time_timer")
    global idx
    global prev_time
    if Timer_on:
        idx += 1
        idx %= 168
    now = df.loc[idx, "new_time_group"] + ", " + day_of_week[df.loc[idx, "day_of_week"]]
    if prev_time==None or Timer_on:
        prev_time = now
    return prev_time

@app_dash.callback(output=Output('example-graph', 'figure'),
              inputs=[Input('timer', 'n_intervals')])
def update_graph(n_clicks):
    # print("graph_timer")
    global idx
    global x
    global y
    global now
    global prev_graph

    # x = [cos(radians((x-1)*360/len(acts)+18)) for x in range(len(acts))]
    # y = [sin(radians((x-1)*360/len(acts)+90)) for x in range(len(acts))]
    marker_size = [df.loc[idx, act] for act in acts]
    acts_with_number = []
    for i in range(len(marker_size)):
        acts_with_number.append(acts[i] + "\n" + str(int(marker_size[i])))
    marker_size = [ms*4 + 10 for ms in marker_size]
    if prev_graph==None or Timer_on:
        prev_graph = {'data' : [
                     go.Scatter(
                        x = x,
                        y = y,
                        mode = 'markers+text',
                        marker = dict(
                        	color=['rgb(93, 164, 214)', 'rgb(255, 144, 14)', 'rgb(44, 160, 101)', 
                        			'rgb(255, 65, 54)', 'rgb(64, 255, 255)', 'rgb(0, 255, 0)']
               					),
                        marker_size = marker_size,
                     	text = acts_with_number,
                     	textfont=dict(
    				        # family="sans serif",
    				        size=30,
    				        # color=font_color,
    			    	)

                	),
                ],
                
                'layout' : go.Layout(
                	showlegend = False,
                    title = "Activity Cluster",
                    titlefont=dict(
    			        family="Courier New, monospace",
    			        size=40,
    			        color="#7f7f7f"
    			    ),
                    width = inf,
                    height = 1000,
                    xaxis = dict(
                    	range = [-2, 2],
                    	showgrid = False,
                    	visible = False,
                    	zeroline = False
                    ),
                    yaxis = dict(
                    	range = [-2, 2],
                    	showgrid = False,
                    	visible = False,
                    	zeroline = False
                    ),
                    # plot_bgcolor=plot_bgcolor,
                )
            }
    return prev_graph
if __name__ == '__main__':
    app.run(debug=True)