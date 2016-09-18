# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:45:35 2016

@author: Ben
"""

class network:
    def __init__(self,name):
        self.name = name
        self.nodes = {}
        self.edges = []
        
    ###GETTER_METHODS###  
    def getNodes(self):
        return self.nodes
    def getEdges(self):
        return self.edges
        
    ###SETTER_METHODS###
    def setNodes(self,nodes):
        self.nodes = nodes
    def setEdges(self,edges):
        self.edges = edges        
    
    ###MUTATOR_METHODS###
    def addNode(self,node):
        cont = 'yes'
        if self.nodes.has_key(node.nodeId()):
            cont = input("Node Already Exists, delete and replace?('yes'/'no')")
        if cont=='yes':  
            self.nodes[node.getId()] = []
            
    def removeNode(self,nodeId):
        del self.nodes[nodeId]
        
    def addEdge(self,edge):
        self.edges += [edge]
        nodeAId = edge.getNodeAid()
        nodeBId = edge.getNodeBid()
        self.nodes[nodeAId] += [edge]
        self.nodes[nodeBId] += [edge]
    def removeEdge(self,edge):
        self.edges.remove(edge)
        
        
    ##OTHER##
    def toString(self):
        nodeString = '\n'.join(["   "+i.toString() for i in self.nodes])
        edgeString = '\n'.join(["   "+i.toString() for i in self.edges])
        return "Network: {} \nNodes:\n{} \nEdges:\n{}".format(self.name,nodeString,edgeString)
        
"""
NETWORK DESC:
A network object stores all information in the network including nodes and edges (players and games)

VARIABLES:
name = network name
nodes = list of all players in the network
edges = list of all edges in the network
"""