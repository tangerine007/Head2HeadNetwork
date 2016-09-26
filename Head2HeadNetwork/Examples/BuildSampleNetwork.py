# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 18:24:25 2016

@author: Ben
"""

from .. import edge, game, network
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
    
    
    #create edges between nodes using games played
    af = edge(a,f,gamesAF)
    ab = edge(a,b,gamesAB)
    cd = edge(c,d,gamesCD)
    bc = edge(b,c,gamesBC)
    ce = edge(c,e,gamesCE)
    cg = edge(c,g,gamesCG)
    eg = edge(e,g,gamesEG)
    
    #Add Edges to network
    sampleNet.addEdge(af)
    sampleNet.addEdge(ab)
    sampleNet.addEdge(cd)
    sampleNet.addEdge(bc)
    sampleNet.addEdge(ce)
    sampleNet.addEdge(cg)
    sampleNet.addEdge(eg)
    
    
    #Oops, I forgot a game
    gamesDG_1 = game(d,g,1,9,datetime(2016,1,1))
    
    #instead of adding edge dg, let's just add the game and have the graph create the edge for us!
    sampleNet.addGame(gamesDG_1)
    
    return sampleNet