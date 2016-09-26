# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:45:35 2016

@author: Ben
"""



from node import node as Node
from edge import edge as Edge
from game import game as Game
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
    def getGames(self):
        return self.games
    def getNodeById(self,nodeId):
        return self.nodes[nodeId]
    def getEdgeById(self,edgeId):
        return self.edges[edgeId]
    def getGamesByEdgeId(self,edgeId):
        if not self.edges.has_key(edgeId):
            return self.edges[edgeId]
        else:
            print "No edge by that ID exists"
        
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
            self.addGame(game)
    
    ###MUTATOR_METHODS###
    def populateNetworkFromGamesCSV(self,path=os.path.split(os.path.abspath(__file__))[0],filename="SampleNetwork.csv",header=True):
        with open(os.path.join(path,filename),'r') as f:
            for line in f:
                if not header:
                    p1,p2,p1w,p2w,y,m,d = line.strip("\n").split(",")
                    p1w,p2w,y,m,d = [int(i) for i in [p1w,p2w,y,m,d]]
                    if '' not in [p1,p2,p1w,p2w,y,m,d]:
                        self.addGame(Game(p1,p2,p1w,p2w,datetime(y,m,d)))
                header=False
        
    def addNodeById(self,nodeId):
        cont = 'no'
        if self.nodes.has_key(nodeId):
            cont = input("Node Already Exists, delete and replace?('yes'/'no')")
        if cont=='yes':  
            self.nodes[nodeId] = Node(nodeId)
            
    def addEdge(self,edge):
        p1 = edge.getNodeAid()
        p2 = edge.getNodeBid()
        if p1==p2:
            print "Can't play game against oneself!"
            return
        sortedIds = sorted([p1,p2])
        edgeId = "-vs-".join(sortedIds);
        if self.edges.has_key(edgeId):
            cont = 'no'
            if self.edges.has_key(edgeId):
                cont = input("Edge Already Exists, delete and replace?('yes'/'no')")
            if cont!='yes':  
                return
        for nodeId in [p1,p2]:
            if not self.nodes.has_key(nodeId):
                self.nodes[nodeId] = Node(nodeId)
            self.nodes[nodeId].addEdgeId(edgeId)
        edge.setID(edgeId)
        self.edges[edgeId] = edge
    
    def addGame(self,game):
        p1 = game.getPlayerAId()
        p2 = game.getPlayerBId()
        if p1==p2:
            print "Can't play game against oneself!"
            return
        sortedIds = sorted([p1,p2])
        edgeId = "-vs-".join(sortedIds);
        for nodeId in [p1,p2]:
            if not self.nodes.has_key(nodeId):
                self.nodes[nodeId] = Node(nodeId)
            self.nodes[nodeId].addEdgeId(edgeId)

        if not self.edges.has_key(edgeId):
            game.setGameID(edgeId+"#0")
            newEdge = Edge(sortedIds[0],sortedIds[1],[game])
            newEdge.setID(edgeId)
            self.edges[edgeId] = newEdge
        else:
            game.setGameID(edgeId+"#"+`len(self.edges[edgeId].getGames())`)
            self.edges[edgeId].addGame(game)
            
     #TODO: Removing a node completely from the network will be a bit more complicated than this, have to remove it from
     #Everywhere
#    def removeNodeById(self,nodeId):
#        del self.nodes[nodeId]
        
          
    #TODO: removeEdge method - remove all places edge is referenced (remove edge from list in both nodes too!)
    #def removeEdgeById(self,edgeId):
      

    
    def runPageRank(self,useSetAlpha=False,alpha=.85,useDate=False,gamesActiveDays=365):
        newPR_part1 = (1-alpha)/(len(self.nodes))+alpha
        tempNodes = self.nodes
        PR_sum= 0
        for tempNode in list(tempNodes.itervalues()):
            nodeEdgeInfo = [self.edges[edgeId].getEdgeInfoForPageRank(tempNode.getId(),useDate,gamesActiveDays) for edgeId in tempNode.getEdgeIds()]
            newPR_complete = sum([self.singleNodePageRank(useSetAlpha,newPR_part1,edgeInfo[0],edgeInfo[1],edgeInfo[2]) for edgeInfo in nodeEdgeInfo])
            tempNode.setPageRank(newPR_complete)
            PR_sum+=newPR_complete
        if PR_sum!=0:
            for tempNode in list(tempNodes.itervalues()):
                tempNode.setPageRank(tempNode.getPageRank()/PR_sum)
            self.nodes = tempNodes
        else:
            return -1
        
    def singleNodePageRank(self,useSetAlpha,newPR_part1,otherId,wins,losses):
        if losses+wins==0:
            part_1 = newPR_part1 if useSetAlpha else 1/len(self.nodes)
        else:
            part_1 = (newPR_part1 if useSetAlpha else (1-losses/(wins+losses))/(len(self.nodes)))+wins/(wins+losses)
        part_2 = (sqrt(len(self.nodes))*self.nodes[otherId].getPageRank())/len(self.nodes[otherId].getEdgeIds())
        return part_1*part_2
        
        
    ##OTHER##
    def toString(self,sortNodesByPageRank=True):
        if sortNodesByPageRank:
            nodeList = sorted(list(self.nodes.itervalues()), key=lambda x: x.pageRank, reverse=True)
        else:
            nodeList = list(self.nodes.itervalues())
        nodeString = '\n'.join(["   "+i.toString() for i in nodeList])
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