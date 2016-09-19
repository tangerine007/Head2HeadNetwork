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
    a,b,c,d,e,f='abcdef'
    
    #Add new players to network
    sampleNet.addNodeById(a)
    sampleNet.addNodeById(b)
    sampleNet.addNodeById(c)
    sampleNet.addNodeById(d)
    sampleNet.addNodeById(e)
    sampleNet.addNodeById(f)
    
    #create some games played between these players [playerId,player2Id,player1Wins,player2Wins,date]
    gameAB_1 = game(a,b,9,1,datetime(2016,1,1))
    gamesAB = [gameAB_1]
    
    gamesBC_1 = game(b,c,9,1,datetime(2016,4,1)) 
    gamesBC = [gamesBC_1]
    
    gamesCD_1 = game(c,d,9,1,datetime(2016,1,1))
    gamesCD = [gamesCD_1]

    gamesCE_1 = game(c,e,9,1,datetime(2016,1,1))
    gamesCE = [gamesCE_1]
    
    
    #create edges between nodes using games played
    ab = edge(a+' vs '+b,a,b,gamesAB)
    cd = edge(c+' vs '+d,c,d,gamesCD)
    bc = edge(b+' vs '+c,b,c,gamesBC)
    ce = edge(c+' vs '+e,c,e,gamesCE)
    
    #Add Edges to network
    sampleNet.addEdge(ab)
    sampleNet.addEdge(cd)
    sampleNet.addEdge(bc)
    sampleNet.addEdge(ce)
    return sampleNet
    
    

if __name__ == "__main__":
    a=buildSampleNetwork()
    print a.toString()
    for i in range(10000):
        a.runPageRank()
    print a.toString()
    
