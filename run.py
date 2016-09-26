# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:43:04 2016

@author: Ben
"""
from Head2HeadNetwork.Examples.BuildSampleNetwork import buildSampleNetwork
from Head2HeadNetwork.Examples.FromCsv import fromCsv
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ex', nargs='*', help='Builds a sample network using the selected method (manual, fromCsv)')   
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
            for i in range(100):
                exampleNet.runPageRank()
            print exampleNet.toString()
        else:
            print "No network was built, please try again"
    
