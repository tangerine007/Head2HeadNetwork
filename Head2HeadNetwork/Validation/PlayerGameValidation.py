# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 14:31:17 2016

@author: Ben
"""

from pandas import read_csv, concat,DataFrame
from sklearn.cross_validation import train_test_split
#----------BELOW CAN BE USED IN A GENERAL SENSE TO TEST REAL DATA------------

#Build Training/Test sets:
#1) Collect one game from all players in the network
#2) From those games, if more games were played against the same opponent, grab all games played between the two players
#3) Randomly select more games (all games between two opponents included) until training is at 'train%'. These games will be added 
    #into the network
#4) The remaining games will be put in a separate pile 'test%' pile
#**for right now let's assume 'train%'=70% and 'test%'=30%

def validate(gameFileIn="Resources/games.csv",playerFileIn="Resources/players.csv"):
    games = read_csv(gameFileIn)
    players = read_csv(playerFileIn)

    trainGames, testGames = splitTrainTestSets(games,players)
    
    
    

#*ensures at least one game from every player is in the training set
def splitTrainTestSets(games,players,testPercent=0.3):
    names=players['playerId'].tolist()
    oneGameEach = DataFrame(data=None,columns=games.columns)
    for i in names:
        playerGames = concat((games.loc[games.p1Id==i],games.loc[games.p2Id==i]))
        if len(playerGames)>0:
            chosenGame = playerGames.sample(n=1)
            oneGameEach = oneGameEach.append(chosenGame)
            games = games[games.index!=chosenGame.index[0]]
    train, test = train_test_split(games, test_size = testPercent)
    train = concat((train,oneGameEach))
    return train, test


#Train/Test the model!:
#1) Train the network using your training set
#2) Based on the output pageranks for each player in the network, predict who will win all of the games in the test set
#3) Display the results



validate();
