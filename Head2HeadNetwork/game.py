# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 15:05:59 2016

@author: Ben
"""

class game:
    def __init__(self,playerAWins,playerBWins,date):
        self.playerAWins = playerAWins
        self.playerBWins = playerBWins
        self.date = date
    ###GETTER_METHODS### 
    def getPlayerAWins(self):
        return self.playerAWins
    def getPlayerBWins(self):
        return self.playerBWins
    def getDate(self):
        return self.date