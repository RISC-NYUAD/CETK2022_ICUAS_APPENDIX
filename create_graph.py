# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 11:19:48 2021

@author: dc4204
"""

import numpy as np
import math
from collections import namedtuple

Node_List = []
Edge_List = []
rot_table = []
hex_num = 0
sq_num = 0
f_l = 0
f_l_num = -1

def fixed_rotation(start,INIT,c):
    prefix = math.pi
    if(start=='h'):
        if(INIT==-1):
            INIT = 3
            prefix = 0
        if(c==6):# 6 reserved for elevated agents            
            c = 3
        angle = (INIT-c)*(math.pi/3) + prefix 
    if(start=='s'):
        if(INIT==-1):
            INIT = 2
            prefix = 0
        if(c==6):
            c = 2
        angle = (INIT-c)*(math.pi/2) + prefix        
    return angle

def process(word, start):
    global hex_num
    global sq_num
    global Node_List
    global Edge_List
    global rot_table
    global f_l
    global f_l_num
    
    l = 0.14
    
    if(start=='h'):
        n_st = start+"_"+str(hex_num)
        Node_List.append(n_st)
        hex_num += 1
    else:
        n_st = start+"_"+str(sq_num)
        Node_List.append(n_st)
        sq_num += 1
    
    L = -1
    INIT = -1
    d = 0
    first = 1
    PHI = 0
    count = 0
    
    for c in word:
        count += 1
        if(d>0):
            d -= 1
            continue
        
        if(first):
            if(c==']'):
                INIT = -1
            else:
                INIT = int(c)
            first = 0
        else:
            if(c.isdigit() or c==')' ):            
                if(L!=-1):
                    n_L = str(L)+"_"+n_st
                    Node_List.append(n_L)
                    if(L!=6):
                        Edge_List.append([n_st,n_L,[l,0,0]])
                    else:
                        Edge_List.append([n_st,n_L,[0,0,0.06]])
                    rot_table.append([n_st,n_L,PHI])
                    if(f_l == 0):
                        f_l = 1
                        f_l_num = PHI
                if(c.isdigit()):
                    L = int(c)
                    PHI = fixed_rotation(start,INIT,L)
                else:
                    break
            if(c.isalpha()):
                # about to call Process(), need to save a local reference to the current next polygon (because of chains)
                if(c=='h'):
                    local_num = hex_num
                else:
                    local_num = sq_num
                n_C = c + "_" + str(local_num)
                d = process(word[count::],c)
                if(L!=6):
                    Edge_List.append([n_st,n_C,[l,0,0]])
                else:
                    Edge_List.append([n_st,n_C,[0,0,0.06]])
                rot_table.append([n_st,n_C,fixed_rotation(start,INIT,L)])
                L = -1
            
    return count    
                
                
if __name__== "__main__" :

    Lexis = "h]10s2036)234)"
#    Lexis = "s]123s10s23)))"
    c = Lexis[0]
    Lexis = Lexis[1::]
    
    process(Lexis, c)
    numeric_edge_list = Edge_List
    for i in range(0,len(Edge_List)):
        s = Edge_List[i][0]
        for j in range(len(Node_List)):
            if(s==Node_List[j]):
                numeric_edge_list[i][0] = j
                break
        s = Edge_List[i][1]
        for j in range(len(Node_List)):
            if(s==Node_List[j]):
                numeric_edge_list[i][1] = j
                break
    for i in range(0,len(rot_table)):
        if(rot_table[i][2] >= 2*math.pi):
            rot_table[i][2] -= 2*math.pi 
        elif(rot_table[i][2] <= -2*math.pi):
            rot_table[i][2] += 2*math.pi 
        rot_table[i][0] = numeric_edge_list[i][0]
        rot_table[i][1] = numeric_edge_list[i][1]        
        
        
        
        
        
        
        
        
        
    
