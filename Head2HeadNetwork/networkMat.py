# -*- coding: utf-8 -*-
"""
Created on Lon Nov 14 18:45:22 2016

@author: Ben
"""

import numpy as np
import datetime
from pandas import read_csv

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

    def runPageRank(self,runType="Head2Head"): 
        if runType=="Vanilla":
            d=.85
            part_1 = np.ones((len(self.players),1))*(1-d)/len(self.players)
            part_2 = (self.M*d).dot(self.PR)
            self.PR = np.add(part_1,part_2)
        elif runType=="Head2Head":
            d=.00001
            part_1 = self.LossMatrix.dot(self.PR*(1-d))/np.array([np.sum(self.LossMatrix,0)]).T#check dimensions
            part_2 = d/len(self.players)
            part_3 = ((self.PR*(1-d))/len(self.players))
            part_3=part_3*np.array([np.ma.masked_equal(np.sum(self.LossMatrix,0),0).mask],int).T
            self.PR = np.add(np.add(part_1,part_2),part_3)
        else:
            print "Invalid runType chosen, valid runtypes are Vanilla/Head2Head"
            
    

z = networkLat('test')
z.validate()
"""
z.addGame('a','b',1,2)
z.addGame('a','b',5,4)
z.addGame('a','c',2,3)   
z.addGame('z','d',2,3)     
z.addGame('c','d',2,3) 
z.addGame('a','d',2,3)
for i in range(100000):
    z.runPageRank()
print z.PR
print sum(z.PR)
"""
