


# https://www.postgresqltutorial.com/postgresql-python/connect/


# http://localhost:5555/browser/
# User: Heikokulinna@gmx.de
# PW: admin


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


# no
# sql1 = """
#         CREATE TABLE team_members (
#             team_id SERIAL PRIMARY KEY,
#             sur_name VARCHAR(255) NOT NULL,
#             pre_name VARCHAR(255) NOT NULL,
#             full_name VARCHAR(255),
#             birthday_date DATE,
#             department_entry DATE,
#             status VARCHAR(20)
#     )
# """


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

# year integer


sql = f"""
    INSERT INTO entity_time (year, entity_id, coverage) VALUES 
    ('{dd_year}', (SELECT entity_id FROM entity WHERE entity_name = '{dd_entity}'),('{coverage_entity}'));
"""


sql = "DROP TABLE team_members"

data=execute_sql(sql = sql)
data



full_name = "Heiko Kulinna"
full_name = "Jenny Willig"

# quer everything
sql = f"""
    SELECT tm.pre_name, tm.sur_name, tm.full_name, tm.email, tm.user_id, e.entity_name, tm.department_entry_date
    FROM team_members tm
    INNER JOIN entity e
    ON tm.legal_entity_id = e.entity_id
"""

# select on query
sql = f"""
    SELECT tm.pre_name, tm.sur_name, tm.full_name, tm.email, tm.user_id, e.entity_name, tm.department_entry_date
    FROM team_members tm
    INNER JOIN entity e
    ON tm.legal_entity_id = e.entity_id
    WHERE tm.full_name = '{full_name}';
"""


data = execute_sql(sql)
data


data=pd.DataFrame(data, columns=["pre_name", "sur_name", "full_name", "email", "user_id", "leagal_entity", "entry_date"])

data

data = data[data["full_name"] == full_name]
data = data.reset_index(drop = True)
data



# look for entit year

dd_year = 2022
dd_entity = "BDS"
full_name = "Heiko Kulinna"

sql = """
    SELECT et.year, e.entity_name, et.coverage
    FROM entity_time et
    INNER JOIN entity e
    ON e.entity_id = et.entity_id;
"""


sql = f"""
        SELECT * from entity_time 
        WHERE
        year ='{dd_year}' AND entity_id in (SELECT entity_id FROM entity WHERE entity_name = '{dd_entity}');
"""

sql = f"""
    SELECT tm.full_name, e.entity_name, et.year, et.coverage
    FROM team_members tm
    INNER JOIN entity e
    ON tm.legal_entity_id = e.entity_id
    INNER JOIN entity_time et
    ON e.entity_id = et.entity_id
    WHERE ((tm.full_name = '{full_name}') AND (et.year = '{dd_year}'));
"""


data = execute_sql(sql)
data






