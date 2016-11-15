# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 18:45:22 2016

@author: Ben
"""

import numpy as np
import datetime

def timer(a,m=100):
    start = datetime.datetime.now()
    for i in range(m):
        a;
    return "{}ms".format((datetime.datetime.now()-start).microseconds/1000.0)


class networkMat:
    def __init__(self,name):
        self.name = name
        self.players = {}#dictionary of N players in network
        self.pagerankMatrix = np.array([[]])#1xN matrix of player pageranks
        self.M = np.array([[]])#NxN matrix of total outgoing edges of each player i when a connection i-j exists
        #TODO: self.LossMatrix
        #TODO: self.dateWeightGames = np.array([[]])
    
    def addGame(self,p1,p2,p1Wins,p2Wins):
        #First get the index of the players in the current game
        playerIndex = []
        playerList = [p1,p2]
        for i in playerList:
            if self.players.has_key(i):
                self.players.get(i) 
            else:
                self.players[i] = len(self.players)
            playerIndex+=[self.players.get(i)]
        #Computer M, M = {1/L(pj), if i-j: else 0}
            