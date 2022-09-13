


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





sql = """CREATE TABLE entity (
        entity_id SERIAL PRIMARY KEY,
        entity_name VARCHAR(255) NOT NULL,
        UNIQUE(entity_name)
    )
    """


sql = """
    CREATE Table entity_time 
    (
        entity_time_id SERIAL UNIQUE PRIMARY KEY,
        year integer NOT NULL,
        entity_id BIGINT NOT NULL, 
        coverage integer NOT NULL
    );
"""



#Name, Surname, Full Name, UserID, Email, LEgal Entity, Contract Year, Contract, Budget required, Activity

sql = """
    CREATE TABLE team_members (
            team_id SERIAL PRIMARY KEY,
            pre_name VARCHAR(100) NOT NULL,
            sur_name VARCHAR(150) NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            email text,
            user_id text NOT NULL,
            legal_entity_id BIGINT,
            department_entry_date DATE,
            status VARCHAR(20)
    )
"""

sql = """
        CREATE TABLE ods (
            od_id SERIAL PRIMARY KEY,
            od_name VARCHAR(10) NOT NULL
        )
"""


sql = """
        CREATE TABLE projects (
            project_id SERIAL PRIMARY KEY,
            project_od INTEGER NOT NULL,
            FOREIGN KEY (project_od)
                REFERENCES ods (od_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            project_desc TEXT
        )
"""


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
            activity VARCHAR(255)
        )
"""

# sql = "DROP TABLE team_info"



sql = """
        CREATE TABLE founding_sources (
            founding_source_id SERIAL PRIMARY KEY,
            founding_source VARCHAR(255) NOT NULL,
            UNIQUE(founding_source)
        )
"""

sql = """
        CREATE TABLE topic_class (
            topic_class_id SERIAL PRIMARY KEY,
            topic_class VARCHAR(255) NOT NULL,
            UNIQUE(topic_class)
        )
"""

sql = "DROP TABLE founding_sources"
sql = "DROP TABLE topic_class"

execute_sql(sql)





#establishing the connection
conn = psycopg2.connect(
    database="team", user='postgres', password='postgres', host='127.30.0.1', port= '5432'
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


sql= "SELECT founding_source FROM founding_sources"
execute_sql(sql)

sql= "SELECT founding_source_id FROM founding_sources"
execute_sql(sql)

value = "ED"
sql = f"SELECT founding_source_id FROM founding_sources WHERE founding_source = '{value}';"
execute_sql(sql)[0][0]


sql= "SELECT * FROM founding_sources"
execute_sql(sql)




sql_statement = "INSERT INTO topic_class(topic_class) VALUES(%s)"

values_list=[
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

sql= "SELECT topic_class FROM topic_class"
execute_sql(sql)

sql= "SELECT * FROM topic_class"
execute_sql(sql)



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

execute_sql(sql)







