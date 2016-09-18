# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:28:50 2016

@author: Ben
"""

class edge:  
    def __init__(self,ID,nodeAid,nodeBid,games):
        self.ID=ID
        self.nodeAid = nodeAid
        self.nodeBid = nodeBid
        self.games = games
        self.nodeAWins = sum([i.getPlayerAWins() for i in games])
        self.nodeBWins = sum([i.getPlayerBWins() for i in games])
        
    ###GETTER_METHODS###  
    def getId(self):
        return self.ID
    def getNodeAid(self):
        return self.nodeAid
    def getNodeBid(self):
        return self.nodeBid
    def getGames(self):
        return self.games
    def getNodeAWins(self):
        return self.nodeAWins
    def getNodeBWins(self):
        return self.nodeBWins
        
    ###SETTER_METHODS###
    def setGames(self,games):
        self.games = games
        self.nodeAWins = sum([i.getPlayerAWins() for i in games])
        self.nodeBWins = sum([i.getPlayerBWins() for i in games])
        
    ###MUTATOR_METHODS###
    def addGame(self,game):
        self.games += [game]
        self.nodeAWins += game.getPlayerAWins()
        self.nodeBWins += game.getPlayerBWins()
        
    def addGameWithParams(self,nodeAWins,nodeBWins,date):
        newGame = game(self.nodeAid,self.nodeBid,nodeAWins,nodeBWins,date)
        self.games += [newGame]
        self.nodeAWins += newGame.getPlayerAWins()
        self.nodeBWins += newGame.getPlayerBWins()
    
    
    ##OTHER##
    def toString(self):
        return "EdgeID:'{}' - #Matches:{} - {} Wins:{} - {} Wins:{}".format(self.ID,len(self.games),self.nodeAid,self.nodeAWins,self.nodeBid,self.nodeBWins)
    
"""
EDGE DESC:
An Edge represents the interactions between two players, storing all games played between them

VARIABLES:
ID = edge ID
nodeAid = 'player A' ID
nodeBid = 'player B' ID
games = list of games played betweeen player A and player B

"""