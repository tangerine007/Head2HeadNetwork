# -*- coding: utf-8 -*-
"""
Created on Lon Nov 14 18:45:22 2016

@author: Ben
"""

import numpy as np
import datetime
from pandas import read_csv, concat, DataFrame
from sklearn.cross_validation import train_test_split
from math import sqrt, log


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
        
    def addGame(self,p1,p2,*args):
        #First get the index of the players in the current game
        if len(args)==1:
            p1Losses = int(args[0]==p2)
            p2Losses = int(args[0]==p1)   
        elif len(args)==2:
            p1Losses = args[0]
            p2Losses = args[1]
        else:
            print "Invalid number of arguments chosen, valid choices are p1Losses/p2Losses, winnerId"
            
        playerIndex = []
        playerList = map(lambda x: x.replace('.0',''),[p1,p2])
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
            winPercent = self.LossMatrix.T/(self.LossMatrix+self.LossMatrix.T)
            winPercent = np.nan_to_num(winPercent)
            newPR = (winPercent * self.M).dot(np.sqrt(self.PR))/log(len(self.players)) 
            self.PR = newPR
        elif runType == "Paper":
            d=.00001
            part_1 = self.LossMatrix.dot(self.PR*(1-d))/np.array([np.sum(self.LossMatrix,0)]).T#check dimensions
            part_2 = d/len(self.players)
            part_3 = ((self.PR*(1-d))/len(self.players))
            part_3=part_3*np.array([np.ma.masked_equal(np.sum(self.LossMatrix,0),0).mask],int).T
            self.PR = np.add(np.add(part_1,part_2),part_3)
        else:
            print "Invalid runType chosen, valid runtypes are Vanilla/Head2Head/paper"
        
        
    def validate(self,gameFileIn="Validation/Resources/games.csv",playerFileIn="Validation/Resources/players.csv",runType="Head2Head",runs=50):
        print "Reading game/player files..."        
        games = read_csv(gameFileIn)
        playersFile = read_csv(playerFileIn)
    
        print "Splitting into training/test sets..."
        trainGames, testGames = self.splitTrainTestSets(games,playersFile)
        
        #Train model
        print "Adding games to model..."
        inputType = ['p1Losses:p2Losses','winnerId']["winnerId" in trainGames.columns]
        for i in trainGames.index:
            game=trainGames.ix[i]
            if inputType=="winnerId":
                self.addGame(`game.p1Id`,`game.p2Id`,`game.winnerId`)
            if inputType=='p1Losses:p2Losses':
                self.addGame(`game.p1Id`,`game.p2Id`,`game.p1Losses`,`game.p2Losses`)
        print "Running pagerank algorithm on data..."
        for i in range(runs):
            self.runPageRank(runType)
        
        totalGames=len(testGames)
        correctPredictions=0.0
        #Test Model
        for i in testGames.index:
            game=testGames.ix[i]
            p1Rank = self.PR[self.players[str(game.p1Id)]][0]
            p2Rank = self.PR[self.players[str(game.p2Id)]][0]

            inputType = ['p1Losses:p2Losses','winnerId']["winnerId" in trainGames.columns]
            if inputType=="winnerId":
                correctPredictions += int(game.winnerId == [game.p1Id,game.p2Id][p1Rank<p2Rank])
            if inputType=='p1Losses:p2Losses':
                correctPredictions += int([game.p1Id,game.p2Id][game.p1Losses>game.p2Losses] == [game.p1Id,game.p2Id][p1Rank<p2Rank])
        return correctPredictions/totalGames
        
    #*ensures at least one game from every player is in the training set
    def splitTrainTestSets(self,games,playersFile,testPercent=0.3):
        #names=playersFile['playerId'].tolist()
        #oneGameEach = DataFrame(data=None,columns=games.columns)
        oneGameEach1 = games.groupby('p1Id').first()
        oneGameEach2 = games.groupby('p2Id').first()
        oneGameEach1= games[games.index.isin(oneGameEach1.index)]
        oneGameEach2= games[games.index.isin(oneGameEach2.index)]
        oneGameEach2 = oneGameEach2[~oneGameEach2['p2Id'].isin(oneGameEach1['p1Id'].tolist())]
        
        oneGameEach = concat((oneGameEach1,oneGameEach2))
        games = games[~games.index.isin(oneGameEach.index)]
        """
        for i in names:
            print i
            playerGames = concat((games.loc[games.p1Id==i],games.loc[games.p2Id==i]))
            if len(playerGames)>0:
                chosenGame = playerGames.sample(n=1)
                oneGameEach = oneGameEach.append(chosenGame)
                games = games[games.index!=chosenGame.index[0]]
        """
        train, test = train_test_split(games, test_size = testPercent)
        train = concat((train,oneGameEach))
        return train, test

def testValidation():
    z = networkLat('test')
    prediction = z.validate(runType="Vanilla")
    print "{}% correct predictions".format(int(prediction*100))
    z = networkLat('test')
    prediction = z.validate(runType="Head2Head")
    print "{}% correct predictions".format(int(prediction*100))
    #z = networkLat('test')
    #prediction = z.validate(runType="Paper")
    #print "{}% correct predictions".format(int(prediction*100))
    return z

def testRunPageRank():
    z = networkLat('test')

    z.addGame('a','b',1,6)
    z.addGame('a','c',2,7)   
    z.addGame('z','d',3,8)     
    z.addGame('c','d',4,9) 
    z.addGame('a','d',5,10)
    for i in range(10):
        z.runPageRank(runType="Vanilla")
    print "----------------"
    return z
"""
part_1 is (1-d)/N part of this
take sqrt of every element in array = np.array(map(lambda x: map(lambda y: sqrt(y),x),wins/total))
"""


z=testValidation()
for i in range(30):
    print sum(z.PR)[0]

"""Loss Matrix Desc:
In this loss matrix we see player z(i=3) has 3 losses to player d(i=4)
In this loss matrix we see player d(i=4) has 8 losses to player z(i=3)
*player(i) will have LossMatrix[j,i] losses to player(j)
*total games played between two players is LossMatrix[i,j]+LossMatrix[j,i] OR (z.LossMatrix+z.LossMatrix.T)[i,j]
[[  0.   1.   2.   0.   5.]
 [  6.   0.   0.   0.   0.]
 [  7.   0.   0.   0.   4.]
 [  0.   0.   0.   0.   3.]
 [ 10.   0.   9.   8.   0.]]
 
[[  0.   7.   9.   0.  15.]
 [  7.   0.   0.   0.   0.]
 [  9.   0.   0.   0.  13.]
 [  0.   0.   0.   0.  11.]
 [ 15.   0.  13.  11.   0.]]
"""