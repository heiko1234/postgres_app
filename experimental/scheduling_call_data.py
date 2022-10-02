

import pandas as pd
import psycopg2

import plotly.express as px
import pandas as pd
import plotly
import numpy as np
import plotly.figure_factory as ff

from datetime import datetime
date = datetime.today().strftime('%Y-%m-%d')
date



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




year = 2022


# starting point
# sql = f"""
#         SELECT p.project_id, tm.full_name, p.start_date, p.end_date, p.topic, tc.topic_class
#         FROM project p
#         INNER JOIN founding_sources fs
#         ON p.funding_id = fs.founding_source_id
#         INNER JOIN topic_class tc
#         ON p.topic_class_id = tc.topic_class_id
#         INNER JOIN project_team_members ptm
#         ON p.project_id = ptm.project_id
#         INNER JOIN team_members tm
#         ON tm.team_id = ptm.team_id
#         INNER JOIN project_budget_planning pbp
#         ON pbp.project_id = p.project_id
#         WHERE pbp.year = '{year}'
# """


year = "2022-01-01"
yearplus = "2023-01-01"


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
        p.start_date >= '{year}'
        AND
        p.start_date < '{yearplus}'
"""


year = "2022-01-01"
yearplus = "2023-01-01"

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
        p.end_date > '{year}'
        AND
        p.start_date < '{yearplus}'
"""


data=execute_sql(sql=sql)
data


data = pd.DataFrame(data=data, columns = ["project_id", "fullname", "Start", "Finish", "Task", "Topic"])
data

#    project_id       fullname       Start      Finish              Task                Topic
# 0           1  Heiko Kulinna  2022-09-01  2022-12-31     EV 1. Project  Underst. Hist. Data
# 1           2   Ralf Kulinna  2022-06-01  2023-07-31  Plant Connection  Underst. Hist. Data
# 2           2  Heiko Kulinna  2022-06-01  2023-07-31  Plant Connection  Underst. Hist. Data
# 3           1   Ralf Kulinna  2022-09-01  2022-12-31     EV 1. Project  Underst. Hist. Data
# 4           1  Frank Kulinna  2022-09-01  2022-12-31     EV 1. Project  Underst. Hist. Data
# 5           3  Heiko Kulinna  2022-10-01  2023-03-31         M project           Softsensor



year = "2022-01-01"
yearplus = "2023-01-01"

sql = f"""
        SELECT p.project_id, p.start_date, p.end_date, p.topic, tc.topic_class, p.project_status, pbp.year, pbp.budget
        FROM project p
        INNER JOIN founding_sources fs
        ON p.funding_id = fs.founding_source_id
        INNER JOIN topic_class tc
        ON p.topic_class_id = tc.topic_class_id
        INNER JOIN project_budget_planning pbp
        ON pbp.project_id = p.project_id
        WHERE
        p.end_date > '{year}'
        AND
        p.start_date < '{yearplus}'
"""


data=execute_sql(sql=sql)
data


data = pd.DataFrame(data=data, columns = ["project_id", "Start", "Finish", "Task", "Topic", "status", "year", "budget"])
data

data = data.groupby(["status"]).sum()
data

data = data.reset_index(drop=False)
data

# >>> data
#    project_id       Start      Finish              Task                Topic    status  year  budget
# 0           1  2022-09-01  2022-12-31     EV 1. Project  Underst. Hist. Data   Planned  2022     400
# 1           2  2022-06-01  2023-07-31  Plant Connection  Underst. Hist. Data  Approved  2022     320
# 2           3  2022-10-01  2023-03-31         M project           Softsensor   Ongoing  2022     200



# >>> data
#      status  project_id  year  budget
# 0  Approved           2  2022     320
# 1   Ongoing           3  2022     200
# 2   Planned           1  2022     400



sql = f"""
    SELECT tm.full_name, ti.year, ti.contract, ti.working_month, ti.activity, et.coverage
    FROM team_members tm
    INNER JOIN team_info ti
    ON tm.team_id = ti.team_id
    INNER JOIN entity_time et
    ON et.entity_id = tm.legal_entity_id and ti.year = et.year
"""
data = execute_sql(sql)


df = pd.DataFrame(data, columns=["Fullname", "Year", "Contract", "Working Month", "Activity", "Coverage"])
df
df = df[df["Year"] == 2022]
df
df["Coverage"].sum()  #580




import plotly.graph_objects as go
import plotly

# fig = go.Figure(go.Waterfall(
#     name = "20", orientation = "v",
#     measure = ["relative", "relative", "total", "relative", "relative", "total"],
#     x = ["Sales", "Consulting", "Net revenue", "Purchases", "Other expenses", "Profit before tax"],
#     textposition = "outside",
#     text = ["+60", "+80", "", "-40", "-20", "Total"],
#     y = [60, 80, 0, -40, -20, 0],
#     connector = {"line":{"color":"rgb(63, 63, 63)"}},
# ))

# fig.update_layout(
#         title = "Profit and loss statement 2018",
#         showlegend = True
# )

# project_status = ["Planned", "Approved", "Ongoing", "Completed", "Rejected"]

fig = go.Figure(go.Waterfall(
    name = "Project Waterfall", orientation="v",
    x = ["Approved", "Ongoing", "Completed", "Total Available", "Needed", "Booked"],
    y = [320, 200, 0.1, 0, -580, 400],
    measure = ["relative", "relative", "relative", "total", "relative", "relative"],
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))

fig.update_layout(
        title = "Profit and loss statement 2022",
        showlegend = True
)

plotly.offline.plot(fig)




from dashapp.app.utilities.plot import (
    sorted_gant
)


year = "2022-01-01"
yearplus = "2023-01-01"

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
        p.end_date > '{year}'
        AND
        p.start_date < '{yearplus}'
"""


data=execute_sql(sql=sql)
data


data = pd.DataFrame(data=data, columns = ["project_id", "fullname", "Start", "Finish", "Task", "Topic"])
data


from datetime import datetime
date = datetime.today().strftime('%Y-%m-%d')
date

sorted_gant(df=data, Task="Task", team_member="fullname", start_date="Start", end_date="Finish", date=None, plot = True)








