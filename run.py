# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:43:04 2016

@author: Ben
"""
from Head2HeadNetwork.Examples.BuildSampleNetwork import buildSampleNetwork
from Head2HeadNetwork.Examples.FromCsv import fromCsv
import argparse

#python run.py --ex fromCsv -toFile
#python run.py -v
error01 = "1) No games played during given timeframe (default is 365 days)"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', nargs='?',default=50, help='Number of iterations pagerank will run.') 
    parser.add_argument('-v', action='store_true', default=False, help='validate?')
    parser.add_argument('--ex', nargs='*', help='Builds a sample network using the selected method (manual, fromCsv)')  
    parser.add_argument('-d', action='store_true', default=False, help='Use game dates when running pagerank?')
    parser.add_argument('--days',nargs='?', default=365, help='Number of days until game is not counted in pagerank when -d flag is set.')
    parser.add_argument('-toFile', action='store_true', default=False, help='Prints output to file when true?')
    parser.add_argument('-p', action='store_true', default=False, help='Print results to terminal?')
    parser.add_argument('-byGames',action='store_true', default=False, help='Rank players taking all games into consideration? Default is to rank players by the winner of matches only.')
    args = parser.parse_args()
    
    if args.ex is not None:
        if "manual" in args.ex:
            exampleNet = buildSampleNetwork()
        elif "fromCsv" in args.ex:
            exampleNet = fromCsv()
        else:
            exampleNet = buildSampleNetwork()
            print "Invalid selection, building sample network"
        if args.v:
            exampleNet.validate()
            
        elif len(exampleNet.getNodes())>0:
            if args.p:
                print exampleNet.toString()
            for i in range(int(args.N)):
                pageRankSuccess = exampleNet.runPageRank(useDate=args.d,useGameWins=args.byGames,gamesActiveDays=int(args.days))
                if pageRankSuccess==-1:
                    print "\n~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!"
                    print "PageRankFailed in "+str(i)+" Iterations, possible reasons:\n"+error01+"\n"
                    print "~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!\n"
                    break
            if args.p:
                print exampleNet.toString()
            if args.toFile:
                with open("Resources/NetworkOutput.txt","w") as f:
                    f.write(exampleNet.toString())
        else:
            print "No network was built, please try again"
    
