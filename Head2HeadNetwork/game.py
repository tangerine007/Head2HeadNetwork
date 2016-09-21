# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 15:05:59 2016

@author: Ben
"""

class game:
    def __init__(self,playerAId,playerBId,playerAWins,playerBWins,date):
        self.ID=-1
        self.playerAWins = playerAWins
        self.playerBWins = playerBWins
        self.playerAId = playerAId
        self.playerBId = playerBId
        self.date = date
        
    ###GETTER_METHODS### 
    def getGameID(self):
        return self.ID
    def getPlayerAId(self):
        return self.playerAId
    def getPlayerBId(self):
        return self.playerBId
    def getPlayerAWins(self):
        return self.playerAWins
    def getPlayerBWins(self):
        return self.playerBWins
    
    #-1 for Tie, otherwise return winner's ID
    def getMatchWinner(self):
        if self.playerAWins==self.playerBWins:
            return -1
        else:
            return [self.playerAId,self.playerBId][self.playerAWins<self.playerBWins]
    def getDate(self):
        return self.date
    ###SETTER_METHODS###
    def setGameID(self,ID):
        self.ID = ID