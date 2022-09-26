


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


# sql = "DROP DATABASE team"
#sql = "CREATE DATABASE team"


sql = """CREATE TABLE entity (
        entity_id SERIAL PRIMARY KEY,
        entity_name VARCHAR(255) NOT NULL,
        UNIQUE(entity_name)
    )
    """
execute_sql(sql)


sql = """
    CREATE Table entity_time 
    (
        entity_time_id SERIAL UNIQUE PRIMARY KEY,
        year integer NOT NULL,
        entity_id BIGINT NOT NULL, 
        coverage integer NOT NULL
    );
"""
execute_sql(sql)


#Name, Surname, Full Name, UserID, Email, LEgal Entity, Contract Year, Contract, Budget required, Activity

sql = """
    CREATE TABLE team_members (
            team_id SERIAL PRIMARY KEY,
            pre_name VARCHAR(100) NOT NULL,
            sur_name VARCHAR(150) NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            UNIQUE(full_name),
            email text,
            user_id text NOT NULL,
            legal_entity_id BIGINT,
            department_entry_date DATE,
            status VARCHAR(20)
    )
"""
execute_sql(sql)


sql = """
        CREATE TABLE ods (
            od_id SERIAL PRIMARY KEY,
            od_name VARCHAR(10) NOT NULL,
            UNIQUE(od_name)
        )
"""
execute_sql(sql)


# sql = """
#         CREATE TABLE projects (
#             project_id SERIAL PRIMARY KEY,
#             project_od INTEGER NOT NULL,
#             FOREIGN KEY (project_od)
#                 REFERENCES ods (od_id)
#                 ON UPDATE CASCADE ON DELETE CASCADE,
#             project_desc TEXT
#         )
# """
# execute_sql(sql)


sql = """
        CREATE TABLE team_info (
            team_info_id SERIAL PRIMARY KEY,
            team_id INTEGER NOT NULL,
            FOREIGN KEY (team_id)
                REFERENCES team_members (team_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            year INTEGER NOT NULL,
            contract INTEGER NOT NULL,
            working_month INTEGER NOT NULL,
            entity_id BIGINT NOT NULL, 
            FOREIGN KEY (entity_id)
                REFERENCES entity (entity_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            activity VARCHAR(255),
            UNIQUE (year, team_id)
        )
"""
execute_sql(sql)


# sql = "DROP TABLE team_info"
# execute_sql(sql)


sql = """
        CREATE TABLE founding_sources (
            founding_source_id SERIAL PRIMARY KEY,
            founding_source VARCHAR(255) NOT NULL,
            UNIQUE(founding_source)
        )
"""
execute_sql(sql)


sql = """
        CREATE TABLE topic_class (
            topic_class_id SERIAL PRIMARY KEY,
            topic_class VARCHAR(255) NOT NULL,
            UNIQUE(topic_class)
        )
"""
execute_sql(sql)


# sql = "DROP TABLE founding_sources"
# sql = "DROP TABLE topic_class"
# execute_sql(sql)





#establishing the connection
conn = psycopg2.connect(
    database="teams", user='postgres', password='postgres', host='127.30.0.1', port= '5432'
)

conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()



sql_statement = "INSERT INTO founding_sources(founding_source) VALUES(%s)"

values_list=[
    ("KDC",),
    ("KTC",),
    ("EV",),
    ("ED",),
    ("PM",)
    ]

cursor.executemany(sql_statement, values_list)


# sql= "SELECT founding_source FROM founding_sources"
# execute_sql(sql)

# sql= "SELECT founding_source_id FROM founding_sources"
# execute_sql(sql)

# value = "ED"
# sql = f"SELECT founding_source_id FROM founding_sources WHERE founding_source = '{value}';"
# execute_sql(sql)[0][0]


# sql= "SELECT * FROM founding_sources"
# execute_sql(sql)




sql_statement = "INSERT INTO topic_class(topic_class) VALUES(%s)"

values_list=[
    ("Data Connection",),
    ("Underst. Hist. Data",),
    ("Root Cause Analysis",),
    ("Anomalie Detection",),
    ("Softsensor",),
    ("What-If Support",),
    ("Closed-Loop RTO",)
    ]

cursor.executemany(sql_statement, values_list)

# end everyting
cursor.close()
conn.close()

# sql= "SELECT topic_class FROM topic_class"
# execute_sql(sql)

# sql= "SELECT * FROM topic_class"
# execute_sql(sql)



# ####

sql = """
        CREATE TABLE project (
            project_id SERIAL PRIMARY KEY,
            funding_id BIGINT NOT NULL,
            FOREIGN KEY (funding_id)
                REFERENCES founding_sources (founding_source_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            topic VARCHAR(255) NOT NULL,
            topic_class_id BIGINT NOT NULL,
            FOREIGN KEY (topic_class_id)
                REFERENCES topic_class (topic_class_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            argus_enabled VARCHAR(5) NOT NULL,
            way_charging VARCHAR(10) NOT NULL,
            recieving_account VARCHAR(50),
            cost_center_respon VARCHAR(255),
            start_date DATE,
            end_date DATE,
            difficulty integer,
            project_status VARCHAR(50),
            project_description TEXT,
            project_goals TEXT
        )
"""

#             project_od INTEGER NOT NULL,
#             FOREIGN KEY (project_od)
#                 REFERENCES ods (od_id)
#                 ON UPDATE CASCADE ON DELETE CASCADE,


# sql = "DROP TABLE project"
# execute_sql(sql)

execute_sql(sql)



sql = f"""CREATE TABLE project_team_members (
    project_id int REFERENCES project (project_id) ON UPDATE CASCADE ON DELETE CASCADE,
    team_id int REFERENCES team_members (team_id) ON UPDATE CASCADE ON DELETE CASCADE,
    UNIQUE (project_id, team_id)
    );
"""
execute_sql(sql)

# sql = "DROP TABLE project_team_members"
# execute_sql(sql)



sql = f"""
    CREATE TABLE project_deadlines (
        project_deadlines_id SERIAL PRIMARY KEY,
        project_id int REFERENCES project (project_id) ON UPDATE CASCADE ON DELETE CASCADE,
        deadline_date DATE,
        deadline_text VARCHAR(255),
        UNIQUE (deadline_date, deadline_text)
    );
"""
execute_sql(sql)



# sql = "DROP TABLE project_deadlines"
# execute_sql(sql)


# sql = "DROP TABLE project_budget_planning"
# execute_sql(sql)


sql = """
    CREATE Table project_budget_planning 
    (
        pbp_id SERIAL UNIQUE PRIMARY KEY,
        year integer NOT NULL,
        project_id integer NOT NULL,
        FOREIGN KEY (project_id) 
            REFERENCES project (project_id) 
            ON UPDATE CASCADE ON DELETE CASCADE,
        budget integer NOT NULL,
        UNIQUE (year, project_id)
    );
"""
execute_sql(sql)



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
execute_sql(sql)

# sql = "DROP TABLE project_time_budget"
# execute_sql(sql)



sql = """
    CREATE Table team_year_project_budget 
    (
        ttpb_id SERIAL UNIQUE PRIMARY KEY,
        year integer NOT NULL,
        team_id INTEGER NOT NULL,
        FOREIGN KEY (team_id)
            REFERENCES team_members (team_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        project_id INTEGER NOT NULL,
        FOREIGN KEY (project_id)
            REFERENCES project (project_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        project_yearly_budget INTEGER NOT NULL,
        UNIQUE (year, team_id, project_id)
    );
"""
execute_sql(sql)

# sql = "DROP TABLE team_year_project_budget"
# execute_sql(sql)
