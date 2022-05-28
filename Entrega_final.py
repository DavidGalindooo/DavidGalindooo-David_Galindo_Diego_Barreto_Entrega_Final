import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import altair as alt
import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


app = dash.Dash()

DATA = pd.read_excel('accid.xlsx')

available_CLASE_VEHICULO_ACCIDENTE = DATA['CLASE_VEHICULO_VICTIMA'].unique()
available_SEXO_VICTIMA = DATA["SEXO_VICTIMA"].unique()


# # # Visualizaciones estaticas

tab = DATA['CLASE_VEHICULO_VICTIMA'].value_counts().rename_axis('label').reset_index(name='counts')

# 1
fig2 = go.Figure(data=[go.Pie(labels=tab['label'], values=tab['counts'], hole=.3)])

# 2
g1 = px.density_heatmap(DATA, x="SEXO_VICTIMA", y="CLASE_VEHICULO_VICTIMA")

# 3?
fignn = sns.catplot(data = DATA,
            kind = "bar",
            estimator = sum,
            x = "CANTIDAD_VICTIMAS",
            y = "GRAVEDAD_ACCIDENTE",
            hue = "CLASE_VEHICULO_VICTIMA",
            col = "SEXO_VICTIMA",
            palette = 'magma',
            ci = None)



# # #   Cuerpo del Dashboard

app.layout = html.Div([
    html.H1(children="DASHBOARD"),

    ### Viz 1 ###
    html.H3(children="Donut Chart"),
    html.Div(dcc.Graph(
                id='vis1',
                figure = fig2,
                style={'height': 1000, 'width': 1600})
            ),

    ### Viz 2 ### mapa
    html.H3(children="Mapa"),
    dcc.Dropdown(
    	id='crossfilter_SEXO_VICTIMA',
        options=[{'label': i, 'value': i} for i in available_SEXO_VICTIMA],
        value = "M"
        ),
    html.Div(dcc.Graph(
                id='vis2',
                style={'height': 1000, 'width': 1600})
            ),
    
                        ],
                         style={'marginBottom': 50, 'marginTop': 25}
)




# # # Con filtros
@app.callback(
  dash.dependencies.Output('vis2', 'figure'),
  [dash.dependencies.Input('crossfilter_SEXO_VICTIMA', 'value')])
    
def update_graph(SEXO):
    cant_SEXO_VICTIMA = DATA[(DATA['SEXO_VICTIMA'] == SEXO)]
    g2 = px.scatter_geo(cant_SEXO_VICTIMA,
                            lat='y_geo',
                            lon='x_geo',
                            size="SEXO_VICTIMA",
                            center = {"lat": 10.9878, "lon": -74.7889})
    return g2


# # # Final
if __name__ == "__main__":
     app.run_server(debug=True)
