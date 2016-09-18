# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:12:47 2016

@author: Ben
"""

class node:
    def __init__(self,ID,edges,pageRank):
        self.ID = ID
        self.edges = edges
        self.pageRank = pageRank
        
    ###GETTER_METHODS### 
    def getId(self):
        return self.ID
    def getEdges(self):
        return self.edges
    def getPageRank(self):
        return self.pageRank
    def getWinsAndLosses(self):
        return [i.getNodeAWins() for i in self.edges]
        
    ###SETTER_METHODS###
    def setEdges(self,edges):
        self.edges=edges
    def setPageRank(self,pageRank):
        self.pageRank = pageRank
        
    ###MUTATOR_METHODS###
    def addEdge(self,edge):
        self.edges += [edge]
    def removeEdge(self,edge):
        self.edges.remove(edge)
    def adjustPageRank(self):
        tempPageRank = self.pageRank
        #DO PAGERANK CALCULATION HERE
    
    ##OTHER##
    def toString(self):
        return 'NodeID:{} - #Edges:{} - PageRank:{}'.format(self.ID,len(self.edges),self.pageRank)



"""
NODE DESC:
A node object is a player in the network.

VARIABLES:
ID = node id, will probably be player tag as string, or int ID linked to player tag in another file
edges = Each 'player' has edges which represent their interactions with other players in the network.
pageRank = Each 'player' has a rank representing their skill.
"""


