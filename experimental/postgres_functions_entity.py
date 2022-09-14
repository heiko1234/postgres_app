


# https://www.postgresqltutorial.com/postgresql-python/connect/


# http://localhost:5555/browser/
# User: Heikokulinna@gmx.de
# PW: admin


import psycopg2
import pandas as pd



# #establishing the connection
# conn = psycopg2.connect(
#     database="suppliers", user='postgres', password='postgres', host='127.30.0.1', port= '5432'
# )

# conn.autocommit = True

# #Creating a cursor object using the cursor() method
# cursor = conn.cursor()

# result = cursor.fetchall()
# result


# # end everyting
# cursor.close()
# conn.close()





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



sql = "SELECT * FROM entity"
execute_sql(sql)



sql = "SELECT * FROM entity_time"
data=execute_sql(sql)

data = pd.DataFrame(data, columns=["id", "year", "entity_id", "coverage"])
data


sql = "ALTER TABLE IF EXISTS public.entity ADD COLUMN entity_id serial NOT NULL;"


sql = """CREATE TABLE entity (
        entity_id SERIAL PRIMARY KEY,
        entity_name VARCHAR(255) NOT NULL,
        UNIQUE(entity_name)
    )
    """


sql = """
    INSERT INTO entity(entity_name) VALUES('EV')
    WHERE NOT IN (SELECT entity_name FROM entity)
"""


sql = """
    INSERT INTO entity(entity_name) VALUES('EV')
"""

sql = """
    INSERT INTO entity(entity_name) VALUES('EX')
"""

sql = """
    SELECT entity_name FROM entity
"""



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

sql = "DROP TABLE entity_time"


dd_year = 2022
dd_entity  ="BASF SES"
coverage_entity = 210


# INSERT INTO bar (description, foo_id) VALUES
#     ( 'testing',     (SELECT id from foo WHERE type='blue') ),
#     ( 'another row', (SELECT id from foo WHERE type='red' ) );


sql = f"""
    INSERT INTO entity_time (year, entity_id, coverage) VALUES 
    ('{dd_year}', (SELECT entity_id FROM entity WHERE entity_name = '{dd_entity}'),('{coverage_entity}'));
"""


sql = f"""SELECT entity_id FROM entity WHERE entity_name = '{dd_entity}';
"""



# selective deleting
dd_year = 2022
dd_entity  ="BASF LU"

sql = f"""SELECT entity_id FROM entity WHERE entity_name = '{dd_entity}';
"""


sql = f"""SELECT entity_id FROM entity_time WHERE year = '{dd_year}';
"""


sql = f"""SELECT entity_id FROM entity_time WHERE entity_id = '7';
"""

sql = """
        DELETE from entity_time 
        WHERE
        year ='{dd_year}' AND entity_id in (SELECT entity_id FROM entity WHERE entity_name = '{dd_entity}');
"""


#delete one
sql = f"""
        DELETE from entity_time 
        WHERE
        entity_id in (SELECT entity_id FROM entity WHERE entity_name = '{dd_entity}');
"""


# delete the next
sql = f"""
        DELETE from entity_time WHERE entity_time.year = '{dd_year}';
"""

# delete combined
sql = f"""
        DELETE from entity_time 
        WHERE
        entity_id in (SELECT entity_id FROM entity WHERE entity_name = '{dd_entity}')
        AND
        entity_time.year = '{dd_year}';
"""


data=execute_sql(sql = sql)
data




# where dublicate, overwrite

# insert into the_table (id, col2, col3, col4, col5)
# values ('ID100', 'b', 'c', 'd', 256)
# on conflict (id) do update
#    set col2 = excluded.col2,
#        col3 = excluded.col3, 
#        col4 = excluded.col4, 
#        col5 = excluded.col5;



sql = """
    SELECT et.year, e.entity_name, et.coverage
    FROM entity_time et
    INNER JOIN entity e
    ON e.entity_id = et.entity_id;
"""








sql = "SELECT * from entity"

sql = "SELECT * from entity_time"


sql = "DROP TABLE entity"


data=execute_sql(sql = sql)
data



import pandas as pd



data=pd.DataFrame(data, columns=["OD"])

data=pd.DataFrame(data, columns=["index","OD"])

data

list(data["OD"])


execute_sql("SELECT * FROM entity")

