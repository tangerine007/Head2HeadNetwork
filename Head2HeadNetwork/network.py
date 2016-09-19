# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:45:35 2016

@author: Ben
"""


from node import node

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
        for tempNode in list(tempNodes.itervalues()):
            nodeEdgeInfo = [self.edges[edgeId].getEdgeInfoForPageRank(tempNode.getId()) for edgeId in tempNode.getEdgeIds()]
            newPR_complete = sum([self.singleNodePageRank(useSetAlpha,newPR_part1,edgeInfo[0],edgeInfo[1],edgeInfo[2]) for edgeInfo in nodeEdgeInfo])
            tempNode.setPageRank(newPR_complete)
        self.nodes = tempNodes
        
    def singleNodePageRank(self,useSetAlpha,newPR_part1,otherId,wins,losses):
        part_1 = (newPR_part1 if useSetAlpha else (1-wins/(wins+losses))/(len(self.nodes)))+wins/(wins+losses)
        part_2 = self.nodes[otherId].getPageRank()/len(self.nodes[otherId].getEdgeIds())
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