# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:28:50 2016

@author: Ben
"""

from Head2HeadNetwork import game

class edge:
    def __init__(self,ID,nodeAid,nodeBid,games):
        self.ID=ID
        self.nodeAid = nodeAid
        self.nodeBid = nodeBid
        self.games = games
        
    ###GETTER_METHODS###  
    def getId(self):
        return self.ID
    def getNodeAid(self):
        return self.nodeAid
    def getNodeBid(self):
        return self.nodeBid
    def getGames(self):
        return self.games
        
    ###SETTER_METHODS###
    def setGames(self,games):
        self.games = games
        
    ###MUTATOR_METHODS###
    def addGame(self,game):
        self.games += [game]
        
    def addGameWithParams(self,nodeAWins,nodeBWins,date):
        self.games += game(nodeAWins,nodeBWins,date)
        
    
"""
EDGE DESC:
An Edge represents the interactions between two players, storing all games played between them

VARIABLES:
ID = edge ID
nodeAid = 'player A' ID
nodeBid = 'player B' ID
games = list of games played betweeen player A and player B

"""