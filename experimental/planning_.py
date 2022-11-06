





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



year=2022

year_max = str(year)+"-12-30"
year_max
year_min= str(year)+"-01-01"

# no team_member
sql=f"""
    SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, p.start_date, p.end_date
    FROM project p
    INNER JOIN founding_sources fs
    ON p.funding_id = fs.founding_source_id
    INNER JOIN topic_class tc
    ON p.topic_class_id = tc.topic_class_id
    LEFT JOIN project_team_members ptm
    ON p.project_id = ptm.project_id
    INNER JOIN project_budget_planning pbp
    ON pbp.project_id = p.project_id
    WHERE p.end_date <= '{year_max}'
    AND
    ptm.team_id IS NULL
    OR
    p.start_date >= '{year_min}'
    AND
    ptm.team_id IS NULL
"""


data=execute_sql(sql)

data=pd.DataFrame(data=data, columns=["id", "topic", "topic class", "founding source", "start date", "end date"])

data




from dashapp.app.utilities.plot import (
    sorted_gant,
    single_gantt
)



year=2022

year_max = str(year)+"-12-30"
year_min= str(year)+"-01-01"

sql=f"""
    SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, p.start_date, p.end_date
    FROM project p
    INNER JOIN founding_sources fs
    ON p.funding_id = fs.founding_source_id
    INNER JOIN topic_class tc
    ON p.topic_class_id = tc.topic_class_id
    LEFT JOIN project_team_members ptm
    ON p.project_id = ptm.project_id
    INNER JOIN project_budget_planning pbp
    ON pbp.project_id = p.project_id
    WHERE p.end_date <= '{year_max}'
    AND
    ptm.team_id IS NULL
    OR
    p.start_date >= '{year_min}'
    AND
    ptm.team_id IS NULL
"""

data=execute_sql(sql)

data = pd.DataFrame(data, columns=["project_id", "Task", "Topic", "Founding Source", "Start", "Finish"])

data = data.sort_values(by="project_id")

data = data.sort_values(by="project_id", ascending=False)
data = data.reset_index(drop = True)

data

fig = single_gantt(df=data, team_member=None, color="Task", Task="Task", Start="Start", Finish="Finish", date=None, plot = True)





