# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:45:35 2016

@author: Ben
"""


from node import node
from game import game
from datetime import datetime
from math import sqrt
import os

class network:
    def __init__(self,name):
        self.name = name
        self.nodes = {}
        self.edges = {}
        
    ###GETTER_METHODS###  
    def getNodes(self):
        return self.nodes
    def getEdges(self):
        return self.edges
    def getNodeById(self,nodeId):
        return self.nodes[nodeId]
    def getEdgeById(self,edgeId):
        return self.edges[edgeId]
        
    ###SETTER_METHODS###
    def setNodes(self,nodes):
        self.nodes = nodes
    def setEdges(self,edges):
        self.edges={}
        for edge in edges:
            self.addEdge(edge)
                 
    
    ###MUTATOR_METHODS###
    def populateNetworkFromGamesCSV(self,nameIn,path=os.path.split(os.path.abspath(__file__))[0],filename=os.path.split(os.path.abspath(__file__))[1]):
        header=True
        sampleNet = network(nameIn)
        with open(os.path.join(path,filename),'r') as f:
            for line in f:
                if not header:
                    p1,p2,p1w,p2w,y,m,d = line[:-1].split(",")
                    tempGame = game(p1,p2,p1w,p2w,datetime(y,m,d))
                header=False
        
    def addNodeById(self,nodeId):
        cont = 'yes'
        if self.nodes.has_key(nodeId):
            cont = input("Node Already Exists, delete and replace?('yes'/'no')")
        if cont=='yes':  
            self.nodes[nodeId] = node(nodeId)
            
    def removeNodeById(self,nodeId):
        del self.nodes[nodeId]
        
    def addEdge(self,edge):
        self.edges[edge.getId()] = edge
        for nodeID in edge.getNodeIds():
            if not self.nodes.has_key(nodeID):
                self.addNodeById(nodeID,[])
            self.nodes[nodeID].addEdgeId(edge.getId())
                
    def removeEdge(self,edgeId):
         del self.edges[edgeId]
    
    def runPageRank(self,useSetAlpha=False,alpha=.5):
        newPR_part1 = (1-alpha)/(len(self.nodes))+alpha
        tempNodes = self.nodes
        PR_sum= 0
        for tempNode in list(tempNodes.itervalues()):
            nodeEdgeInfo = [self.edges[edgeId].getEdgeInfoForPageRank(tempNode.getId()) for edgeId in tempNode.getEdgeIds()]
            newPR_complete = sum([self.singleNodePageRank(useSetAlpha,newPR_part1,edgeInfo[0],edgeInfo[1],edgeInfo[2]) for edgeInfo in nodeEdgeInfo])
            tempNode.setPageRank(newPR_complete)
            PR_sum+=newPR_complete
        for tempNode in list(tempNodes.itervalues()):
            tempNode.setPageRank(tempNode.getPageRank()/PR_sum)
        self.nodes = tempNodes
        
    def singleNodePageRank(self,useSetAlpha,newPR_part1,otherId,wins,losses):
        part_1 = (newPR_part1 if useSetAlpha else (1-losses/(wins+losses))/(len(self.nodes)))+wins/(wins+losses)
        part_2 = (sqrt(len(self.nodes))*self.nodes[otherId].getPageRank())/len(self.nodes[otherId].getEdgeIds())
        return part_1*part_2
        
        
    ##OTHER##
    def toString(self):
        nodeString = '\n'.join(["   "+i.toString() for i in list(self.nodes.itervalues())])
        edgeString = '\n'.join(["   "+i.toString() for i in list(self.edges.itervalues())])
        return "Network: {} \nNodes:\n{} \nEdges:\n{}".format(self.name,nodeString,edgeString)
        
"""
NETWORK DESC:
A network object stores all information in the network including nodes and edges (players and games)

VARIABLES:
name = network name
nodes = list of all players in the network
edges = list of all edges in the network
"""