


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





project_id = 1
fullname = "Jenni Willig"

sql = f"""
    INSERT INTO project_team_members(project_id, team_id) VALUES
    (
        (SELECT project_id FROM project WHERE project_id = '{project_id}'),
        (SELECT team_id FROM team_members WHERE full_name = '{fullname}')
    )
"""
execute_sql(sql)



project_id = 1
# full table für alle leute, tabelle
sql = f"""
    SELECT tm.full_name
    FROM team_members tm
    INNER JOIN project_team_members ptm
    ON ptm.team_id = tm.team_id
    INNER JOIN project p
    ON p.project_id = ptm.project_id
    WHERE p.project_id = '{project_id}'
    """

data = execute_sql(sql)
data

data = pd.DataFrame(data, columns=["Teammembers"])
data





project_id = 1
fullname = "Heiko Kulinna"

sql = f"""
    DELETE FROM project_team_members
    WHERE
    project_id in (SELECT project_id FROM project WHERE project_id = '{project_id}')
    AND
    team_id in (SELECT team_id FROM team_members WHERE full_name = '{fullname}');
"""
execute_sql(sql)


sql = f"""
    SELECT * FROM project_team_members
    """
execute_sql(sql)






# sql = f"""
#     CREATE TABLE project_deadlines (
#         project_deadlines_id SERIAL PRIMARY KEY,
#         project_id int REFERENCES project (project_id) ON UPDATE CASCADE ON DELETE CASCADE,
#         deadline_date DATE,
#         deadline_text VARCHAR(255),
#         UNIQUE (deadline_date, deadline_text)
#     );
# """

new_date = "2022-10-15"
deadline_text = "Gate Meeting"
project_id=1

sql = f"""
    INSERT INTO project_dealines(project_id, deadline_date, deadline_text) VALUES
    (
        (SELECT project_id FROM project WHERE project_id = '{project_id}'),
        '{new_date}',
        '{deadline_text}'
    );
"""
execute_sql(sql)




project_id = 1
sql = f"""
    SELECT deadline_date, deadline_text FROM project_deadlines
    WHERE project_id = {project_id}
    """
data=execute_sql(sql)
data


data = pd.DataFrame(data, columns=["Date", "Topic"])
data






####
#
#  sql = """
#         CREATE TABLE project (
#             project_id SERIAL PRIMARY KEY,
#             funding_id BIGINT NOT NULL,
#             FOREIGN KEY (funding_id)
#                 REFERENCES founding_sources (founding_source_id)
#                 ON UPDATE CASCADE ON DELETE CASCADE,
#             topic VARCHAR(255) NOT NULL,
#             topic_class_id BIGINT NOT NULL,
#             FOREIGN KEY (topic_class_id)
#                 REFERENCES topic_class (topic_class_id)
#                 ON UPDATE CASCADE ON DELETE CASCADE,
#             argus_enabled VARCHAR(5) NOT NULL,
#             way_charging VARCHAR(10) NOT NULL,
#             recieving_account VARCHAR(50),
#             cost_center_respon VARCHAR(255),
#             start_date DATE,
#             end_date DATE,
#             difficulty integer,
#             project_status VARCHAR(50),
#             project_description TEXT,
#             project_goals TEXT
#         )
#         """

#     SELECT tm.full_name
    # FROM team_members tm
    # INNER JOIN project_team_members ptm
    # ON ptm.team_id = tm.team_id
    # INNER JOIN project p
    # ON p.project_id = ptm.project_id


sql="""
    SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, tm.full_name
    FROM project p
    INNER JOIN founding_sources fs
    ON p.funding_id = fs.founding_source_id
    INNER JOIN topic_class tc
    ON p.topic_class_id = tc.topic_class_id
    INNER JOIN project_team_members ptm
    ON ptm.project_id = p.project_id
    INNER JOIN team_members tm
    ON ptm.team_id = tm.team_id
"""


sql="""
    SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, p.project_description
    FROM project p
    INNER JOIN founding_sources fs
    ON p.funding_id = fs.founding_source_id
    INNER JOIN topic_class tc
    ON p.topic_class_id = tc.topic_class_id
"""

data=execute_sql(sql)
data





# CREATE Table project_budget_planning 
# (
#     pbp_id SERIAL UNIQUE PRIMARY KEY,
#     year integer NOT NULL,
#     project_id integer NOT NULL,
#     FOREIGN KEY (project_id) 
#         REFERENCES project (project_id) 
#         ON UPDATE CASCADE ON DELETE CASCADE,
#     budget integer NOT NULL,
#     UNIQUE (year, project_id)
# );

# INSERT INTO project_budget_planing (project_id, year, budget) VALUES
# (
#     {project_id},
#     {budget_year},
#     {yearly_budget}
# );


project_id = 1
budget_year = 2022
yearly_budget = 500


sql = f"""
    INSERT INTO project_budget_planning (project_id, year, budget) VALUES
    (
        (SELECT project_id FROM project WHERE project_id = '{project_id}'),
        '{budget_year}',
        '{yearly_budget}'
    );
"""
execute_sql(sql)


sql = "SELECT * FROM project_budget_planning"
execute_sql(sql)


project_id = 1
budget_year = 2022

sql = f"""
        DELETE FROM project_budget_planning
        WHERE
        project_id = '{project_id}'
        AND
        year = '{budget_year}';
        """
execute_sql(sql)



project_id = 1
budget_year = 2022
yearly_budget = 480

sql = f"""
    UPDATE project_budget_planning
    SET
    project_id = (SELECT project_id FROM project WHERE project_id = '{project_id}'),
    year = '{budget_year}',
    budget = '{yearly_budget}'
    WHERE project_id = '{project_id}' AND year = '{budget_year}';
"""
execute_sql(sql)



sql = "SELECT * FROM project_budget_planning"
execute_sql(sql)

