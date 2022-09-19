


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



sql = f"""
    SELECT YEAR FROM project_budget_planning
"""

data = execute_sql(sql)

data = list(set(data))
data.sort()
data


fullname = "Heiko Kulinna"
year = "2022"

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
    WHERE pbp.year = '{year}'
    AND
    tm.team_id in (SELECT team_id FROM team_members WHERE full_name = '{fullname}')
"""

data=execute_sql(sql)

data



# sql = """
#     CREATE Table project_time_budget 
#     (
#         ptb_id SERIAL UNIQUE PRIMARY KEY,
#         year integer NOT NULL,
#         month integer NOT NULL,
#         team_id INTEGER NOT NULL,
#         FOREIGN KEY (team_id)
#             REFERENCES team_members (team_id)
#             ON UPDATE CASCADE ON DELETE CASCADE,
#         working_hours integer,
#         working_booking integer,
#         project_id integer NOT NULL,
#         FOREIGN KEY (project_id) 
#             REFERENCES project (project_id) 
#             ON UPDATE CASCADE ON DELETE CASCADE,
#         UNIQUE (year, month, team_id, project_id)
#     );
# """



# sql = f"""
#     INSERT INTO team_info (team_id, year, contract, working_month, entity_id, activity) VALUES 
#     (
#         (SELECT team_id FROM team_members WHERE full_name = '{fullname}'),
#         '{year}',
#         '{contract}',
#         '{working_month}',
#         (SELECT legal_entity_id FROM team_members WHERE full_name = '{fullname}'),
#         '{activity}'
#     );
# """


team_id = 1

fullname = "Heiko Kulinna"
year =2022
sql = f"""
    SELECT project_id, month, working_hours from project_time_budget
    WHERE team_id in (SELECT team_id FROM team_members WHERE full_name = '{fullname}')
    AND year = '{year}';
"""

data=execute_sql(sql = sql)
data

months = [1,2,3,4,5,6,7,8,9,10,11,12]
ids = [1, 2]

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
data=data.pivot(index="project_id", columns="month", values="working_days")
data = data.reset_index(drop = False)
data

data = None

data = pd.DataFrame(data, columns = ["id", "month", "working_days"])
data
data.pivot(index="id", columns="month", values="working_days")


fullname = "Heiko Kulinna"
project_id = 1
year = 2022
months = [1,2,3,4,5,6,7,8,9,10,11,12]
working_days = [10, 15, 16, 17, 18, 19, 20, 9, 8, 10, 12, 19]


for i in range(len(months)):

    sql = f"""
        INSERT INTO project_time_budget (year, month, working_hours, team_id, project_id) VALUES
        (
            '{year}',
            '{months[i]}',
            '{working_days[i]}',
            (SELECT team_id FROM team_members WHERE full_name = '{fullname}'),
            '{project_id}'
        )
    """
    data=execute_sql(sql = sql)
data


# DELETE from team_info 
# WHERE
# team_id in (SELECT team_id FROM team_members WHERE full_name = '{fullname}')
# AND
# team_info.year = '{dd_year}';

fullname = "Heiko Kulinna"
year = 2022
sql = f"""
    DELETE from project_time_budget
    WHERE
    team_id in (SELECT team_id FROM team_members WHERE full_name = '{fullname}')
    AND
    year = '{year}';
"""
data=execute_sql(sql = sql)



