


import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff



# df = data
df

Task="project_id"
Task="Task"
team_member="project_id"
team_member="Task"
#  sorted_gant(df=data, Task="project_id", team_member="Task", start_date="Start", end_date="Finish", date=None, plot = True)
# _plotly_utils.exceptions.PlotlyError: Error. The number of colors in 'colors' must be no less than the 
# number of unique index values in your group column.
# 10

def sorted_gant(df, Task, team_member, start_date=None, end_date=None, date=None, plot = True):

    df = df.sort_values(by=Task)
    df = df.reset_index(drop = True)
    df
    df.shape

    df = df.iloc[:10,:]
    df

    Task_id_list = list(df[Task])
    Task_id_list = np.array(Task_id_list)
    Task_id_list = list(np.where(Task_id_list[:-1] != Task_id_list[1:])[0])
    Task_id_list

    # colormap = {s:c for s,c in zip(df["Task"].unique(), px.colors.named_colorscales())}
    # colormap
    # colors=[colormap[i] for i in df["Task"]]
    # colors



    fig = ff.create_gantt(df, index_col=team_member, task_names = Task, colors=colormap, group_tasks=False, show_colorbar=True)
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
    df = df[df["fullname"]==team_member]
    df = df.reset_index(drop = True)

    fig = px.timeline(df, x_start=Start, x_end=Finish, y=Task, color=color)
    fig.update_yaxes(autorange="reversed")
    if date != None:
        fig.add_vline(x=date, line_width=3, line_color="black")
    if plot:
        plotly.offline.plot(fig)
    else:
        return fig




import pandas as pd
import psycopg2


def execute_sql(sql):
    #establishing the connection
    conn = psycopg2.connect(
        database="teams", user='postgres', password='postgres', host='127.30.0.1', port= '5432'
    )
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()


    cursor.execute(sql)

    try:
        result = cursor.fetchall()

    except BaseException:
        result = cursor.rowcount
        if result == -1:
            result = "Done"

    # end everyting
    cursor.close()
    conn.close()

    return result





year = "2022"

name = "Tobias Kulinna"

low_year = f"{str(int(year))}"+"-01-01"
upper_year = f"{str(int(year)+1)}"+"-01-01"

# Ohne Name
sql = f"""
        SELECT p.project_id, tm.full_name, p.start_date, p.end_date, p.topic, tc.topic_class
        FROM project p
        INNER JOIN founding_sources fs
        ON p.funding_id = fs.founding_source_id
        INNER JOIN topic_class tc
        ON p.topic_class_id = tc.topic_class_id
        INNER JOIN project_team_members ptm
        ON p.project_id = ptm.project_id
        INNER JOIN team_members tm
        ON tm.team_id = ptm.team_id
        WHERE
        p.end_date > '{low_year}'
        AND
        p.start_date < '{upper_year}'
"""


# mit Name
sql = f"""
        SELECT p.project_id, tm.full_name, p.start_date, p.end_date, p.topic, tc.topic_class
        FROM project p
        INNER JOIN founding_sources fs
        ON p.funding_id = fs.founding_source_id
        INNER JOIN topic_class tc
        ON p.topic_class_id = tc.topic_class_id
        INNER JOIN project_team_members ptm
        ON p.project_id = ptm.project_id
        INNER JOIN team_members tm
        ON tm.team_id = ptm.team_id
        WHERE
        p.end_date > '{low_year}'
        AND
        p.start_date < '{upper_year}'
        AND
        tm.full_name = '{name}'
"""




data = execute_sql(sql=sql)


data = pd.DataFrame(data=data, columns = ["project_id", "fullname", "Start", "Finish", "Task", "Topic"])
data

data=data.sort_values(by="Start", ascending=False)
data = data.reset_index(drop = True)
data

df = data

name

single_gantt(df=data, team_member=name, color="Task", Task="Task", Start="Start", Finish="Finish", date=None, plot = True)


sorted_gant(df=data, Task="Task", team_member="project_id", start_date="Start", end_date="Finish", date=None, plot = True)


# mit Name
sorted_gant(df=data, Task="project_id", team_member="Task", start_date="Start", end_date="Finish", date=None, plot = True)  # das hier



# ohne Name
import datetime
date = datetime.datetime.today().strftime('%Y-%m-%d')
date

sorted_gant(df=data, Task="Task", team_member="fullname", start_date="Start", end_date="Finish", date=date, plot = True)





df = pd.DataFrame([
    dict(Task="Task 1", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
    dict(Task="Task 2", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
    dict(Task="Task 3", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
    dict(Task="Task 4", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
    dict(Task="Task 5", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
    dict(Task="Task 6", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
    dict(Task="Task 7", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
    dict(Task="Task 8", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
    dict(Task="Task 9", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
    dict(Task="Task 10", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
    dict(Task="Task 11", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
])

df["Task"].unique()

px.colors.qualitative.Plotly
px.colors.sequential.swatches_continuous()

s,c in zip(df["Task"].unique())


# px.colors.qualitative.

colormap = {s:c for s,c in zip(df["Task"].unique(), px.colors.qualitative.Plotly)}
colormap = {s:c for s,c in zip(df["Task"].unique(), px.colors.named_colorscales())}

colormap = {s:c for s,c in zip(df["project_id"].unique(), px.colors.sequential.Plasma)}
colormap

n_colors = len(df["project_id"].unique())
n_colors
colors = px.colors.sample_colorscale("turbo", [n/(n_colors -1) for n in range(n_colors)])
colors

px.colors.qualitative.Prism
px.colors.sequential.Jet
colormap = {s:c for s,c in zip(df["project_id"].unique(), px.colors.sequential.Plasma)}
colormap = {s:c for s,c in zip(df["project_id"].unique(), px.colors.qualitative.Prism)}

colormap = {s:c for s,c in zip(df["project_id"].unique(), colors)}
colormap

colors=[colormap[i] for i in df["project_id"]]
colors=[colormap[i] for i in df["Task"]]

colors
df


Task="Task"
team_member="fullname"
start_date="Start"
end_date="Finish"

px.colors.sample_colorscale()

# def sorted_gant(df, Task, team_member, start_date=None, end_date=None, date=None, plot = True):

#     df = df.sort_values(by=Task)
#     df = df.reset_index(drop = True)
#     df
#     df.shape

#     Task_id_list = list(df[Task])
#     Task_id_list = np.array(Task_id_list)
#     Task_id_list = list(np.where(Task_id_list[:-1] != Task_id_list[1:])[0])
#     Task_id_list

#     n_colors = len(df[Task].unique())
#     n_colors
#     colors = px.colors.sample_colorscale("turbo", [n/(n_colors -1) for n in range(n_colors)])
#     colors = px.colors.sample_colorscale("bluered", [n/(n_colors -1) for n in range(n_colors)])
    
#     colors

#     colormap = {s:c for s,c in zip(df[Task].unique(), colors)}

#     colors=[colormap[i] for i in df[Task]]
#     colors

#     fig = ff.create_gantt(df, index_col=Task, task_names = Task, colors=colors, group_tasks=False, show_colorbar=True)
#     fig.update_yaxes(autorange="reversed")

#     for i in Task_id_list:
#         fig.add_hline(y = i+0.5, line_width=4, line_color="white")

#     if date != None:
#         fig.add_vline(x=date, line_width=3, line_color="black")

#     if (start_date != None) and (end_date != None):
#         fig.update_xaxes(range=[start_date, end_date])

#     if plot:
#         plotly.offline.plot(fig)
#     else:
#         return fig

# sorted_gant(df=data, Task="Task", team_member="project_id", start_date="Start", end_date="Finish", date=None, plot = True)





def sorted_gant(df, Task, team_member, start_date=None, end_date=None, date=None, colorscale="turbo", plot = True):

    df = df.sort_values(by=Task)
    df = df.reset_index(drop = True)

    Task_id_list = list(df[Task])
    Task_id_list = np.array(Task_id_list)
    Task_id_list = list(np.where(Task_id_list[:-1] != Task_id_list[1:])[0])
    Task_id_list

    n_colors = len(df[team_member].unique())
    colors = px.colors.sample_colorscale(colorscale, [n/(n_colors -1) for n in range(n_colors)])

    colormap = {s:c for s,c in zip(df[team_member].unique(), colors)}

    fig = ff.create_gantt(df, index_col=team_member, task_names = Task, colors=colormap, group_tasks=False, show_colorbar=True)
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

sorted_gant(df=data, Task="Task", team_member="fullname", start_date="Start", end_date="Finish", date=None, plot = True)
sorted_gant(df=data, Task="Task", team_member="fullname", start_date="Start", end_date="Finish",colorscale="turbo", date=None, plot = True)




sorted_gant(df=df, Task="Task", team_member="Task", start_date="Start", end_date="Finish", colorscale="turbo", date=None, plot = True)
sorted_gant(df=df, Task="Task", team_member="Task", start_date="Start", end_date="Finish", colorscale="bluered", date=None, plot = True)


