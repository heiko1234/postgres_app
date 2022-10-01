


import pandas as pd
import psycopg2


def execute_sql(sql):
    #establishing the connection
    conn = psycopg2.connect(
        # database="teams", user='postgres', password='postgres', host='127.30.0.1', port= '5432'
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




project_id = 1

sql = f"""
    SELECT typb.year, tm.full_name, typb.project_yearly_budget
    FROM team_year_project_budget typb
    INNER JOIN team_members tm
    ON typb.team_id = tm.team_id
    WHERE typb.project_id = '{project_id}'
"""
data=execute_sql(sql)
data


year = 2022
project_id = 1
teammember = "Heiko Kulinna"
teammember_budget = 50


sql = f"""
    INSERT INTO team_year_project_budget(project_id, year, team_id, project_yearly_budget) VALUES
    (
        (SELECT project_id FROM project WHERE project_id = '{project_id}'),
        '{year}',
        (SELECT team_id FROM team_members WHERE full_name ='{teammember}'),
        '{teammember_budget}'
    );
"""
data = execute_sql(sql)



sql = f"""
    UPDATE team_year_project_budget
    SET
    project_yearly_budget = '{teammember_budget}'
    WHERE project_id = '{project_id}' AND year = '{year}' AND team_id = (SELECT team_id FROM team_members WHERE full_name ='{teammember}');
"""
execute_sql(sql)


sql = f"""
    DELETE FROM team_year_project_budget
    WHERE
    project_id = '{project_id}'
    AND
    year = '{year}'
    AND
    team_id = (SELECT team_id FROM team_members WHERE full_name ='{teammember}');
    """
execute_sql(sql)



import pandas as pd

df = pd.DataFrame()


df["names"] = ["Hiko", "Ralf"]
df["2021"] = [100, 150]
df["2022"] = [50, 90]

df["Sum"] = df[df.columns].sum(axis=1, numeric_only=True)
df

df[df.columns].sum(axis=0, numeric_only=True)

["Sum"]+list(df[df.columns].sum(axis=0, numeric_only=True))

# df.append(pd.Series(["Sum"]+list(df[df.columns].sum(axis=0, numeric_only=True))), ignore_index=True)

inter_df = pd.DataFrame([["Sum"]+list(df[df.columns].sum(axis=0, numeric_only=True))], columns = df.columns)
inter_df

pd.concat([df, inter_df], axis=0)



overview_teammember = "Heiko Kulinna"
overview_year = 2022


sql = f"""
    SELECT project_id, month, working_days, working_booking FROM project_time_budget
    WHERE team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
    AND year = '{overview_year}';
"""

data=execute_sql(sql = sql)
data = pd.DataFrame(data, columns=["project_id", "month", "working_days", "working_booking"])
data = data.pivot(index="project_id", columns="month", values="working_booking")
data = data.reset_index(drop = False)
data = data.reset_index(drop = True)

data = data.sort_values(by="project_id")
data

data.columns
# Index(['project_id', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], dtype='object', name='month')


list_sum = ["sum"]+list(data[data.columns[1:]].sum(axis=0, numeric_only=True))
print(list_sum)
len(list_sum)
print(list(data.columns))
len(list(data.columns))  #13
inter_data = pd.DataFrame([list_sum], columns = data.columns)
inter_data

print(inter_data)

# add Sum column and rows
# data["Sum"] = round(data[data.columns[1:]].sum(axis=1, numeric_only=True),2)




# data=pd.concat([data, inter_data], axis=0)
# data = inter_data
data = data.reset_index(drop = True)





overview_teammember = "Heiko Kulinna"
overview_year = 2023
project_id = 1



sql = f"""
    SELECT typb.year, tm.full_name, typb.project_yearly_budget
    FROM team_year_project_budget typb
    INNER JOIN team_members tm
    ON typb.team_id = tm.team_id
    WHERE typb.project_id = '{project_id}'
"""
data=execute_sql(sql)

data = pd.DataFrame(data, columns=["Year", "Team member", "Budget"])

data = data.pivot(index="Team member", columns = "Year", values= "Budget")
data =data.reset_index(drop=False)

data = data.sort_values(by="Team member")

inter_data = pd.DataFrame([["Sum"]+list(data[data.columns].sum(axis=0, numeric_only=True))], columns = data.columns)
data=pd.concat([data, inter_data], axis=0)

data["Sum"] = data[data.columns].sum(axis=1, numeric_only=True)

data = data.reset_index(drop = True)
data


sql = f"""
    SELECT typb.project_id, typb.year, tm.full_name, typb.project_yearly_budget
    FROM team_year_project_budget typb
    INNER JOIN team_members tm
    ON typb.team_id = tm.team_id
    WHERE typb.team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
    AND
    typb.year = '{overview_year}'
"""
data=execute_sql(sql)
data


data = pd.DataFrame(data, columns=["project_id", "year", "fullname", "yearly_budget"])
data








project_id = 1
teammember = "Heiko Kulinna"
costcenter = "DE95123456"


# sql = f"""
#     CREATE Table project_costcenter
#     (
#         pc_id SERIAL UNIQUE PRIMARY KEY,
#         project_id int REFERENCES project (project_id) ON UPDATE CASCADE ON DELETE CASCADE,
#         costcenter VARCHAR(50) NOT NULL
#     );
# """


project_id = 1
teammember = "Heiko Kulinna"
costcenter = "DE95123456"


sql = f"""
    INSERT INTO project_costcenter(project_id, costcenter) VALUES
    (
        (SELECT project_id FROM project WHERE project_id = '{project_id}'),
        '{costcenter}'
    );
"""
data = execute_sql(sql)


project_id = 2
sql = f"""
    SELECT project_id, costcenter FROM project_costcenter
    WHERE 
    project_id ='{project_id}';
"""
execute_sql(sql)


project_id = None
sql = f"""
    DELETE FROM project_costcenter
    WHERE 
    project_id ='{project_id}';
"""
execute_sql(sql)




# sql = f"""
#     CREATE Table active_project_person_costcenter
#     (
#         appc_id SERIAL UNIQUE PRIMARY KEY,
#         project_id int REFERENCES project (project_id) ON UPDATE CASCADE ON DELETE CASCADE,
#         team_id int REFERENCES team_members (team_id) ON UPDATE CASCADE ON DELETE CASCADE,
#         costcenter VARCHAR(100) NOT NULL,
#         UNIQUE (project_id, team_id)
#     );
# """

project_id = 1
teammember = "Heiko Kulinna"
costcenter = "DE95123456"


sql = f"""
    INSERT INTO active_project_person_costcenter (project_id, team_id, costcenter) VALUES
    (
        (SELECT project_id FROM project WHERE project_id = '{project_id}'),
        (SELECT team_id FROM team_members WHERE full_name = '{teammember}')
        '{costcenter}',
    );
"""
data = execute_sql(sql)













