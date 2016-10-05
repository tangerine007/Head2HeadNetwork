# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 18:32:47 2016

@author: Ben
"""

from .. import network
from os.path import isdir
from os.path import isfile

#AonHeadToHead2016
#MensTennis2016
def fromCsv(fileIn="AonHeadToHead2016.csv"):
    fromCsvNetwork = network("sampleNetwork")
    if isdir("Resources"):
        if isfile("Resources/"+fileIn):
            fromCsvNetwork.populateNetworkFromGamesCSV("Resources",fileIn)
    else:
        print "File or directory not found."
        print "Please create file SampleNetwork.csv in Resources folder"
        fileContent = """player1,player2,wins1,wins2,dateYear,dateMonth,dateDay
a,f,9,5,2016,1,1
a,b,9,1,2016,1,1
b,c,9,1,2016,4,1
c,d,9,1,2016,1,1
c,e,9,1,2016,1,1
c,g,1,9,2016,1,1
e,g,1,9,2016,1,1
d,g,1,9,2016,1,1
"""
        print "Here is the content of that file:\n\n" +fileContent                
            
    return fromCsvNetwork