import dash
import os
import plotly.express as px
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import json


def fetch_counties():
    with open(os.path.join(os.path.dirname(__file__), '../counties.json'), "r") as f:
        counties = json.load(f)

    return counties

def create_fig(df, counties):
    fig = px.choropleth(
        data_frame=df,
        geojson=counties,
        color="log(infected+1)",
        color_continuous_scale='oranges',
        hover_name='infected',
        hover_data=['Landkreis'],
        locations="Landkreis",
        featureidkey="properties.NAME_3",
        projection="mercator",
        animation_frame='date',
        range_color=[0, 7]
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        height=800,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    return fig


def load_data():
    global data
    _ = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data.csv'))
    return _


data = load_data()

counties = fetch_counties()

fig = create_fig(df=data, counties=counties)

external_stylesheets = [dbc.themes.BOOTSTRAP]

dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


dash_app.layout = html.Div([
        dbc.Container([
            html.H1(children='Visualization of reported Covid-19 cases in Germany by Districts'),
            dbc.Row([
                html.A(
                'Click here for the associated article',
                href='https://towardsdatascience.com/an-interactive-visualization-of-the-covid-19-development-in-germany-2b87e50a5b3e',
                target="_blank"
            )]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='infected-graph',
                        figure=fig
                    ),
                ], md=12)
            ]),
            html.A(
                'Data taken from the RKI page',
                href='https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Gesamt.html',
                target="_blank"
            )
    ], fluid=True)
])

app = dash_app.server


if __name__ == '__main__':
    app.run()