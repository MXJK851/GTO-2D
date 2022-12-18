import pandas 
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
def coord_file_parser(file_name_of_coord):
    """
    :param file_name_of_coord coord file 
    :type file_name_of_coord opened output file
    :return: np array
    """        

    # this matrix includes series number: the first C
    result = pd.read_csv(file_name_of_coord, sep='\s+', header=None)
    coord = np.array(result)
    return coord

def moment_file_parser(mom_out_file):
    """
    :param mom_out_file moment file
    :type mom_out_file opened output file
    :return: np.array
    """        
    
    mom_output = pd.read_csv(mom_out_file, sep='\s+', header=None, skiprows=7)
    mom_x = mom_output[4]
    mom_y = mom_output[5]
    mom_z = mom_output[6]
    mom_states_x = np.array(mom_x)
    mom_states_y = np.array(mom_y)
    mom_states_z = np.array(mom_z)
    return mom_states_x, mom_states_y, mom_states_z

    
app = Dash(__name__)
coord = coord_file_parser('coord.60.out')
mom_states_x, mom_states_y, mom_states_z = moment_file_parser('3.out')
app.layout = html.Div([
    html.Div(
        "Colourbar",
    ),
    html.Div(dcc.Dropdown(['Blackbody','Bluered','Blues','Cividis','Earth','Greens','Greys','Hot','Jet','Picnic','Portland','Rainbow','RdBu','Reds','Viridis','YlGnBu','YlOrRd'], 'Electric', id='colourbar'),),
    dcc.Graph(id='spin-size'),
    html.Div(
            "Relative Spin Radius",
        ),
    dcc.Slider(
        max=0.2,
        min=0.005,
        value=0.03,   
        id='spinsize-slider',
        marks=None,
        tooltip={"placement": "bottom", "always_visible": True},
    )
])


@app.callback(
    Output('spin-size', 'figure'),
    Input('colourbar', 'value'),
    Input('spinsize-slider', 'value'))
    
def update_figure(cbar,radius):

    df = pd.DataFrame({'x':coord[:,1],'y':coord[:,2],'z':coord[:,3],'u':mom_states_x,'v':mom_states_y,'w':mom_states_z,})

    fig = go.Figure(data = go.Cone(
        x=df['x'],
        y=df['y'],
        z=df['z'],
        u=df['u'],
        v=df['v'],
        w=df['w'],
        colorscale=cbar,
        sizemode="absolute",
        sizeref=40,
        cmin=-1, cmid= 0, cmax=1))

    fig.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=radius),
                                camera_eye=dict(x=0, y=0, z=1)))
    
    fig.update_layout(
    title_text='Monolayer spin configuration',
    height=750,
    width=750
    )

    fig.update_layout(
    margin=dict(l=50, r=50, t=50, b=50),
    )
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)