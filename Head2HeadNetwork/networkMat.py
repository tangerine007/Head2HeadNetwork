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

#j are columns #'s
#i are row #'s
class networkLat:
    def __init__(self,name='test'):
        self.name = name
        self.players = {}#dictionary of N players in network
        self.PR = np.ones((1,1))#1xN matrix of player pageranks
        self.L = np.zeros((1,1))#adjacency matrix for all nodes
        self.M = np.zeros((1,1))#NxN matrix of total outgoing edges of each player i when a connection i-j exists   
        self.LossMatrix = np.zeros((1,1))#loss adjacency matrix (how many times has player i lost to player j)
        #TODO: self.dateWeightGames = np.array([[]])
    
    def addGame(self,p1,p2,p1Losses,p2Losses):
        #First get the index of the players in the current game
        playerIndex = []
        playerList = [p1,p2]
        for i in playerList:
            if not self.players.has_key(i):
                self.players[i] = len(self.players)
                if len(self.players)>1:
                    self.PR = np.vstack([self.PR,[self.PR.mean()]])
                    self.L = np.concatenate((self.L,np.zeros((self.L.shape[0],1)).T),0)
                    self.L = np.concatenate((self.L,np.zeros((self.L.shape[0],1))),1)
                    self.LossMatrix = np.concatenate((self.LossMatrix,np.zeros((self.LossMatrix.shape[0],1)).T),0)
                    self.LossMatrix = np.concatenate((self.LossMatrix,np.zeros((self.LossMatrix.shape[0],1))),1)
            playerIndex+=[self.players.get(i)]
        self.L[playerIndex[0]][playerIndex[1]]=1
        self.L[playerIndex[1]][playerIndex[0]]=1
        self.LossMatrix[playerIndex[0]][playerIndex[1]]+=p1Losses
        self.LossMatrix[playerIndex[1]][playerIndex[0]]+=p2Losses
        self.M = self.L / self.L.sum(axis=0)

    def runPageRank(self):
        d = 0.85
        part_1 = np.multiply(np.ones((len(self.players),1)),(1-d)/len(self.players))
        print part_1
        part_2 = np.multiply(self.M,d).dot(self.PR)
        self.PR = np.add(part_1,part_2)
        print self.PR


z = networkLat('test')
z.addGame('a','b',1,2)
z.addGame('a','b',5,4)
z.addGame('a','c',2,3)   
z.addGame('z','d',2,3)     
z.addGame('c','d',2,3) 
z.addGame('a','d',2,3)
for i in range(10):
    z.runPageRank()
