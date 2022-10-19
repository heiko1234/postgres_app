# https://www.postgresqltutorial.com/postgresql-python/connect/


# http://localhost:5555/browser/
# User: Heikokulinna@gmx.de
# PW: admin

import os
import psycopg2


from dotenv import load_dotenv

load_dotenv()

local_run = os.getenv("LOCAL_RUN")
local_run


def get_option_list(a_list):
    cnames_data = a_list
    options_list = []
    for i in cnames_data:
        options_list.append({"label": i, "value": i})
    return options_list



def execute_sql(sql):
    load_dotenv()

    local_run = os.getenv("LOCAL_RUN", False)
    if local_run:
    #establishing the connection
        conn = psycopg2.connect(
            database="teams",
            user='postgres',
            password='postgres',
            host='127.30.0.1',
            port= '5432'
        )
    else:
        conn = psycopg2.connect(
            database="teams",
            user='postgres',
            password='postgres',
            host='0.0.0.0',
            port= '5432'
        )
        # conn = psycopg2.connect(
        #     database=os.getenv("POSTGRES_DATABASE"),
        #     user=os.getenv("POSTGRES_USER"),
        #     password=os.getenv("POSTGRES_PASSWORD"),
        #     host=os.getenv("POSTGRES_HOST"),
        #     port=os.getenv("POSTGRES_PORT")
        # )
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




