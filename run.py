# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:43:04 2016

@author: Ben
"""
from Head2HeadNetwork import edge, game, network
from datetime import datetime

def buildSampleNetwork():
    #first create the network
    sampleNet = network("sampleNet")
    
    #create sample nodes (players)  [nodeID]
    a,b,c,d='abcd'
    
    #Add new players to network
    sampleNet.addNodeById(a)
    sampleNet.addNodeById(b)
    sampleNet.addNodeById(c)
    sampleNet.addNodeById(d)

    #create some games played between these players [playerId,player2Id,player1Wins,player2Wins,date]
    gameAB_1 = game(a,b,2,0,datetime(2016,1,1))
    gameAB_2 = game(a,b,2,1,datetime(2016,3,1))  
    gameAB_3 = game(a,b,2,0,datetime(2016,6,1)) 
    gamesAB = [gameAB_1,gameAB_2,gameAB_3]#player A wins 3 matches against player B with scores 2-0, 2-1, 2-0
    
    gamesCD_1 = game(c,d,1,2,datetime(2016,1,1))
    gamesCD_2 = game(c,d,2,1,datetime(2016,3,1))  
    gamesCD_3 = game(c,d,2,3,datetime(2016,6,1)) 
    gamesCD = [gamesCD_1,gamesCD_2,gamesCD_3]
    
    gamesBC_1 = game(b,c,3,0,datetime(2016,4,1)) 
    gamesBC = [gamesBC_1]
    
    
    #create edges between nodes using games played
    ab = edge(a+' vs '+b,a,b,gamesAB)
    cd = edge(c+' vs '+d,c,d,gamesCD)
    bc = edge(b+' vs '+c,b,c,gamesBC)
    
    #Add Edges to network
    sampleNet.addEdge(ab)
    sampleNet.addEdge(cd)
    sampleNet.addEdge(bc)

    return sampleNet
    
    

if __name__ == "__main__":
    a=buildSampleNetwork()
    for i in range(300):
        a.runPageRank()
    print a.toString()
    
