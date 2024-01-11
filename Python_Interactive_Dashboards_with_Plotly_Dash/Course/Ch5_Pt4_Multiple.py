from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

happiness = pd.read_csv('world_happiness.csv')

app=Dash()

app.layout=html.Div([
    html.H1('World Happiness Dashboard'),
    html.P(['This dashboard shows the happiness score.',
            html.Br(),
            html.A('World Happiness Report Data Source',
                   href='https://worldhappiness.report',
                   target='_blank')]),
    dcc.Dropdown(id='country-dropdown',
                 options=happiness['country'].unique(),
                 value='United States'),
    dcc.RadioItems(id='data-radio',
                   options={ #must be list or dictionary. keys below are columns in dataset
                       'happiness_score': 'Happiness Score',
                       'happiness_rank': 'Hapiness Rank'
                   },
                   value='happiness_score'), # initial value
    dcc.Graph(id='happiness_graph')])

#decorator
@app.callback(
    Output('happiness_graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('data-radio', 'value')
)

# order of inputs in the function must match order from the decorator
def update_graph(selected_country, selected_data):
    filtered_happiness=happiness[happiness['country']==selected_country]
    line_fig=px.line(filtered_happiness,
                     x='year', y=selected_data,
                     title=f'{selected_data} in {selected_country}')
    return line_fig


if __name__ == '__main__':
    app.run_server(debug=True)