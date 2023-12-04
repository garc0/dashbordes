from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import numpy as np
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('text.csv')

app = Dash(__name__)

def tttt(a):
    return pd.to_datetime(a, format="%Y-%m-%d")

gg = df['Категория'].unique()
#df['Дата'] = tttt(df['Дата']).astype(int)/ 10**9


TEST = "FFFF"
app.layout = html.Div([

    html.H4('Круговой и "временной график" по категории'),
    html.Div([
        html.P("Категория:"),
        dcc.Dropdown(id='names',
            options=df["Категория"].unique(),
            value='Электроника', clearable=False
        ),
    ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),

    html.Div([ dcc.Graph(id="piegraph"),], 
        style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
       
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            0,
            len(gg)-1,
            step=None,
            value=0,
            marks={str(i):  (str(gg[i])) for i in range(0, len(gg))},
            id='year-slider'
    )], style={'display': 'inline-lobck', 'width': '90%'}),
    html.Div([
        html.H4('График рассеивания'),
         html.Div([
            html.P('Товар:'),
            dcc.Dropdown(id='crossfilter-yaxis-column',
                options=df["Товар"].unique(),
                value='Ноутбук', clearable=False
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='crossfilter-xaxis-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
        
        html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter'
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    ])

])


@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.Категория == df['Категория'][int(selected_year)]]

    fig = px.scatter(filtered_df, x="Сумма", y="Товар", color ="Товар", size="Количество", hover_name="Товар",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output("piegraph", "figure"), 
    Input("names", "value"))
def generate_chart(names):
    jjj = df[df.Категория == names]
    fig = px.pie(jjj, values='Количество', names='Товар', hole=.3)
    return fig



@callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('names', 'value'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type):
    dff = df[df['Категория'] == xaxis_column_name]
    if(len(dff[dff['Товар'] == yaxis_column_name]) == 0):
        TEST = "AAAA"
        return
    fig = px.scatter(
            x=dff[dff['Товар'] == yaxis_column_name]['Сумма'],
            y=dff[dff['Товар'] == yaxis_column_name]['Количество'],
            hover_name=dff[dff['Товар'] == yaxis_column_name]['Товар']
            )

    fig.update_traces(customdata=dff[dff['Товар'] == yaxis_column_name]['Количество'])

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig

if __name__ == '__main__':
    app.run(debug=True)