# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:02:10 2016

@author: Ben
"""
from random import random,randint,gauss,uniform
from math import log, ceil, sqrt
from pandas import read_csv, concat
from scipy.stats import norm

#First create 'N' players in network:
#DONE - 1) Randomly assign them skill levels normal between 0-100 (mimic Microsoft TrueSkill)
#DONE - 2) Randomly assign them a region (out of 'R'available regions)
def generatePlayers(fileOut='Resources/players.csv',simulatedPlayersN=10000,regionR=4,localL=10,skillSigma=5):
    with open(fileOut,'w') as f:
        f.write("playerId,region,local,skillMean,skillSigma\n")
        for i in range(simulatedPlayersN):
            playerId=`i`
            region=`randint(1,regionR)`
            local=`randint(1,localL)`
            skillMean=`min(max(gauss(50,10),0),100)`
            skillSigmaToWrite=`uniform(skillSigma/2,skillSigma)`
            writeString = playerId+","+region+","+local+","+skillMean+","+skillSigmaToWrite+'\n'
            f.write(writeString)
            
#Generate 'G' games:
#1) Randomly generate many 'Local' tournaments with ~N/1000 players each in each region
#2) Randomly generate fewer 'Regional' tournaments with ~N/100 players each
#3) Randomly generate very few 'National' tournaments with ~N/10 players each ex. N=10,000, there will be ~1000 players
#**Make sure that few out of region players are at locals where more out of region players are at Regionals/Nationals
#**Use proper seeding based on skill levels
#**Make sure higher ranked players are more likely to be included in Regional/National tournaments
def seed(n):
    ol = [1]
    for i in range(int(ceil(log(n)/log(2)))):
        l = 2*len(ol) + 1
        ol = [e if e <= n else 0 for s in [[el, l-el] for el in ol] for e in s]
    return ol

def pWin(p1,p2):
    if type(p1)==int:
        return p2
    if type(p2)==int:
        return p1
    deltaMu = p1.skillMean - p2.skillMean
    rsss = sqrt(p1.skillSigma**2 + p2.skillSigma**2)
    return [p1,p2][norm.cdf(deltaMu/rsss)<random()]
    
    
    
def runTournament(tourneyPlayers):
    games=[]
    tourneyPlayers = tourneyPlayers.sort_values(by='skillMean',ascending=False) 
    tourneySeed = [tourneyPlayers.iloc[i-1] if i>0 else 0 for i in seed(len(tourneyPlayers))]
    #Start with single elimination, add option for double elimination later?
    #each game takes form of [p1Id,p2Id,winnerPlayerId]
    while len(tourneySeed)>1:
        tourneySeed = map(None, *([iter(tourneySeed)] * 2))
        nextRound=[]
        for game in tourneySeed:
            winner = pWin(game[0],game[1])
            if type(game[0])!=int and type(game[1])!=int:
                games+=[map(int,[game[0].playerId,game[1].playerId,winner.playerId])]
            nextRound+=[winner]
        tourneySeed=nextRound
    return games
        

#Break down into Generating one tournament at a time, running them to collect the games
def generateLocalTournament(region,local,fileIn='Resources/players.csv',playerTravelIndex=.01):
    players = read_csv(fileIn)
    nationalPlayers = players.query('region!='+`region`)
    regionPlayers = players.query('region=='+`region`+' and local!='+`local`)
    localPlayers = players.query('region=='+`region`+' and local=='+`local`)
    tourneySize = randint(len(localPlayers)/4,len(localPlayers)*4/5)
    playerTypeList=[0,0,0]#local,regional,national
    for i in range(tourneySize):
        if random()<=playerTravelIndex**2:
            playerTypeList[2]+=1
        elif random()>=1-playerTravelIndex:
            playerTypeList[1]+=1
        else:
            playerTypeList[0]+=1

    if playerTypeList[2]>0 and len(nationalPlayers)>0:
        nationalPlayers = nationalPlayers.sample(n=playerTypeList[2])
    if playerTypeList[1]>0 and len(regionPlayers)>0:
        regionPlayers = regionPlayers.sample(n=playerTypeList[1])
    if playerTypeList[0]>0:
        localPlayers = localPlayers.sample(n=playerTypeList[0])
        
    tourneyPlayers = concat((localPlayers,regionPlayers,nationalPlayers))
    return runTournament(tourneyPlayers)

    
    
#playerTravelIndex: % of a regional player entering in a local
#playerTravelIndex**2: % of a national player playing in a local
def generateTournaments(fileIn='Resources/players.csv',fileOut='Resources/games.csv',playerTravelIndex=.01,maxTourneysPerLocal=20):
    players = read_csv(fileIn)
    regionsR = players['region'].max()
    localsL= players['local'].max()
    
    with open(fileOut,'w') as f:
        f.write("p1Id,p2Id,winnerId,region,local,tourneyType\n")
        
        print "Generating Local Tournaments..."
        for region in range(1,regionsR+1):
            for local in range(1,localsL+1):
                localTourneyNumChooser = randint(1,maxTourneysPerLocal)
                for i in range(localTourneyNumChooser):
                    games = generateLocalTournament(region=region,local=local,fileIn=fileIn,playerTravelIndex=playerTravelIndex)
                    for j in games:
                        p1Id = j[0]
                        p2Id = j[1]
                        winnerId =j[2]
                        tourneyType="local"
                        writeString = `p1Id`+","+`p2Id`+","+`winnerId`+","+`region`+","+`local`+","+tourneyType+'\n'
                        f.write(writeString)
                            
#RUN
mainFile=False
if mainFile:
    generatePlayers(fileOut='Resources/players.csv',simulatedPlayersN=100,regionR=1,localL=5,skillSigma=0)
    generateTournaments(fileIn='Resources/players.csv',fileOut='Resources/games.csv',playerTravelIndex=1.0,maxTourneysPerLocal=10)