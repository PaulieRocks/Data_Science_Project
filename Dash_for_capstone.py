import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update


app = dash.Dash(__name__)
spacex_data=pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')
print(spacex_data['Launch Site'].value_counts())

app.layout = html.Div(children=[
                        html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center','color':'#503D36','font-size':24}),
                        html.Div([
                            html.H1('Launch Site Selection', style={'textAlign': 'left', 'color': '#503D36', 'font-size': 18})]),
                        dcc.Dropdown
                                (id='site-dropdown',
                                  options=[{'label': 'All Sites', 'value': 'ALL'},
                                           {'label':'site 1', 'value':'CCAFS LC-40'},
                                           {'label':'site 2','value':'KSC LC-39A'},
                                           {'label':'site 3','value':'VAFB SLC-4E'},
                                           {'label':'site 4','value':'CCAFS SLC-40'}],
                                  value='ALL',
                                  placeholder='Select a Launch Site Here',
                                  searchable=True
                                  ),
                        html.Div([], id='success-pie-chart'),
                        dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000,marks={0: '0',1000: '1000',2000:'2000',3000:'3000',4000:'4000',5000:'5000',6000:'6000',7000:'7000',8000:'8000',9000:'9000',10000:'10000'},value=[0, 10000]),
                        html.Div([], id='success-payload-scatter-chart')
                     ]
                    )

@app.callback([Output(component_id="success-pie-chart",component_property="children")],
              [Output(component_id="success-payload-scatter-chart",component_property="children")],
              [Input(component_id='site-dropdown', component_property='value')],
              [Input(component_id='payload-slider', component_property='value')])
def get_pie_chart(site,payload):

    min = payload[0]
    max = payload[1]

    if site == 'ALL':

        df = spacex_data[(spacex_data['Payload Mass (kg)'] >= min) & (spacex_data['Payload Mass (kg)'] <= max)]
        pie_fig = px.pie(df, values='class', names='Launch Site')
        scatter_fig=px.scatter(df,x='Payload Mass (kg)',y='class', color="Booster Version")

    else:

        df = spacex_data[(spacex_data['Payload Mass (kg)'] >= min) & (spacex_data['Payload Mass (kg)'] <= max) & (spacex_data['Launch Site'] == site)]
        pie_fig = px.pie(df, values='class', names='Mission Outcome')
        scatter_fig=px.scatter(df,x='Payload Mass (kg)',y='class',color="Booster Version")

    return [dcc.Graph(figure=pie_fig), dcc.Graph(figure=scatter_fig)]


if __name__ == '__main__':
    app.run_server()

