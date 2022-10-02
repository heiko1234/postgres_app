

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



overview_year = 2022
month = 10


sql = """
    CREATE Table project_time_budget 
    (
        ptb_id SERIAL UNIQUE PRIMARY KEY,
        year integer NOT NULL,
        month integer NOT NULL,
        team_id INTEGER NOT NULL,
        FOREIGN KEY (team_id)
            REFERENCES team_members (team_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        working_days integer,
        working_booking float,
        project_id integer NOT NULL,
        FOREIGN KEY (project_id) 
            REFERENCES project (project_id) 
            ON UPDATE CASCADE ON DELETE CASCADE,
        UNIQUE (year, month, team_id, project_id)
    );
"""

sql = f"""
    CREATE Table active_project_person_costcenter
    (
        appc_id SERIAL UNIQUE PRIMARY KEY,
        project_id int REFERENCES project (project_id) ON UPDATE CASCADE ON DELETE CASCADE,
        team_id int REFERENCES team_members (team_id) ON UPDATE CASCADE ON DELETE CASCADE,
        costcenter VARCHAR(100) NOT NULL,
        UNIQUE (project_id, team_id)
    );
"""


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


overview_year = 2022
month = 6

# irgentwie ne
sql = f"""
    SELECT  p.project_id, appc.costcenter, p.topic, appc.working_booking, tm.full_name
    FROM active_project_person_costcenter appc
    INNER JOIN project p
    ON p.project_id = appc.project_id AND appc.team_id = tm.team_id
    INNER JOIN team_members tm
    ON tm.team_id = appc.team_id
    WHERE 
    ptb.year = '{overview_year}' 
    AND
    ptb.month = '{month}'
    AND 
    ptb.working_booking IS NOT NULL
    AND
    appc.costcenter IS NOT NULL
"""

# INNER JOIN project_time_budget ptb
# ON ptb.project_id = p.project_id




overview_year = 2022
month = 6

sql = f"""
    SELECT ptb.year, ptb.month, ptb.team_id, ptb.project_id, ptb.working_booking
    FROM project_time_budget ptb
    WHERE 
    ptb.year = '{overview_year}' 
    AND
    ptb.month = '{month}'
"""

data=execute_sql(sql)
data


data = pd.DataFrame(data, columns=["year", "month", "team_id", "project_id", "working_booking"])
data

# >>> data
#    year  month  team_id  project_id  working_booking
# 0  2022      6        3           1            10.29
# 1  2022      6        1           1             7.92
# 2  2022      6        1           2             7.92
# 3  2022      6        2           1             1.67
# 4  2022      6        2           2             4.17



# Fulljoin


overview_year = 2022
month = 6

sql = f"""
    SELECT ptb.year, ptb.month, ptb.team_id, ptb.project_id, p.topic, p.project_status, ptb.working_booking, tm.full_name, appc.costcenter
    FROM project_time_budget ptb
    INNER JOIN team_members tm
    ON tm.team_id = ptb.team_id
    INNER JOIN active_project_person_costcenter appc
    ON appc.project_id = ptb.project_id AND appc.team_id = ptb.team_id
    INNER JOIN project p
    ON p.project_id = appc.project_id
    WHERE 
    ptb.year = '{overview_year}' 
    AND
    ptb.month = '{month}'
"""

data=execute_sql(sql)
data


data = pd.DataFrame(data, columns=["year", "month", "team_id", "project_id", "topic", "status", "working_booking", "fullname", "Costcenter"])
data

status_list = ["Approved"]

data = data[data["status"].isin(status_list)]
data

# >>> data
#    year  month  team_id  project_id  working_booking       fullname Costcenter
# 0  2022      6        1           1             7.92  Heiko Kulinna   DE952345
# 1  2022      6        3           1            10.29  Frank Kulinna   DE951234


#    year  month  team_id  project_id  working_booking       fullname Costcenter
# 0  2022      6        1           1             7.92  Heiko Kulinna   DE952345
# 1  2022      6        3           1            10.29  Frank Kulinna   DE951234
# 2  2022      6        2           1             1.67   Ralf Kulinna  DE8512345
# 3  2022      6        1           2             7.92  Heiko Kulinna   QD123456
# 4  2022      6        2           2             4.17   Ralf Kulinna     BE2345


data = pd.DataFrame(data, columns=["year", "month", "team_id", "project_id", "topic", "status", "working_booking", "fullname", "Costcenter"])
data = data.loc[:,["project_id", "topic", "working_booking", "Costcenter"]]
data

data.groupby(['Costcenter', "project_id", "topic"]).sum()




# Left JOIN

overview_year = 2022
month = 6

sql = f"""
    SELECT ptb.year, ptb.month, ptb.team_id, ptb.project_id, p.topic, p.project_status, ptb.working_booking, tm.full_name, appc.costcenter
    FROM project_time_budget ptb
    INNER JOIN team_members tm
    ON tm.team_id = ptb.team_id
    INNER JOIN project p
    ON p.project_id = ptb.project_id
    LEFT JOIN active_project_person_costcenter appc
    ON appc.project_id = ptb.project_id AND appc.team_id = ptb.team_id
    WHERE 
    ptb.year = '{overview_year}' 
    AND
    ptb.month = '{month}'
    AND
    appc.costcenter IS NULL

"""

data=execute_sql(sql)
data

data = pd.DataFrame(data, columns=["year", "month", "team_id", "project_id", "topic", "status", "booking", "name", "costcenter"])
data

# >>> data
#    year  month  team_id  project_id      topic  booking           name costcenter
# 0  2022      6        1           3  M project     1.58  Heiko Kulinna       None







