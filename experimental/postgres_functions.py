


# https://www.postgresqltutorial.com/postgresql-python/connect/


# http://localhost:5555/browser/
# User: Heikokulinna@gmx.de
# PW: admin


import psycopg2



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


sql = "DROP TABLE entity"


data=execute_sql(sql = sql)
data


import pandas as pd



data=pd.DataFrame(data, columns=["OD"])

data=pd.DataFrame(data, columns=["index","OD"])

data

list(data["OD"])


execute_sql("SELECT * FROM entity")

