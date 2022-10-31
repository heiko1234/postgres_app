


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



# SQL How to search
sql = f"""SELECT project_id FROM project WHERE project_description LIKE 'project' """


sql = """SELECT project_id FROM project WHERE project_description ~* '(\mproject\M)' """



fullname = "Heiko Kulinna"
year =2023
sql = f"""
    SELECT project_id, month, FROM project_time_budget
    WHERE team_id in (SELECT team_id FROM team_members WHERE full_name = '{fullname}')
    AND year = '{year}';
"""


# first search with a search term
searchterm = "project"

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
        WHERE project_description ~* '(\m{searchterm}\M)' 
    """


# search of project overview list
sql = f"""
        SELECT p.project_id, p.start_date, p.end_date, p.topic, tc.topic_class
        FROM project p
        INNER JOIN founding_sources fs
        ON p.funding_id = fs.founding_source_id
        INNER JOIN topic_class tc
        ON p.topic_class_id = tc.topic_class_id
        WHERE project_description ~* '(\m{searchterm}\M)' 
    """


# multi search terms
searchterm = "project"
searchterm2 = "target"

sql = f"""
        SELECT p.project_id, p.start_date, p.end_date, p.topic, tc.topic_class
        FROM project p
        INNER JOIN founding_sources fs
        ON p.funding_id = fs.founding_source_id
        INNER JOIN topic_class tc
        ON p.topic_class_id = tc.topic_class_id
        WHERE project_description ~* '(\m{searchterm}\M)|(\m{searchterm2}\M)'
        OR
        project_goals ~* '(\m{searchterm}\M)|(\m{searchterm2}\M)'
    """

search_date = execute_sql(sql)
search_date

data = pd.DataFrame(data=search_date, columns = ["project_id", "Start", "Finish", "Task", "Topic"])
data


project_id = 1
sql = f"""
    SELECT topic, topic_class_id, argus_enabled, way_charging, recieving_account, cost_center_respon, start_date, end_date, difficulty, project_status, project_description, project_goals FROM project
    WHERE project_id = '{project_id}';
"""

sql_table = execute_sql(sql)
sql_table






# create a search function
# 

searchterm = "project"
searchterm2 = "target"
f'(\m{searchterm}\M)|(\m{searchterm2}\M)'

search_string = "project Projects IT"

search_string.split(" ")




def create_searchterm(search_string):
    output = ""
    for count, value in enumerate(search_string.split(" ")):
        if count==0:
            output=output+f"(\m{value}\M)"
        else:
            output=output+f"|(\m{value}\M)"
    return output


search_string = "cool"

statement = create_searchterm(search_string)
statement


sql = f"""
        SELECT p.project_id, p.start_date, p.end_date, p.topic, tc.topic_class
        FROM project p
        INNER JOIN founding_sources fs
        ON p.funding_id = fs.founding_source_id
        INNER JOIN topic_class tc
        ON p.topic_class_id = tc.topic_class_id
        WHERE project_description ~* '{statement}'
        OR
        project_goals ~* '{statement}'
    """


search_date = execute_sql(sql)
search_date

data = pd.DataFrame(data=search_date, columns = ["project_id", "Start", "Finish", "Task", "Topic"])
data


project_id = 2  #2
sql = f"""
    SELECT fs.founding_source, p.topic, tc.topic_class, p.argus_enabled, p.way_charging, p.cost_center_respon, p.start_date, p.end_date, p.difficulty, p.project_status, p.project_description, p.project_goals
    FROM project p
    INNER JOIN topic_class tc
    ON p.topic_class_id = tc.topic_class_id
    INNER JOIN founding_sources fs
    ON p.funding_id = fs.founding_source_id
    WHERE p.project_id = '{project_id}';
"""

data = execute_sql(sql)
data

data = pd.DataFrame(data, columns=["funding", "topic", "topic_class", "argus", "charging", "account_resp", "start", "end", "difficulty", "status", "description", "target"])
data


