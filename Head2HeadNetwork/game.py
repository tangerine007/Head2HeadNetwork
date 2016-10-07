# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 15:05:59 2016

@author: Ben
"""

class game:
    def __init__(self,playerAId,playerBId,playerAWins,playerBWins,date):
        self.ID=-1
        sortedIds = sorted([playerAId,playerBId])
        self.playerAId = sortedIds[0]
        self.playerBId = sortedIds[1]
        self.playerAWins = [playerBWins,playerAWins][self.playerAId==playerAId]
        self.playerBWins = [playerAWins,playerBWins][self.playerAId==playerAId]
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
    def getPlayerWinsById(self,playerId):
        if playerId==self.playerAId:
            return self.playerAWins
        if playerId==self.playerBId:
            return self.playerBWins
        print "No game played with that PlayerId"
        return -1
    def getPlayerLossesById(self,playerId):
        if playerId==self.playerAId:
            return self.playerBWins
        if playerId==self.playerBId:
            return self.playerAWins
        print "No game played with that PlayerId"
        return -1
    def getOpponentId(self,playerId):
        if playerId==self.playerAId:
            return self.playerBId
        if playerId==self.playerBId:
            return self.playerAId
        print "No game played with that PlayerId"
        return -1
    
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
        
    def toString(self):
        return "GameID:{} | PlayerA:{} - PlayerB:{} | #Games:{} | {} Wins:{} {} Wins:{} | Date:{}".format(self.ID, self.playerAId,
self.playerBId,(self.playerAWins+self.playerBWins),self.playerAId,self.playerAWins,self.playerBId,self.playerBWins,self.date)