



import plotly.express as px
import pandas as pd
import plotly
import numpy as np
import plotly.figure_factory as ff

from datetime import datetime
date = datetime.today().strftime('%Y-%m-%d')
date




df = pd.DataFrame([
    dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Completion_pct=50),
    dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Completion_pct=25),
    dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Completion_pct=75)
])


df

fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Completion_pct")
fig.update_yaxes(autorange="reversed")


df = pd.DataFrame([
    dict(Project="Project A", Team="Heiko", Start="2022-01-15", Finish="2022-12-15", Working_hours=400),
    dict(Project="Project B", Team="Ralf", Start="2022-04-15", Finish="2022-09-30", Working_hours=300),
    dict(Project="Project A", Team="Ralf", Start="2022-01-15", Finish="2022-12-15", Working_hours=200),
    dict(Project="Project C", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
])

df


fig = px.timeline(df, x_start="Start", x_end="Finish", y="Project", color="Working_hours")
fig.update_yaxes(autorange="reversed")


fig = px.timeline(df, x_start="Start", x_end="Finish", y="Project", color="Team")

fig = px.timeline(df, x_start="Start", x_end="Finish", y="Team", color="Project")

fig = px.timeline(df, x_start="Start", x_end="Finish", y=["Team", "Project"], color="Working_hours")



# how to update x axes

fig.update_xaxes(range=["2022-01", "2023-01"])


plotly.offline.plot(fig)







# Task, Start, Finish
df

df = pd.DataFrame([
    dict(Task="Task A", Team="Heiko", Start="2022-01-15", Finish="2022-06-15", Working_hours=400),
    dict(Task="Task B", Team="Ralf", Start="2022-04-15", Finish="2022-09-30", Working_hours=300),
    dict(Task="Task A", Team="Ralf", Start="2022-06-15", Finish="2022-12-15", Working_hours=200),
    dict(Task="Task C", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
])
df

df["Task_Team"] = df["Task"]+df["Team"]




# build a colormap for status 
colormap = {s:c for s,c in zip(df["Task"].unique(), px.colors.qualitative.Plotly)}
colormap


df

df = df.sort_values(by="Task")
df

fig = ff.create_gantt(df, index_col='Task', group_tasks=True)
fig = ff.create_gantt(df, index_col='Task', group_tasks=False)


# fig = ff.create_gantt(df, index_col='Task', colors="Team", group_tasks=False)
fig = ff.create_gantt(df, index_col='Task', colors=colormap, group_tasks=False)

fig = ff.create_gantt(df, index_col='Team', group_tasks=True)

fig = ff.create_gantt(df, index_col='Task_Team', group_tasks=True)

fig = ff.create_gantt(df, index_col='Task_Team', group_tasks=False)


date = "2022-10-13"
fig.add_vline(x=date, line_width=3, line_color="black")


plotly.offline.plot(fig)




####################




df = pd.DataFrame([
    dict(Task="Task A", Team="Heiko", Start="2022-01-15", Finish="2022-06-15", Working_hours=400),
    dict(Task="Task B", Team="Ralf", Start="2022-04-15", Finish="2022-09-30", Working_hours=300),
    dict(Task="Task A", Team="Ralf", Start="2022-04-15", Finish="2022-12-15", Working_hours=200),
    dict(Task="Task C", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
])
df

df = df.sort_values(by="Task")
df = df.reset_index(drop = True)
df

colormap = {s:c for s,c in zip(df["Team"].unique(), px.colors.qualitative.Plotly)}
colormap

df["Team"]
list(df["Team"])
# ['Heiko', 'Ralf', 'Ralf', 'Tobi']
[colormap[i] for i in df["Team"]]
# ['#636EFA', '#EF553B', '#EF553B', '#00CC96']


fig = ff.create_gantt(df, index_col='Task', colors=[colormap[i] for i in df["Team"]], group_tasks=False)
plotly.offline.plot(fig)


{i: colormap[df.loc[i,"Team"]] for i in df.index}

df["Task"]

df["index"] = df.index 

# fig = ff.create_gantt(df, index_col='Task', colors=colormap, group_tasks=False)
# plotly.offline.plot(fig)


fig = ff.create_gantt(df, index_col='Task', colors={i: colormap[df.loc[i,"Team"]] for i in df.index}, group_tasks=False)
plotly.offline.plot(fig)


df
fig = ff.create_gantt(df, index_col="index", task_names = "Task", colors={i: colormap[df.loc[i,"Team"]] for i in df.index}, group_tasks=False)
plotly.offline.plot(fig)



# Das hier !



df = pd.DataFrame([
    dict(Task="Task A", Team="Heiko", Start="2022-01-15", Finish="2022-06-15", Working_hours=400),
    dict(Task="Task B", Team="Ralf", Start="2022-04-15", Finish="2022-09-30", Working_hours=300),
    dict(Task="Task A", Team="Ralf", Start="2022-04-15", Finish="2022-12-15", Working_hours=200),
    dict(Task="Task C", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
])
df

df = df.sort_values(by="Task")
df = df.reset_index(drop = True)
df



list(df["Team"])
# ['Heiko', 'Ralf', 'Ralf', 'Tobi']
df

# da wo der Wert sich ändert
v = list(df["Task"])
v = np.array(v)
v
list(np.where(v[:-1] != v[1:])[0])
# [1, 2]



fig = ff.create_gantt(df, index_col="Team", task_names = "Task",  group_tasks=False, show_colorbar=True)
fig.update_yaxes(autorange="reversed")
fig.add_hline(y = 2.5, line_width=3, line_color="white")
fig.add_hline(y = 1.5, line_width=3, line_color="white")
fig.add_vline(x=date, line_width=3, line_color="black")
plotly.offline.plot(fig)



fig = ff.create_gantt(df, index_col="Team", task_names = "Task",  group_tasks=True)
fig.update_yaxes(autorange="reversed")
plotly.offline.plot(fig)





# 


df = pd.DataFrame([
    dict(Task="Task A", Team="Heiko", Start="2022-01-15", Finish="2022-06-15", Working_hours=400),
    dict(Task="Task B", Team="Ralf", Start="2022-04-15", Finish="2022-09-30", Working_hours=300),
    dict(Task="Task A", Team="Ralf", Start="2022-04-15", Finish="2022-12-15", Working_hours=200),
    dict(Task="Task C", Team="Tobi", Start="2022-06-15", Finish="2022-11-01", Working_hours=350),
    dict(Task="Task D", Team="Anna", Start="2022-04-15", Finish="2022-07-01", Working_hours=350),
    dict(Task="Task D", Team="Max", Start="2022-04-15", Finish="2022-07-01", Working_hours=350),
    dict(Task="Task D", Team="Lena", Start="2022-04-15", Finish="2022-07-01", Working_hours=350),
])
df




def sorted_gant(df, Task, team_member, Start=None, Finish=None, date=None, plot = True):

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

    if (Start != None) and (Finish != None):
        fig.update_xaxes(range=[Start, Finish])

    if plot:
        plotly.offline.plot(fig)
    else:
        return fig




sorted_gant(df=df, Task="Task", team_member="Team", date=None, plot = True)



sorted_gant(df=df, project="Task", team_member="Team", Start="2022-04-01", Finish="2022-09-30", date=None, plot = True)



from datetime import datetime
date = datetime.today().strftime('%Y-%m-%d')
date

sorted_gant(df=df, project="Task", team_member="Team", Start="2022-04-01", Finish="2022-09-30", date=date, plot = True)

sorted_gant(df=df, project="Task", team_member="Team", Start=None, Finish=None, date=date, plot = True)




dft = df[df["Team"] == "Ralf"]
dft


fig = px.timeline(dft, x_start="Start", x_end="Finish", y="Task", color="Working_hours")
fig.update_yaxes(autorange="reversed")

plotly.offline.plot(fig)




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



single_gantt(df=df, team_member="Ralf", Task="Task", color="Working_hours", Start="Start", Finish="Finish", date=None, plot = True)


single_gantt(df=df, team_member="Ralf", Task="Task", color="Working_hours", Start="Start", Finish="Finish", date=date, plot = True)





df

df = df.sort_values(by="Team")
df = df.reset_index(drop = True)
df


v = list(df["Team"])
v = np.array(v)
v = list(np.where(v[:-1] != v[1:])[0])
v

fig = ff.create_gantt(df, index_col="Team", task_names = "Task",  group_tasks=False, show_colorbar=True)
fig.update_yaxes(autorange="reversed")

for i in v: 
    fig.add_hline(y = i+0.5, line_width=4, line_color="white")


fig.add_vline(x=date, line_width=3, line_color="black")
plotly.offline.plot(fig)





from dashapp.app.utilities.app_utilities import (
    execute_sql
)

overview_year = 2023
overview_teammember = "Heiko Kulinna"


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
        INNER JOIN project_budget_planning pbp
        ON pbp.project_id = p.project_id
        WHERE pbp.year = '{overview_year}'
        AND
        tm.team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
"""


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
        INNER JOIN project_budget_planning pbp
        ON pbp.project_id = p.project_id
        WHERE pbp.year = '{overview_year}'
"""



data=execute_sql(sql=sql)
data


data = pd.DataFrame(data=data, columns = ["project_id", "fullname", "Start", "Finish", "Task", "Topic"])
data

sorted_gant(df=data, Task="Task", team_member="fullname", date=None, plot = True)












df = pd.DataFrame()

df["Project"] = ["Project A", "Project B", "Project C"]
df["Status"] = ["Booked", "Booked", "Booked"]
df["Budget"] = [50, 100, 150]

df

sum(df["Budget"])

new_df = pd.DataFrame([{"Project": "Required", "Status": "Needed", "Budget": 450}])
new_df


df = pd.concat([new_df, df], axis=0)
df = df.reset_index(drop=True)
df


import plotly.express as px


fig = px.bar(df, x="Status", y="Budget", color="Project", text_auto=True)

plotly.offline.plot(fig)











