#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 19:44:00 2017

@author: kaggle
"""
import random
import networkx as nx
import numpy as np
infolder = '/home/kaggle/Downloads'
fname = infolder + '/B-small-practice.in'
#import matplotlib

# input() reads a string with a line of input, stripping the '\n' (newline) at the end.
# This is all you need for most Google Code Jam problems.
def mod_input(t):    
    t.pop(0)
    ti = [x[:-1] for x in t]
#    print (len(ti))
    inputmod = [] 
    for pancakes in ti:
        num_pancakes = len(pancakes)
        if num_pancakes <= 2:
            pass
        else:    
            flipper_size = random.randint(2,num_pancakes -1)  
            a = pancakes + ' ' + str(flipper_size) + '\n'
            inputmod.append(a)           
#            print(len(inputmod))    
    inputmod.insert(0,len(inputmod)) 
    return inputmod



  # pancakes cooked in a single row
  # flipper flips K consecutive pancakes
  # goal: all lines == +   
#---+---++ 3 where 


"""
m == flipper size 
n == number of pancakes 
impossible if m is even and n is odd 
if n >= 2m, it is always possible to do in less than n/m + 2 flips
if n and m are both even, n/m + 1
if n is even and m = n -1 then it requires exactly n operations
"""
def flip_n_pancakes(pancakes,start,f):
    flipsec = pancakes[start:start + f]
    return pancakes [:start] + [ x + 1 if x == 0 else x - 1 for x in flipsec] + pancakes[start + f:]

def flip_pancakes(pancakes,start,f):
    if start + f > len(pancakes):
        print ("can't flip that, too close to the edge! pancakes = {} start point = {} flipper size = {}".format(pancakes,start,f))
    else:
        a = flip_n_pancakes([int(p) for p in pancakes],start,f)
        a = [str(a) for a in a]
        return "".join(a)
    
#    len(range(-1, (3- 2)))
    
class pancake_flipper_graph(object):
    def __init__(self,n_pancakes,flipper_size):        
#        print('making graph for {} pancakes and {} flipper'.format(n_pancakes,flipper_size))
        self.g = nx.Graph(plen = n_pancakes,flen = flipper_size)
        arrangement = [str(1)] * n_pancakes
        self.topnode = arrangement = ''.join(arrangement)
        nodeatts = {"arrangement":arrangement,"wsolved":True}  
        self.add_node(nodeatts)
        self.make_all_nodes()  
    
    def add_node (self,nodeatts):
        try: 
            node = (nodeatts["arrangement"]) #,nodeatts["solved"])                
            self.g.add_node(node) # ,nodeatts)
        except KeyError: 
            print("nodeatts must be 'arrangement' and 'solved', not {}".format(nodeatts.keys())    )
            
    def make_all_nodes(self):
        nodecount = int(self.g.number_of_nodes())
        startpoint = int(nodecount)
        keepgoing = True
        first_node = self.g.nodes()[0] 
        self.make_nodes(first_node)
        while keepgoing:
            ncstart = int(self.g.number_of_nodes() ) 
            for parent in self.g.nodes()[startpoint:]:                               
                self.make_nodes(parent)                
            if int(self.g.number_of_nodes()) == ncstart:                 
                keepgoing = False
            else:                
                startpoint = startpoint + (int(self.g.number_of_nodes()) - ncstart)
                nodecount = int(self.g.number_of_nodes())                
        
        
    def make_nodes(self,parent_node):        
        self.possible_positions = range(-1,self.g.graph['plen']  - self.g.graph['flen'])
        arrangement = parent_node
        for pos in self.possible_positions:
            next_arrangement = flip_pancakes(arrangement,(pos  + 1),self.g.graph['flen'])
            solved = False
            nodeatts = {"arrangement":next_arrangement,"solved":solved}
            self.add_node(nodeatts)
            self.g.add_edge(arrangement,nodeatts["arrangement"])                        
            

        

def main() :
    file = open(fname, 'r')
    t = file.readlines()
    inputmod = mod_input(t)    
    inputmod.pop(0)
    try: 
        pancakes = [x[:-3] for x in inputmod]
    except TypeError:
        return inputmod
    flippersizes = [int(x[-2]) for x in inputmod]     
    outputs = {} 
    for p, m in zip(pancakes,flippersizes):
        impossible = False
        distance = np.nan
        pn = len(p)    
        plist =  [0 if p == '-' else 1 for p in p]         
        pb = "".join([str(0) if p == '-' else str(1) for p in p] )
        if sum(plist) == pn :
            print('this one is already happy {} '.format(plist))                        
        else:            
            g = pancake_flipper_graph(pn,m)
            if g.g.has_node(pb):                
                print ("graph for {} does have node {}".format(g.topnode,pb))                
                distance = len(nx.shortest_path(g.g,g.topnode,pb))
                output = "case #{} : {}".format(len(outputs), distance)                
            else:
                print ("graph does not have node {}".format(pb))                
                output = "case #{} : {}".format(len(outputs), "IMPOSSIBLE")
            outputs[(p,m)] = output
    return outputs
#            return pn,m, plist, g, distance, impossible 

if __name__ ==  "__main__":
    output = main()
#    plen, flippa, plist, g , d, i = main()

import Matplotlib
#nx.draw(test.g)