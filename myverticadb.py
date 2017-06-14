# Spencer
# My collection of Vertica database functions

import vertica_python
from vertica_python import errors as vp_errs

import os


def connectToDatabase(search_path, **conn_info):
    """
    Connect to Vertica database
    :param search_path: the search path that contains the schema name to connect to the database
    :param conn_info: database connection information
    :return: cursor object to database
    """

    connection = None
    try:
        connection = vertica_python.connect(**conn_info)
    except vp_errs.ConnectionError:
        print("Error connecting to Vertica database on: " + conn_info.get('host'))
    except Exception, e:
        print("Error connecting to Vertica: " + str(e))

    cur = None
    if connection:
        # "dict" option returns queries as a list of dictionaries
        cur = connection.cursor('dict')

        cur.execute("SET SEARCH_PATH TO " + search_path)

    return cur


def getDDLforDatabaseTables(search_path, cur, parent_folder):
    """
    Get and write out the DDL for each table
    :param search_path: the search path that contains the schema name to connect to the database
    :param cur: the cursor to use when executing SQL
    :param parent_folder: the parent folder to output the data csv files
    :return: None
    """

    table_names = []

    # get table list
    cur.execute("select distinct table_name from columns where table_schema = '" + search_path + "' order by table_name")

    rows = cur.fetchall()

    ddl_dir = getOutputFolder(parent_folder, "ddl")

    for item in rows:
        table_names.append(item['table_name'])

    for item in table_names:
        cur.execute("select export_objects('','" + item + "')")
        sqldump = cur.fetchall()
        table_ddl = sqldump[0]['export_objects']
        table_ddl = table_ddl.replace(search_path + ".", "")
        outfile = open(ddl_dir + "/" + item + ".ddl", "w")
        outfile.write(table_ddl)
        outfile.close

    return


def createCSVforDatabaseTables(cur, delimiter, parent_folder, read_tables):
    """
    Create CSV file for each database table that is queried/read from
    :param cur: the cursor to use when executing SQL
    :param delimiter: the column separator delimiter
    :param parent_folder: the parent folder to output the data csv files
    :param read_tables: the list of read table grouping
    :return: None
    """

    data_dir = getOutputFolder(parent_folder, "data")

    for item in read_tables:
        tables = item.get('tables')
        start_time = item.get('start-time')
        end_time = item.get('end-time')
        for table in tables:
            print("reading table: " + table)

            # time provided is UTC
            if start_time is not None:
                cur.execute("select * from " + table + " where cal_timestamp_time >= " + "'" + str(start_time) + "'" + " and cal_timestamp_time <= " + "'" + str(end_time) + "'")
            else:
                cur.execute("select * from " + table)

            sqlresult = cur.fetchall()

            if sqlresult:
                f = open(data_dir + "/" + table+".csv", "w")

                # get first row to extract the column headers once
                row = sqlresult[0]

                # create string of delimiter separated column headers
                header = delimiter.join(row)
                #    print header
                f.write(header + "\n")

                for row in sqlresult:
                    # create string of comma separate values for a row of data
                    values = delimiter.join(["%s" % (v) for k, v in row.items()])
                    # search and replace None entries with empty string
                    values = values.replace("None","")
                    f.write(values + "\n")
                    # print values

                f.close()
            else:
                print("no data returned for: " + table)

    return


def writeCSVtoDatabaseTables(cur, delimiter, parent_folder, write_tables):
    """
    Write csv files containing rows of data into the database tables
    :param cur: the cursor to use when executing SQL
    :param delimiter: the column separator delimiter
    :param write_tables: the list of write table grouping
    :return: None
    """

#TODO: cleanup
#    currentdir = os.getcwd()
#    data_dir = currentdir + "/data"
    data_dir = getOutputFolder(parent_folder, "data")

    for item in write_tables:
        tables = item.get('tables')
        for table in tables:
            print("writing table: " + table)

            f = None
            filename = data_dir + "/" + table+".csv"
            try:
                f = open(filename, "r")
            except IOError:
                print("Error: cannot open " + filename)

            if f:
                # do not include the headers in the csv we pass to insert into db table
                #headers = f.readline()
                # it turns out passing the headers works fine, so we can include them

                rows_list = []
                for row in f:
                    rows_list.append(row)

                f.close()

                # convert list of rows into a single string
                rows = ''.join(rows_list)

                cur.copy("COPY " + table + " from stdin DELIMITER " + "'" + delimiter + "'", rows)

    return


def deleteDataFromDatabaseTables(cur, delete_tables):
    """
    Delete data from the given list of database tables

    :param cur: the cursor to use when executing SQL
    :param delete_tables:
    :return: None
    """
    for item in delete_tables:
        tables = item.get('tables')
        for table in tables:
            print("deleting data from table: " + table)
            cur.execute("delete from " + table)

    cur.execute("commit")
    return


def getOutputFolder(parent_folder, child_folder):
    """
    Create output folder if not already created from a combination of given parent and child folders
    :param parent_folder: parent folder
    :param child_folder: child folder
    :return: output folder path string
    """
    if parent_folder == ".":
        parent_folder = os.getcwd()
    output_folder = parent_folder + "/" + child_folder

    try:
        os.mkdir(parent_folder)
    except:
        pass

    try:
        os.mkdir(output_folder)
    except:
        pass

    return output_folder