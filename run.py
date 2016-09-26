# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:43:04 2016

@author: Ben
"""
from Head2HeadNetwork.Examples.BuildSampleNetwork import buildSampleNetwork
from Head2HeadNetwork.Examples.FromCsv import fromCsv
import argparse


error01 = "1) No games played during given timeframe (default is 365 days)"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', nargs='?',default=100, help='Number of iterations pagerank will run.')  
    parser.add_argument('--ex', nargs='*', help='Builds a sample network using the selected method (manual, fromCsv)')  
    parser.add_argument('-d', action='store_true', default=False, help='Use game dates when running pagerank?')
    parser.add_argument('--days',nargs='?', default=365, help='Number of days until game is not counted in pagerank when -d flag is set.')
    args = parser.parse_args()
    if args.ex is not None:
        if "manual" in args.ex:
            exampleNet = buildSampleNetwork()
        elif "fromCsv" in args.ex:
            exampleNet = fromCsv()
        else:
            exampleNet = buildSampleNetwork()
            print "Invalid selection, building sample network"            
            
        if len(exampleNet.getNodes())>0:
            print exampleNet.toString()
            for i in range(int(args.N)):
                pageRankSuccess = exampleNet.runPageRank(useDate=args.d,gamesActiveDays=int(args.days))
                if pageRankSuccess==-1:
                    print "\n~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!"
                    print "PageRankFailed in "+str(i)+" Iterations, possible reasons:\n"+error01+"\n"
                    print "~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!\n"
                    break
            print exampleNet.toString()
        else:
            print "No network was built, please try again"
    
