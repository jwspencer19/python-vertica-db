# Spencer
# Python program to read data from Vertica database tables and write to CSV files

import vertica_python
from vertica_python import errors as vperrs

import os
import string


def main():
    # connection info for Vertica database
    conn_info = {'host': 'put-host-ip-here',
                 'port': 5433,
                 'user': 'db-user-here',
                 'password': 'password-here',
                 'database': 'database-here',
                 # 10 minutes timeout on queries
                 'read_timeout': 600,
                 # default throw error on invalid UTF-8 results
                 'unicode_error': 'strict',
                 # SSL is disabled by default
                 'ssl': False}

    # search_path contains the schema to use when accessing the Vertica database
    search_path = "search-path-here"

    cur = connectToDatabase(search_path, **conn_info)

#    getDDLforDatabaseTables(search_path, cur)

    createCSVforDatabaseTables(search_path, cur)


def connectToDatabase(search_path, **conn_info):
    """
    Connect to Vertica database
    :param search_path: the search path that contains the schema name to connect to the database
    :param conn_info: database connection information
    :return: cursor object to database
    """

    connection = vertica_python.connect(**conn_info)

    # "dict" option returns querys as a list of dictionaries
    cur = connection.cursor('dict')

    cur.execute("SET SEARCH_PATH TO " + search_path)

    return cur


def getDDLforDatabaseTables(search_path, cur):
    """
    Get and write out the DDL for each table

    :param search_path: the search path that contains the schema name to connect to the database
    :param cur: the cursor to use when executing SQL
    :return: none
    """

    table_names = []

    # get table list
    cur.execute("select distinct table_name from columns where table_schema = '" + search_path + "' order by table_name")

    rows = cur.fetchall()

    currentdir = os.getcwd()
    ddl_dir = currentdir + "/ddl"

    try:
        os.mkdir(ddl_dir)
    except:
        pass

    for item in rows:
        table_names.append(item['table_name'])

    for item in table_names:
        cur.execute("select export_objects('','" + item + "')")
        sqldump = cur.fetchall()
        table_ddl = sqldump[0]['export_objects']
        table_ddl = table_ddl.replace(search_path + ".", "")
        outfile = open(ddl_dir + "/" + item + ".ddl", "wb")
        outfile.write(table_ddl)
        outfile.close

    return


def createCSVforDatabaseTables(search_path, cur):

    cur.execute("select * from f_ksi")
    sqlresult = cur.fetchall()

    f = open("table-name.csv", "w+")

    # get first row to extract the column headers once
    row = sqlresult[0]

#    for k, v in row.items():
#        print(k, v)

#    for k in row:
#        print(k)

    # create string of comma separate column headers
    header = ",".join(row)
#    print header
    f.write(header + "\n")

    for row in sqlresult:
        # create string of comma separate values for a row of data
        values = ",".join(["%s" % (v) for k, v in row.items()])
        f.write(values + "\n")
#        print values

    f.close()

    return


if __name__=="__main__":
    main()
