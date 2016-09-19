# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:12:47 2016

@author: Ben
"""

class node:
    def __init__(self,ID):
        self.ID = ID
        self.edgeIds = []
        self.pageRank = 1
        
    ###GETTER_METHODS### 
    def getId(self):
        return self.ID
    def getEdgeIds(self):
        return self.edgeIds
    def getPageRank(self):
        return self.pageRank
    def getWinsAndLosses(self):
        return [i.getNodeAWins() for i in self.edges]
        
    ###SETTER_METHODS###
    def setEdgeIds(self,edgeIds):
        self.edgeIds=edgeIds
    def setPageRank(self,pageRank):
        self.pageRank = pageRank
        
    ###MUTATOR_METHODS###
    def addEdgeId(self,edgeId):
        self.edgeIds += [edgeId]
    def removeEdge(self,edge):
        self.edges.remove(edge)
    def adjustPageRank(self,newPageRank):
        self.pageRank = newPageRank
    
    ##OTHER##
    def toString(self):
        return 'NodeID:{} - #Edges:{} - PageRank:{}'.format(self.ID,len(self.edgeIds),self.pageRank)



"""
NODE DESC:
A node object is a player in the network.

VARIABLES:
ID = node id, will probably be player tag as string, or int ID linked to player tag in another file
    ->ID can be of any type as long as it is unique
edges = Each 'player' has edges which represent their interactions with other players in the network.
    ->list<String>
pageRank = Each 'player' has a rank representing their skill.
    ->float
"""


