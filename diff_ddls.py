# Spencer
# Python program to provide diffs of two sets of DDLs.
# Note: DDLs can be created using ddl_for_diffs Python script that reads Vertica db schemas to create DDLs

import os
import sys


def main():

    if len(sys.argv) == 3:
        firstDDLfolder = sys.argv[1]
        secondDDLfolder = sys.argv[2]
    else:
        print("Usage: python " + sys.argv[0] + " first-DDL-folder second-DDL-folder")
        quit()

    if not os.path.exists(firstDDLfolder):
        print("Error: first-DDL-folder not found: " + firstDDLfolder)
        quit()

    if not os.path.exists(secondDDLfolder):
        print("Error: second-DDL-folder not found: " + secondDDLfolder)
        quit()

    firstDDLfolderList = os.listdir(firstDDLfolder)
    secondDDLfolderList = os.listdir(secondDDLfolder)

    for f in firstDDLfolderList:
#        print(f)
        if f not in secondDDLfolderList:
            print("table: " + f + " only in " + firstDDLfolder)
            print
        else:
            firstDDLFile = firstDDLfolder + '/'+ f
            f_file = open(firstDDLFile, 'r')
            firstFields = parseFile(f_file)

            secondDDLFile = secondDDLfolder + '/'+ f
            s_file = open(secondDDLFile, 'r')
            secondFields = parseFile((s_file))

            compareFields(f, firstDDLFile, secondDDLFile, firstFields, secondFields)

    for s in secondDDLfolderList:
#        print(s)
        if s not in firstDDLfolderList:
            print("table: " + s + " only in " + secondDDLfolder)
            print


def parseFile(file):
    """
    parse the given file object containing ddl for a table and extract the fields and types
    :param file: the file object to parse
    :return: Dictionary containing fields as keys and type as values
    """
    startParsing = False
    fields = {}

    for line in file:
        if startParsing:
            if (line == ')\n') or (line == ');\n') :
                startParsing = False
            else:
#                print line,
                words = line.split()
#                print words

#                if len(words) == 0:
#                    temp1 = 1;

                if words[0] not in fields:
                    # convert list of type words into a string as the value
                    fields[words[0]] = " ".join(words[1:])

        if line == '(\n':
            startParsing = True

    return fields


def compareFields(tableName, firstDDLFile, secondDDLFile, firstFields, secondFields):
    """
    compare the fields and types of the two sets of given fields
    :param tableName: Table name being compared
    :param firstDDLFile: First DDL file
    :param secondDDLFile: Second DDL file
    :param firstFields: Dictionary of fields from first table
    :param secondFields: Dictionary of fields from second table
    :return:
    """

    tableNamePrinted = False

    for firstKey, firstValue in firstFields.items():
        # first check if table name is in both first and second
        if firstKey not in secondFields:
            if not tableNamePrinted:
                print(tableName)
                tableNamePrinted = True
            print("field: " + firstKey + " " + firstValue + " only in " + firstDDLFile)
            print
            # remove field from dictionary, since already checked
            del firstFields[firstKey]
        else:
            # check if the types match
            secondValue = secondFields[firstKey]
            if firstValue != secondValue:
                if not tableNamePrinted:
                    print(tableName)
                    tableNamePrinted = True
                #print("type difference " + firstKey + ": " + firstValue + " " + secondValue)
                print("field: " + firstKey + " type difference " + firstValue + " " + secondValue)
                print
            # remove field from dictionaries, since already checked
            del firstFields[firstKey]
            del secondFields[firstKey]

    # check if any fields are left over
    for firstKey, firstValue in firstFields.items():
        if not tableNamePrinted:
            print(tableName)
            tableNamePrinted = True
        print("field: " +  firstKey + " " + firstValue + " only in " + firstDDLFile)
        print

    for secondKey, secondValue in secondFields.items():
        if not tableNamePrinted:
            print(tableName)
            tableNamePrinted = True
        print("field: " +  secondKey + " " + secondValue + " only in " + secondDDLFile)
        print

    return None


if __name__ == "__main__":
    main()