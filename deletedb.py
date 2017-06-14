# Spencer
# Python program to delete data from the list of Vertica database tables

import os
import sys
import myverticadb
import myyaml

def main():
    if (len(sys.argv) == 2):
        yamlDeleteFile = sys.argv[1]
    else:
        yamlDeleteFile = "delete.yaml"

    if not os.path.exists(yamlDeleteFile):
        print("Error: yaml output file not found: " + yamlDeleteFile)
        quit()

    myyaml.readYamlFile(yamlDeleteFile)
    conn_info = myyaml.search('connection-delete')
    if conn_info is None:
        print("Error: No connection-delete defined in " + yamlDeleteFile)
        quit()

    # schema_delete contains the schema to use when accessing the Vertica database
    schema_delete = myyaml.search('schema-delete')
    if (schema_delete is None):
        print("Error: No schema-delete defined in " + yamlDeleteFile)
        quit()

    prompt_connection = raw_input("Do you want to delete data from the Vertica database on: " + conn_info.get("host") + " and schema: " + schema_delete + " ? ")
    if prompt_connection == "y" or prompt_connection == "Y":
        cur = myverticadb.connectToDatabase(schema_delete, **conn_info)
        if cur:
            delete_tables = myyaml.searchMultiple('tables-to-delete')
            if delete_tables:
                print("Do you want to delete data from these tables:")
                prompt_delete_tables = raw_input(str(delete_tables) + " ? ")
                if prompt_delete_tables == "y" or prompt_delete_tables == "Y":
                    myverticadb.deleteDataFromDatabaseTables(cur, delete_tables)
            else:
                print("No tables-to-delete defined")


if __name__=="__main__":
    main()