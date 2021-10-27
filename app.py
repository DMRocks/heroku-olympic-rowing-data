import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import pandas as pd
import plotly.express as px


url = 'https://raw.githubusercontent.com/DMRocks/Olympic-Rowing-Data/main/Olympic%20Rowing%20Data'
data = pd.read_csv(url, index_col = 'Year')

external_stylesheets= ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server


#App Layout
app.layout = html.Div([
    #Title
    html.H1("Olympic Rowing Times (Final A)", style={'text-align':'center'}),
    html.H5("Data Pulled from: Olympic Database, World Rowing and the New York Times"),
    html.Div("As you explore this dataset note not only how times get faster, but competition gets tighter."),
        #Dropdown Menu
    html.Div([
        dcc.Dropdown(
        id='event', clearable=False,
        value= f"Men's Single Gold", options=[
            {'label': c, 'value': c}
            for c in data.columns
        ], multi = True),
    ], style={'display': 'inline', 'width': '15%'}),
    #Main Graph
    html.Div([
        dcc.Graph(id='graph')
    ]),
    #Text Callbacks
    html.H3("How much faster have we become?", style={
        'text-align':'center'}),
    html.Div("To look at how much faster we have become, let us compare the top times from the eight event in 1920-1936 and the 2012-2020 Olympics (We take mean due to try to minimize the effect of wind). Here, as we can see a difference of 42 seconds."),
        
    html.Div([
        dcc.Graph(id='old_new')
    ]),

    html.Div("Here, take a look at times year by year and event by event."),
    #Add slider Sam
    dcc.Slider(
        id='bar_slider',
        min=1920,
        max=2020,
        step=4,
        value=1976,
        tooltip={"placement": "bottom", "always_visible": True},
        marks={
            1920: {'label': '1920', 'style': {'color': '#FFA500'}},
            1940: {'label': '1940', 'style': {'color': '#f50'}},
            1972: {'label': '1972', 'style': {'color': '#FFA500'}},
            2024: {'label': '2024'}
    }),
    html.Div([
        dcc.Graph(id='bar_chart')
    ]),    
])

# Graph Event
@app.callback(
    Output('graph', 'figure'),
    Input("event", "value")
)

def graph_callback(event):

    fig1 = px.scatter(data, x = data.index, y = event)
    
    fig1.update_layout(
    yaxis_title='Final Time (Seconds)',
    xaxis_title= 'Olympic Year',
    xaxis = dict(
        tickmode = 'linear',
        range=[1916, 2024],
        tick0 = 0,
        dtick = 8
        )
    )


    return fig1

#Fastest Time
@app.callback(
    Output(component_id='old_new', component_property='figure'),
    Input(component_id='event', component_property='value')
)
def update_output_div(event):

    data_time_comp_old = data.iloc[0:4, 12]

    data_time_comp_new = data.iloc[20:22, 12]

    old_mean = data_time_comp_old.mean()

    new_mean = data_time_comp_new.mean()

    mean_data = {'mean': [old_mean, new_mean]}

    mean_data = pd.DataFrame(mean_data, index=['1920-1936','2012-2020'])

    mean_bar_fig = px.bar(mean_data)


    mean_bar_fig.update_layout(
    title_text='Mean of Olympic Eight Gold Times (1920-1936, 2012-2020)',
    yaxis_title='Final Time (Seconds)',
    xaxis_title= 'Mean of Olympic Years',
    showlegend=False,
    yaxis = dict(
        tickmode = 'linear',
        range=[310, 390],
        tick0 = 0,
        dtick = 25
        )
)

    return mean_bar_fig

#Bar Chart
@app.callback(
    Output(component_id='bar_chart', component_property='figure'),
    Input("bar_slider", "value")
)
def run_bar_chart(slider):

    data_selection = data.loc[slider]

    bar_fig = px.bar(data_selection, barmode = 'group')


    bar_fig.update_layout(
    yaxis_title='Final Time (Seconds)',
    xaxis_title= 'Olympic Year',
    showlegend=False,
    yaxis = dict(
        tickmode = 'linear',
        range=[310, 510],
        tick0 = 0,
        dtick = 25
        )
    )


    return bar_fig



# Run app
if __name__ == '__main__':
    app.run_server()
