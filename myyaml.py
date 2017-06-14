# Spencer
# My collection of Yaml functions

import os
import yaml

yamlData = None


def readYamlFile(yamlFileName="read.yaml"):
    """
    Read in the Yaml file containing read data information
    :param yamlFileName: the Yaml filename to read
    :return: the Yaml data as an List of entries
    """
    yamlFile = file(yamlFileName, 'r')
    global yamlData
    yamlData = yaml.load(yamlFile)
#    print yaml.dump(yamlData)

    return yamlData


def search(entryName):
    """
    Search the Yaml data for a given entry name
    :param entryName: the name to search for in the Yaml data
    :return: the Yaml entry object
    """
    for entry in yamlData:
        entryNameDict = entry.get(entryName)
        if entryNameDict is not None:
            return entryNameDict


def searchMultiple(entryName):
    """
    Search the Yaml data for a given entry name. Will support finding multiple entry names
    :param entryName: the name to search for in the Yaml data
    :return: a list of Yaml objects
    """
    multipleList = []
    for entry in yamlData:
        entryNameDict = entry.get(entryName)
        if entryNameDict is not None:
            multipleList.append(entryNameDict)
    return multipleList

