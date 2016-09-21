# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:45:35 2016

@author: Ben
"""



from node import node as Node
from game import game as Game
from datetime import datetime
from math import sqrt
import os

class network:
    def __init__(self,name):
        self.name = name
        self.nodes = {}
        self.edges = {}
        self.games = {}
        
    ###GETTER_METHODS###  
    def getNodes(self):
        return self.nodes
    def getEdges(self):
        return self.edges
    def getGames(self):
        return self.games
    def getNodeById(self,nodeId):
        return self.nodes[nodeId]
    def getEdgeById(self,edgeId):
        return self.edges[edgeId]
    def getGameById(self,edgeId,gameId):
        returnGame = [game for game in self.games[edgeId] if game.getGameID()==gameId]
        if len(returnGame)==1:
            return returnGame
        else:
            print "No game by that ID exists"
        
    ###SETTER_METHODS###
    def setNodes(self,nodes):
        self.nodes = nodes
    def setEdges(self,edges):
        self.edges={}
        for edge in edges:
            self.addEdge(edge)
    def setGames(self,games):
        self.games={}
        for game in games:
            #TODO: add games here
    
    ###MUTATOR_METHODS###
    def populateNetworkFromGamesCSV(self,nameIn,path=os.path.split(os.path.abspath(__file__))[0],filename=os.path.split(os.path.abspath(__file__))[1]):
        header=True
        sampleNet = network(nameIn)
        with open(os.path.join(path,filename),'r') as f:
            for line in f:
                if not header:
                    p1,p2,p1w,p2w,y,m,d = line[:-1].split(",")
                    tempGame = Game(p1,p2,p1w,p2w,datetime(y,m,d))
                header=False
        
    def addNodeById(self,nodeId):
        cont = 'yes'
        if self.nodes.has_key(nodeId):
            cont = input("Node Already Exists, delete and replace?('yes'/'no')")
        if cont=='yes':  
            self.nodes[nodeId] = Node(nodeId)
            
    def removeNodeById(self,nodeId):
        del self.nodes[nodeId]
        
    def addEdge(self,edge):
        #TODO: check if edge exists, might want to remove this method completely and only add
        #things by node and by game
        self.edges[edge.getId()] = edge
        for nodeID in edge.getNodeIds():
            if not self.nodes.has_key(nodeID):
                self.addNodeById(nodeID,[])
            self.nodes[nodeID].addEdgeId(edge.getId())
            
    def addGame(self,game):
        p1 = game.getPlayerAId()
        p2 = game.getPlayerBId()
        if p1==p2:
            print "Can't play game against oneself!"
            return
        for nodeid in [p1,p2]:
            if not self.nodes.has_key(nodeid):
                self.nodes[nodeId] = Node(nodeId)
        sortedIds = sorted([p1,p2])
        edgeId = "-vs-".join(sortedIds);
        
        if not self.edges.has_key(edgeId):
            self.edges[edgeId] = edge(edgeId,sortedIds[0],sortedIds[1],[edgeId+"#0"])
        else:
            self.edges[edgeId].addGame([edgeId+"#"+`len(self.edges[edgeId].getGames())`])
        
        
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