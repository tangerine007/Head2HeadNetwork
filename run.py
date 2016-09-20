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
    a,b,c,d,e,f,g='abcdefg'
    
    #Add new players to network
    sampleNet.addNodeById(a)
    sampleNet.addNodeById(b)
    sampleNet.addNodeById(c)
    sampleNet.addNodeById(d)
    sampleNet.addNodeById(e)
    sampleNet.addNodeById(f)
    sampleNet.addNodeById(g)
    
    #create some games played between these players [playerId,player2Id,player1Wins,player2Wins,date]
    gameAF_1 = game(a,f,9,5,datetime(2016,1,1))
    gamesAF = [gameAF_1]
    
    gameAB_1 = game(a,b,9,1,datetime(2016,1,1))
    gamesAB = [gameAB_1]
    
    gamesBC_1 = game(b,c,9,1,datetime(2016,4,1)) 
    gamesBC = [gamesBC_1]
    
    gamesCD_1 = game(c,d,9,1,datetime(2016,1,1))
    gamesCD = [gamesCD_1]

    gamesCE_1 = game(c,e,9,1,datetime(2016,1,1))
    gamesCE = [gamesCE_1]
    
    gamesCG_1 = game(c,g,1,9,datetime(2016,1,1))
    gamesCG = [gamesCG_1]
    
    gamesEG_1 = game(e,g,1,9,datetime(2016,1,1))
    gamesEG = [gamesEG_1]
    
    gamesDG_1 = game(d,g,1,9,datetime(2016,1,1))
    gamesDG = [gamesDG_1]
    
    
    #create edges between nodes using games played
    af = edge(a+' vs '+f,a,f,gamesAF)
    ab = edge(a+' vs '+b,a,b,gamesAB)
    cd = edge(c+' vs '+d,c,d,gamesCD)
    bc = edge(b+' vs '+c,b,c,gamesBC)
    ce = edge(c+' vs '+e,c,e,gamesCE)
    cg = edge(c+' vs '+g,c,g,gamesCG)
    eg = edge(e+' vs '+g,e,g,gamesEG)
    dg = edge(d+' vs '+g,d,g,gamesDG)
    
    #Add Edges to network
    sampleNet.addEdge(af)
    sampleNet.addEdge(ab)
    sampleNet.addEdge(cd)
    sampleNet.addEdge(bc)
    sampleNet.addEdge(ce)
    sampleNet.addEdge(cg)
    sampleNet.addEdge(eg)
    sampleNet.addEdge(dg)
    
    return sampleNet
    
    

if __name__ == "__main__":
    a=buildSampleNetwork()
    print a.toString()
    for i in range(1000):
        a.runPageRank()
    print a.toString()
    
