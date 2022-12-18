import plotly.graph_objects as go
from plotly.colors import n_colors
import numpy as np

def plot_ridegline(fitness_data,path):
    data_len = len(fitness_data)
    if data_len < 10:
        data = (fitness_data)
        colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', data_len, colortype='rgb')
        fig = go.Figure()
        for data_line, color in zip(data, colors):
            fig.add_trace(go.Violin(x=data_line, line_color=color))
        fig.update_traces(orientation='h', side='positive', width=3, points=False)
        fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)
        fig.write_image(path)
    else:
        date_temp = []
        for i in np.linspace(1,data_len-1,10).astype(int):
            date_temp.append(fitness_data[i])
        data = (date_temp)
        colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', 10, colortype='rgb')
        fig = go.Figure()
        for data_line, color in zip(data, colors):
            fig.add_trace(go.Violin(x=data_line, line_color=color))
        fig.update_traces(orientation='h', side='positive', width=3, points=False)
        fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)
        fig.write_image(path)

