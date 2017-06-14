# Spencer
# Python program to write data from CSV files into the Vertica database tables

import os
import sys
import myverticadb
import myyaml

def main():
    if (len(sys.argv) == 2):
        yamlOutputFile = sys.argv[1]
    else:
        yamlOutputFile = "write.yaml"

    if not os.path.exists(yamlOutputFile):
        print("Error: yaml output file not found: " + yamlOutputFile)
        quit()

    myyaml.readYamlFile(yamlOutputFile)
    conn_info = myyaml.search('connection-write')
    if conn_info is None:
        print("Error: No connection-write defined in " + yamlOutputFile)
        quit()

    # schema_write contains the schema to use when accessing the Vertica database
    schema_write = myyaml.search('schema-write')
    if (schema_write is None):
        print("Error: No schema-write defined in " + yamlOutputFile)
        quit()

    cur = myverticadb.connectToDatabase(schema_write, **conn_info)
    if cur:
        parent_folder = myyaml.search('parent-data-folder')
        if parent_folder is None:
            parent_folder = "."

        delimiter = myyaml.search('delimiter')
        if delimiter is None:
            delimiter = ","

        write_tables = myyaml.searchMultiple('tables-to-write')
        if write_tables:
            myverticadb.writeCSVtoDatabaseTables(cur, delimiter, parent_folder, write_tables)
        else:
            print("No tables-to-write defined")


if __name__=="__main__":
    main()