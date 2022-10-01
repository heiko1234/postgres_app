import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff


def budget_paretoplot(list_of_names, list_of_values, sum_value, yname=None, xname=None, title=None, plot=True):
    
    if xname is None:
        xname = list_of_names
    
    if yname is None:
        yname = "counts"

    Y_data = list_of_values
    X_data = list_of_names

    # x_list = [ "." + str(i) for i in X_data]
    x_list = [str(i) for i in X_data]
    x_list = np.asarray(x_list)

    y_per = [element_y / sum_value * 100 for element_y in Y_data]

    output = []
    for i in range(1, len(y_per)+1):
        output.append(sum(y_per[0:i]))
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            name="Barplot",
            x = x_list,
            y = Y_data
        ),
        secondary_y = False
    )
    fig.add_trace(
        go.Scatter(
            x = x_list,
            y = output, 
            mode = "lines+markers",
            name = "percentage line", 
            marker = dict(
                color="red"
            )
        ),
        secondary_y = True
    )
    if title is None:
        title = "Paretoplot"
    fig.update_layout(
        title_text = title,
        xaxis = dict(categoryorder = "array", categoryarray = x_list)
    )
    fig.update_yaxes(
        title_text="percentage",
        range=(0, 105),
        showgrid= True,
        gridwidth=1,
        gridcolor="white", 
        secondary_y=True
        )
    fig.update_yaxes(
        title_text=yname,
        showgrid=True,
        gridwidth=1,
        gridcolor="black",
        secondary_y=False
        )
    fig.update_xaxes(
        title_text=xname,
        )

    if plot:
        plotly.offline.plot(fig, filename="paretoplot.html")
    else:
        return fig





def sorted_gant(df, Task, team_member, start_date=None, end_date=None, date=None, plot = True):

    df = df.sort_values(by=Task)
    df = df.reset_index(drop = True)

    Task_id_list = list(df[Task])
    Task_id_list = np.array(Task_id_list)
    Task_id_list = list(np.where(Task_id_list[:-1] != Task_id_list[1:])[0])



    fig = ff.create_gantt(df, index_col=team_member, task_names = Task,  group_tasks=False, show_colorbar=True)
    fig.update_yaxes(autorange="reversed")

    for i in Task_id_list:
        fig.add_hline(y = i+0.5, line_width=4, line_color="white")

    if date != None:
        fig.add_vline(x=date, line_width=3, line_color="black")

    if (start_date != None) and (end_date != None):
        fig.update_xaxes(range=[start_date, end_date])

    if plot:
        plotly.offline.plot(fig)
    else:
        return fig





def single_gantt(df, team_member, color="Working_hours", Task="Task", Start="Start", Finish="Finish", date=None, plot = True):
    df = df[df["Team"]==team_member]
    df = df.reset_index(drop = True)

    fig = px.timeline(df, x_start=Start, x_end=Finish, y=Task, color=color)
    fig.update_yaxes(autorange="reversed")
    if date != None:
        fig.add_vline(x=date, line_width=3, line_color="black")
    if plot:
        plotly.offline.plot(fig)
    else:
        return fig







