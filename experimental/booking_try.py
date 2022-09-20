


import pandas as pd
import psycopg2


def execute_sql(sql):
    #establishing the connection
    conn = psycopg2.connect(
        database="team", user='postgres', password='postgres', host='127.30.0.1', port= '5432'
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





overview_teammember = "Heiko Kulinna"
overview_year =2022







sql=f"""
    SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, p.project_description
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
data=execute_sql(sql)
data = pd.DataFrame(data, columns=["project_id", "topic", "topic_class", "founding_source", "project_descrition"])

list_ids = list(set(data["project_id"]))

# project_ids where projects exist
list_ids




sql = f"""
    SELECT project_id, month, working_hours FROM project_time_budget
    WHERE team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
    AND year = '{overview_year}';
"""

data=execute_sql(sql = sql)
data


data = pd.DataFrame(data, columns=["project_id", "month", "working_days"])
data


try:
    list_ids_available = list(set(data["project_id"]))
except BaseException:
    list_ids_available = []


ids = [element for element in list_ids if element not in list_ids_available]
ids


data=data.pivot(index="project_id", columns="month", values="working_days")
data
data = data.reset_index(drop = False)
data = data.reset_index(drop = True)
pda = data
pda


# pda = pda.iloc[0, :]
# pda

# pda=pda.pivot(index="project_id", columns="month", values="working_days")
# pda = pda.reset_index(drop = False)
# pda = pda.reset_index(drop = True)
# pda
# # data

# ids = [2]

months = [1,2,3,4,5,6,7,8,9,10,11,12]
all_zero = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

data = pd.DataFrame()

if len(data) == 0:
    for id in ids:
        new_data = pd.DataFrame()
        new_data["month"] = months
        new_data["working_days"] = all_zero
        new_data["project_id"] = id
        data = pd.concat([data, new_data], axis=0)

data
if len(data) != 0:
    data=data.pivot(index="project_id", columns="month", values="working_days")
    data
    data = data.reset_index(drop = False)
    data = data.reset_index(drop = True)
    pdata = data
    pdata
else:
    pdata = None

pda
pdata


new_df = pd.concat([pda, pdata], axis=0)
new_df = new_df.reset_index(drop = True)
new_df





sql = f"""
    DELETE from project_time_budget
    WHERE
    team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
    AND
    year = '{overview_year}';
"""
data=execute_sql(sql = sql)
data


# new_df = pdata
# new_df


months = [1,2,3,4,5,6,7,8,9,10,11,12]

for project_id in list(new_df["project_id"]):
    print(project_id)
    selected_data = new_df.loc[new_df["project_id"]==project_id]
    selected_data = selected_data.reset_index(drop = True)
    working_days = list(selected_data.loc[0, [1,2,3,4,5,6,7,8,9,10,11,12]])

    for i in list(range(len(months))):

        sql = f"""
            INSERT INTO project_time_budget (year, month, working_hours, team_id, project_id) VALUES
            (
                '{overview_year}',
                '{months[i]}',
                '{working_days[i]}',
                (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}'),
                '{project_id}'
            );
        """
        output=execute_sql(sql = sql)
        output



