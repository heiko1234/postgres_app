


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




funding="KDC"
topic="Irgentwas"
topic_class="Softsensor"
argus="Yes"
charging="Manuall"
rec_account="eine Kostenstelle"
account_resp="ein Name"
start="2022-02-15"
end="2022-05-18"
difficulty="8"
status="pending"
description="ein langer Text"
target= "auch ein langer Text"



sql = f"""
    INSERT INTO project (funding_id, topic, topic_class_id, argus_enabled, way_charging, recieving_account, cost_center_respon, start_date, end_date, difficulty, project_status, project_description, project_goals) VALUES 
    (
        (SELECT founding_source_id FROM founding_sources WHERE founding_source = '{funding}'),
        '{topic}',
        (SELECT topic_class_id FROM topic_class WHERE topic_class = '{topic_class}'),
        '{argus}',
        '{charging}',
        '{rec_account}',
        '{account_resp}',
        '{start}',
        '{end}',
        '{difficulty}',
        '{status}',
        '{description}',
        '{target}'
    );
"""

data = execute_sql(sql)




sql= "SELECT project_id FROM project"
data=execute_sql(sql)

data=pd.DataFrame(data, columns=["project_id"])
list_data=list(data["project_id"])


project_id = 1
sql = f"""
    SELECT topic, topic_class_id, argus_enabled, way_charging, recieving_account, cost_center_respon, start_date, end_date, difficulty, project_status, project_description, project_goals FROM project
    WHERE project_id = '{project_id}';
"""


sql = f"""SELECT * FROM project"""


data = execute_sql(sql)
data


data = pd.DataFrame(data, columns=["funding", "topic", "topic_class", "argus", "charging", "rec_account", "account_resp", "start", "end", "difficulty", "status", "description", "target"])




# SELECT tm.pre_name, tm.sur_name, tm.full_name, tm.email, tm.user_id, e.entity_name, tm.department_entry_date
# FROM team_members tm
# INNER JOIN entity e
# ON tm.legal_entity_id = e.entity_id
# WHERE tm.full_name = '{fullname}';


project_id = 1
sql = f"""
    SELECT fs.founding_source, p.topic, tc.topic_class, p.argus_enabled, p.way_charging, p.recieving_account, p.cost_center_respon, p.start_date, p.end_date, p.difficulty, p.project_status, p.project_description, p.project_goals
    FROM project p
    INNER JOIN topic_class tc
    ON p.topic_class_id = tc.topic_class_id
    INNER JOIN founding_sources fs
    ON p.funding_id = fs.founding_source_id
    WHERE p.project_id = '{project_id}';
"""

data = execute_sql(sql)
data


data = pd.DataFrame(data, columns=["funding", "topic", "topic_class", "argus", "charging", "rec_account", "account_resp", "start", "end", "difficulty", "status", "description", "target"])
data




# 
# sql=f"""
#     UPDATE team_members
#     SET 
#     pre_name = '{new_name}',
#     sur_name = '{new_surname}',
#     full_name = '{new_fullname}',
#     email = '{new_email}',
#     user_id = '{new_user_id}',
#     legal_entity_id = (SELECT entity_id FROM entity WHERE entity_name = '{new_legal_entity}'),
#     department_entry_date = '{new_entry_date}'
#     WHERE team_id in (SELECT team_id FROM team_members WHERE full_name = '{old_fullname}');
# """



# fs.founding_source, p.topic, tc.topic_class, p.argus_enabled, p.way_charging, p.recieving_account, 
# p.cost_center_respon, p.start_date, p.end_date, p.difficulty, p.project_status, p.project_description, 
# p.project_goals

funding="KDC"
topic="Irgentwas"
topic_class="Softsensor"
argus="Yes"
charging="Manuall"
rec_account="eine Kostenstelle"
account_resp="ein Name"
start="2022-02-15"
end="2022-05-18"
difficulty="8"
status="pending"
description="ein langer Text"
target= "auch ein langer Text"
project_id = 1


sql = f"""
    UPDATE project
    SET
    funding_id = (SELECT founding_source_id FROM founding_sources WHERE founding_source = '{funding}'),
    topic = '{topic}',
    topic_class_id = (SELECT topic_class_id FROM topic_class WHERE topic_class = '{topic_class}'),
    argus_enabled = '{argus}',
    way_charging = '{charging}',
    recieving_account = '{rec_account}',
    cost_center_respon = '{account_resp}',
    start_date = '{start}',
    end_date = '{end}',
    difficulty = '{difficulty}',
    project_status = '{status}',
    project_description = '{description}',
    project_goals = '{target}'
    WHERE project_id = '{project_id}';
"""

data = execute_sql(sql)
data







