# -*- coding: utf-8 -*-
"""
Created on Lon Nov 14 18:45:22 2016

@author: Ben
"""

import numpy as np
import datetime

def timer(a,m=100):
    start = datetime.datetime.now()
    for i in range(m):
        a;
    return "{}ms".format((datetime.datetime.now()-start).microseconds/1000.0)


class networkLat:
    def __init__(self,name='test'):
        self.name = name
        self.players = {}#dictionary of N players in network
        self.pagerankMatrix = np.ones(1)#1xN matrix of player pageranks
        self.L = np.zeros((1,1))#NxN matrix of total outgoing edges of each player i when a connection i-j exists
        #TODO: self.LossLatrix
        #TODO: self.dateWeightGames = np.array([[]])
    
    def addGame(self,p1,p2,p1Wins,p2Wins):
        #First get the index of the players in the current game
        playerIndex = []
        playerList = [p1,p2]
        for i in playerList:
            if not self.players.has_key(i):
                self.players[i] = len(self.players)
                if len(self.players)>1:
                    self.pagerankMatrix = np.append(self.pagerankMatrix,[self.pagerankMatrix.mean()])
                    self.L = np.concatenate((self.L,np.zeros((self.L.shape[0],1)).T),0)
                    self.L = np.concatenate((self.L,np.zeros((self.L.shape[0],1))),1)
            playerIndex+=[self.players.get(i)]
        self.L[playerIndex[0]][playerIndex[1]]=1
        self.L[playerIndex[1]][playerIndex[0]]=1
        print self.L
        #Computer L, L = {1/L(pj), if i-j: else 0}


z = networkLat('test')
z.addGame('a','b',1,2)
z.addGame('a','b',5,4)
z.addGame('a','c',2,3)   
z.addGame('z','d',2,3)      