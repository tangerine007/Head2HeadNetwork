# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 15:05:59 2016

@author: Ben
"""

class game:
    def __init__(self,playerAId,playerBId,playerAWins,playerBWins,date):
        self.playerAWins = playerAWins
        self.playerBWins = playerBWins
        self.playerAId = playerAId
        self.playerBId = playerBId
        self.date = date
    ###GETTER_METHODS### 
    def getPlayerAId(self):
        return self.playerAId
    def getPlayerBId(self):
        return self.playerBId
    def getPlayerAWins(self):
        return self.playerAWins
    def getPlayerBWins(self):
        return self.playerBWins
    
    #-1 for Tie, otherwise return winner's ID
    def getWinner(self):
        if self.playerAWins==self.playerBWins:
            return -1
        else:
            return [self.playerAId,self.playerBId][self.playerAWins<self.playerBWins]
    def getDate(self):
        return self.date