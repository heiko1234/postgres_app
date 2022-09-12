


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


execute_sql(sql)
