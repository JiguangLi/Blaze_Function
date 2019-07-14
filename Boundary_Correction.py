#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:06:30 2019

@author: jiguangli
"""
# Boundary Correction


# Load essential packages
import pandas as pd
import numpy as np

# Input variables:

# order1: the left order. An n1 by 2 dataframe.
# order2: the right order. An n2 by 2 dataframe.

# Return variable: a 2-element tuple (order1,order2), where order1 and order2
# have corrected boundaries.

def Boundary_correction(order1,order2):
    # Change the column names and format of the dataset. 
     order1.columns=["wv","intens"]
     order2.columns=["wv","intens"]
   
    # start: the start index of the overlap region in the left order.
     start= order1[order1["wv"] >=order2["wv"][0]].index[0]

     
    # temp: records the intensities of the overlap region.
    # temp <- order1$intens[start:n1]
     temp = order1["intens"].values[start:]
    
    # This chunk of code does the weighted average. 
     n_temp= len(temp) 
     for i in range(n_temp):
         w=(i+1)/n_temp
         temp[i]= (1-w)*order1["intens"][start+i]+w*order2["intens"][i]
    
     # Revise the original orders with the corrected region.
     order1.loc[start:,"intens"] = temp
     order2.loc[0:(n_temp-1),"intens"]= temp
     
     return (order1,order2)
     



