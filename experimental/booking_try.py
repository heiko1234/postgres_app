


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





overview_teammember = "Heiko Kulinna"
overview_year =2022







sql=f"""
    SELECT p.project_id, p.topic, tc.topic_class, fs.founding_source, p.project_description
    FROM project p
    INNER JOIN founding_sources fs
    ON p.funding_id = fs.founding_source_id
    INNER JOIN topic_class tc
    ON p.topic_class_id = tc.topic_class_id
    INNER JOIN project_team_members ptm
    ON p.project_id = ptm.project_id
    INNER JOIN team_members tm
    ON tm.team_id = ptm.team_id
    INNER JOIN project_budget_planning pbp
    ON pbp.project_id = p.project_id
    WHERE pbp.year = '{overview_year}'
    AND
    tm.team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
"""
data=execute_sql(sql)
data = pd.DataFrame(data, columns=["project_id", "topic", "topic_class", "founding_source", "project_descrition"])

list_ids = list(set(data["project_id"]))

# project_ids where projects exist
list_ids




sql = f"""
    SELECT project_id, month, working_hours FROM project_time_budget
    WHERE team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
    AND year = '{overview_year}';
"""

data=execute_sql(sql = sql)
data


data = pd.DataFrame(data, columns=["project_id", "month", "working_days"])
data


try:
    list_ids_available = list(set(data["project_id"]))
except BaseException:
    list_ids_available = []


ids = [element for element in list_ids if element not in list_ids_available]
ids


data=data.pivot(index="project_id", columns="month", values="working_days")
data
data = data.reset_index(drop = False)
data = data.reset_index(drop = True)
pda = data
pda


# pda = pda.iloc[0, :]
# pda

# pda=pda.pivot(index="project_id", columns="month", values="working_days")
# pda = pda.reset_index(drop = False)
# pda = pda.reset_index(drop = True)
# pda
# # data

# ids = [2]

months = [1,2,3,4,5,6,7,8,9,10,11,12]
all_zero = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

data = pd.DataFrame()

if len(data) == 0:
    for id in ids:
        new_data = pd.DataFrame()
        new_data["month"] = months
        new_data["working_days"] = all_zero
        new_data["project_id"] = id
        data = pd.concat([data, new_data], axis=0)

data
if len(data) != 0:
    data=data.pivot(index="project_id", columns="month", values="working_days")
    data
    data = data.reset_index(drop = False)
    data = data.reset_index(drop = True)
    pdata = data
    pdata
else:
    pdata = None

pda
pdata


new_df = pd.concat([pda, pdata], axis=0)
new_df = new_df.reset_index(drop = True)
new_df





sql = f"""
    DELETE from project_time_budget
    WHERE
    team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
    AND
    year = '{overview_year}';
"""
data=execute_sql(sql = sql)
data


# new_df = pdata
# new_df


months = [1,2,3,4,5,6,7,8,9,10,11,12]

for project_id in list(new_df["project_id"]):
    print(project_id)
    selected_data = new_df.loc[new_df["project_id"]==project_id]
    selected_data = selected_data.reset_index(drop = True)
    working_days = list(selected_data.loc[0, [1,2,3,4,5,6,7,8,9,10,11,12]])

    for i in list(range(len(months))):

        sql = f"""
            INSERT INTO project_time_budget (year, month, working_hours, team_id, project_id) VALUES
            (
                '{overview_year}',
                '{months[i]}',
                '{working_days[i]}',
                (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}'),
                '{project_id}'
            );
        """
        output=execute_sql(sql = sql)
        output




# 
# 


sql = f"""
    SELECT project_id, month, working_days FROM project_time_budget
    WHERE team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
    AND year = '{overview_year}';
"""

data=execute_sql(sql = sql)
data


data = pd.DataFrame(data, columns=["project_id", "month", "working_days"])
data


# data = data.pivot(index="project_id", columns="month", values="working_days")
# data

# data = data/20 * 170/12
# data = round(data,1)
# data



full_name = "Heiko Kulinna"
year = 2022


sql = f"""
    SELECT et.coverage, tm.full_name 
    FROM team_members tm
    INNER JOIN entity_time et
    ON et.entity_id = tm.legal_entity_id
    WHERE 
    tm.full_name = '{full_name}'
    AND
    et.year = '{year}'
"""
data=execute_sql(sql = sql)
data
data = pd.DataFrame(data, columns=["coverage", "fullname"])
data
data["coverage"][0]




overview_teammember = "Heiko Kulinna"
overview_year = 2022

sql = f"""
    SELECT ptb.project_id, ptb.month, ptb.working_days, ROUND(ptb.working_days*et.coverage/240,2)
    FROM project_time_budget ptb
    INNER JOIN team_members tm
    ON tm.team_id = ptb.team_id
    INNER JOIN entity_time et
    ON et.entity_id = tm.legal_entity_id
    WHERE ptb.team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
    AND ptb.year = '{overview_year}';
"""
data=execute_sql(sql = sql)
data
data = pd.DataFrame(data, columns=["project_id", "month", "working_days", "working_bookings"])
data

data = data.pivot(index="project_id", columns="month", values="working_bookings")
data
list(data.index)



# caclulate booking from working days
# caclulate booking from working days
sql = f"""
    SELECT ptb.project_id, ptb.team_id, ptb.year, ptb.month, ptb.working_days, ROUND(ptb.working_days*et.coverage/240,2)
    FROM project_time_budget ptb
    INNER JOIN team_members tm
    ON tm.team_id = ptb.team_id
    INNER JOIN entity_time et
    ON et.entity_id = tm.legal_entity_id
    WHERE ptb.team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
    AND ((ptb.year = '{overview_year}') AND (et.year = '{overview_year}'));
"""
data=execute_sql(sql = sql)
print("fetched data")
data = pd.DataFrame(data, columns=["project_id", "year", "month", "working_days", "working_bookings"])
data = data.pivot(index="project_id", columns="month", values="working_bookings")
print(data)








overview_teammember = "Heiko Kulinna"
overview_year =2022



for project_id in list(data.index):
    for month in list(data.columns):
        money = data.loc[project_id, month]
        sql = f"""
            UPDATE project_time_budget
            SET 
            working_booking = '{money}'
            WHERE 
            project_id = '{project_id}' 
            AND year = '{overview_year}'
            AND month = '{month}'
            AND team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}');
        """
        execute_sql(sql)






overview_teammember = "Ralf Kulinna"
overview_year =2022


sql = f"""
    SELECT project_id, month, working_days, working_booking FROM project_time_budget
    WHERE team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
    AND year = '{overview_year}';
"""

data=execute_sql(sql = sql)
data
data = pd.DataFrame(data, columns=["project_id", "month", "working_days", "working_booking"])
data


data = data.pivot(index="project_id", columns="month", values="working_booking")
data









overview_teammember = "Ralf Kulinna"
overview_year =2022



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


list_sum = ["sum"]+list(round(data[data.columns[1:]].sum(axis=0, numeric_only=True), 2))
inter_data = pd.DataFrame([list_sum], columns = data.columns)
data=pd.concat([data, inter_data], axis=0)

data["Sum"] = round(data[data.columns[1:]].sum(axis=1, numeric_only=True),2)

data = data.reset_index(drop = True)

data




sql = f"""
    SELECT typb.project_id, typb.project_yearly_budget
    FROM team_year_project_budget typb
    INNER JOIN team_members tm
    ON typb.team_id = tm.team_id
    WHERE typb.team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
    AND
    typb.year = '{overview_year}'
"""
fdata=execute_sql(sql)
fdata


fdata = pd.DataFrame(fdata, columns=["project_id", "assigned budget"])
fdata




data
fdata

data

pd.concat([data, fdata], axis=1, )



mdata=pd.merge(left=data, right=fdata, left_on="project_id", right_on="project_id")
mdata


list_sum = ["sum"]+list(round(mdata[mdata.columns[1:]].sum(axis=0, numeric_only=True), 2))
inter_mdata = pd.DataFrame([list_sum], columns = mdata.columns)
mdata=pd.concat([mdata, inter_mdata], axis=0)
mdata



# make bar plot

from dashapp.app.utilities.plot import (
    budget_paretoplot
)


mdata
mdata.columns[1:-2]

cnames = mdata.columns[1:-2]
cnames
scnames = [str(element) for element in cnames]
scnames

fig = budget_paretoplot(list_of_names=cnames, 
    list_of_values = mdata.loc[1,cnames], 
    sum_value=mdata.loc[1,"assigned budget"], 
    yname="Budget", 
    xname="Month", 
    title="Budget plan", 
    plot=True)







fullname = "Ralf Kulinna"
year = 2022


sql = f"""
    SELECT tm.full_name, ti.year, ti.contract, ti.working_month, ti.activity, et.coverage
    FROM team_members tm
    INNER JOIN team_info ti
    ON tm.team_id = ti.team_id
    INNER JOIN entity_time et
    ON et.entity_id = tm.legal_entity_id and ti.year = et.year
    WHERE tm.full_name = '{fullname}'
    AND
    ti.year = '{year}'
"""
data = execute_sql(sql)
data

# WHERE typb.team_id in (SELECT team_id FROM team_members WHERE full_name = '{overview_teammember}')
# AND
# typb.year = '{overview_year}'


df = pd.DataFrame(data, columns=["Fullname", "Year", "Contract", "Working Month", "Activity", "Coverage"])


df["eff. Coverage"] = round(df["Contract"] * df["Working Month"] * df["Coverage"] * 1/100 * 1/12, 1)
df

df["eff. Coverage"][0]








raw_data = [{'1': 10, '2': 0, '3': 0, '4': 0, '5': 15, '6': 10, '7': 5, '8': 15, '9': 0, '10': 0, '11': 0, '12': 0, 'project_id': 1}, {'1': 10, '2': 0, '3': 0, '4': 0, '5': 5, '6': 10, '7': 15, '8': 5, '9': 0, '10': 0, '11': 0, '12': 0, 'project_id': 2}]


raw_data = [{'1': 8.33, '2': 7.5, '3': 6.67, '4': 5.83, '5': 5, '6': 0, '7': 8.33, '8': 5, '9': 0, '10': 0, '11': 0, '12': 0, 'project_id': 1, 'Sum': 46.66, 'assigned budget': 50}, {'1': 8.33, '2': 7.5, '3': 6.67, '4': 5.83, '5': 5, '6': 0, '7': 8.33, '8': 5, '9': 0, '10': 0, '11': 0, '12': 0, 'project_id': 'sum', 'Sum': 46.66, 'assigned budget': 50}]


data = pd.DataFrame(data=raw_data)
data


cnames = ["project_id",  "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "Sum", "assigned budget"]


mdata = pd.DataFrame(data = raw_data)
mdata


mdata.loc[:,cnames]






