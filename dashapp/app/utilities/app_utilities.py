# https://www.postgresqltutorial.com/postgresql-python/connect/


# http://localhost:5555/browser/
# User: Heikokulinna@gmx.de
# PW: admin


import psycopg2



def get_option_list(a_list):
    cnames_data = a_list
    options_list = []
    for i in cnames_data:
        options_list.append({"label": i, "value": i})
    return options_list



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




