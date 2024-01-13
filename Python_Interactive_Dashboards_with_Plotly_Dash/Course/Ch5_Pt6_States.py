from dash import Dash, html, dcc, Input, Output, State
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
    dcc.RadioItems(id='region-radio',
                   options=happiness['region'].unique(),
                   value='North America'),
    dcc.Dropdown(id='country-dropdown'), #options and value are not needed as they will now be chained),
    dcc.RadioItems(id='data-radio',
                   options={ #must be list or dictionary. keys below are columns in dataset
                       'happiness_score': 'Happiness Score',
                       'happiness_rank': 'Happiness Rank'
                   },
                   value='happiness_score'), # initial value
    html.Br(), # line break for cleaner appearance
    html.Button(id='submit-button',
                n_clicks=0, # integer that shows number of times component has been clicked
                children='Update the output'),
    dcc.Graph(id='happiness_graph'),
    html.Div(id='average-div')])

#decorator

#output country dropdown based on selected region
@app.callback(
    Output('country-dropdown', 'options'),
    Output('country-dropdown', 'value'),
    Input('region-radio', 'value')
)

def update_dropdown(selected_region):
    filtered_happiness = happiness[happiness['region'] == selected_region]
    country_options=filtered_happiness['country'].unique()
    return country_options, country_options[0] # prev had been pre-selecting 'United States' which no longer makes sense b/c of regional radio filter

@app.callback(
    Output('happiness_graph', 'figure'),
    Output('average-div', 'children'),
    Input('submit-button', 'n_clicks'),
    # change below two inputs to state
    # callback order must be all outputs then all inputs then all states
    State('country-dropdown', 'value'),
    State('data-radio', 'value')
)

# with the bottom two inputs being changed to state, only the submit button will trigger the refresh

# order of inputs in the function must match order from the decorator
def update_graph(button_click, selected_country, selected_data):
    filtered_happiness=happiness[happiness['country']==selected_country]
    line_fig=px.line(filtered_happiness,
                     x='year', y=selected_data,
                     title=f'{selected_data} in {selected_country}')
    selected_average=filtered_happiness[selected_data].mean()
    return line_fig, f'The average {selected_data} for {selected_country} is {selected_average}'


if __name__ == '__main__':
    app.run_server(debug=True)