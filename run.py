# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:43:04 2016

@author: Ben
"""
from Head2HeadNetwork import node, edge, game, network
from datetime import datetime

def buildSampleNetwork():
    #first create the network
    sampleNet = network("sampleNet")
    
    #create sample nodes (players)  [nodeID]
    a='a'
    b='b'
    c='c'
    d='d'
    
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
    print a.toString()
    
"""
def buildSampleNetwork_Old():
    #first create the network
    sampleNet = network("sampleNet")
    
    #create sample nodes (players)  [nodeID,edges,pagerank]
    a = node('a',[],1)
    b = node('b',[],1)
    c = node('c',[],1)
    d = node('d',[],1)

    #create some games played between these players [playerId,player2Id,player1Wins,player2Wins,date]
    gameAB_1 = game(a.getId(),b.getId(),2,0,datetime(2016,1,1))
    gameAB_2 = game(a.getId(),b.getId(),2,1,datetime(2016,3,1))  
    gameAB_3 = game(a.getId(),b.getId(),2,0,datetime(2016,6,1)) 
    gamesAB = [gameAB_1,gameAB_2,gameAB_3]#player A wins 3 matches against player B with scores 2-0, 2-1, 2-0
    
    gamesCD_1 = game(c.getId(),d.getId(),1,2,datetime(2016,1,1))
    gamesCD_2 = game(c.getId(),d.getId(),2,1,datetime(2016,3,1))  
    gamesCD_3 = game(c.getId(),d.getId(),2,3,datetime(2016,6,1)) 
    gamesCD = [gamesCD_1,gamesCD_2,gamesCD_3]
    
    gamesBC_1 = game(b.getId(),c.getId(),3,0,datetime(2016,4,1)) 
    gamesBC = [gamesBC_1]
    
    
    #create edges between nodes 
    ab = edge(a.getId()+' vs '+b.getId(),a.getId(),b.getId(),gamesAB)
    cd = edge(c.getId()+' vs '+d.getId(),c.getId(),d.getId(),gamesCD)
    bc = edge(b.getId()+' vs '+c.getId(),b.getId(),c.getId(),gamesBC)
    
    #add edges to all corresponding nodes (we can do this by adding one edge at a time or by using setter method)
    a.addEdge(ab)
    b.addEdge(ab)
    c.addEdge(cd)
    d.addEdge(cd)
    b.addEdge(bc)
    c.addEdge(bc)
    
    #add all edges and nodes to the network (let's do this with setter methods to save space)
    sampleNet.setNodes([a,b,c,d])
    sampleNet.setEdges([ab,cd,bc])
    
    return sampleNet
    """