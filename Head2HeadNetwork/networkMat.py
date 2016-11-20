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
from Validation.PlayerGameSimulation import generatePlayers, generateTournaments
import matplotlib.pyplot as plt


def timer(a,m=100):
    start = datetime.datetime.now()
    for i in range(m):
        a;
    return "{}s".format((datetime.datetime.now()-start).microseconds/1000.0)

#j are columns #'s
#i are row #'s
class networkLat:
    def __init__(self,name='test'):
        self.name = name
        self.players = {}#dictionary of N players in network
        self.PR = np.ones((1,1))#1xN matrix of player pageranks
        self.L = np.zeros((1,1))#adjacency matrix for all nodes
        self.M = np.zeros((1,1))#NxN matrix of total outgoing edges of each player i when a connection i-j exists   
        self.WinMatrix = np.zeros((1,1))#loss adjacency matrix (how many times has player i lost to player j)
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
                    self.WinMatrix = np.concatenate((self.WinMatrix,np.zeros((self.WinMatrix.shape[0],1)).T),0)
                    self.WinMatrix = np.concatenate((self.WinMatrix,np.zeros((self.WinMatrix.shape[0],1))),1)
            playerIndex+=[self.players.get(i)]
        self.L[playerIndex[0]][playerIndex[1]]=1
        self.L[playerIndex[1]][playerIndex[0]]=1
        self.WinMatrix[playerIndex[0]][playerIndex[1]]+=p1Losses
        self.WinMatrix[playerIndex[1]][playerIndex[0]]+=p2Losses
        self.M = self.L / self.L.sum(axis=0)
        
    def addGamesInBulk(self,allGames,playersFile,inputType="winnerId"):
        playersN = len(playersFile)
        self.PR = np.ones((playersN,1))#1xN matrix of player pageranks 
        self.WinMatrix = np.zeros((playersN,playersN))
        self.L = np.zeros((playersN,playersN))
        playerIndex=0
        for i in playersFile["playerId"].tolist():
            self.players[`i`.replace('.0','')] = playerIndex
            playerIndex+=1
        
        count=1
        #start = datetime.datetime.now()
        for game in allGames.itertuples():
            """
            if count%500==0:
                (datetime.datetime.now()-start).seconds / 500.0 * 1000
                print "{}ms per 1000 iterations".format((datetime.datetime.now()-start).microseconds/1000.0 / 500.0 * 1000)
                endTime = (len(allGames.index)-count)*(max((datetime.datetime.now()-start).microseconds/1000.0,.000001) / 500.0) /60.0/60
                print "Estimated end time in... {} minutes...".format(endTime)
                print "{} games left to process...".format(len(allGames.index)-count)
                start = datetime.datetime.now()
            """
            if inputType=="winnerId":
                p1Losses = int(game.winnerId==game.p1Id)
                p2Losses = int(game.winnerId==game.p2Id) 
            if inputType=='p1Losses:p2Losses':
                self.addGame(`game.p1Id`,`game.p2Id`,`game.p1Losses`,`game.p2Losses`)
                p1Losses = game.p1Losses
                p2Losses = game.p2Losses
            playerIndex = [self.players.get(`game.p1Id`.replace('.0','')),self.players.get(`game.p2Id`.replace('.0',''))] 
            self.WinMatrix[playerIndex[0]][playerIndex[1]]+=p1Losses
            self.WinMatrix[playerIndex[1]][playerIndex[0]]+=p2Losses
            self.L[playerIndex[0]][playerIndex[1]]=1
            self.L[playerIndex[1]][playerIndex[0]]=1
            count+=1
        self.M = self.L / self.L.sum(axis=0)
        self.removePlayersWithNoGames()        
        
    def removePlayersWithNoGames(self):
        while min(map(sum,self.L))==0:
            deadRow=0
            for lRow in range(len(self.L)):
                if(sum(self.L[lRow])==0):
                    deadRow = lRow
            self.L=np.delete(self.L,deadRow,0)
            self.L=np.delete(self.L,deadRow,1)
            self.M=np.delete(self.M,deadRow,0)
            self.M=np.delete(self.M,deadRow,1)
            self.WinMatrix=np.delete(self.WinMatrix,deadRow,0)
            self.WinMatrix=np.delete(self.WinMatrix,deadRow,1)
            self.PR=np.delete(self.PR,deadRow,0)
            self.players.pop(self.players.keys()[self.players.values().index(deadRow)])
            for i in self.players.iterkeys():
                if self.players[i]>deadRow:
                    self.players[i]-=1

        
    #M is the NxN matrix of total outgoing edges of each player i when a connection i-j exists  
    def getM(self):
        return  np.nan_to_num(self.getL() / self.getL().sum(axis=0))
        
    #L is the adjacency matrix for all nodes
    def getL(self):
        return (self.WinMatrix+self.WinMatrix.T != 0).astype(float)

    def runPageRank(self,runType="Head2Head"): 
        if runType=="Vanilla":
            d=.85
            part_1 = np.ones((len(self.players),1))*(1-d)/len(self.players)
            part_2 = (self.getM()*d).dot(self.PR)
            self.PR = np.add(part_1,part_2)
        elif runType=="Head2Head":
            lossPercent = self.WinMatrix.T/(self.WinMatrix+self.WinMatrix.T)
            lossPercent = np.nan_to_num(lossPercent)
            winPercent = self.WinMatrix/(self.WinMatrix+self.WinMatrix.T)
            winPercent = np.nan_to_num(winPercent)
            newPR = ((winPercent+(lossPercent)/len(self.players)) * self.getM()).dot(np.sqrt(self.PR)/log(len(self.players)))
            self.PR = newPR
        elif runType == "Paper":
            d=.00001
            part_1 = self.WinMatrix.dot(self.PR*(1-d))/np.array([np.sum(self.WinMatrix,0)]).T#check dimensions
            part_2 = d/len(self.players)
            part_3 = ((self.PR*(1-d))/len(self.players))
            part_3=part_3*np.array([np.ma.masked_equal(np.sum(self.WinMatrix,0),0).mask],int).T
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
        self.addGamesInBulk(trainGames,playersFile,"winnerId")

        print "Running pagerank algorithm on data..."
        #start = datetime.datetime.now()
        for i in range(runs):
            self.runPageRank(runType)
            """
            endTime = (runs-i)*((datetime.datetime.now()-start).microseconds / 1000.0 / 1000.0)
            print "Estimated completion in... {} seconds...".format(endTime)
            start = datetime.datetime.now()
            """
        totalGames=0
        correctPredictions=0.0
        #Test Model
        for game in testGames.itertuples():
            if self.players.has_key(str(game.p1Id)) and self.players.has_key(str(game.p2Id)):  
                p1Rank = self.PR[self.players[str(game.p1Id)]][0]
                p2Rank = self.PR[self.players[str(game.p2Id)]][0]
                inputType = ['p1Losses:p2Losses','winnerId']["winnerId" in trainGames.columns]
                if inputType=="winnerId":
                    correctPredictions += int(game.winnerId == [game.p1Id,game.p2Id][p1Rank<p2Rank])
                if inputType=='p1Losses:p2Losses':
                    correctPredictions += int([game.p1Id,game.p2Id][game.p1Losses>game.p2Losses] == [game.p1Id,game.p2Id][p1Rank<p2Rank])
                totalGames+=1
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
        
        
        
def testValidationGamesWithSigmas():
    accuracy=[]
    sigs=[]
    for sig in range(0,50,1):
        generatePlayers(fileOut='Validation/Resources/players.csv',simulatedPlayersN=300,regionR=1,localL=10,skillSigma=sig)
        generateTournaments(fileIn='Validation/Resources/players.csv',fileOut='Validation/Resources/games.csv',playerTravelIndex=1.0,maxTourneysPerLocal=10)
        z = networkLat('test')
        prediction = z.validate(runType="Head2Head",runs=30)
        print "[{},{}%]".format(sig,int(prediction*100))
        accuracy+=[int(prediction*100)]
        sigs+=[sig]
    plt.plot(sigs,accuracy)

def testValidation(runs=25):
    z = networkLat('test')
    prediction = z.validate(runType="Vanilla",runs=runs)
    print "{}% correct predictions".format(int(prediction*100))
    z = networkLat('test')
    prediction = z.validate(runType="Head2Head",runs=runs)
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


#z=testValidation(runs=30)
testValidationGamesWithSigmas()


"""Loss Matrix Desc:
In this loss matrix we see player z(i=3) has 3 losses to player d(i=4)
In this loss matrix we see player d(i=4) has 8 losses to player z(i=3)
*player(i) will have WinMatrix[j,i] losses to player(j)
*total games played between two players is WinMatrix[i,j]+WinMatrix[j,i] OR (z.WinMatrix+z.WinMatrix.T)[i,j]
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