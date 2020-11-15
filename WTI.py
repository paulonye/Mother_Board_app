import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ClientsideFunction
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
#import base64
#from plotly.subplots import make_subplots

from clean import WTI, BRENT

#Oil Price Tracker
#opt = pd.read_excel('oil price tracker.xlsx')
#rop = pd.read_csv('rop2.csv')
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


#available_indicators = opt.columns
filt = WTI['Month'].unique()
image_filename = '/Users/Hp/Documents/new_spe.png'
#encoded_image = base64.b64encode(open('/Users/Hp/Documents/new_spe.png', 'rb').read())

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

layout = dict(
    autosize=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)

app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(id="output-clientside"),
        html.Div(
            [

                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("new_spe.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    'Oil Price Data',
                                    style = {"margin-bottom":"0px"},
                                ),
                                html.H5(
                                    'Historical Data',
                                    style={"margin-top": "0px"},
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id  ="title"
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Contact Us", id="learn-more-button"),
                            href = "ibadanstudents@gmail.com",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),    
            ],
            id = "header",
            className = "row flex-display",
            style = {"margin-bottom":"25px"},
        ),
        html.Div(
            [

                html.Div(
                    [
                        html.P(
                            "Filter by construction date (or select range in histogram):",
                            className="control_label",
                        ),
                        dcc.Dropdown(
                            id="year_slider",
                            options=[{'label': i, 'value': i} for i in WTI['Year'].unique()],
                            value="2018",
                            className="dcc_control",
                        ),
                        html.P("Filter by well status:", className="control_label"),
                        dcc.RadioItems(
                            id="well_status_selector",
                            options=[
                                {"label": "WTI", "value": "WTI"},
                                {"label": "Brent", "value": "Brent"},
                            ],
                            value="WTI",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="well_statuses",
                            options=[{'label': i, 'value': i} for i in filt],
                            value="January",
                            className="dcc_control",
                        ),
                        dcc.Checklist(
                            id="lock_selector",
                            options=[{"label": "Lock camera", "value": "locked"}],
                            className="dcc_control",
                            value=[],
                        ),
                        html.P("Filter by well type:", className="control_label"),
                        dcc.RadioItems(
                            id="well_type_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Productive only ", "value": "productive"},
                                {"label": "Customize ", "value": "custom"},
                            ],
                            value="productive",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="well_types",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Productive only ", "value": "productive"},
                                {"label": "Customize ", "value": "custom"},
                            ],
                            multi=True,
                            value="productive",
                            className="dcc_control",
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="well_text"), html.P("Benchmark")],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="gasText"), html.P("Min")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="oilText"), html.P("Avg")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="waterText"), html.P("Max")],
                                    id="water",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="count_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),                
    ],
    id = "mainContainer",
    style = {"display": "flex", "flex-direction": "column"},
)

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("count_graph", "figure")],
)

@app.callback(
    Output('count_graph', 'figure'),
    [Input('year_slider', 'value'),
    Input('well_statuses', 'value'),
    Input('well_status_selector', 'value')])
def change_month(year, yaxis_column, type_1):
    if year == '2020' and yaxis_column == 'December':
        yaxis_column = 'November'

    if type_1 == 'Brent':
        rop = BRENT[BRENT['Year'] == year][BRENT['Month']==yaxis_column]
    else:
        rop = WTI[WTI['Year'] == year][WTI['Month']==yaxis_column]
    
    
    y_t1 = rop['Price'].min()
    

    y_t2 = rop['Price'].max()
    

    
     

    fig = go.Figure()
    fig.add_trace(go.Scatter(
                        x = rop['Month-Day'],
                        y = rop['Price'],
                        mode = 'lines+markers',
                        line = dict(
                            color = 'red' if rop['Price'].iloc[0] > rop['Price'].iloc[-1] else 'green'
                            ),
                        marker = dict(
                            color = 'red' if rop['Price'].iloc[0] > rop['Price'].iloc[-1] else 'green'
                            ),
                        stackgroup = 'one',
                        fillcolor = 'red' if rop['Price'].iloc[0] > rop['Price'].iloc[-1] else 'green'
                        ,
                        hoverinfo = 'x+y'
                        )
    )


    fig.update_layout(layout)


    fig.update_layout(
                    xaxis = dict(tickangle = 90,
                    showgrid = False),
                    yaxis = dict(range = (y_t1-0.8, y_t2+0.8),
                    showgrid = False, showticklabels = False),
                    showlegend = False,
                    title = yaxis_column+' '+year,
                    plot_bgcolor = 'rgb(248, 248, 255)',
                    paper_bgcolor = 'rgb(248, 248, 255)'
    )

    return fig

@app.callback(
    Output("aggregate_data", "data"),
    [
        Input("year_slider", "value"),
        Input("well_statuses", "value"),
        Input("well_status_selector", "value")
    ],
)
def  update_production_text(year, yaxis_column, type_1):
    if year == '2020' and yaxis_column == 'December':
        yaxis_column = 'November'

    if type_1 == 'Brent':
        rop = BRENT[BRENT['Year'] == year][BRENT['Month']==yaxis_column]
    else:
        rop = WTI[WTI['Year'] == year][WTI['Month']==yaxis_column]
    
    p1 = rop['Price'].min()
    p2 = rop['Price'].mean()
    p3 = rop['Price'].max()
    return p1, p2, p3


@app.callback(
    [	
        Output("gasText", "children"),
        Output("oilText", "children"),
        Output("waterText", "children"),
        
    ],
    [Input("aggregate_data", "data")],
)
def update_text(data):

    
    return '${:.1f}'.format(data[0]), '${:.1f}'.format(data[1]), '${:.1f}'.format(data[2])



if __name__ == '__main__':
    app.run_server(debug=True)
