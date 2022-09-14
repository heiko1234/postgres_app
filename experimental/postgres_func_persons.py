


# https://www.postgresqltutorial.com/postgresql-python/connect/


# http://localhost:5555/browser/
# User: Heikokulinna@gmx.de
# PW: admin


import pandas as pd
import psycopg2

from dashapp.app.pages.construct import entity_dropdown


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

dd_year = 2022
dd_entrity = "BDS"
coverage_entity = 250


sql = f"""
    INSERT INTO entity_time (year, entity_id, coverage) VALUES 
    ('{dd_year}', (SELECT entity_id FROM entity WHERE entity_name = '{dd_entrity}'),('{coverage_entity}'));
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


# full table für alle leute, tabelle
sql = f"""
    SELECT tm.full_name, e.entity_name, et.year, et.coverage
    FROM team_members tm
    INNER JOIN entity e
    ON tm.legal_entity_id = e.entity_id
    INNER JOIN entity_time et
    ON e.entity_id = et.entity_id
    """

data = execute_sql(sql)
data

df = pd.DataFrame(data, columns=["Fullname", "Entity", "Year", "Coverage"])

pdf = df.pivot(index="Fullname", columns="Year", values="Coverage")
pdf






#####

# How to insert in team_info

dd_year = 2022
dd_entrity = "BDS"
coverage_entity = 250


sql = f"""
    INSERT INTO entity_time (year, entity_id, coverage) VALUES 
    ('{dd_year}', (SELECT entity_id FROM entity WHERE entity_name = '{dd_entrity}'),('{coverage_entity}'));
"""

# CREATE TABLE team_info (
#     team_info_id SERIAL PRIMARY KEY,
#     team_id INTEGER NOT NULL,
#     FOREIGN KEY (team_id)
#         REFERENCES team_members (team_id)
#         ON UPDATE CASCADE ON DELETE CASCADE,
#     year INTEGER NOT NULL,
#     contract INTEGER NOT NULL,
#     working_month INTEGER NOT NULL,
#     entity_id BIGINT NOT NULL, 
#     FOREIGN KEY (entity_id)
#         REFERENCES entity (entity_id)
#         ON UPDATE CASCADE ON DELETE CASCADE

dd_year = 2025
dd_entrity = "BDS"
# coverage_entity = 230
fullname = "Heiko Kulinna"
contract = 80
working_month = 8


sql = f"""
    INSERT INTO team_info (team_id, year, contract, working_month, entity_id) VALUES 
    (
        (SELECT team_id FROM team_members WHERE full_name = '{fullname}'),
        '{dd_year}',
        '{contract}',
        '{working_month}',
        (SELECT entity_id FROM entity WHERE entity_name = '{dd_entrity}')
    );
"""

data = execute_sql(sql)
data



# full table für alle leute, tabelle
sql = f"""
    SELECT tm.full_name, ti.year, ti.contract, ti.working_month, et.coverage
    FROM team_members tm
    INNER JOIN team_info ti
    ON tm.team_id = ti.team_id
    INNER JOIN entity e
    ON tm.legal_entity_id = e.entity_id
    INNER JOIN entity_time et
    ON e.entity_id = et.entity_id
    """



data = execute_sql(sql)
data

df = pd.DataFrame(data, columns=["Fullname", "Year", "Contract", "Working Month", "Coverage"])
df

df["eff. Coverage"] = round(df["Contract"] * df["Working Month"] * df["Coverage"] * 1/100 * 1/12,1)

df

df.pivot(index = "Fullname", columns="Year", values="eff. Coverage").reset_index(drop=False)



fullname = "Heiko Kulinna"
dd_year = 2024


# delete combined
sql = f"""
        DELETE from team_info 
        WHERE
        team_id in (SELECT team_id FROM team_members WHERE full_name = '{fullname}')
        AND
        team_info.year = '{dd_year}';
"""


data = execute_sql(sql)
data




sql = """
    SELECT * FROM team_info
    """

data = execute_sql(sql)
data



year=2025
contract=100
working_month=12
fullname="Heiko Kulinna"
activity=None

sql = f"""
    INSERT INTO team_info (team_id, year, contract, working_month, entity_id, activity) VALUES 
    (
        (SELECT team_id FROM team_members WHERE full_name = '{fullname}'),
        '{year}',
        '{contract}',
        '{working_month}',
        (SELECT legal_entity_id FROM team_members WHERE full_name = '{fullname}'),
        '{activity}'
    );
"""
data=execute_sql(sql = sql)
data



sql = f"""
    SELECT tm.full_name, ti.year, ti.contract, ti.working_month, ti.activity, e.entity_id
    FROM team_members tm
    INNER JOIN team_info ti
    ON tm.team_id = ti.team_id
    INNER JOIN entity e
    ON tm.legal_entity_id = e.entity_id
    """
data = execute_sql(sql)
data


sql = f"""
    SELECT tm.full_name, ti.year, ti.contract, ti.working_month, ti.activity, et.coverage, et.entity_id
    FROM team_members tm
    INNER JOIN team_info ti
    ON tm.team_id = ti.team_id
    INNER JOIN entity_time et
    ON tm.legal_entity_id = et.entity_id
    """
data = execute_sql(sql)
data



data = execute_sql(sql)
data
data = pd.DataFrame(data, columns = ["fullname", "year", "contract", "workingmonth", "activity", "coverage", "entity"])
data



sql = """
    SELECT * FROM entity_time
    """
data = execute_sql(sql)
data



sql = f"""
    SELECT tm.full_name, ti.year, ti.contract, ti.working_month, ti.activity, et.coverage
    FROM team_members tm
    INNER JOIN team_info ti
    ON tm.team_id = ti.team_id
    INNER JOIN entity e
    ON tm.legal_entity_id = e.entity_id
    INNER JOIN entity_time et
    ON e.entity_id = et.entity_id
"""
data = execute_sql(sql)


sql = f"""
    SELECT tm.full_name, ti.year, ti.contract, ti.working_month, ti.activity, et.coverage
    FROM team_info ti
    LEFT JOIN team_members tm
    ON tm.team_id = ti.team_id
    LEFT JOIN entity e
    ON tm.legal_entity_id = e.entity_id
    LEFT JOIN entity_time et
    ON e.entity_id = et.entity_id
"""
data = execute_sql(sql)
data


# team_info: -> team_id, year, entity_id
# team_members: -> legal_entity_id
# entity: entity -> entity_id
# entity_time: -> entity_id: year, coverage

sql = f"""
    SELECT tm.full_name, ti.year, ti.contract, ti.working_month, ti.activity, tm.legal_entity_id, et.coverage
    FROM team_members tm
    INNER JOIN team_info ti
    ON tm.team_id = ti.team_id
    INNER JOIN entity_time et
    ON et.entity_id = tm.legal_entity_id and ti.year = et.year
"""
data = execute_sql(sql)
data



#####
# UPDATE courses
# SET published_date = '2020-08-01' 
# WHERE course_id = 3;

# CREATE TABLE team_members (
#         team_id SERIAL PRIMARY KEY,
#         pre_name VARCHAR(100) NOT NULL,
#         sur_name VARCHAR(150) NOT NULL,
#         full_name VARCHAR(255) NOT NULL,
#         email text,
#         user_id text NOT NULL,
#         legal_entity_id BIGINT,
#         department_entry_date DATE,
#         status VARCHAR(20)


new_name = "HEiko"
new_surname = "Kulina"
new_fullname = new_name+" "+new_surname
new_email = "HikoKulinna@gmx.de"
new_user_id = "KulinnH"
# new_leagal_entity_id = 1
new_leagal_entity = "BASF SE"
new_entry_date = "2022-01-15"
dd_fullname = "Heiko Kulinna"

sql=f"""
        UPDATE team_members
        SET 
        pre_name = '{new_name}',
        sur_name = '{new_surname}',
        full_name = '{new_fullname}',
        email = '{new_email}',
        user_id = '{new_user_id}',
        legal_entity_id = (SELECT entity_id FROM entity WHERE entity_name = '{new_leagal_entity}'),
        department_entry_date = '{new_entry_date}'
        WHERE team_id in (SELECT team_id FROM team_members WHERE full_name = '{dd_fullname}');
"""

data = execute_sql(sql)
data


sql = """
    SELECT * FROM team_members
    """

data = execute_sql(sql)
data


