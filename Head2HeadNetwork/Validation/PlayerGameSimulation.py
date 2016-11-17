# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:02:10 2016

@author: Ben
"""
import random

#First create 'N' players in network:
#DONE - 1) Randomly assign them skill levels normal between 0-100 (mimic Microsoft TrueSkill)
#DONE - 2) Randomly assign them a region (out of 'R'available regions)

def generatePlayers(fileOut='players.csv',simulatedPlayersN=1000,regionR=1,skillSigma=0):
    regions = range(regionR)
    with open("Resources/"+fileOut,'w') as f:
        f.write("playerId,region,skillMean,skillSigma\n")
        for i in range(simulatedPlayersN):
            playerId=`i`
            region=`random.choice(regions)`
            skillMean=`min(max(random.gauss(50,10),0),100)`
            skillSigmaToWrite=`random.uniform(skillSigma/2,skillSigma)`
            writeString = playerId+","+region+","+skillMean+","+skillSigmaToWrite+'\n'
            f.write(writeString)
        



 



#Generate 'G' games:
#1) Randomly generate many 'Local' tournaments with ~N/1000 players each in each region
#2) Randomly generate fewer 'Regional' tournaments with ~N/100 players each
#3) Randomly generate very few 'National' tournaments with ~N/10 players each ex. N=10,000, there will be ~1000 players
#**Make sure that few out of region players are at locals where more out of region players are at Regionals/Nationals
#**Use proper seeding based on skill levels
#**Make sure higher ranked players are more likely to be included in Regional/National tournaments

#Run generated Tournaments:
#1) Create a likelyhood that a player will beat another player based on their difference in skill level (mimic Microsoft TrueSkill)
#2) Collect all games played and outcomes


#----------BELOW CAN BE USED IN A GENERAL SENSE TO TEST REAL DATA------------

#Build Training/Test sets:
#1) Collect one game from all players in the network
#2) From those games, if more games were played against the same opponent, grab all games played between the two players
#3) Randomly select more games (all games between two opponents included) until training is at 'train%'. These games will be added 
    #into the network
#4) The remaining games will be put in a separate pile 'test%' pile
#**for right now let's assume 'train%'=70% and 'test%'=30%

#Train/Test the model!:
#1) Train the network using your training set
#2) Based on the output pageranks for each player in the network, predict who will win all of the games in the test set
#3) Display the results



#RUN
generatePlayers(fileOut='players.csv',simulatedPlayersN=1000,regionR=1,skillSigma=0)