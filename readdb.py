# Spencer
# Python program to read data from Vertica database tables and write to CSV files

import os
import sys
import myverticadb
import myyaml


def main():
    if (len(sys.argv) == 2):
        yamlInputFile = sys.argv[1]
    else:
        yamlInputFile = "read.yaml"

    if not os.path.exists(yamlInputFile):
        print("Error: yaml input file not found: " + yamlInputFile)
        quit()

    myyaml.readYamlFile(yamlInputFile)
    conn_info = myyaml.search('connection-read')
    if conn_info is None:
        print("Error: No connection-read defined in " + yamlInputFile)
        quit()

    # schema_read contains the schema to use when accessing the Vertica database
    schema_read = myyaml.search('schema-read')
    if (schema_read is None):
        print("Error: No schema-read defined in " + yamlInputFile)
        quit()

    cur = myverticadb.connectToDatabase(schema_read, **conn_info)
    if cur:
        parent_folder = myyaml.search('parent-data-folder')
        if parent_folder is None:
            parent_folder = "."

        write_database_ddl = myyaml.search('write-database-ddl')
        if write_database_ddl:
            myverticadb.getDDLforDatabaseTables(schema_read, cur, parent_folder)

        delimiter = myyaml.search('delimiter')
        if delimiter is None:
            delimiter = ","

        read_tables = myyaml.searchMultiple('tables-to-read')
        if read_tables:
            myverticadb.createCSVforDatabaseTables(cur, delimiter, parent_folder, read_tables)
        else:
            print("No tables-to-read defined")


if __name__=="__main__":
    main()